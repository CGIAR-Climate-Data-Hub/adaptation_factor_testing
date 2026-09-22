# Adaptation factor testing

A small, auditable reference implementation for recording **E-stress** estimates
and combining them into adaptation factors for agricultural innovations and
innovation bundles.

## Provisional method (pending confirmation)

> **Important:** this equation is a testable working interpretation, not a
> transcription of the latest Tier B PowerPoint. The linked SharePoint deck
> requires authenticated access and was not available when this prototype was
> written. The exact equation, symbols, denominator, and aggregation rules must
> be confirmed from the source deck before the implementation is treated as a
> MELIAF specification. See [`docs/methodology_questions.md`](docs/methodology_questions.md).

An estimate is stored in the outcome unit that matters to the decision maker
(income, dietary diversity, probability of school attendance, and so on). The
current working estimand is the additional effect of an innovation when stress
occurs:

```text
E_stress = (Y_innovation,stress - Y_comparator,stress)
         - (Y_innovation,no-stress - Y_comparator,no-stress)
```

This difference-in-differences separates adaptation benefit from benefits that
also occur without stress. A study may instead submit a directly estimated
`E_stress` from an RCT, quasi-experiment, model, or policy analysis. Direct and
four-cell estimates are retained with method and provenance; they are never
silently mixed.

Stress is classified from its **observed depression of the comparator outcome**,
rather than a universal rainfall or temperature threshold:

```text
depression = (comparator_no_stress - comparator_stress) / abs(comparator_no_stress)
```

Default bands are: none (`<5%`), low (`5–15%`), moderate (`15–30%`), severe
(`30–50%`), and extreme (`>=50%`). Projects should pre-register locally valid
thresholds and directionality. Chronic/marginal systems can use a documented
external counterfactual and set `stress_basis=external_counterfactual`. New
enterprises (for example, adding a fish pond) should use zero for the absent
baseline component, but value the outcome over the **whole system** to avoid
creating an artificial infinite percentage change.

An aggregation factor is a transparent weighted mean within compatible outcome
units:

```text
AF = sum(weight_i * E_stress_i) / sum(weight_i)
```

Weights can represent population, adoption, area, or explicit portfolio policy.
The tool refuses to aggregate unlike units. Co-benefits are stored separately
with an `enabled_by_derisking` flag, so they remain visible without being
mislabelled as E-stress.

See [`docs/data_protocol.md`](docs/data_protocol.md) for the collection protocol,
edge cases, minimum quality checks, and candidate datasets.

## Quick start

Python 3.10+ is sufficient; there are no runtime dependencies.

```bash
python -m adaptation_factor init adaptation.db
python -m adaptation_factor import-csv adaptation.db examples/estimates.csv
python -m adaptation_factor list adaptation.db
python -m adaptation_factor aggregate adaptation.db --outcome-unit usd_per_household_year
```

The CSV importer is transactional: one invalid row rejects the entire file. Use
`python -m adaptation_factor --help` for all options.

## Development

```bash
python -m unittest discover -s tests -v
```
