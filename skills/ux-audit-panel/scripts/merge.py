#!/usr/bin/env python3
"""Merge independent evaluator JSON files into results.json + divergence.md.

usage: merge.py <raw_dir> <out_dir> <project.json>
"""
import json
import sys
from pathlib import Path

SHEETS = {
    "1. Consistency": (4, 9), "2. Aesthetic": (4, 10), "3.Recover": (4, 8),
    "4. Recognition": (4, 7), "5. Accessibility": (4, 9), "6. Attention": (4, 9),
    "7. Status": (4, 8), "8. Real world": (4, 7), "9. Important": (4, 9),
}
SPLIT = 2


def short(label):
    """Evaluators sometimes echo their whole brief. Keep the first clause."""
    label = label.split(". ")[0]
    return label.strip().rstrip(".")[:45]


def load(raw_dir):
    files = sorted(Path(raw_dir).glob("evaluator-*.json"))
    if len(files) < 2:
        raise SystemExit(f"need at least 2 evaluator files, found {len(files)}")
    return [json.loads(f.read_text()) for f in files]


def statements(template):
    import openpyxl
    wb = openpyxl.load_workbook(template)
    return {t: {r: wb[t].cell(r, 2).value for r in range(a, b + 1)}
            for t, (a, b) in SHEETS.items()}


def main():
    raw_dir, out_dir, project_file = sys.argv[1:4]
    out = Path(out_dir)
    evals = load(raw_dir)
    names = [short(e["perspective"]) for e in evals]
    text = statements(Path(__file__).resolve().parent.parent / "assets" / "template.xlsx")

    scores, divergences = {}, []
    for sheet, (first, last) in SHEETS.items():
        scores[sheet] = {}
        for row in range(first, last + 1):
            cells = []
            for e in evals:
                entry = e["scores"].get(sheet, {}).get(str(row))
                if entry is None:
                    raise SystemExit(f"{names[evals.index(e)]}: missing {sheet} row {row}")
                cells.append(entry)
            vals = [c["score"] for c in cells]
            notes = "\n".join(f"{n} ({c['score']}): {c.get('note', '').strip()}"
                              for n, c in zip(names, cells))
            scores[sheet][str(row)] = {"scores": vals, "note": notes}
            nums = [v for v in vals if isinstance(v, (int, float))]
            if len(nums) >= 2 and max(nums) - min(nums) >= SPLIT:
                divergences.append({
                    "sheet": sheet, "row": row, "statement": text[sheet][row],
                    "spread": max(nums) - min(nums),
                    "detail": [(n, c["score"], c.get("note", "")) for n, c in zip(names, cells)],
                })

    project = json.loads(Path(project_file).read_text())
    (out / "results.json").write_text(json.dumps(
        {"project": project, "evaluators": names, "scores": scores}, indent=1))

    divergences.sort(key=lambda d: -d["spread"])
    lines = [f"# Divergence report — {project.get('app_name', 'audit')}", "",
             f"{len(names)} independent evaluators scored 49 statements without seeing "
             f"each other's work: {', '.join(names)}.", "",
             f"They split by {SPLIT} points or more on **{len(divergences)} of 49** statements.",
             "", "## Where they disagreed", ""]
    for d in divergences:
        lines.append(f"### {d['sheet']} row {d['row']} (spread {d['spread']})")
        lines.append(f"> {d['statement']}")
        lines.append("")
        for name, score, note in d["detail"]:
            lines.append(f"- **{name} — {score}**: {note}")
        lines.append("")
    if not divergences:
        lines += ["The evaluators agreed within 1 point on every statement.", ""]

    lines += ["## Top issues, by evaluator", ""]
    for e in evals:
        lines.append(f"### {e['perspective']}")
        for i in e.get("top_issues", []):
            lines.append(f"- **{i.get('title')}** ({i.get('severity', 'n/a')}) — "
                         f"{i.get('where')}. {i.get('why')}")
        lines.append("")
    (out / "divergence-report.md").write_text("\n".join(lines))
    print(f"{len(divergences)} divergences; wrote results.json and divergence-report.md")


if __name__ == "__main__":
    main()
