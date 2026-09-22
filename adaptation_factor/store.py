"""SQLite persistence for estimates and co-benefits."""

import csv
import sqlite3
from pathlib import Path
from typing import Iterable

from .model import Estimate, StressBand, calculate_estress


SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS estimates (
  id INTEGER PRIMARY KEY,
  study_id TEXT NOT NULL,
  innovation TEXT NOT NULL,
  comparator TEXT NOT NULL,
  context TEXT NOT NULL,
  outcome TEXT NOT NULL,
  outcome_unit TEXT NOT NULL,
  method TEXT NOT NULL,
  stress_band TEXT NOT NULL CHECK(stress_band IN ('none','low','moderate','severe','extreme')),
  estress REAL NOT NULL,
  standard_error REAL,
  sample_size INTEGER,
  weight REAL NOT NULL DEFAULT 1 CHECK(weight > 0),
  stress_basis TEXT NOT NULL,
  source TEXT NOT NULL DEFAULT '',
  notes TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(study_id, innovation, context, outcome, stress_band)
);
CREATE TABLE IF NOT EXISTS co_benefits (
  id INTEGER PRIMARY KEY,
  estimate_id INTEGER NOT NULL REFERENCES estimates(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  value REAL NOT NULL,
  unit TEXT NOT NULL,
  enabled_by_derisking INTEGER NOT NULL DEFAULT 0 CHECK(enabled_by_derisking IN (0,1)),
  UNIQUE(estimate_id, name, unit)
);
"""


class AdaptationStore:
    def __init__(self, path: str | Path):
        self.path = str(path)

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(SCHEMA)

    def add(self, estimate: Estimate) -> int:
        estimate.validate()
        values = (
            estimate.study_id, estimate.innovation, estimate.comparator, estimate.context,
            estimate.outcome, estimate.outcome_unit, estimate.method, estimate.stress_band.value,
            estimate.estress, estimate.standard_error, estimate.sample_size, estimate.weight,
            estimate.stress_basis, estimate.source, estimate.notes,
        )
        with self.connect() as connection:
            cursor = connection.execute(
                """INSERT INTO estimates
                (study_id,innovation,comparator,context,outcome,outcome_unit,method,stress_band,
                 estress,standard_error,sample_size,weight,stress_basis,source,notes)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", values)
            return int(cursor.lastrowid)

    def rows(self) -> list[sqlite3.Row]:
        with self.connect() as connection:
            return connection.execute("SELECT * FROM estimates ORDER BY study_id, innovation").fetchall()

    def aggregate(self, outcome_unit: str, stress_band: StressBand | None = None) -> dict[str, float | int | str]:
        clauses, params = ["outcome_unit = ?"], [outcome_unit]
        if stress_band:
            clauses.append("stress_band = ?")
            params.append(stress_band.value)
        with self.connect() as connection:
            row = connection.execute(
                f"""SELECT COUNT(*) AS n, SUM(weight * estress) / SUM(weight) AS factor,
                    SUM(weight) AS total_weight FROM estimates WHERE {' AND '.join(clauses)}""", params
            ).fetchone()
        if row["n"] == 0:
            raise ValueError("no compatible estimates found")
        return {"outcome_unit": outcome_unit, "n": row["n"], "factor": row["factor"], "total_weight": row["total_weight"]}

    def import_csv(self, path: str | Path) -> int:
        with open(path, newline="", encoding="utf-8-sig") as handle:
            items = [self._from_row(row, line) for line, row in enumerate(csv.DictReader(handle), 2)]
        # Validate everything before opening the transaction.
        for item in items:
            item.validate()
        with self.connect() as connection:
            for item in items:
                connection.execute(
                    """INSERT INTO estimates
                    (study_id,innovation,comparator,context,outcome,outcome_unit,method,stress_band,
                     estress,standard_error,sample_size,weight,stress_basis,source,notes)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (item.study_id,item.innovation,item.comparator,item.context,item.outcome,item.outcome_unit,
                     item.method,item.stress_band.value,item.estress,item.standard_error,item.sample_size,item.weight,
                     item.stress_basis,item.source,item.notes))
        return len(items)

    @staticmethod
    def _from_row(row: dict[str, str], line: int) -> Estimate:
        try:
            direct = row.get("estress", "").strip()
            estress = float(direct) if direct else calculate_estress(*[
                float(row[name]) for name in ("innovation_stress", "comparator_stress", "innovation_no_stress", "comparator_no_stress")
            ])
            return Estimate(
                study_id=row["study_id"], innovation=row["innovation"], comparator=row["comparator"],
                context=row["context"], outcome=row["outcome"], outcome_unit=row["outcome_unit"],
                method=row["method"], stress_band=StressBand(row["stress_band"].lower()), estress=estress,
                standard_error=float(row["standard_error"]) if row.get("standard_error", "").strip() else None,
                sample_size=int(row["sample_size"]) if row.get("sample_size", "").strip() else None,
                weight=float(row.get("weight") or 1), stress_basis=row.get("stress_basis") or "observed_counterfactual",
                source=row.get("source", ""), notes=row.get("notes", ""),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"CSV line {line}: {error}") from error

