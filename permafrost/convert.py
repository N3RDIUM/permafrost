import markdown
import yaml
from .metadata import extract_metadata, trim_metadata

DEFAULT_TEMPLATE = """<!--meta start
{raw_metadata}
meta end-->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <script
        async
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"
    ></script>
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['\\$','\\$']],
                displayMath: [['\\$$','\\$$']]
            }},
            options: {{
                renderActions: {{
                    findScript: [10, function (doc) {{
                        for (const node of document.querySelectorAll('script[type^="math/tex"]')) {{
                            const display = node.type.includes('mode=display');
                            const math = new doc.options.MathItem(
                                node.textContent,
                                doc.inputJax[0],
                                display
                            );
                            const text = document.createTextNode('');
                            node.parentNode.replaceChild(text, node);
                            math.start = {{node: text, delim: '', n: 0}};
                            math.end = {{node: text, delim: '', n: 0}};
                            doc.math.push(math);
                        }}
                    }}, '']
                }}
            }}
        }};
    </script>
    <style>.MathJax_Preview {{ display: none }}</style>
</head>
<body>
    <div class="content">
        {content}
    </div>
</body>
</html>
"""

DEFAULT_METADATA = {
    "title": "Lorem Ipsum",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
}

def md_to_html(source: str, template: str = DEFAULT_TEMPLATE, build_url=None) -> str:
    raw_metadata = extract_metadata(source)
    metadata = yaml.safe_load(raw_metadata)

    stripped = trim_metadata(source)

    extension_configs: dict = {
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

    return template.format(
        content=content,
        raw_metadata=raw_metadata.strip("\n"), 
        **metadata
    )

