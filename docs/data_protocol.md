# E-stress evidence protocol

## Minimum record

Each record describes one innovation or explicitly named bundle, comparator,
context, outcome, outcome unit, stress band, causal method, estimate, uncertainty,
sample size, aggregation weight, stress-classification basis, and source. Preserve
the bundle composition in `innovation`; do not add component effects unless the
study identifies their interaction.

Acceptable designs include randomized trials, difference-in-differences, panel or
matching designs with defensible identification, crop/economic models with
validated counterfactuals, and policy analysis. `method`, `source`, and `notes`
must make assumptions auditable. Record standard errors where available; absence
is allowed but should lower evidence confidence in downstream review.

## Workflow

1. Pre-specify the decision-relevant outcome and its direction (the software's
   stress classifier assumes higher is better).
2. Define the production system, population, time window, innovation/bundle, and
   comparator. Avoid comparing unlike system boundaries.
3. Define locally meaningful stress using depression of the comparator outcome.
   Record the hazard metric too in notes, but do not assume a rainfall threshold
   transfers between systems.
4. Estimate the treatment contrast under stress and no stress. Compute E-stress
   as their difference, or import a direct causal estimate.
5. Record always-present co-benefits separately. Mark benefits plausibly enabled
   by reduced risk, but do not count them twice in E-stress.
6. Aggregate only identical units and report the weighting policy, coverage,
   heterogeneity, and individual estimates beside the mean.

## Edge cases

* **Chronically stressed systems:** use a historical, matched, modelled, or policy
  target counterfactual; record `external_counterfactual` and sensitivity ranges.
* **New enterprise absent at baseline:** use zero only for that component and
  evaluate net whole-farm welfare, including opportunity and operating costs.
* **Loss/risk outcomes:** transform to a higher-is-better measure before applying
  the default classifier, or pre-register reversed rules.
* **No-stress co-benefit:** a positive ordinary treatment effect is not itself an
  adaptation benefit. Preserve it in `co_benefits`.
* **Multiple outcomes:** retain separate records and units. A cross-unit index is
  permissible only with a documented normalization and welfare weighting scheme.

## Candidate test datasets

Prioritize datasets with treatment/comparator observations across stress regimes:

| Dataset type | Suitable tests | Main limitation |
|---|---|---|
| Multi-environment crop variety trials | Yield stability, severity gradients | Plot-to-farm external validity |
| Agricultural RCT/panel microdata | Income, food security, investment, schooling | Rare extreme events; attrition |
| Index insurance trials | Risk-taking and enabled benefits | Basis risk and take-up selection |
| Irrigation/water-harvesting evaluations | Drought E-stress and crop diversification | Endogenous placement |
| Remote sensing + household panels | Spatial aggregation and hazard linkage | Outcome measurement error |
| Process crop/economic simulations | Counterfactual and extreme stress tests | Model structural uncertainty |
| Administrative shock/policy panels | Large-scale policy effects | Parallel-trends assumptions |

Begin with a synthetic four-cell benchmark, then a public multi-environment trial,
then household panel/RCT evidence. Before portfolio use, test sign conventions,
missingness, duplicate studies, unit mismatches, sensitivity to stress thresholds,
and sensitivity to weights.

