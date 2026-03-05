import markdown
import yaml
from .metadata import extract_metadata, trim_metadata

DEFAULT_METADATA = {
    "title": "Lorem Ipsum",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
}

def md_to_html(source: str, templates: dict[str, str], build_url=None) -> str:
    raw_metadata = extract_metadata(source)
    metadata = yaml.safe_load(raw_metadata)

    stripped = trim_metadata(source)

    extension_configs: dict = {  # TODO configurable extensions
        "pymdownx.quotes": {
            "callouts": True
        }
    }
    if build_url is not None:
        extension_configs["mdx_wikilink_plus"] = {
            "build_url": build_url,
            "end_url": ".html",
        }

    content =  markdown.markdown(
        stripped,
        extensions=[  # TODO configurable extensions
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
            "pymdownx.smartsymbols"
        ],
        extension_configs=extension_configs,
    )

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

