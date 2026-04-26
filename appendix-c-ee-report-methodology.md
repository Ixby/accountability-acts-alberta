# Appendix C — Methodology proposal for the Enforcement Equity Report

*A drafted starting point for the Auditor General's office. Released under CC-BY-SA 4.0. Not a final methodology; a structured proposal designed to be revised in consultation with the office that would administer it.*

---

## Why this is an appendix

The Enforcement Equity Report at Bill 2 §7 is the most novel provision in the package and the most underspecified. Part V names a four-part methodological framework — a definition of "similarly-situated parties," a comparator-pool methodology, a covariate model, and a publication standard — but does not develop any of them in operational detail. A reader who is asked to take the provision seriously without seeing what its administration would actually look like has reasonable cause to set the brief down at that point.

This appendix runs the framework. It is not a final methodology. It is a structured proposal for what one looks like, written so that the Auditor General's office, regulators, scholars, and members of the regulated public can argue with it section by section. The intended use is the first-year *draft for comment* contemplated by Part V — a document the AG's office would publish, receive submissions on, and refine before the first formal Enforcement Equity Report is tabled.

The appendix borrows nothing operational from any specific Canadian or international regulator's existing practice, because none has published a methodology for systemic enforcement-equity analysis at provincial scale. Where the appendix gestures at analogues, those analogues are partial — fairness-in-policing analyses, securities-enforcement reviews, tax-administration audits — and none of them resolves the core problem the EE Report is built to address.

---

## Purpose and scope

The EE Report asks one question. When a regulator makes an enforcement decision — to inspect, to sanction, to refer for prosecution, to resolve administratively, to defer, to close — does the pattern of those decisions, when assembled across cases, correlate with characteristics of the regulated parties that should not be driving enforcement?

The report does not adjudicate any individual case. Individual adjudication is what the regulator's existing processes do. The report does not replace regulator judgement. It sits one layer above the case file, looking at decisions in aggregate.

The report covers regulatory bodies, administrative tribunals, and enforcement agencies as defined in Bill 2 §7. The first report covers a small number of bodies; coverage expands to all designated bodies within five years. The five-year timeline is deliberate, because the methodology has to be developed in the open and refined iteratively. A fully formed methodology dropping in at year one would be either undercooked or a fiction.

What the report does *not* cover: the Crown's own conduct in litigation; case-specific privilege; matters subject to active law-enforcement investigation; regulatory decisions that are already subject to judicial review on the same record. The report is a pattern-detector. It is not a court.

---

## The four-part framework, developed

### Part 1 — Similarly-situated parties

The hardest definition in the appendix. Two regulated parties are "similarly-situated" for the purposes of the EE Report if their underlying conduct is comparable on the regulator's own definitional terms, and the parties are comparable along axes the regulator's enforcement decisions might reasonably attend to.

Four operational tests for similarity. Each is a necessary condition; together they are sufficient for inclusion in a comparator pool.

**Sector.** Same regulated activity, defined by the regulator's own classification system or by NAICS / NOC code where the regulator does not maintain one. Cross-sector comparisons are not what the report is for. A pipeline operator's enforcement record is not comparable to a hospital's enforcement record, regardless of how the underlying conduct might appear similar in a procurement-style abstraction.

**Scale.** Comparable approximate scale, defined by whichever metric the regulator uses to set its own enforcement tier — production volume, employee count, revenue band, number of regulated assets. The metric matters: a regulator that classifies operators by production volume produces enforcement tiers that look different from a regulator that classifies by revenue. The EE Report uses the regulator's own scale metric, not an externally imposed one.

**Regulatory history.** Comparable prior regulatory record, defined by the recency, severity, and resolution of prior enforcement actions. A first-time violation at a party with a clean ten-year history is not comparable to the same violation at a party with three prior violations resolved at escalating severity. The covariate model in Part 3 holds prior history statistically constant; the similarity test ensures the comparator pool is at least minimally comparable on this dimension before the model runs.

**Geography (where geography matters).** Some regulators have geographic enforcement variation that is operationally legitimate — different field offices, different inspection timetables, different regional capacity. Where geography matters, similarity is bounded within geography. Where geography does not matter operationally, the geographic axis is dropped.

