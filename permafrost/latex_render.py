import subprocess
import tempfile
from pathlib import Path

COLOR = "ebdbb2"

def latex_to_svg(latex: str) -> str:
    tex_template = rf"""
\documentclass[16pt]{{article}}
\pagestyle{{empty}}
\usepackage{{amsmath}}
\usepackage{{xcolor}}
\color[HTML]{{{COLOR}}} % set default text/math color
\begin{{document}}
{{\LARGE ${latex}$}}
\end{{document}}
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        tex_file = tmp / "eq.tex"
        _ = tex_file.write_text(tex_template)

        _ = subprocess.run(
            ["latex", "-interaction=nonstopmode", "eq.tex"],
            cwd=tmp,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )

        _ = subprocess.run(
            ["dvisvgm", "eq.dvi", "-n", "-o", "eq.svg"],
            cwd=tmp,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )

        svg = (tmp / "eq.svg").read_text(encoding="utf-8")

    return svg
