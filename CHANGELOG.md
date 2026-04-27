# Changelog

Version history for the Honest Government and Open Books Acts drafting package.

Entries below mark substantive changes to the legislation. Intermediate editorial passes are not listed.

## v1.16

Consolidation pass. No substantive changes to the regime; tightens repeated patterns and moves operational detail to regulation.

- **Bill 2 §8B (new common provision)** — Consolidates two patterns that previously appeared four times across §§3–6: (1) the failure-to-publish enforcement clause (formerly §4(5), §5(5), §6(5)), and (2) the right-of-correction provision (formerly §3(7A), §4(7A), §5(6A), §6(5A)). Both now apply uniformly to every Beneficiary Disclosure Statement, Proponent Disclosure Record, Concessional Arrangement Disclosure, and Individual Exemption Disclosure through a single common provision. Privilege carve-outs remain in their respective sections because they vary by actor (sponsor, regulatory body, Minister) and grounds. Subsections in §§4, 5, 6 renumbered accordingly.
- **Bill 1 §15A(2)(c)** — Country-specific identifier examples (US SSN, UK NI, AU TFN) moved to regulation. The provision now reads "a foreign persistent national identification number prescribed by regulation." The principle (use a persistent national ID, not a passport number) stays in legislation; the country list is regulation-level detail that will need updates over time.
- **Bill 1 §15A(7)** — "Platform dependency" provision moved from §15A operational subsections to §31(5) Transitional Provisions. Its function is implementation transitional — it handles the case where MADI cannot issue persistent cross-application identifiers — and ceases to have effect once Service Alberta confirms the capability. Former §15A(8) good-faith defense renumbered to §15A(7).
- **costing.md** — Updated to reflect the v1.15 privacy architecture additions: MADI integration, blind hash architecture, cross-registry similarity matching engine, and Tier 0 automated compliance check infrastructure increase year-one capital from $1.5M to $1.7M; ongoing technology operating from $400–700K to $450–800K. Tier 0 audit automation partially offsets manual audit labour. Steady-state estimate stays at ~$5M.

## v1.15

Privacy architecture — ten provisions across both bills addressing collection minimization, identity consistency, automated audit tiers, and data subject rights.

- **Bill 1 §2(w)** — "family member" defined. Spouse, common-law partner, dependent child only; adult children, parents, siblings excluded unless they are also an ISC of the same entity. Closes definitional gap in §15(2) which already referenced the term.
- **Bill 1 §15(2A)** — Blind hash cross-reference. The contribution registry cross-reference under §15(2) now proceeds as a hash comparison returning only a match/no-match indicator. No contribution history disclosed at any level unless a match is confirmed. On match, the Commissioner accesses history solely for the §15(2) review; records are confidential under §25(9). Addresses the Charter §2(b) concern that routine disclosure of political contribution history chills political expression.
- **Bill 1 §15(8)** — Accountability as procurement condition. Bidders above the full-disclosure threshold are deemed to have acknowledged, by submitting a bid, that ISC disclosure compliance is a procurement condition, in the same manner as other Crown contracting conditions.
- **Bill 1 §15A** — Identity consistency via MADI/provincial ID (new section). Primary: MyAlberta Digital Identity platform (named by regulation so provision survives platform upgrades). Fallback chain: AB driver's licence/AB ID Card → SIN → foreign persistent national ID under sworn declaration → DOB + country combination with notarization. Passport numbers explicitly excluded (change on renewal; not persistent identifiers). Separate entity track using AB corporate registry number / CRA Business Number / foreign registry number. Automated similarity matching with name consistency notices for inadvertent variation. Escalating consequences for deliberate fragmentation: first finding (correction + fee + 12-month enhanced scrutiny), second within 5 years (§25 penalty + 24-month procurement suspension for all ISC entities), third or systematic (maximum penalty + permanent ban + criminal referral). Good-faith defense applies; cultural naming practices and legal name changes are not fragmentation.
- **Bill 1 §25(9) amended** — Data minimization principle added to end of existing Verification of Means provision.
- **Bill 1 §25(9A)–(9B)** — Self-declaration cascade and financial information destruction. Capacity determined in order: public filings → self-declaration under oath (14 days) → audited statements/tax filings → net asset investigation. Financial information destroyed no later than 90 days after proceedings conclude or appeal period expires; written confirmation to respondent.
- **Bill 1 §27(2) revised** — Tiered automated audit. Three-tier structure: Tier 0 (automated cross-reference only, no human review, closes at Tier 0 if no discrepancy), Tier 1 (documentary review on flag, limited to records already held or required to be maintained), Tier 2 (active investigation on specific Tier 1 indicators, full investigative powers, full procedural rights from commencement). Verifiable randomness and published methodology requirements preserved.
- **Bill 1 §27(6A)** — Clean-file destruction. Audits closing at Tier 0 or Tier 1: personal and financial records destroyed within 90 days, written confirmation to audited person, aggregate data and closure note retained (closure note does not identify the individual in public reports).
- **Bill 1 §29A** — Personal information retention maximums (new section). 10-year maximum, subject to ongoing proceedings, public domain, and anonymization exceptions. Annual retention schedule published and tabled.
- **Bill 1 §30(2) amended** — Privacy impact assessment requirement added. Review must include assessment of privacy proportionality and operation of retention/destruction provisions. Commissioner publishes PIA within 12 months of commencement, per IPC standards.
- **Bill 2 §3(7A), §4(7A), §5(6A), §6(5A)** — Right of correction for published disclosures. Any person whose personal information appears in a Beneficiary Disclosure Statement, Proponent Disclosure Record, Concessional Arrangement Disclosure, or Individual Exemption Disclosure may apply within 60 days to correct material inaccuracy. Commissioner determines within 30 days; correction notice published alongside original (original not removed, correction notice prominently linked).
- **red-team.md** — Restructured into six Parts: Method and Sources (I), Case Studies (II), Failure Mode Analysis §1–12 ordered LOW to HIGH severity (III), Motivated Actor Scenarios §13–16 (IV), What the Regime Gets Right (V), Residual Risk Register (VI).

