import pathlib
from bs4 import BeautifulSoup
import re
import markdown
import yaml

from .metadata import extract_metadata, trim_metadata
from .latex_render import latex_to_svg


DEFAULT_METADATA = {
    "title": "Lorem Ipsum",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
}


_ARITH_INLINE = re.compile(
    r'<span class="arithmatex">\\\((.*?)\\\)</span>',
    re.DOTALL
)

_ARITH_BLOCK = re.compile(
    r'<div class="arithmatex">\\\[(.*?)\\\]</div>',
    re.DOTALL
)


def _render_math(html: str, path: pathlib.Path) -> str:
    """
    Parse HTML with BeautifulSoup and replace math blocks with SVG.
    Supports both inline and display math.
    """

    soup = BeautifulSoup(html, "html.parser")

    # Find all math containers
    for math_div in soup.find_all(class_="arithmatex"):
        # Look for the <script type="math/tex"> inside
        script = math_div.find("script", type=lambda t: t and t.startswith("math/tex"))
        if script and script.string:
            latex = script.string.strip()
            svg_file = latex_to_svg(latex, path)
            svg = f"<img src='{svg_file}' alt='LaTeX render'/>"
            # Replace the entire math_div with SVG
            math_div.replace_with(BeautifulSoup(svg, "html.parser"))

    return str(soup)

def md_to_html(source: str, templates: dict[str, str], tex_path: str, build_url=None) -> str:
    raw_metadata = extract_metadata(source)
    metadata = yaml.safe_load(raw_metadata)

    stripped = trim_metadata(source)

    # InlineHilite handles math directly
    extension_configs: dict = {
        "pymdownx.quotes": {"callouts": True},
        "pymdownx.arithmatex": {
            "preview": False,
        }
    }

    if build_url is not None:
        extension_configs["mdx_wikilink_plus"] = {
            "build_url": build_url,
            "end_url": ".html",
        }

    content = markdown.markdown(
        stripped,
        extensions=[
            "extra",
            "toc",
            "mdx_wikilink_plus",
            "pymdownx.arithmatex",
            "pymdownx.tilde",
            "pymdownx.saneheaders",
            "pymdownx.magiclink",
            "pymdownx.fancylists",
            "pymdownx.betterem",
            "pymdownx.quotes",
            "pymdownx.escapeall",
            "pymdownx.highlight",
            "pymdownx.inlinehilite",
            "pymdownx.emoji",
            "pymdownx.progressbar",
            "pymdownx.smartsymbols",
        ],
        extension_configs=extension_configs,
    )

    content = _render_math(content, pathlib.Path(tex_path))

    if not metadata:
        metadata = DEFAULT_METADATA
    if "title" not in metadata:
        metadata["title"] = DEFAULT_METADATA["title"]
    if "description" not in metadata:
        metadata["description"] = DEFAULT_METADATA["description"]

    template = templates.get(
        "DEFAULT",
        "Something is really messed up. The default template couldn't be loaded either."
    )

    template_name = metadata.get("template")
    if template_name in templates:
        template = templates[template_name]

    return template.format(
        content=content,
        raw_metadata=raw_metadata.strip("\n"),
        **metadata
    )
