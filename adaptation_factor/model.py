"""Domain model and pure calculation functions."""

from dataclasses import dataclass
from enum import Enum
import math


class StressBand(str, Enum):
    NONE = "none"
    LOW = "low"
    MODERATE = "moderate"
    SEVERE = "severe"
    EXTREME = "extreme"


def _finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def calculate_estress(
    innovation_stress: float,
    comparator_stress: float,
    innovation_no_stress: float,
    comparator_no_stress: float,
) -> float:
    """Return the stress-specific difference-in-differences effect."""
    values = [
        _finite(innovation_stress, "innovation_stress"),
        _finite(comparator_stress, "comparator_stress"),
        _finite(innovation_no_stress, "innovation_no_stress"),
        _finite(comparator_no_stress, "comparator_no_stress"),
    ]
    return (values[0] - values[1]) - (values[2] - values[3])


def classify_stress(comparator_no_stress: float, comparator_stress: float) -> StressBand:
    """Classify stress by proportional depression of a higher-is-better outcome."""
    normal = _finite(comparator_no_stress, "comparator_no_stress")
    stressed = _finite(comparator_stress, "comparator_stress")
    if normal == 0:
        raise ValueError("comparator_no_stress cannot be zero; use an external counterfactual")
    depression = (normal - stressed) / abs(normal)
    if depression < 0.05:
        return StressBand.NONE
    if depression < 0.15:
        return StressBand.LOW
    if depression < 0.30:
        return StressBand.MODERATE
    if depression < 0.50:
        return StressBand.SEVERE
    return StressBand.EXTREME


@dataclass(frozen=True)
class Estimate:
    study_id: str
    innovation: str
    comparator: str
    context: str
    outcome: str
    outcome_unit: str
    method: str
    stress_band: StressBand
    estress: float
    standard_error: float | None = None
    sample_size: int | None = None
    weight: float = 1.0
    stress_basis: str = "observed_counterfactual"
    source: str = ""
    notes: str = ""

    def validate(self) -> None:
        for name in ("study_id", "innovation", "comparator", "context", "outcome", "outcome_unit", "method"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} is required")
        _finite(self.estress, "estress")
        if self.standard_error is not None and _finite(self.standard_error, "standard_error") < 0:
            raise ValueError("standard_error must be non-negative")
        if self.sample_size is not None and self.sample_size <= 0:
            raise ValueError("sample_size must be positive")
        if _finite(self.weight, "weight") <= 0:
            raise ValueError("weight must be positive")

