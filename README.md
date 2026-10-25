# 🔬 Scientific Notes & Research Curriculum Skill Suite (`scinote-suite`)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![OpenCode Skills](https://img.shields.io/badge/OpenCode-Agent%20Skills-purple.svg)](https://agentskills.io)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-orange.svg)](https://jupyter.org/)

A production-grade, multi-agent skill suite designed for **OpenCode** (and compatible agent harnesses) to plan, research, and author comprehensive, first-principles scientific notes in Jupyter notebooks (`.ipynb`), complemented by academic literature downloads (arXiv PDFs + BibTeX) and hands-on chapter projects.

Inspired by the `/wayfinder` architectural planning pattern, `scinote-suite` uses a **local Markdown ticket system** with dynamic context handoffs. This ensures that you can learn, research, and write massive textbooks or research notes across dozens of clean chat sessions **without ever degrading model intelligence or exceeding context limits**.

---

## 🎯 What Is It?

`scinote-suite` is an automated, human-in-the-loop (HITL) educational and scientific authoring framework composed of 4 modular skills:

1. **`scinote-scaffold`**: Plans the master curriculum from Parts $\to$ Chapters $\to$ Sections $\to$ Subsections, scaffolds directory structures, initializes shared virtual environments and Jupyter kernels, and generates an unblocked dependency graph of markdown tickets.
2. **`scinote-section-writer`**: Reads an individual subsection ticket in a fresh chat, checks your background level, and writes a self-contained, fully runnable `.ipynb` notebook containing LaTeX proofs, dual-rendered Mermaid flowcharts, executable Python code with plots, academic citations, and self-assessment questions.
3. **`scinote-paper-finder`**: Discovers relevant academic literature for each chapter, downloads official PDFs into local storage, generates standardized BibTeX citation files, and writes an analytical synthesis guide.
4. **`scinote-project-builder`**: Enforces a proposal-first companion practical build for every chapter, scaffolding a dedicated 4-folder structure (`proposal/`, `docs/`, `notes/`, `src/`) and testing code in an isolated project virtual environment.

---

## 💡 Why Does This Exist?

When using LLMs or coding agents to learn complex scientific subjects or write comprehensive notes:

| Typical Agent Failure Mode | How `scinote-suite` Solves It |
|---|---|
| **Context Bloat / Amnesia**: Running a long conversation to write an entire chapter degrades reasoning, causes repetition, and hits token limits. | **Local Ticket DAG**: Every subsection is its own Markdown ticket. You run each ticket in a **fresh chat session**, consuming $\approx 5\text{k}$ tokens instead of $150\text{k}+$. |
| **Superficial Answers & Jargon**: Agents love hand-wavy explanations ("it is obvious that...") and unexplained notation. | **First-Principles Invariant**: Employs an intake diagnostic and per-ticket level checkpoints that force derivations from first principles without unexplained jargon. |
| **Broken Notebook JSON**: Models frequently output invalid JSON when escaping LaTeX backslashes (`\frac`, `\mathbb`) or quotes. | **Deterministic Python CLI (`nb_tool.py`)**: All notebooks are assembled and verified programmatically via Python, eliminating JSON syntax errors. |
| **Rigid Layout Assumptions / "Rule of Twos"**: LLMs naturally default to toy outlines (e.g., forcing 2 parts, 2 chapters, 2 sections, 2 subsections), destroying genuine academic rigor. | **Strict Anti-Toy Invariant & Dynamic Topology**: Chapters and sections adapt naturally to the mathematical domain. Foundational or dense chapters feature 5 to 12+ sections, each decomposing into as many subsections as needed for cognitive clarity. |
| **Dependency Hell**: Projects across different chapters collide in Python package requirements. | **Dual Environment Architecture**: A single unified virtual environment for all study notes (`scinotes-kernel`), paired with isolated `.venv` per chapter project. |

---

## 🗺️ System Architecture

```
                                      [User Prompt / Topic Request]
                                                    │
                                                    ▼
                                         ┌─────────────────────┐
                                         │  scinote-scaffold   │
                                         └──────────┬──────────┘
                                                    │
                   ┌────────────────────────────────┼────────────────────────────────┐
                   ▼                                ▼                                ▼
         ┌───────────────────┐            ┌───────────────────┐            ┌───────────────────┐
         │   PAPER-XX.md     │            │   SEC-XX-YY-ZZ    │            │     PROJ-XX.md    │
         │ (Academic Papers) │            │  (Subsection Note)│            │  (Chapter Project)│
         └─────────┬─────────┘            └─────────┬─────────┘            └─────────┬─────────┘
                   │                                │                                │
                   ▼                                ▼                                ▼
        ┌──────────────────────┐        ┌──────────────────────┐        ┌──────────────────────┐
        │ scinote-paper-finder │        │scinote-section-writer│        │scinote-project-builder
        └──────────┬───────────┘        └──────────┬───────────┘        └──────────┬───────────┘
                   │                                │                                │
                   ▼                                ▼                                ▼
         papers/chXX/                    notes/chXX/secYY/               projects/chXX/
         ├── papers.bib                  └── 01-topic.ipynb              ├── proposal/proposal.md
         ├── reading-guide.md            (LaTeX, Code, Mermaid,          ├── docs/
         └── paper.pdf                    Visualizations, Citations)     ├── notes/
                                                                         └── src/
```

---

## 📦 Directory Structure Standard

When you initialize a curriculum in a project directory, the suite creates and maintains:

```
my-study-topic/
├── curriculum/
│   ├── syllabus.md              # High-level syllabus, learning goals, and TOC
│   └── PROGRESS.md              # Real-time completion checklist
├── tickets/
│   ├── PAPER-01.md              # Literature discovery & reading guide ticket
│   ├── SEC-01-01-01.md          # Subsection ticket with context handoff & prompt card
│   ├── SEC-01-01-02.md
│   └── PROJ-01.md               # Chapter companion project ticket
├── notes/
│   └── ch01-hilbert-spaces/
│       └── sec01-complex-vectors/
│           ├── 01-inner-products.ipynb     # Fully runnable notebook
│           └── 02-cauchy-schwarz.ipynb
├── papers/
│   └── ch01-hilbert-spaces/
│       ├── papers.bib           # BibTeX citations
│       ├── reading-guide.md     # Deep analytical reading guide
│       └── 01-dirac-1930.pdf    # Downloaded arXiv PDF
└── projects/
    └── ch01-hilbert-spaces/
        ├── .venv/               # Isolated per-chapter virtual environment
        ├── proposal/
        │   └── proposal.md      # Formal project specification
        ├── docs/                # Architecture docs and API references
        ├── notes/               # Experiment logs and observations
        └── src/                 # Tested, modular Python source code
```

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/mahan2079/scinote-skills.git /home/mahan/Work/scinote-skills
cd /home/mahan/Work/scinote-skills
```

### 2. Register Skills into OpenCode
Symlink the skills into your global agent directory (`~/.agents/skills/`):
```bash
ln -sfn $(pwd)/scinote-scaffold ~/.agents/skills/scinote-scaffold
ln -sfn $(pwd)/scinote-section-writer ~/.agents/skills/scinote-section-writer
ln -sfn $(pwd)/scinote-paper-finder ~/.agents/skills/scinote-paper-finder
ln -sfn $(pwd)/scinote-project-builder ~/.agents/skills/scinote-project-builder
```

OpenCode will automatically discover the skills.

---

## 📖 Step-by-Step Usage Guide

### Phase 1: Scaffold a New Subject (`scinote-scaffold`)
In your terminal or in an OpenCode chat, prompt the agent:
```text
scinote-scaffold
# Or: "I want to create comprehensive scientific notes on Geometric Deep Learning"
```
The agent will launch an interactive intake diagnostic:
1. **Topic & Destination**: Identifies your desired subject and whether you want theoretical proofs, practical code, or a blend.
2. **Curriculum Topology**: Calibrates how many Parts, Chapters, Sections, and Subsections are needed (variable sizing).
3. **Background Level**: Calibrates explanation density to your math and coding background.

The skill will generate:
- `curriculum/syllabus.md` and `curriculum/PROGRESS.md`
- Complete directory trees and unblocked tickets under `tickets/`
- Shared virtual environment `.venv-notes` with registered Jupyter kernel `scinotes-kernel`

---

### Phase 2: Check the Frontier
To see what tickets are ready to be worked on:
```bash
python3 /home/mahan/Work/scinote-skills/scripts/ticket_tool.py list
```
Tickets marked `[FRONTIER]` are unblocked and ready to execute.

---

### Phase 3: Research Papers (`scinote-paper-finder`)
Open a fresh chat and run the prompt from `tickets/PAPER-XX.md`:
```text
scinote-paper-finder tickets/PAPER-01.md
```
The agent queries arXiv, downloads the actual PDFs into `papers/ch01/`, compiles `papers/ch01/papers.bib`, and authors `reading-guide.md`.

---

### Phase 4: Author Subsection Notebooks (`scinote-section-writer`)
Open a **fresh chat session** and paste the prompt card:
```text
scinote-section-writer tickets/SEC-01-01-01.md
```
The agent:
1. Conducts a quick 2-question checkpoint to tune depth.
2. Builds `notes/ch01-.../01-...ipynb` using `scripts/nb_tool.py`:
   - Step-by-step LaTeX derivations
   - Dual-mode Mermaid diagram (native markdown + interactive HTML loader)
   - Executable Python simulations using `numpy`/`matplotlib`
   - Citations and self-assessment exercises
3. Headlessly executes the notebook cells to verify 0 errors.
4. Marks the ticket `done`, updates `PROGRESS.md`, and **propagates a summary recap** into the next ticket's context.

---

### Phase 5: Build Chapter Projects (`scinote-project-builder`)
When you reach a chapter project ticket:
```text
scinote-project-builder tickets/PROJ-01.md
```
The agent enforces proposal-first discipline:
1. Drafts `proposal/proposal.md` and reviews it with you.
2. Creates an isolated `.venv` inside `projects/ch01/`.
3. Implements modular source code in `src/` and unit tests in `tests/`.
4. Runs `pytest` to guarantee all tests pass.

---

## 🛠️ CLI Utilities Reference

The suite comes with standalone, battle-tested Python scripts under `scripts/`:

| Tool | Purpose | Key Commands |
|---|---|---|
| `scripts/nb_tool.py` | Safe Jupyter construction, validation, and execution. | `init`, `add-markdown`, `add-code`, `add-mermaid`, `build`, `validate`, `execute` |
| `scripts/ticket_tool.py` | Ticket lifecycle, frontier queries, and context propagation. | `init-curriculum`, `list`, `resolve` |
| `scripts/paper_tool.py` | arXiv query engine, PDF downloader, and BibTeX generator. | `search`, `fetch` |
| `setup_notes_env.sh` | High-speed `uv` environment setup and kernel registration. | `./setup_notes_env.sh` |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