The output of Part 1 is, for any given enforcement decision, a definitional rule that identifies a pool of similarly-situated parties facing comparable underlying conduct. The pool is constructed from the regulator's own records and verified independently by the AG.

### Part 2 — Comparator pool construction

The pool for any given enforcement decision is the set of all similarly-situated parties who, over a comparable window, faced comparable underlying conduct on the regulator's own definitional terms, and for whom the regulator made an enforcement decision (including the decision not to enforce, where that decision is recorded).

Three construction rules:

**The window.** The comparable window is calibrated to the regulator's own enforcement cycle and the conduct's typical duration. For a one-time violation, the window is the period from the conduct's occurrence to the next regulator review of the operator. For a continuous-conduct violation, the window is the regulator's standard inspection or audit cycle. Where the regulator has no standard cycle, the AG sets a window with reasons published.

**The corpus.** The full corpus from which pools are drawn is the regulator's complete enforcement-decision record over the relevant window. This includes decisions to inspect, decisions to issue warnings, administrative penalties, prosecution referrals, settlements, and decisions to take no action where conduct was identified. The AG accesses the record through a confidentiality protocol described in the *Data architecture* section below.

**Verification.** The pool the AG constructs is verified independently against the regulator's own records by sampling: the AG draws a 5% random sample of pool decisions and asks the regulator to confirm the relevant facts (the conduct, the parties, the decision, the date). Discrepancies above a published tolerance — meaning more than two percent of sampled decisions cannot be confirmed — trigger reconstruction of the pool with the regulator's input. This is iterative and may take more than one cycle to settle.

The output of Part 2 is a defensible comparator pool for each enforcement decision examined, with the construction methodology documented so the regulator and the public can examine it.

### Part 3 — The covariate model

Once the comparator pool is constructed, the question is whether the regulator's decisions across the pool show patterns that correlate with characteristics of the parties that should not be driving enforcement. The naive version of this analysis — simply observing that party A was sanctioned and party B was not — does not survive any serious regulator's response, because regulators have many legitimate reasons to treat similar cases differently.

The covariate model holds the legitimate explanations statistically constant before testing the residual variance for problematic correlations.

**Variables held constant.** At minimum:

- *Cooperation.* Did the party cooperate with the regulator at the moment of enforcement? Cooperative parties routinely receive lighter administrative responses than uncooperative ones; this is operationally legitimate. The covariate is binary at the gross level (cooperated / did not cooperate) and ordinal at the fine level (degree of cooperation, recorded by the regulator).
- *Severity.* The regulator's own severity scoring of the underlying conduct. A spill of one barrel and a spill of ten thousand barrels are not comparable by the regulator's own terms even where both fall within the same statutory provision.
- *Complexity.* Is the regulator's decision constrained by the case's legal or technical complexity? A novel question of statutory interpretation may legitimately produce a softer enforcement response while precedent develops. The covariate is ordinal, set by the regulator's own complexity flag where one exists.
- *Voluntary disclosure.* Did the party self-report the conduct to the regulator? Self-reporting is widely treated as mitigating, and properly so. The covariate is binary.
- *Prior compliance history.* The covariate the similarity test held only minimally constant, now controlled in detail at the model stage. Number of prior actions, severity of priors, time since most recent prior.

**Variables tested for.** After holding the legitimate variables constant, the residual variance is tested against:

- *Industry sub-sector* (within the broad sector that defined the pool).
- *Party size class* (within the broad scale band that defined the pool).
- *Political contribution history of the party's individuals with significant control* (drawing on the Bill 1 §15 cross-reference register; the contribution history examined is from the four-year window preceding the conduct or the enforcement decision, whichever is earlier).
- *Recent receipt of state benefit* (concessional arrangement, regulatory approval, ministerial individual exemption — drawing on the Bill 2 disclosure registers).
- *Stated location relative to government caucus seats* (where the regulator covers province-wide activity).

The tests are statistical. The model produces correlation coefficients with confidence intervals. A correlation that survives at the published confidence threshold is "pattern identified." A correlation that does not is "pattern not identified." Neither characterization implies a corruption finding.

