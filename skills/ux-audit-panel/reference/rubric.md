# Scoring rubric

Every statement gets a whole number 0–4, or `"N/A"`.

| Score | Meaning |
|---|---|
| 4 | Fully met. You looked for exceptions and found none. |
| 3 | Met, with one minor exception you can name. |
| 2 | Partially met. Inconsistent across screens or states. |
| 1 | Mostly not met. Isolated good cases at best. |
| 0 | Not met, or actively working against the user. |
| `"N/A"` | Cannot be judged from the evidence you were given. |

## Rules

**Any score of 2 or below needs a note that names the screen and the element.**
"Contrast is poor" is not a finding. "The grey placeholder text in the email field
on signup-desktop-fold.png is too light against white" is a finding.

**Use `"N/A"` honestly.** Some statements cannot be answered from screenshots and
page text. The clearest case is `8. Real world` row 7, about whether user research
was conducted, which no screenshot can show. Marking N/A is correct and the row
drops out of the score. Guessing a 2 to avoid an empty cell corrupts the average.

**Do not cluster on 3.** If the evidence supports a 0 or a 4, give a 0 or a 4.
A run where every score is 2 or 3 tells the reader nothing.

**Score what you can see.** If a statement covers behaviour you have no evidence
of (an error state nobody captured, an undo action you cannot trigger), that is
`"N/A"`, not a low score. Absence of evidence is not evidence of failure.

## Output format

Write one JSON file to the path you were given. Nothing else. No markdown fences.

```json
{
  "perspective": "short code and name only, e.g. A1 Accessibility-first",
  "scores": {
    "1. Consistency": {
      "4": {"score": 3, "note": "Specific, cites a screen and an element."},
      "5": {"score": 0, "note": "..."}
    }
  },
  "top_issues": [
    {"title": "Short name", "where": "screen and element", "why": "impact on the user", "severity": "high|medium|low"}
  ]
}
```

Sheet names and row numbers must match `statements.md` exactly, including the
missing space in `3.Recover`. Every one of the 49 rows must be present.
`top_issues` holds the 3–6 problems you consider most worth fixing.
Keep `perspective` to the code and name. Do not paste your whole brief into it;
it becomes a column header in a spreadsheet.
