# Methodology interpretation and decisions needed

## Access limitation

The current SharePoint link to *Workshop CGIAR Adaptation Indicators Tier B-v2*
requires CGIAR/Microsoft authentication from this environment. The relevant
content is identified as **slides 48–66**, but those slides still cannot be read
here. Consequently, the repository does not yet claim that its equation
reproduces the latest slide deck. Because this interface does not accept the
presentation file types, verification requires the text of slides 48–66 to be
pasted into the conversation (including relevant speaker notes and descriptions
of equations or diagrams), or made available at a directly accessible,
non-authenticated URL.

## Current working interpretation

The prototype presently interprets **E-stress** as an interaction effect:

```text
E_stress = (Y innovation, stress - Y comparator, stress)
         - (Y innovation, no stress - Y comparator, no stress)
```

In words: first estimate the innovation's effect relative to the counterfactual
in stressed conditions; then subtract the effect it would have delivered in
non-stressed conditions. This isolates the stress-contingent incremental effect
and avoids counting an ordinary productivity benefit twice.

That interpretation implies:

* the sign and unit of E-stress are inherited from the outcome;
* a beneficial innovation can have zero or negative E-stress even when its total
  effect is positive, if it helps equally or more in non-stress conditions;
* stress must be defined independently of treatment and relative to a credible
  counterfactual outcome;
* co-benefits and benefits enabled by de-risking are separate quantities unless
  the official formulation explicitly includes them; and
* the current `Agr` implementation is only a weighted arithmetic mean of
  compatible E-stress estimates, not a confirmed transcription of the deck.

These are hypotheses to validate against the slides—not settled methodological
decisions.

## Information needed to bound the work

### 1. Authoritative formulation

1. Paste the text of the formulation slides and speaker notes into the
   conversation, including descriptions of equations/diagrams, or provide a
   directly accessible text/HTML version.
2. Identify the equation's exact symbols, parentheses, numerator, denominator,
   sign convention, and expected output range.
3. Clarify whether E-stress is a level, percentage, ratio, avoided loss,
   probability-weighted expected benefit, or normalized index.
4. Confirm whether the no-stress treatment effect is subtracted, retained as a
   co-benefit, or included elsewhere in the indicator.

### 2. Unit of analysis and counterfactual

1. What is the intended unit: plot, farm, household, person, landscape, project,
   innovation, or portfolio?
2. Is the comparator no innovation, business-as-usual, a locally common
   practice, or the best available alternative?
3. What time horizon and discounting rule apply?
4. For bundles, should the database store one bundle-level causal estimate,
   component effects plus interactions, or both?

### 3. Stress definition

1. Is stress defined from hazard intensity, exposure, outcome depression, a
   percentile relative to local history, or a combination?
2. Are the no/low/moderate/severe/extreme cut-offs prescribed by CGIAR or chosen
   per context? Who approves them?
3. Is classification based on the comparator only and fixed before observing
   treatment outcomes?
4. How should chronic stress, multiple simultaneous hazards, slow-onset change,
   and conditions with no observed non-stress baseline be handled?

### 4. Outcomes and valuation

1. Which outcomes are admissible (income, yield, nutrition, poverty, avoided
   loss, variance/downside risk, investment, schooling, conflict), and which are
   primary versus secondary?
2. Must outcomes be converted to money or another common unit? If so, provide
   prices, welfare weights, normalization, currency year, and purchasing-power
   rules.
3. Can negative effects and trade-offs offset benefits?
4. How are benefits enabled by de-risking attributed, timed, and protected from
   double counting?

### 5. Evidence and uncertainty

1. Which designs qualify: RCT, difference-in-differences, matching, structural or
   process models, expert elicitation, and policy analysis?
2. What minimum metadata and quality/risk-of-bias assessment are mandatory?
3. Should estimates store standard errors, confidence intervals, posterior
   draws, scenario ranges, or all of these?
4. How should missing cells, extrapolation, heterogeneous effects, spillovers,
   and correlated estimates from the same study be treated?

### 6. Aggregation (`Agr`)

1. What does `Agr` mean in the deck, and is it inside or outside the adaptation
   benefit equation?
2. What is the aggregation target and weighting basis: adopters, beneficiaries,
   hectares, probability of stress, investment, evidence quality, or portfolio
   policy?
3. May unlike outcome units be combined? If yes, what explicit conversion or
   multi-criteria rule is authoritative?
4. Are totals, averages, distributions, or conservative lower bounds required?
5. How are overlaps between innovations, bundles, populations, and benefits
   deduplicated?

### 7. Product boundary and validation

1. Is the required deliverable a research simulation, evidence registry,
   calculator, API, dashboard, or production reporting system?
2. Who are the users, reviewers, and data stewards, and what decisions must the
   output support?
3. Supply two or three worked examples with expected answers, including one
   bundle and one edge case. These should become acceptance tests.
4. Identify candidate datasets, access constraints, licensing, sensitive fields,
   and the expected scale of ingestion.
5. Define acceptance criteria: numerical agreement, reproducibility, audit trail,
   uncertainty reporting, performance, and export format.

## Recommended minimum next step

The smallest useful next step is a 60–90 minute formulation review using the
actual slides. Produce a signed-off one-page specification containing: the exact
equation; definitions for every term; one ordinary worked example; one chronic
stress/new-enterprise example; the `Agr` rule; and the required uncertainty
output. Only then should the database schema and calculator be treated as more
than a disposable prototype.
