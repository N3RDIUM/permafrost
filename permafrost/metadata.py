import re

_FRONTMATTER_RE = re.compile(
    r"\A---\s*\n(?P<frontmatter>.*?\n)---\s*(?:\n|$)",
    re.DOTALL,
)

def extract_metadata(md: str) -> str:
    match = _FRONTMATTER_RE.match(md)
    if match is None:
        return ""

    return match.group("frontmatter")

def trim_metadata(md: str) -> str:
    match = _FRONTMATTER_RE.match(md)
    if match is None:
        return md

    return md[match.end():]
