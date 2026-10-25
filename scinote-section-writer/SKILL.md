---
name: scinote-section-writer
description: "Research and write a standalone, fully runnable scientific Jupyter notebook for a specific subsection ticket. Performs HITL level checkpointing, includes rigorous LaTeX derivations, Mermaid flowcharts, executable Python code with plots, academic citations, self-assessment questions, and automated execution verification."
category: development
risk: safe
source: self
author: OpenCode Scientific Suite
tags:
  - education
  - scientific-writing
  - jupyter
  - latex
  - python
  - mermaid
tools:
  - opencode
  - question
  - shell
  - write
  - read
  - edit
---

# Scinote Section Writer

Author an authoritative, standalone, first-principles scientific Jupyter notebook for any subsection ticket.

## When to Use

- Use when you have a pending subsection ticket (e.g. `tickets/SEC-01-01-01.md`) in a curriculum.
- Trigger when the user passes a ticket file path or requests writing a specific section/subsection note.
- Designed to be run in a **fresh OpenCode session** to maintain maximum token efficiency.

---

## Operating Invariants

1. **HITL Level Checkpoint First**: Before writing a single cell, ask the user the 2 pedagogical checkpoint questions specified in the ticket using the OpenCode `question` tool. Adjust explanation density to their response.
2. **First Principles Guarantee**: Assume zero unexplained jargon. Every symbol, variable, and theorem must be defined before use.
3. **Dual Mermaid Rendering**: Always provide both a markdown ```` ```mermaid ```` block (for GitHub/VS Code viewers) and an interactive IPython HTML loader cell (for classic JupyterLab rendering).
4. **Automated Verification**: Never mark a ticket as done until the notebook is validated and executed headlessly with 0 errors using `nb_tool.py execute`.
5. **Context Propagation**: Always execute `ticket_tool.py resolve` with an executive summary so the next ticket inherits continuous context.

---

## Step-by-Step Procedure

### Step 1: Read the Ticket & Context
Read the specified ticket file (e.g., `tickets/SEC-01-01-01.md`). Extract:
- Target notebook path (e.g., `notes/ch01-.../sec01-.../01-...ipynb`)
- Prerequisite concepts and `## Previous Sections Review`
- `## Pedagogical Level Checkpoints` questions
- Target learning goals and key formulas

### Step 2: Level Diagnostic Checkpoint (HITL)
Invoke the OpenCode `question` tool to present the 2 diagnostic questions from the ticket to the user. For instance:
- Option A: Emphasize geometric/physical intuition with visual analogies.
- Option B: Emphasize rigorous mathematical derivations and proofs.
- Option C: Emphasize computational/algorithmic implementation and numerical stability.

Incorporate the user's choices into the notebook depth.

### Step 3: Author Notebook Cells via `nb_tool.py`

Initialize the notebook:
```bash
python3 /home/mahan/Work/scinote-skills/scripts/nb_tool.py init "<target_notebook_path>"
```

Append structured cells in sequence:

#### Cell 1: Header & First-Principles Motivation (Markdown)
- Title, Chapter, Section context
- The core motivating question: "Why do we care about this concept?"
- Intuitive mental model with everyday or geometric analogy.

#### Cell 2: Rigorous Mathematical Formulation (Markdown with LaTeX)
- Precise definitions, axioms, or physical laws.
- Step-by-step mathematical derivation showing intermediate steps.
- Use display math blocks:
  $$\begin{aligned}
  \langle u, v \rangle &= \sum_{i=1}^n u_i^* v_i
  \end{aligned}$$

#### Cell 3 & 4: Mermaid Flowchart (Markdown + Interactive Loader)
Add the structural architecture, algorithm pipeline, or state transitions:
```bash
python3 /home/mahan/Work/scinote-skills/scripts/nb_tool.py add-mermaid "<target_notebook_path>" --code "graph TD
    A[Input Vector Space V] --> B[Inner Product Map]
    B --> C[Norm and Distance Metric]
    C --> D[Hilbert Space Completeness]"
```

#### Cell 5 & 6: Executable Code & Data Visualizations (Code)
Write clean, reproducible Python code using `numpy`, `scipy`, `matplotlib`, or `sympy`.
The code must:
- Generate clean data or simulate the mathematical concept.
- Plot figures with labeled axes, titles, grid, and legends.
- Use `plt.show()` so output displays directly in notebook.

#### Cell 7: Academic Citations & Context (Markdown)
Cite relevant papers from `papers/chXX/papers.bib` or foundational literature with author, title, year, and arXiv/DOI link.

#### Cell 8: Self-Assessment Exercises (Markdown)
Provide 2 targeted conceptual/computational questions followed by expandable or detailed solutions to cement active learning.

### Step 4: Validate & Execute Headlessly
Run headless execution using the notes environment:
```bash
python3 /home/mahan/Work/scinote-skills/scripts/nb_tool.py validate "<target_notebook_path>"
python3 /home/mahan/Work/scinote-skills/scripts/nb_tool.py execute "<target_notebook_path>" --python-bin .venv-notes/bin/python
```
If errors occur, fix the code cells immediately and re-run until execution passes with 0 errors.

### Step 5: Resolve Ticket & Propagate Summary
Generate a 2-3 sentence executive recap of what this note covered and execute:
```bash
python3 /home/mahan/Work/scinote-skills/scripts/ticket_tool.py resolve \
  --id "<ticket_id>" \
  --summary "<recap_of_topics_and_key_takeaways>" \
  --tickets-dir tickets
```

Print confirmation, display the next unblocked ticket on the frontier, and present the user with the prompt for their next chat session.
