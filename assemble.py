"""Assemble policy-brief.md from narrative-v5.md + Appendices A and B (the bills only).

Earlier versions of this brief carried five additional companion appendices
(C–G): cost analysis, philosophical defence, adversarial failure-mode
analysis, legislative cross-reference, policy recommendations. Those
documents are now folded into the main narrative; only the bill texts
remain as appendices in the published brief.

Run: python assemble.py  (then build-policy-brief-html.py + build-pdf.js)
"""

from pathlib import Path

ROOT = Path(__file__).parent
NARRATIVE = ROOT / "narrative-v5.md"
BILL_1 = ROOT / "bill-1-honest-government-act.md"
BILL_2 = ROOT / "bill-2-open-books-act.md"
TARGET = ROOT / "policy-brief.md"

LICENSE_TAG = "Released under CC-BY-SA 4.0."


def strip_first_h1(text: str) -> str:
    """Drop the first '# ' line of a source file so we can prepend our own appendix heading."""
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        return "\n".join(lines[1:]).lstrip()
    return text


def section(heading: str, blurb: str, body: str) -> str:
    return (
        "\n\n---\n\n"
        f"# {heading}\n\n"
        f"*{blurb}*\n\n"
        "---\n\n"
        f"{body}\n"
    )


def main():
    narrative = NARRATIVE.read_text(encoding="utf-8")
    bill_1 = strip_first_h1(BILL_1.read_text(encoding="utf-8"))
    bill_2 = strip_first_h1(BILL_2.read_text(encoding="utf-8"))

    out = (
        narrative.rstrip()
        + section(
            "Appendix A — Bill 1: The Honest Government Act",
            f"Full drafted text. {LICENSE_TAG}",
            bill_1,
        )
        + section(
            "Appendix B — Bill 2: The Open Books Act",
            f"Full drafted text. {LICENSE_TAG}",
            bill_2,
        )
    )
    TARGET.write_text(out, encoding="utf-8")
    word_count = len(out.split())
    print(f"Wrote {TARGET} ({word_count:,} words)")


if __name__ == "__main__":
    main()
