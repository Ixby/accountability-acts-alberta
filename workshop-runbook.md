# Workshop Runbook — Iterative Manuscript Refinement

*Reproducible process for putting a long-form manuscript through a multi-expert workshop and applying the consensus findings as concrete revisions. Designed for the Alberta accountability bills brief but generalizable to any long-form policy or nonfiction work.*

---

## Goals (the success metric)

A reader who finishes the manuscript should want to:

1. **Share it** — forward a passage, screenshot a sentence, post a quote.
2. **Advocate for it** — speak publicly and specifically about the substance.
3. **Insist their MLA read it** — actually contact their representative, not just intend to.

Subordinate goals, in service of the above: elegance, beat, rhythm, accuracy, ear, mouth. Every line earns its space; every transition bridges; every paragraph sounds right read aloud. **Above all: zero hallucinations.** No factual claim should appear that has not been verified.

---

## The Eleven-Expert Panel

Each expert reads only the narrative portion (Parts I through VII; everything before "# Appendix A"). Each is given a focused brief asking for line-level findings rather than essay-style critique. Findings are returned in a `LOCATION / QUOTE / DIAGNOSIS / FIX` block format.

**The panel:**

1. **Poet** — read-aloud quality, vowel and consonant work, beat, breath, the line that should be there.
2. **Author** (working Canadian nonfiction author) — voice, persona, narrative drive, three sentences worth envying / three to cut.
3. **Educator** (senior university teacher in political science or public policy) — pedagogical scaffolding, glossary check, stairs vs. cliffs, hardest concepts.
4. **Lawyer** (Canadian admin/constitutional practitioner) — doctrinal accuracy, statutes, cases, charter exposure.
5. **Editor** (senior nonfiction structural editor) — architecture, pacing, length per section, hard cuts and adds.
6. **Document designer** — information architecture, navigation, hierarchy, signposting.
7. **Graphic designer** — visual register, palette, contrast, hierarchy at glance-distance, cover and residue.
8. **Book designer** (Bringhurst tradition) — typeface, leading, measure, margin, what kind of book this is.
9. **Layout artist** — page-level breaks, orphans/widows, composition, the cost table.
10. **Copy editor** — line-level precision, repetition, register shifts, tics, opening and closing sentences of each Part.
11. **Fact-checker** — every empirical claim verified against contemporary reporting and primary sources; every uncertain claim flagged.

**Add or substitute when relevant:**

- **Advocacy strategist** — shareability test, "send to your MLA" sentence, advocacy gap analysis. *Required if the success metric includes advocacy behaviour.*
- **Average reader** (a non-specialist standing in for the intended public audience — for the Alberta brief this was a Red Deer high school social studies teacher) — what they actually read, where they stalled, what they would forward.
- **Constitutional scholar** — for documents implicating Charter, parliamentary privilege, or division of powers, an academic-register pass distinct from a practitioner's.
- **Indigenous governance advisor** — required when the manuscript touches Indigenous law or rights. *Should not be a substitute for actual Indigenous co-authorship.*

---

## The Process

The full cycle is **read → critique → debate → synthesize → apply → commit → iterate**.

### Phase 1 — Parallel critiques

All eleven experts spawned in a single message as parallel sub-agents. Each receives a focused brief specifying:

- The file path of the manuscript.
- The exact section to read (narrative only, not appendices).
- The expert's specific lens.
- A list of patterns or claims to look for (not a list of conclusions to reach).
- The required output format (`LOCATION / QUOTE / DIAGNOSIS / FIX` blocks).
- Word count target (1,500–2,500 words for most; up to 3,000 for fact-checker).
- Explicit instruction to return findings only — no preamble, no closing summary.

Critical brief discipline:

- **Tell them what's been said before.** Each subsequent iteration should brief the experts on the prior round's findings so they don't surface the same issues; they should look for what's still wrong after the last pass.
- **Flag the zero-hallucinations rule.** Especially for fact-checker, lawyer, and constitutional scholar.
- **Use specific quotes.** Vague critique is worth nothing; specific quotes drive specific edits.

### Phase 2 — Synthesis

Read all eleven critiques. Identify:

- **Convergence** — points where three or more experts independently identify the same issue. These are non-negotiable.
- **Tension** — points where experts disagree (e.g., book designer wants no display type; graphic designer wants one display moment). These need adjudication via paired debate.
- **Singletons** — points raised by one expert that other experts didn't notice. Treat as nice-to-have unless the expert's domain authority is determinative for the issue (fact-checker on facts, lawyer on law).

### Phase 3 — Final-round paired debates

Three to four paired or three-way debates, each adjudicating a specific tension or producing a joint deliverable:

1. **Lawyer × Fact-checker** → joint must-fix accuracy list.
2. **Author × Editor** → readiness verdict + ten-day list.
3. **Book designer × Document designer × Graphic designer** → joint design brief.
4. **Poet × Educator × Copy editor** → joint language work list.

Each debate spawned as a single moderating agent, given:

