# arely-skills

Claude Code skills I built for my own design work, shared openly. Free to use, MIT licensed.

## Skills

| Skill | What it does |
| --- | --- |
| [`design-critique`](skills/design-critique) | Runs a four-designer critique panel on a UI's visual craft |
| [`ux-audit-panel`](skills/ux-audit-panel) | Runs a heuristic UX audit with independent evaluators and fills out the audit spreadsheet |

More will land here over time.

## design-critique

A real design crit, run by four designers instead of one generic reviewer.

You hand it a design and it casts four relevant designer voices (the lenses are picked per run
based on what you showed it), critiques through each one, then synthesizes where the panel agrees,
where it disagrees, and what to fix first.

**It accepts:**

- a localhost or live URL
- screenshot file paths
- a Figma file or frames
- multi-screen flows in any of the above

**It gives you:**

- what's working and 3 to 4 findings per designer, each tagged Blocker / Major / Minor / Polish
- points raised by two or more designers, flagged as high-confidence priorities
- genuine disagreements surfaced as decisions for you rather than resolved silently
- top 3 next steps

It covers layout, hierarchy, typography, color, spacing, consistency, iconography, microcopy,
states, cross-screen flow, accessibility, and design-system adherence when you point it at a system.

Everything runs in one pass with no subagents, and screenshots are resolution-capped, so a typical
crit stays cheap.

### Usage

```
/design-critique http://localhost:3000
/design-critique ./screens/checkout-1.png ./screens/checkout-2.png
/design-critique http://localhost:3000/pricing --focus "typography and hierarchy"
```

It also triggers on plain language: "critique this", "review this design", "how's the design".

Before critiquing it asks up to three quick questions (goal and audience and stage, which design
system to check against, anything to focus on or leave alone). Answer them in your first message
and it skips straight to the crit.

### What this is not

Visual craft only. For a scored heuristic audit, use [`ux-audit-panel`](skills/ux-audit-panel).

## ux-audit-panel

A heuristic audit run by several evaluators who never see each other's work.

Point it at a site and it captures the evidence once, then launches one subagent per evaluator.
Each scores the same 49 statements from a different designer perspective, blind to the others.
Their scores are averaged into a spreadsheet, and the places where they disagreed become a
separate report.

The disagreements are the point. A single reviewer gives you one reading of a screen and you
never learn that another reading existed. Running Linear through it, the accessibility lens and
the visual craft lens both scored the homepage a 4 while the first-time-user lens scored it a 1,
on eight separate statements. All three were right about the same page.

**It accepts:**

- a localhost or live URL
- several URLs that make up a flow
- a folder of screenshots, for competitors or native apps

**It gives you:**

- the audit spreadsheet filled in, with a column per evaluator and every note in its own voice
- a global score and a score per heuristic category
- a divergence report listing every statement the panel split on, worst spread first
- the issues multiple evaluators flagged independently, which is the closest thing to confirmation
  this method offers

Agreement tells you what to fix. Disagreement tells you what to take to real users.

**The 49 statements** cover consistency, aesthetic and minimalism, error recovery, recognition
over recall, accessibility, attention, system status, matching the real world, and hierarchy.
Every evaluator answers all of them, so their scores stay comparable. The perspective changes
what each one notices, never what they are scoring.

Statements with no evidence behind them are marked N/A and dropped from the score rather than
guessed at. A whole category can drop out this way, and the skill tells you when it does.

### Usage

```
/ux-audit-panel https://example.com
/ux-audit-panel https://example.com https://example.com/pricing https://example.com/signup
```

It asks what to audit, how many evaluators (3 by default, 5 maximum), where to save, and the
project details that head the spreadsheet. Then it runs.

It also triggers on plain language: "audit this site", "heuristic audit", "run a UX audit".

### Requirements

```bash
npm install -g @playwright/cli
pip install openpyxl
```

Everything runs on Claude Code subagents under your own subscription. No API key, no SDK.

## Install

Clone the repo and copy the skill into your Claude Code skills folder:

```bash
git clone https://github.com/emiliacurie/arely-skills.git
cp -R arely-skills/skills/design-critique ~/.claude/skills/
cp -R arely-skills/skills/ux-audit-panel ~/.claude/skills/
```

That makes it available in every project. To scope it to one project instead, copy it into that
project's `.claude/skills/` folder.

Restart Claude Code, then run `/design-critique` or `/ux-audit-panel`.

### Requirements

#### design-critique

Nothing extra for critiquing pasted images or Figma frames.

For URL capture and image downscaling, the skill uses `scripts/capture.py`, which needs:

```bash
pip install playwright pillow
playwright install chromium
```

Figma support uses whichever Figma MCP server you already have connected.

#### ux-audit-panel

```bash
npm install -g @playwright/cli
pip install openpyxl
```

## License

MIT. Use it, change it, ship it.