**Multiple comparisons.** The covariate model runs many tests simultaneously. The AG corrects for multiple comparisons using a published method (false discovery rate at q = 0.05 is the appendix's working proposal; the office may choose a different correction with reasons published). Without correction, the EE Report would generate spurious patterns; with conservative correction, it would miss real ones. The chosen correction is documented and re-examined annually.

**Statistical software and reproducibility.** All analyses are conducted in software that produces reproducible scripts. The scripts, with personal-information redaction, are published alongside the report so independent analysts can replicate the analysis on the same data or run sensitivity analyses with different parameters.

### Part 4 — Publication standard

The report distinguishes three states for any given regulator-conduct combination:

- **Pattern not identified.** The covariate model finds no statistically significant correlation between residual variance and any of the tested variables, after multiple-comparisons correction. The report so reports.
- **Pattern identified, no further inquiry warranted.** A statistically significant pattern is detected, but its magnitude or direction does not warrant further inquiry — for example, a pattern that is statistically real but operationally trivial, or a pattern in a direction the regulator can defensibly explain on the public record.
- **Pattern identified, further inquiry warranted.** A statistically significant pattern is detected whose magnitude, direction, or covariate combination raises questions the regulator's standard processes do not resolve. The report so reports, and the matter is referred to the Ethics Commissioner under Bill 1 §22 if the pattern implicates conduct within the Commissioner's jurisdiction, or remains a published finding for the political process and the press to act on.

Each report category includes:

- The methodology used (which can change year-over-year as the methodology refines).
- The data accessed.
- The pool construction details.
- The covariate model parameters.
- The correlation results, with confidence intervals.
- The multiple-comparisons correction applied.
- The regulator's response, where one is provided.
- The Auditor General's comments on the response.
- The communications log under Bill 2 §7(8).

A "pattern identified" finding is not a corruption finding. The report so states, prominently, in every relevant section. The point of the regime is to surface patterns the regulator's own data reveals when assembled across cases, not to replace adjudication.

---

## Data architecture

The AG needs access to the regulator's enforcement-decision record. Three architectural questions: what data, on what schedule, under what confidentiality.

**What data.** A unified record that captures, for each regulatory action over the relevant window:

- The regulated party (entity name + ISC where the entity has one).
- The conduct identified.
- The regulator's classification of severity.
- The regulator's classification of complexity.
- The cooperation indicator.
- The voluntary-disclosure indicator.
- The decision (no action, warning, administrative penalty, prosecution referral, settlement, other).
- The date of the decision.
- The geographic locus where geography matters.
- Any cross-references to prior actions involving the same party.

Most regulators already collect most of this. Where they do not, the EE Report's first-year coverage is limited to the regulators that do, and the others are added as their data infrastructure catches up.

**On what schedule.** The data refresh is annual, in the first quarter of the calendar year, covering the preceding fiscal year. Incremental updates are tracked but not separately reported.

**Under what confidentiality.** Three layers.

The AG's office holds the data under the existing confidentiality framework that governs AG audits — the *Auditor General Act* preserves the AG's access to public-body information without compromising business confidentiality of regulated parties. The EE Report regime sits inside that framework.

The published report aggregates and anonymizes. Specific parties are named only where the underlying conduct is already a matter of public record (e.g., a published enforcement decision) and where naming the party adds analytical value the report cannot otherwise convey. Where naming is unnecessary, parties are coded.

The reproducibility scripts published alongside the report use anonymized data with personal-information redaction. The full underlying record remains with the AG and the regulator.

---

## A worked illustration: the Alberta Energy Regulator

A concrete pass through the methodology, applied to a notional EE Report on the AER's enforcement of the *Oil and Gas Conservation Act* over a five-year window. This is illustrative; the AER would be one of the bodies covered, and the methodology would apply broadly similarly to other regulators.

**Pool construction.** For each enforcement decision in the window — say, an administrative penalty issued for a flaring exceedance — the comparator pool is all operators with comparable production volume, comparable past five-year compliance history, operating in the same operational region, who recorded a flaring exceedance in the same statutory window. The pool is drawn from AER's own enforcement record, verified by a 5% sample.

**Covariates held constant.** AER's own compliance-investigation records identify cooperation, severity, complexity, voluntary disclosure, and prior compliance history for each enforcement decision. The covariate model uses these AER-recorded values directly.

**Variables tested.** The model tests whether residual variance in enforcement disposition (warning vs. administrative penalty vs. prosecution referral) correlates with: operator size sub-class within the comparable production-volume band; operator's ISCs' political contribution history within the four-year window; operator's receipt of a regulatory approval, concessional arrangement, or ministerial individual exemption within the four-year window; operator's geographic concentration relative to government caucus seats.

**Possible outputs.** Three illustrative scenarios:

*Scenario A.* The covariate model finds no statistically significant correlation. The report so reports. The regulator's enforcement of the *Oil and Gas Conservation Act* over the window is consistent with the legitimate explanations the model controlled for. Public confidence is reinforced; the regime imposed minor cost on AER and the AG; no further inquiry follows.

*Scenario B.* The model finds a statistically significant correlation between operator size class and enforcement severity, after controlling for cooperation, severity, complexity, and prior history. Larger operators receive proportionally lighter administrative responses than smaller operators for comparable conduct. The report identifies the pattern and notes that a defensible explanation exists — larger operators have more sophisticated counsel and may resolve enforcement more efficiently — but the magnitude warrants further inquiry. The regulator responds; the AG comments. The political process reads the report.

*Scenario C.* The model finds a statistically significant correlation between operator ISC contribution history and enforcement disposition: operators whose ISCs contributed above the four-year threshold to the governing party receive proportionally lighter responses. The report so reports. The matter is referred to the Ethics Commissioner under §22; the political process reads the report. No corruption finding has been made, by the AG or by the Commissioner; what has happened is that a pattern in the regulator's own data has been surfaced.

The illustrations are notional. None corresponds to a current AER enforcement record. The point is to show what an actual EE Report output looks like at the level a regulator and the public can engage with it.

---

## What the methodology cannot do

Honest accounting. Five limits.

**It cannot replace regulator judgement on individual cases.** The report is a pattern-detector across cases, not an adjudicator within them. Every individual enforcement decision the report examines was made by the regulator on its own grounds; the report does not unmake any of those decisions.

**It cannot identify causation.** Statistical correlation between residual variance and a tested variable does not establish that the variable caused the variance. The report identifies the pattern; the political process, the regulator, the Commissioner, and the public draw inferences.

**It cannot detect patterns smaller than its statistical power admits.** Where a regulator handles few decisions per year, or where the comparator pool is small, the model may not detect a real pattern that a larger pool would have surfaced. The report is honest about this; "pattern not identified" does not mean "no pattern exists."

**It cannot cover regulators whose data infrastructure is inadequate.** The first-year coverage is limited to bodies whose enforcement records meet the methodology's data requirements. Coverage expands as data matures. Where a regulator is excluded from a year's report for data reasons, the report so notes.

**It cannot prevent the regime from being weaponised.** A captured Auditor General who selects which patterns to publish, or who calibrates the methodology to surface or suppress particular kinds of correlation, can corrupt the report from inside. The defences against this are upstream of the methodology: the Auditor General's two-thirds appointment and removal under Bill 1 §11B; the §24 budget floor; the §7(8) communications log. The methodology's own contribution is procedural — published methodology, reproducibility scripts, regulator-response sections, multiple-comparisons correction with stated parameters. None of those are guarantees.

---

## Iterative refinement

The methodology is published in draft form in the AG's first year of operation under §7. The draft is open for written submissions from regulators, the regulated public, scholars, civil-society organizations, and members of the public. The AG publishes the submissions received and a written response. The methodology is revised based on the submissions and the AG's analysis; the revised methodology is the basis for the first formal EE Report.

The methodology is reviewed every three years thereafter. The five-year coverage timeline at Bill 2 §7 is calibrated to the iterative-refinement schedule: year one is draft-for-comment; years two through four are first-cycle reports with one or two regulatory bodies; year five expands to full coverage of designated bodies.

Methodology changes are published with reasons. A revision that materially changes how a pattern would be classified ("identified" vs. "not identified") is published with a parallel re-analysis of the prior year's report under the new methodology, so longitudinal comparability is preserved.

---

## What other jurisdictions do

A short comparative survey, partial because the analogues are partial.

**Federally.** The Canada Revenue Agency conducts large-scale random-audit programs whose findings are aggregated annually but not disaggregated by enforcement-equity dimensions of the kind this methodology would examine. The Office of the Auditor General of Canada conducts performance audits that occasionally examine enforcement-equity questions for specific programs but does not maintain a continuous methodology of the kind proposed here.

**Peer provinces.** No Canadian province currently produces an annual systemic enforcement-equity report under a published methodology. Some provincial Information and Privacy Commissioners have produced one-off systemic studies; none is annual or regularised.

**Comparable international practice.** The United Kingdom's National Audit Office and Australia's National Audit Office both conduct enforcement-pattern analyses on specific programs but have not generalised to a continuous province- or state-wide methodology. United States state-level analogues are partial, focused on specific enforcement domains (policing, securities, environmental), and uneven in methodology.

**The EE Report's distinctiveness.** What the EE Report adds is the combination: continuous, province-wide, methodologically uniform, statistically rigorous, published with reproducibility scripts, paired with a communications log that catches ministerial pressure. None of the analogues combines all of those elements, which is why Part V calls the report "genuinely new in Canadian provincial practice."

---

## Statistical robustness

Five tests the methodology should pass before any formal report is published.

**Sample-size adequacy.** Each comparator pool must contain enough decisions to detect a meaningful pattern at the chosen confidence threshold. The methodology specifies a minimum pool size; pools that fall below the minimum are reported as "insufficient data" rather than as "pattern not identified."

**Multiple-comparisons correction.** The chosen correction (false discovery rate at q = 0.05 in the working proposal) is applied transparently and re-examined annually.

**Sensitivity analysis.** Each "pattern identified" finding is tested against alternative covariate specifications, alternative pool-construction rules, and alternative correction methods. The robustness of the finding to specification changes is reported.

**Independent replication.** The reproducibility scripts published alongside the report allow independent analysts to replicate the analysis. The AG's office welcomes replication submissions and publishes responses.

**Public verifiability.** A non-technical reader cannot verify the underlying statistics directly, but can verify the methodology is being followed (by reading the methodology document and the report's methodology section), and can verify the data is what the AG said it was (by reading the regulator's response section). The report is not a black box.

---

## Sample published-report template

A skeleton of what an annual EE Report looks like as a document.

*Front matter.* The report's title, the AG's signature, the date, the bodies covered, the period covered.

*Methodology section.* The current methodology, with any changes from the prior year flagged. The pool-construction rules. The covariate-model specification. The multiple-comparisons correction.

*Per-body sections.* For each regulatory body covered:

- Description of the body's enforcement role.
- Data accessed and the period covered.
- Pool-construction details specific to the body.
- Patterns examined (the variables tested).
- Findings — pattern not identified / pattern identified, no further inquiry / pattern identified, further inquiry warranted.
- Regulator's response.
- AG's comments on the response.

*Cross-cutting sections.* Patterns that appear across bodies. Methodological refinements proposed for the next cycle.

*Communications log.* The §7(8) record of all communications received about the report's scope, methodology, selection, or findings, with the characterizations the section requires (informational, advisory, directive). A nil return where appropriate.

*Reproducibility appendix.* Pointers to the published scripts and anonymized data sets.

*Methodology evolution.* The changes from the prior year's methodology, with reasons.

The report is a substantial document. It should be. The methodology argues that what is being measured matters; the report's length is the cost of doing it carefully.

---

## Final note

This is a starting point. The Auditor General's office, in consultation with the bodies it covers and the public it serves, will produce a methodology that supersedes most of what this appendix proposes. That is the design intent: the appendix exists so the conversation has somewhere to start, not so the AG is bound to anything in particular.

What the appendix does not concede is the proposition that systemic enforcement-equity analysis at provincial scale is impossible. It is hard. It has not been done in the form Bill 2 §7 contemplates. The methodology developed here is one good-faith attempt at showing how it could be done. Better attempts will follow. That is the right pattern for a hard problem.