- Both/all experts' prior findings in summary.
- The specific points to adjudicate (with the experts' positions stated).
- A required output of speaker-tagged transcript plus a joint statement.

The poet must be in at least one debate per iteration. The fact-checker's findings carry veto authority on accuracy; everything else is editorial judgment.

### Phase 4 — Master synthesis

A single document recording:

- What the workshop confirmed.
- The MUST-FIX list (accuracy non-negotiables — every item independently verified).
- The SHOULD-FIX list (structural and language items — every item with at least two-expert convergence).
- The DESIGN priority list (in priority order).
- What was not resolved (flagged for external review).
- The final verdict.

### Phase 5 — Application

The manuscript is rewritten/edited against the master synthesis. **Discipline: zero new factual claims.** Only:

- Cuts (any sentence the workshop flagged as not earning its space).
- Restructures (reordering, signposting, scaffolding).
- Corrections (replacing inaccurate claims with verified ones, citing the verifying source in the commit).
- Insertions that don't add facts (metaphors, transitions, named patterns).

Each accuracy correction must trace to a specific verified source from the fact-checker's report. If the fact-checker flagged a claim as uncertain rather than verified, **soften or remove it; do not assert a different version.**

### Phase 6 — Build and commit

- Reassemble the full document (narrative + appendices).
- Rebuild any rendered formats (HTML, PDF) using the existing build script.
- Commit with a message that lists the major changes and cites the workshop iteration.
- Push.

### Phase 7 — Iterate

Iterations decrease in scope, not depth. The first iteration finds the largest issues; the second tightens what survived; the third polishes the result. Three iterations is usually enough.

For each iteration after the first, the brief to each expert should explicitly cite the prior iteration's findings and ask: *given that pass has been done, what remains?* Without this brief discipline, experts will re-surface issues already addressed and the iteration produces no marginal value.

---

## File and tool layout

For the Alberta accountability brief, the canonical files are at `C:\Users\email\Documents\Claude\Projects\accountability-acts-alberta\`:

- `policy-brief.md` — the assembled manuscript (narrative + 7 appendices).
- `policy-brief.html` — rendered single-page HTML (built from policy-brief.md).
- `build-policy-brief-html.py` — converter, run via `python build-policy-brief-html.py`.
- `narrative-v5.md` — the canonical narrative (Parts I–VII, the case for the bills); reassembled into `policy-brief.md` by concatenating with the appendices. Earlier iteration drafts are preserved in `drafts/` (e.g., `drafts/narrative-v2.md`, `drafts/narrative-v3.md`, `drafts/narrative-v4.md`); the working file at root is whichever vN reflects the latest iteration.
- `bill-1-government-accountability-act.md`, `bill-2-open-books-act.md` — primary statutory text (Appendices A and B).
- `costing.md`, `moral-defence.md`, `red-team.md`, `legislative-cross-reference.md`, `policy-recommendations.md` — companion documents (Appendices C through G).
- `workshop-final-round.md`, `workshop-iteration-N.md` — workshop records per iteration.
- `workshop-runbook.md` — this document.

The rebuild command, run after the narrative is updated:

```bash
{
  cat /c/Users/email/Documents/Claude/Projects/accountability-acts-alberta/narrative-vN.md
  echo ""; echo "---"; echo ""
  echo "# Appendix A — Bill 1: The Government Accountability Act"
  echo ""; echo "*Full drafted text. Released under CC-BY-SA 4.0.*"
  echo ""; echo "---"; echo ""
  cat /c/Users/email/Documents/Claude/Projects/accountability-acts-alberta/bill-1-government-accountability-act.md
  # ... and so on for B through G
} > /c/Users/email/Documents/Claude/Projects/accountability-acts-alberta/policy-brief.md
cd /c/Users/email/Documents/Claude/Projects/accountability-acts-alberta && python build-policy-brief-html.py
```

---

## Discipline principles

1. **Zero hallucinations.** Every factual claim must trace to a verified source. If the fact-checker flagged uncertainty, the claim must soften (or be removed), not be asserted in a different form.

2. **Convergence wins; singletons get evaluated.** When three or more experts independently identify the same issue, fix it. When one expert raises something the others missed, evaluate based on their domain authority.

3. **Cuts before insertions.** Each iteration should remove more than it adds, until the document reaches the leanest version that still does its job.

4. **No claudisms.** AI-typical patterns — em-dashes as glue, three-part rhythms used reflexively, "Not A. B." inversions, reader-instruction, sentence-final codas, performative scaffolding — must be edited out at the line level. The copy editor's pass surfaces these; the application step cuts them.

5. **Every line earns its space.** The model paragraph (the CEC paragraph in Part I, in the Alberta brief) is the test. Each sentence does work the surrounding sentences do not.

6. **Bridge, don't restart.** Section transitions and paragraph transitions should carry the reader. The structural editor's pass identifies failed bridges; application replaces stalls with transitions.

7. **Read aloud.** The poet's pass tests for ear and mouth. If a passage doesn't sound right read aloud, it isn't right.

8. **The reader's test is the final test.** Would a non-specialist reader of the intended audience finish this and want to share it / advocate for it / contact their MLA? If not, the iteration is incomplete.

---

## What this runbook is not

It is not a guarantee. Eleven experts converge on the bigger issues; smaller things slip through every pass. Three iterations get most of what's gettable. Four or five does not produce four or five times the result.

It is not a substitute for the things the workshop cannot do: legal opinion, Indigenous co-development, fiscal validation, legislative drafter review. Those are external requirements. The workshop is the in-house preparation; the externals are the gating items before tabling.

It is not a guarantee of voice. The workshop sharpens what is already there; it does not generate authorial voice that is missing. A manuscript without voice cannot be edited into having one.

It is, however, a process that takes the manuscript from "competent draft" to "ready to release publicly," reproducibly, with a paper trail. That is its scope.
