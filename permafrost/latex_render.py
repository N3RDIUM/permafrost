import subprocess
import tempfile
import hashlib
from pathlib import Path

COLOR = "ebdbb2"


def latex_to_svg(latex: str, out_dir: Path) -> str:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # hash of latex string
    h = hashlib.sha256(latex.encode("utf-8")).hexdigest()
    out_file = out_dir / f"{h}.svg"

    # return early if cached
    if out_file.exists():
        return out_file.name

    tex_template = rf"""
\documentclass[16pt]{{article}}
\pagestyle{{empty}}
\usepackage{{amsmath}}
\usepackage{{xcolor}}
\color[HTML]{{{COLOR}}}
\begin{{document}}
{{\LARGE ${latex}$}}
\end{{document}}
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        tex_file = tmp / "eq.tex"
        tex_file.write_text(tex_template)

        subprocess.run(
            ["latex", "-interaction=nonstopmode", "eq.tex"],
            cwd=tmp,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )

        subprocess.run(
            ["dvisvgm", "eq.dvi", "-n", "-o", "eq.svg"],
            cwd=tmp,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )

        svg = (tmp / "eq.svg").read_text(encoding="utf-8")
        out_file.write_text(svg, encoding="utf-8")

    return out_file.name

