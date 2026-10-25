#!/usr/bin/env python3
"""
nb_tool.py - Deterministic Jupyter Notebook builder and executor.
Safely constructs .ipynb files with proper cells (markdown, code, raw),
handles LaTeX escape sequences, injects interactive Mermaid loaders,
and can headlessly execute notebooks with nbconvert / ipykernel or report execution status.
"""

import sys
import os
import json
import argparse
from typing import List, Dict, Any, Optional

def create_base_notebook() -> Dict[str, Any]:
    return {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.12.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

def make_markdown_cell(source: str) -> Dict[str, Any]:
    if "\\n" in source and "\n" not in source:
        try:
            source = source.encode("utf-8").decode("unicode_escape")
        except Exception:
            pass
    lines = [line + "\n" for line in source.splitlines()]
    if lines and lines[-1].endswith("\n"):
        lines[-1] = lines[-1][:-1]
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": lines
    }

def make_code_cell(source: str) -> Dict[str, Any]:
    if "\\n" in source and "\n" not in source:
        try:
            source = source.encode("utf-8").decode("unicode_escape")
        except Exception:
            pass
    lines = [line + "\n" for line in source.splitlines()]
    if lines and lines[-1].endswith("\n"):
        lines[-1] = lines[-1][:-1]
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": lines
    }

def make_mermaid_cell(mermaid_code: str, diagram_id: str = "mermaid-diagram") -> Dict[str, Any]:
    """Creates a code cell that uses IPython.display.HTML with mermaid.js CDN for interactive rendering in notebooks."""
    py_code = f'''from IPython.display import HTML, display

mermaid_code = """{mermaid_code.strip()}"""

html_content = f"""
<div class="mermaid">
{{mermaid_code}}
</div>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
    if (window.mermaid) {{
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
        mermaid.init(undefined, document.querySelectorAll('.mermaid'));
    }}
</script>
"""
display(HTML(html_content))
'''
    return make_code_cell(py_code)

def cmd_init(args: argparse.Namespace):
    nb = create_base_notebook()
    os.makedirs(os.path.dirname(os.path.abspath(args.path)), exist_ok=True)
    with open(args.path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"Initialized blank notebook at: {args.path}")

def cmd_add_markdown(args: argparse.Namespace):
    if not os.path.exists(args.path):
        nb = create_base_notebook()
    else:
        with open(args.path, "r", encoding="utf-8") as f:
            nb = json.load(f)

    if args.file:
        with open(args.file, "r", encoding="utf-8") as sf:
            content = sf.read()
    else:
        content = args.text

    nb["cells"].append(make_markdown_cell(content))
    with open(args.path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"Added markdown cell to {args.path}")

def cmd_add_code(args: argparse.Namespace):
    if not os.path.exists(args.path):
        nb = create_base_notebook()
    else:
        with open(args.path, "r", encoding="utf-8") as f:
            nb = json.load(f)

    if args.file:
        with open(args.file, "r", encoding="utf-8") as sf:
            content = sf.read()
    else:
        content = args.code

    nb["cells"].append(make_code_cell(content))
    with open(args.path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"Added code cell to {args.path}")

def cmd_add_mermaid(args: argparse.Namespace):
    if not os.path.exists(args.path):
        nb = create_base_notebook()
    else:
        with open(args.path, "r", encoding="utf-8") as f:
            nb = json.load(f)

    if args.file:
        with open(args.file, "r", encoding="utf-8") as sf:
            content = sf.read()
    else:
        content = args.code

    # Add fallback markdown cell first
    fallback = f"```mermaid\n{content.strip()}\n```"
    nb["cells"].append(make_markdown_cell(fallback))
    # Add interactive HTML runner
    nb["cells"].append(make_mermaid_cell(content))

    with open(args.path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"Added Mermaid diagram cell to {args.path}")

def cmd_build(args: argparse.Namespace):
    """Build a complete notebook from a structured JSON spec file."""
    with open(args.spec, "r", encoding="utf-8") as f:
        spec = json.load(f)

    nb = create_base_notebook()
    for item in spec.get("cells", []):
        c_type = item.get("type", "markdown")
        content = item.get("content", "")
        if c_type == "markdown":
            nb["cells"].append(make_markdown_cell(content))
        elif c_type == "code":
            nb["cells"].append(make_code_cell(content))
        elif c_type == "mermaid":
            fallback = f"```mermaid\n{content.strip()}\n```"
            nb["cells"].append(make_markdown_cell(fallback))
            nb["cells"].append(make_mermaid_cell(content))

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"Successfully built complete notebook at: {args.output} ({len(nb['cells'])} cells)")

