---
name: scinote-project-builder
description: "Scaffold and build a hands-on companion project for any chapter project ticket. Enforces a proposal-first workflow, scaffolds proposal/, docs/, notes/, and src/ directories, configures an isolated virtual environment, implements modular code with tests, and resolves tickets."
category: development
risk: safe
source: self
author: OpenCode Scientific Suite
tags:
  - project-scaffolding
  - proposal-writing
  - python
  - testing
  - scientific-implementation
tools:
  - opencode
  - question
  - shell
  - write
  - read
  - edit
---

# Scinote Project Builder

Architect, specify, and build a hands-on companion engineering and scientific project for any chapter.

## When to Use

- Use when working on a `tickets/PROJ-XX.md` ticket.
- Trigger when the user requests building, specifying, or running the companion practical project for a curriculum chapter.
- Can be invoked in a fresh OpenCode chat session.

---

## Operating Invariants

1. **Proposal-First Discipline**: Never jump straight into code implementation. Always draft and review `proposal/proposal.md` with the user first via the `question` tool.
2. **Strict 4-Folder Project Architecture**: Every project must contain:
   - `proposal/`: Detailed problem statement, equations, architecture diagram, and acceptance criteria.
   - `docs/`: Module explanations, API docs, and run instructions.
   - `notes/`: Experiment logs, mathematical scratchpad, and benchmark observations.
   - `src/`: Clean, modular, type-hinted Python code with automated unit tests.
3. **Environment Isolation**: Always create a self-contained virtual environment inside `projects/chXX-<slug>/.venv` using `uv` or `python -m venv`. Never pollute the global or notes environment.
4. **Automated Test Verification**: All core mathematical functions and algorithms must have passing unit tests before the project is marked complete.

---

## Step-by-Step Procedure

### Step 1: Read the Project Ticket
Read `tickets/PROJ-XX.md`. Retrieve:
- Chapter number and title
- Project title and core objectives
- Target directory `projects/chXX-<slug>/`

### Step 2: Draft the Project Proposal
Create `projects/chXX-<slug>/proposal/proposal.md` using the standard proposal template:
- Problem formulation and scientific motivation
- Core mathematical equations to be implemented
- System architecture diagram (Mermaid)
- Benchmark criteria and expected outputs

### Step 3: HITL Proposal Review
Present the proposal architecture to the user using the `question` tool:
- Implementation scope: Minimal reference implementation vs fully benchmarked modular package.
- Target hardware/acceleration: Pure CPU (NumPy/SciPy) vs GPU accelerated (PyTorch/JAX).
- Incorporate user feedback into `proposal/proposal.md`.

### Step 4: Environment & Dependency Setup
In `projects/chXX-<slug>/`:
Create `pyproject.toml` or `requirements.txt`:
```bash
cd "projects/chXX-<slug>"
uv venv .venv
source .venv/bin/activate
uv pip install numpy scipy matplotlib pytest
```

### Step 5: Implement Modular Source Code & Tests
Under `src/`:
- `src/__init__.py`
- `src/core.py`: Core mathematical equations and algorithms.
- `src/models.py`: Architecture or simulation engine.
- `src/utils.py`: Visualization and data utilities.
- `tests/test_core.py`: Pytest suite asserting numerical tolerances and edge cases.

Under `docs/`:
- `docs/README.md`: How to run the project, explanations of outputs.

Under `notes/`:
- `notes/experiments.md`: Log of benchmark runs and parameter studies.

### Step 6: Run Tests & Verification
Execute the test suite in the project environment:
```bash
cd "projects/chXX-<slug>"
.venv/bin/pytest tests/
```
Ensure all tests pass.

### Step 7: Resolve the Project Ticket
Execute `ticket_tool.py resolve`:
```bash
python3 /home/mahan/Work/scinote-skills/scripts/ticket_tool.py resolve \
  --id "PROJ-XX" \
  --summary "Drafted proposal, initialized isolated .venv, implemented modular src/ code with passing pytest suite and benchmark documentation." \
  --tickets-dir tickets
```
Print project summary and provide next steps.
