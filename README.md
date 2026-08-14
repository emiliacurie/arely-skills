# arely-skills

Claude Code skills I built for my own design work, shared openly. Free to use, MIT licensed.

## Skills

| Skill | What it does |
| --- | --- |
| [`design-critique`](skills/design-critique) | Runs a four-designer critique panel on a UI's visual craft |

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

Visual craft only. For usability testing or a heuristic audit, use a different skill.

## Install

Clone the repo and copy the skill into your Claude Code skills folder:

```bash
git clone https://github.com/emiliacurie/arely-skills.git
cp -R arely-skills/skills/design-critique ~/.claude/skills/
```

That makes it available in every project. To scope it to one project instead, copy it into that
project's `.claude/skills/` folder.

Restart Claude Code, then run `/design-critique`.

### Requirements

Nothing extra for critiquing pasted images or Figma frames.

For URL capture and image downscaling, the skill uses `scripts/capture.py`, which needs:

```bash
pip install playwright pillow
playwright install chromium
```

Figma support uses whichever Figma MCP server you already have connected.

## License

MIT. Use it, change it, ship it.