## v1.14

- **Bill 1 §21B** — Writ period rule. No new investigations commenced from writ issue to writ return. Ongoing investigations continue in all respects. Outputs from ongoing investigations not delayed or accelerated by the writ; Commissioner shall not time releases to coincide with electoral events. Certificates issued during writ are held for tabling on the first sitting day after return. Complaints received during the writ are held and investigation commences after return. Resolves the open question flagged in the README.

## v1.13

Five structural gap provisions, each addressing a vulnerability identified in the post-v1.12 robustness review as not covered by the sunshine philosophy: gaps where public record-keeping alone was insufficient and legislative enforcement was available.

- **Bill 1 §11B** — Auditor General appointment independence. Mirrors the §11A Commissioner appointment fix: 2/3 Committee (Standing Committee on Public Accounts) + 2/3 Assembly for appointment; eligibility bar on anyone who held elected office or party executive position within the prior 7 years; 2/3 Assembly for removal; Chief Justice of King's Bench vacancy fallback at 120 days. The Enforcement Equity Report (Bill 2 §7) is the AG's primary function under this regime; leaving the AG appointment unprotected made §7 contingent on the will of the appointing government.
- **Bill 1 §16(4A)-(4B)** — Censure-as-disposal gap closed. A resolution consisting solely of censure does not satisfy the Assembly's obligation under §16(4) where the Certificate incorporates a financial penalty determination above the threshold. Certificate remains open until the Assembly passes a substantive resolution, closes it by 2/3 supermajority with written reasons, or exhausts the 60-sitting-day clock triggering deemed law enforcement referral. Prevents a hostile majority from making the enforcement ladder cosmetically rather than substantively operative.
- **Bill 1 §18A** — Whistleblower preservation orders. Commissioner may issue a preservation order at commencement of investigation directing: (a) specified records not be altered or destroyed; (b) employment status of complainants and witnesses not be altered pending determination. Status quo order, not reinstatement. Willful breach in category warranting Certificate without prior tier escalation. Practice direction to issue routinely at investigation commencement. Closes the gap between disclosure protection (which was strong) and evidence preservation (which was absent).
- **Bill 1 §22A** — Protection against proceedings for delay. Where the Commissioner has reasonable grounds to believe a challenge was brought primarily for delay, Commissioner may apply for expedited Court hearing within 20 business days. Costs awarded presumptively to Commissioner on solicitor-client basis on any failed challenge. Stay under §22(4) is limited: does not apply to Commissioner publications, record production obligations, or ongoing investigation. Security for costs available. Closes the asymmetric litigation cost vulnerability.
- **Bill 1 §24(6)-(7)** — Budget floor with recorded vote requirement. Main estimates must include appropriation not below the greater of: (a) prior year adjusted for CPI; (b) minimum operational level from most recent resource plan and adequacy notice. Where estimates fall below: President of Treasury Board must table written consequences statement with Commissioner's written response; reduction voted separately and by recorded vote in Committee of Supply. Constitutional qualification preserves Assembly appropriation authority; the provision operates as a procedural disclosure requirement, not a spending mandate.

