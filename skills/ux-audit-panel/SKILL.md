---
name: ux-audit-panel
description: Run a heuristic UX audit with a panel of independent evaluator subagents and fill out a heuristic audit spreadsheet. Each evaluator scores the same 49 statements from a different designer perspective without seeing the others' work, then their scores are averaged into the template and their disagreements written up as a divergence report. Use when the user asks for a UX audit, a heuristic audit, an audit spreadsheet, a multi-perspective design review, or says "audit this site/app/flow".
---

# UX audit panel

Fills the audit template using several evaluators that never see each other's
work. The averages go in the spreadsheet. The disagreements are the other half of
the deliverable.

**Runs entirely on Claude Code subagents under the user's subscription.** Never call
the Anthropic API, never use an API key, never install or invoke an SDK.

## Step 1 — Ask

Ask these one at a time, not as a block. Skip any the user already answered.

1. What to audit: one URL, several URLs that form a flow, or a folder of screenshots.
2. How many evaluators. Default 3, maximum 5, minimum 2.
3. Where to save the output.
4. Project details for the "About the project" sheet: app name, flow being audited,
   goal of the audit, link, any notes.

Then pick perspectives from `reference/perspectives.md`. Defaults are A1, A2, A3 for
three evaluators. Never assign the same perspective twice. Tell the user which
perspectives are in the room and let them swap any before you start.

Create the run folder, and copy this skill's two reference files into it so the run is
self-contained and the evaluator prompts carry no machine-specific paths:

```
<chosen folder>/<app-slug>-audit-<month>-<year>/
  evidence/  raw/  reference/
```

```bash
mkdir -p <run>/evidence <run>/raw <run>/reference
cp <skill>/reference/statements.md <skill>/reference/rubric.md <run>/reference/
```

`<skill>` is this skill's own directory. `<run>` is the folder you just created. Use absolute
paths for both. Every command below is written relative to `<skill>`.

## Step 2 — Capture

For URLs:

```bash
scripts/capture.sh <run>/evidence <url> [<url> ...]
```

This captures desktop fold, desktop full page, mobile fold, mobile full page, the
accessibility snapshot, and console output for each screen, in an isolated browser
session. If the user gave a screenshots folder, copy its contents into
`<run>/evidence` instead and skip this step.

Write `<run>/project.json` with the project details from step 1, using the keys
`app_name`, `flow`, `goal`, `link`, `notes`.

## Step 3 — Evaluate

Launch every evaluator in a **single message** so they run in parallel, using the
Agent tool with `subagent_type: "general-purpose"`.

Each evaluator gets this prompt, with its own perspective and output path:

> You are conducting a heuristic UX audit as a single evaluator.
>
> Your perspective: **[full text of the chosen perspective from perspectives.md]**
>
> Read `<run>/reference/statements.md` for the 49 statements and
> `<run>/reference/rubric.md` for how to score and what to output.
>
> The evidence is in `<run>/evidence/`. Read every screenshot with the Read tool and
> every snapshot and console file. `urls.tsv` maps screen numbers to URLs.
>
> You are the only evaluator on this audit. Do not read, list, or look for any other
> file in `<run>/raw/`. Do not look for other agents' output anywhere. Your judgement
> must come only from the evidence and your own perspective.
>
> Score all 49 statements and write your JSON to `<run>/raw/evaluator-N.json`.
> Write nothing else to disk.

Isolation rules you must hold to:

- Never tell an evaluator how many others there are, who they are, or what they found.
- Never pass one evaluator's output into another's prompt.
- Never run them sequentially with the earlier results in context.
- If an evaluator fails, relaunch it with the same prompt. Do not patch its scores
  yourself and do not let another evaluator cover for it.

## Step 4 — Merge and write

```bash
python3 scripts/merge.py <run>/raw <run> <run>/project.json
python3 scripts/write_audit.py <run>/results.json <run>/<app-slug>-audit-<month>-<year>.xlsx
```

`merge.py` builds `results.json`, keeps every evaluator's note in its own voice in the
Notes column, and writes `divergence-report.md` listing every statement where the
evaluators split by 2 points or more, worst spread first.

Then add a short synthesis at the top of `divergence-report.md`, under a
`## What this means` heading, in at most 15 lines: the sharpest disagreements and why
they happened, and the issues that multiple evaluators independently flagged. Agreement
is what to fix. Disagreement is what to take to real users.

## Step 5 — Report back

Tell the user the global score, the three weakest sheets, how many of the 49 statements
the panel split on, and the paths to both files. Do not paste the whole report.

## How the spreadsheet is filled

Evaluators 1 and 2 go in columns C and D. Evaluators 3, 4 and 5 go in J, K and L, to
the right of Notes, so nothing marked "don't move" moves. Only the E column formula
changes, widening to average across however many evaluators ran. Columns F, G, H and
the Summary sheet are never touched.

A statement scored `"N/A"` by every evaluator has its E, G and H cells cleared so the
row drops out of the sheet grade instead of poisoning it. This is correct and intended.

## Constraints

- Never edit `assets/template.xlsx`. It is the source template.
- Never write scores yourself. Every number in the spreadsheet comes from an evaluator.
- If fewer than 2 evaluator files exist, stop and say so. Do not produce a partial audit.