def cmd_validate(args: argparse.Namespace):
    """Validate JSON format and schema for .ipynb."""
    try:
        with open(args.path, "r", encoding="utf-8") as f:
            nb = json.load(f)
        assert "cells" in nb, "Missing 'cells' key"
        assert "metadata" in nb, "Missing 'metadata' key"
        assert "nbformat" in nb, "Missing 'nbformat' key"
        print(f"VALID: {args.path} has {len(nb['cells'])} cells (nbformat: {nb['nbformat']}.{nb.get('nbformat_minor', 0)})")
        return 0
    except Exception as e:
        print(f"INVALID: {args.path} failed validation: {e}", file=sys.stderr)
        return 1

def cmd_execute(args: argparse.Namespace):
    """Execute notebook cells headlessly using python's jupyter/nbconvert if installed, or fallback python exec for code cells."""
    import subprocess
    import tempfile

    print(f"Executing notebook: {args.path}...")
    venv_python = args.python_bin or sys.executable

    # Try jupyter nbconvert --execute first
    res = subprocess.run([
        venv_python, "-m", "jupyter", "nbconvert", "--to", "notebook",
        "--execute", "--inplace", args.path
    ], capture_output=True, text=True)

    if res.returncode == 0:
        print(f"Execution succeeded (via nbconvert) on {args.path}")
        return 0
    
    # If nbconvert is not installed in current environment, run fallback validation of code cells
    print(f"nbconvert not present or failed: {res.stderr.strip()[:200]}. Attempting code-block verification...")
    with open(args.path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    code_cells = [cell for cell in nb.get("cells", []) if cell.get("cell_type") == "code"]
    combined_code = "\n\n".join("".join(c.get("source", [])) for c in code_cells)

    # Filter out IPython magics if any for standard python testing
    clean_code_lines = []
    for line in combined_code.split("\n"):
        if line.strip().startswith("%") or line.strip().startswith("!"):
            clean_code_lines.append(f"# {line}")
        else:
            clean_code_lines.append(line)
    clean_code = "\n".join(clean_code_lines)

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tf:
        tf.write(clean_code)
        temp_path = tf.name

    try:
        run_res = subprocess.run([venv_python, temp_path], capture_output=True, text=True)
        if run_res.returncode == 0:
            print(f"All {len(code_cells)} code cells executed successfully via python fallback test!")
            return 0
        else:
            print(f"Code execution ERROR:\n{run_res.stderr}", file=sys.stderr)
            return 1
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def main():
    parser = argparse.ArgumentParser(description="Notebook builder and verification CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_init = subparsers.add_parser("init", help="Initialize a new blank .ipynb file")
    p_init.add_argument("path", help="Path to destination .ipynb")

    p_add_md = subparsers.add_parser("add-markdown", help="Append markdown cell")
    p_add_md.add_argument("path", help="Path to .ipynb")
    p_add_md.add_argument("--text", default="", help="Markdown text")
    p_add_md.add_argument("--file", help="Read markdown from file")

    p_add_code = subparsers.add_parser("add-code", help="Append code cell")
    p_add_code.add_argument("path", help="Path to .ipynb")
    p_add_code.add_argument("--code", default="", help="Python code")
    p_add_code.add_argument("--file", help="Read code from file")

    p_add_mm = subparsers.add_parser("add-mermaid", help="Append mermaid flowchart cell")
    p_add_mm.add_argument("path", help="Path to .ipynb")
    p_add_mm.add_argument("--code", default="", help="Mermaid flowchart definition")
    p_add_mm.add_argument("--file", help="Read mermaid definition from file")

    p_build = subparsers.add_parser("build", help="Build notebook from JSON spec")
    p_build.add_argument("--spec", required=True, help="Path to spec JSON")
    p_build.add_argument("--output", required=True, help="Path to output .ipynb")

    p_val = subparsers.add_parser("validate", help="Validate notebook JSON format")
    p_val.add_argument("path", help="Path to .ipynb")

    p_exec = subparsers.add_parser("execute", help="Execute and verify notebook")
    p_exec.add_argument("path", help="Path to .ipynb")
    p_exec.add_argument("--python-bin", help="Python binary path to use (e.g. from .venv-notes)")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args)
    elif args.command == "add-markdown":
        cmd_add_markdown(args)
    elif args.command == "add-code":
        cmd_add_code(args)
    elif args.command == "add-mermaid":
        cmd_add_mermaid(args)
    elif args.command == "build":
        cmd_build(args)
    elif args.command == "validate":
        sys.exit(cmd_validate(args))
    elif args.command == "execute":
        sys.exit(cmd_execute(args))

if __name__ == "__main__":
    main()
