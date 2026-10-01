"""Check deck-content.yaml against the language rules (brief sections 5 and 14).

Usage: python3 scripts/lint_content.py [work/deck-content.yaml]
Exit code 1 if any hard rule fails. Placeholders are reported, not failed.
"""
import re
import sys
from pathlib import Path

import yaml

BANNED = [
    "leverage", "synergy", "holistic", "360", "seamless", "robust", "cutting-edge",
    "elevate", "unlock", "empower", "journey", "ecosystem", "game-changer",
    "next-level", "best-in-class", "world-class", "solutions", "digital transformation",
    "passionate", "innovative", "ai-powered",
    # final-check strings (section 14)
    "monarch", "10%", "20%", "conversion", "roi", "leads", "rebrand", "overhaul",
    "campaign", "yaric", "geric",
    # word-choice table (section 5)
    "digital presence", "gmb", "seo", "traffic", "stakeholder", "audience",
]
TABLE_TYPES = {"table", "pricing"}
MAX_BODY_WORDS = 40


def strings(node, path=""):
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from strings(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from strings(v, f"{path}[{i}]")


def visible(text):
    """Text as printed: placeholders and template refs removed."""
    text = re.sub(r"\[\[[^\]]*\]\]", "", text)
    return re.sub(r"\{[a-z_.0-9]+\}", "", text)


def main(path):
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    errors, placeholders = [], []
    for p, s in strings(data):
        placeholders += [(p, m) for m in re.findall(r"\[\[[^\]]*\]\]", s)]
        v = visible(s)
        low = v.lower()
        for w in BANNED:
            if re.search(rf"(?<![a-z0-9]){re.escape(w)}(?![a-z0-9])", low):
                errors.append(f"{p}: banned '{w}': {s}")
        if "—" in v:
            errors.append(f"{p}: em dash: {s}")
        if "!" in v:
            errors.append(f"{p}: exclamation mark: {s}")

    print("slide | words | title")
    for sl in data["slides"]:
        body = {k: v for k, v in sl.items() if k not in ("n", "type", "title", "image", "source", "kicker")}
        if sl["type"] in TABLE_TYPES:
            # table furniture and the fine-print notes under the pricing table
            body = {k: v for k, v in body.items() if k not in ("rows", "columns", "notes")}
        if sl["type"] in ("sitemaps", "wireframe", "columns5", "plan", "checklist", "twocol", "closing"):
            # structured layouts: count only free prose
            body = {k: v for k, v in body.items() if k in ("body", "note", "closing", "lead")}
        words = sum(len(visible(s).split()) for _, s in strings(body))
        title_words = len(sl["title"].split())
        flag = " <-- over 40" if words > MAX_BODY_WORDS else ""
        print(f"{sl['n']:>5} | {words:>5} | ({title_words}w) {sl['title']}{flag}")
        if words > MAX_BODY_WORDS:
            errors.append(f"slide {sl['n']}: {words} body words")

    print(f"\nPlaceholders: {len(placeholders)}")
    for p, m in placeholders:
        print(f"  {p}: {m}")
    print(f"\nErrors: {len(errors)}")
    for e in errors:
        print("  " + e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "work/deck-content.yaml"))