## v1.12

Defensive provisions addressing the eight highest-priority partisan attack vectors. Philosophy: where enforcement is constitutionally unavailable, substitute mandatory public record-keeping. Build the record; let voters and journalists decide.

- **Bill 1 §13(5)** — Mandate letter non-disclosure log. Where a mandate letter is withheld under §13(4) exceptions, the withholding is recorded in a public IPC-maintained register: Minister, subject matter (assessed for adequacy by IPC on application), date, and exception claimed. Content stays protected; the claim of protection is visible.
- **Bill 1 §24(4)** — Monthly resource adequacy notice. Fixed pre-announced publication date. Mandatory Commissioner-prescribed format covering caseload, funded capacity, and infrastructure build status. Auto-tabled with Speaker on starvation or build failure.
- **Bill 1 §24(5)** — Cooperation register. Annual log of every threshold-setting request to LGIC, whether a responsive regulation was made within 90 days, and adequacy assessment. Makes regulatory non-cooperation a matter of public record.
- **Bill 1 §26(5)** — Opinion-shopping disclosure. Defense now requires disclosure of all legal opinions obtained on the same question, not just the one relied upon. Pattern of discarding contrary opinions and relying on a permissive minority opinion is evidence of wilful blindness under §26(4)(c).
- **Bill 1 §28(7)** — Threshold adequacy mechanism. Commissioner annual adequacy assessment; Commissioner/AG may issue counter-regulation where LGIC threshold would substantially defeat operative effect; counter-regulation prevails unless Assembly disallows; every disallowance recorded in cooperation register with operational consequence stated.
- **Bill 2 §7(8)** — AG communications log. Every Enforcement Equity Report includes a complete log of all communications from Ministers/officials about scope, methodology, selection, or findings; characterized as informational/advisory/directive with reasons; nil return required where none received.
- **Bill 2 §8A** — Named-party compliance assessment. Commissioner annual assessment identifying every Bill meeting §2(f) criteria for which no Beneficiary Disclosure Statement was filed, with reasons. Framed as administrative opinion, not a ruling on parliamentary procedure.

## v1.11

Substantive structural fixes to both bills and costing.md, addressing the three highest-priority gaps identified in the defensibility review.

**Bill 1 — §22(5) McIver fix.** Court confirmation for large penalties split by respondent type. *McIver v Alberta (Ethics Commissioner)*, 2017 ABQB 695 establishes that courts have no jurisdiction over Ethics Commissioner decisions involving sitting MLAs due to parliamentary privilege — court confirmation against a sitting Member would not survive a privilege challenge. §22(5) now has two tracks: (a) court confirmation for non-Members (unchanged), and (b) for sitting Members, the penalty is incorporated into a Certificate of Malfeasance and enforced exclusively through the Assembly process under §16.

**Bill 1 — §11A Commissioner appointment.** Neither bill previously addressed how the Commissioner is appointed. A compliant appointment defeats every other protection before the first investigation opens. §11A amends Conflicts of Interest Act s.15: appointment now requires two-thirds of the Select Standing Committee on Legislative Offices plus two-thirds of the full Legislative Assembly (up from a simple majority Assembly motion); term extended to 7 years non-renewable (up from 5); eligibility bar on anyone who held elected office or party executive position within the prior 7 years; removal requires Committee report plus two-thirds Assembly resolution. Based on BC Conflict of Interest Commissioner (2/3 supermajority model) and federal Auditor General (open competition + legislative approval) best practices.

**Bill 2 — §2(f) named-party definition tightened.** "A small number" was undefined, giving the Speaker no concrete anchor and opponents a broad attack surface. Third prong was broad enough to catch concentrated-industry legislation where one or two parties dominate a sector by nature, not by legislative design. Fix: "small number" replaced with explicit five-or-fewer threshold; third prong adds a reg-prescribed value threshold to exclude trivial applications; four safe harbors added for general-criteria legislation, public infrastructure legislation (where private benefit is incidental), treaty and court-order implementation, and transitional legislation giving effect to pre-existing entitlements.

