import os

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

def scan_templates(templates: dict[str, str] | None, source_dir: str) -> dict[str, str]:
    ret = {"DEFAULT": DEFAULT_TEMPLATE}
    if templates is None:
        return ret
    for name, path in templates.items():
        fullpath = os.path.join(source_dir, path)
        with open(fullpath, "r") as f:
            ret[name] = f.read()
    return ret

