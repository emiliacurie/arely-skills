# Critique Checklist

Loaded only when a critique runs. Two parts:

- **Part A — Designer roster:** the candidate voices to cast the panel from (pick 4 per run).
- **Part B — Craft dimensions:** what each designer looks at, shared across the panel.

---

## Part A — Designer roster (cast 4 per run)

Pick the four most relevant to what was shown. Each has a lens and a tell — what they reliably
notice and push on.

- **Visual craft designer** — typography, color, spacing, hierarchy, polish. Notices weak type
  scale, muddy color, inconsistent spacing, weak focal point.
- **UX / interaction & flow designer** — the journey across screens, information architecture,
  transitions, friction, affordances. Notices dead ends, unclear next steps, inconsistent
  navigation, missing states.
- **Accessibility & inclusivity designer** — contrast, focus states, tap-target size, text size,
  state coverage. Notices low-contrast text, tiny touch targets, color-only signals, missing focus.
- **Brand / design-system guardian** — token and system adherence, consistency. Notices off-system
  colors/spacing/type, one-off components, drift from the named system.
- **Content / UX-writing designer** — labels, microcopy, tone, clarity. Notices vague buttons,
  jargon, inconsistent voice, unhelpful empty/error copy. Cast for text-heavy screens.
- **Conversion / product designer** — does the flow drive its goal: CTA hierarchy, friction,
  drop-off risk, value clarity. Cast for landing, marketing, signup, or checkout flows.
- **Motion / interaction-detail designer** — transitions, feedback, perceived performance,
  micro-interactions. Cast when motion or interactive states are central.
- **Data-density designer** — tables, dashboards, dense data UI: scan-ability, alignment,
  legibility under load. Cast for data-heavy or admin interfaces.

---

## Part B — Craft dimensions

What the panel evaluates against. Qualitative — no scores or rubrics. 2–4 "look for" prompts each.

### Layout & composition
- Is there a consistent grid? Are elements aligned to it?
- Is whitespace used to group and separate, or is the screen crowded or empty?
- Is there visual balance, or does weight pile up on one side?

### Visual hierarchy
- Where does the eye land first? Is that the most important thing?
- Are size, weight, and contrast used to order importance?
- Can the screen be scanned in a few seconds?

### Typography
- Is the type scale deliberate, with clear steps between levels?
- Are line length (~45–75 chars) and line height comfortable?
- Are font weights and styles used consistently, not ad hoc?

### Color
- Is the palette disciplined, or are there too many unrelated colors?
- Does body text meet WCAG contrast (4.5:1, or 3:1 for large text)?
- Is color used semantically (success, danger, action) and consistently?

### Spacing & rhythm
- Is spacing on a consistent scale (4/8px or the system's), or arbitrary?
- Is padding inside components even and predictable?
- Is vertical rhythm consistent between sections?

### Consistency
- Are repeated patterns (buttons, cards, inputs) actually identical?
- Are components reused, or reinvented per screen?
- Do the same actions look and sit in the same place across screens?

### Iconography & imagery
- Are icons one consistent style and weight?
- Do images earn their place, or are they decoration/filler?
- Is image quality and crop consistent?

### Content & microcopy
- Are labels and buttons clear about what they do?
- Is the tone consistent and appropriate for the audience?
- Do empty, error, and loading states have helpful copy?

### State & responsiveness (when applicable)
- Are empty, loading, error, and success states designed, not just the happy path?
- Does the layout hold up at the relevant breakpoints?

### Flow & cross-screen (when it's a flow)
- Is each step's next action clear? Any dead ends?
- Do patterns stay consistent across screens, or drift?
- Do transitions between steps make sense and keep momentum?

### Accessibility
- Sufficient contrast for text and meaningful UI?
- Visible focus states for keyboard users?
- Tap targets at least ~44px? Text large enough to read?

### Design-system adherence (only when a system is applied)
- Are colors, spacing, and type pulled from the system's tokens?
- Any off-system values that should map to an existing token?
- Are components the system's, or one-off recreations?