**costing.md — counterfactual savings figures removed.** Per-case savings estimates ($10–30M, $20–40M, $20–50M) were drafter speculation. Aggregate table and net-return paragraph replaced with a cost-comparison table (annual regime cost vs. taxpayer cost of each case) and explicit acknowledgement that the case is structural, not predictive. Scenario analysis narratives retained — they describe which provisions engage and at what decision points, which is verifiable; what those provisions would have saved is not.

## v1.10

No substantive changes to the legislation. Companion documents revised for factual accuracy and confidence framing after a verification pass against external sources.

- README, social-media-post: scandal cost figures corrected. DynaLIFE updated to reflect $31.5M cash plus ~$66M assumed liabilities and the Auditor General's November 2025 estimate of approximately $109M total taxpayer cost. Turkish Tylenol corrected to clarify Health Canada only approved $21M worth of the $80M total, with most supply remaining in storage. Canadian Energy Centre corrected to clarify $30M was the initial budget (cut to ~$12M from 2020 onward), with the agency wound down June 2024 and lifetime cost estimated at $50–100M.
- README cost case table: removed "Net if prevented" column that overclaimed counterfactual prevention. Replaced with side-by-side cost comparison; the prevention claim is now explicitly counterfactual and uncertain in surrounding text.
- README "What makes this different" → "What this regime tries to do differently": reframed throughout to distinguish design intent from accomplished fact.
- README opening paragraph: added explicit "this is the opening of a conversation" framing and acknowledgement that external review is required for several specific items before tabling.
- Tagline: "two bills, costed, defended, and built to bind whoever holds power" → "two bills with cost analysis, philosophical defence, and adversarial analysis of failure modes. Released to open a conversation, not to close one."

## v1.9

- §28 consolidated: former subsections (5) and (5A) merged into a single Assembly oversight provision covering tabling, disallowance, ongoing amendment authority, and annual reporting.
- §25(6) Cost proportionality and decline tracking streamlined. Register mechanics and threshold-notification rule tightened.
- §26(1) Good-faith defense restructured into (a)(b)(c) subclauses for clarity: good-faith requirement, reasonable-reliance bases, and knowledge test.
- §30(2) Statutory Review scope tightened. Same substantive review areas; more compact drafting.

No substantive changes to the regime.

## v1.8

- §10(1) post-employment cooling-off period set at 18 months. Balances deterrent effect against legitimate public-service mobility.

## v1.6

- §14A Duty to Document added to Part 4 (ATIA amendments). Decisions subject to disclosure under either Act must be documented. Standards set by the Information and Privacy Commissioner by regulation. Willful or repeated failure is penalty-tracked.
- §26(5) Disclosure of advice relied upon added to the good-faith defense. A respondent invoking the defense must disclose the scope of the mandate provided to counsel, facts provided, and any conflicting advice received. Limited privilege waiver for defense purposes only.

## v1.4

- Bill 2 §2(f) "named-party legislation" expanded with indirect benefit prong: captures legislation whose ostensible beneficiary is generic but whose practical effect is benefit to a small class of identifiable parties.
- §29(4) False complaint fee added. Complaints found frivolous, vexatious, or made in bad faith may be fee-recovered against the complainant. Proportional under §25. Does not apply to journalists, whistleblowers, or first-time complainants regarding personal experience.
- Bill 2 §7(7) Phased implementation of the Enforcement Equity Report. Three regulatory bodies covered in year one, full implementation across all designated bodies within five years.
- §25(9) Tax-filing proxy added. Where net asset verification is impractical, the Commissioner may use three-year gross income from Income Tax Act filings as a verifiable capacity proxy.
- §22(6) Cabinet confidence preservation clarified. The §13 amendment does not otherwise affect Cabinet confidence privilege.

## v1.3

- §28 Regulation-making authority substantially rewritten. Commissioner and Auditor General jointly make most operational regulations, with Legislative Assembly disallowance within 30 sitting days as the check. Lieutenant Governor in Council retains baseline threshold-setting and regulations affecting private rights.
- §21A First Nations, Métis, and Inuit Governance added to Part 8. Internal governance carved out entirely. Consultation required before action affecting Indigenous-owned entities. Materiality threshold set by regulation. Section 35 rights and treaty rights expressly preserved.
- §15(1A) Simplified small-bidder track added. Annual declaration instead of per-bid disclosure. Lower processing fee cap.

## v1.2

- §6 Principles reordered to put institutional deference first.
- §25(2) Calibration principle consolidated into a single unified provision.
- Severity ordering applied throughout: §9(1) escalation triggers, §16 Recall framework, §19(1) whistleblower triggers, §26(4) defense unavailability grounds.
- Short titles at §1 of each bill — "The Government Accountability Act" and "The Open Books Act" — become the operative names.

## v1.1

- Short title placed at §1 of each bill per legislative drafting convention.
- Definitions alphabetized in both bills.
- Good-faith defense relocated to §26, immediately after the proportional penalty framework at §25.
- Commencement separated from transitional provisions.

## v1.0

Initial combined package.

Bill 1 coverage:

- Lobbyists Act amendments
- Conflicts of Interest Act amendments and escalation framework (Public Report → Compliance Order → Certificate of Malfeasance)
- Access to Information Act amendments
- Financial Administration Act amendments (ISC disclosure)
- Recall Act amendments
- Public Interest Disclosure Act amendments
- Common procedural provisions including proportional penalties, good-faith defense, random audit, threshold calibration, cost recovery, and statutory review

Bill 2 coverage:

- Named-party legislation disclosure
- Regulatory approval proponent disclosure
- Concessional arrangement disclosure
- Ministerial individual exemption disclosure
- Auditor General enforcement equity reporting
- Enforcement and common provisions

---

## Companion documents

### costing.md v1.1

Sources and confidence section added upfront distinguishing empirically verified figures, drafter's estimates, and counterfactual scenario estimates. Scandal cost figures corrected against Auditor General report (DynaLIFE) and contemporary reporting. Scenario savings ranges adjusted with explicit confidence ratings (low to moderate, moderate to high). "Pays for itself" framing removed. Peer jurisdiction budget figures softened to ranges with explicit acknowledgement that they are approximate and that the Alberta proposal's per-capita rate is somewhat higher than peers — a difference attributed to broader scope but flagged for external review rather than asserted as justified.

### costing.md v1.0

FTE breakdown across oversight offices. Technology and infrastructure costs. Phase-in schedule. Scenario analysis of three recent Alberta cases against the proposed regime. Comparison to peer Canadian oversight budgets.

### moral-defence.md v1.1

Note on philosophical sources added — references to Burke, Mill, and others framed as general characterizations rather than specific quotations. Proportional penalty argument softened from "any of the main theories of justice" to "defenders within several major theories." Closing claim about Albertan opinion ("Most Albertans across the political spectrum would endorse them in principle") softened to "the empirical question this package opens rather than answers."

### moral-defence.md v1.0

Central claim: accountability is a condition of legitimate government. Engages objections from state-overreach, chilling-effects, corruption-vs-patronage, criminalization, proportionality, institutional humility, partisan neutrality, good-faith defense, and Indigenous sovereignty perspectives.

### red-team.md v1.1

Sources and confidence section added. SNC-Lavalin "nine witnesses" detail clarified — nine of twenty witnesses had constrained testimony due to Cabinet confidence; Privy Council Clerk Ian Shugart denied Dion's waiver request. §13 amendment effect on future SNC-Lavalin-style cases softened — narrows the available shield without eliminating it. Comparative claim that the regime is "meaningfully better than" other Canadian regimes softened to "addresses several gaps that have undermined comparable Canadian regimes" with explicit acknowledgement that whether it improves outcomes is empirical and uncertain.

### red-team.md v1.0

Adversarial analysis of failure modes drawn from documented Canadian and international experience. Empirical baseline covers SNC-Lavalin, Aga Khan, McIver, Smith-Pawlowski, Hinshaw, Trudeau-Trudeau-2, Trussler-Redford, federal Lobbying Act review failures, PSDPA whistleblower regime collapse, and Public Sector Integrity Commissioner resource starvation. Twelve failure mode categories analyzed against proposed regime provisions with residual risk named. Four motivated-actor scenarios traced through regime defenses. Top ten residual risks ranked by severity with hardening recommendations.

### policy-recommendations.md v1.0

Recommended starting values for regulatory parameters deferred to regulation under §28. Covers thresholds, percentages, sample sizes, materiality cutoffs, phased introduction multipliers, and enforcement equity scope. Identifies implementation priorities for year 1 and year 2 regulation-making, plus items requiring further policy development before regulations are drafted.
