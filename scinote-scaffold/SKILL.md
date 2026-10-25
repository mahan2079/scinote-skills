---
name: scinote-scaffold
description: "Scaffold a comprehensive scientific notes curriculum on any topic. Conducts HITL intake diagnostics, plans Parts -> Chapters -> Sections -> Subsections, generates folder structures, sets up shared notes virtual environments, and creates an unblocked dependency graph of markdown tickets."
category: development
risk: safe
source: self
author: OpenCode Scientific Suite
tags:
  - education
  - scientific-computing
  - jupyter
  - curriculum-design
  - ticket-orchestration
tools:
  - opencode
  - question
  - shell
  - write
  - read
  - glob
---

# Scinote Scaffold

Plan and scaffold a comprehensive, first-principles scientific curriculum with companion research papers, hands-on chapter projects, and runnable Jupyter notebooks.

## When to Use

- Use when starting a new study or research curriculum on any scientific, mathematical, or engineering subject (e.g. quantum computing, deep learning, algebraic topology, statistical mechanics, computational neuroscience).
- Trigger when the user mentions "scaffold notes", "create curriculum", "plan scientific notes", or invokes `scinote-scaffold`.
- Do NOT use for writing an individual subsection note (use `scinote-section-writer` instead).
- Do NOT use for finding papers for an existing chapter (use `scinote-paper-finder` instead).

---

## Operating Invariants

1. **HITL Diagnostic First**: Always use the OpenCode `question` tool to interview the user regarding learning outcomes, mathematical background, and target scope. Assume nothing.
2. **Variable Topology & Granular Flexibility (NO Fixed Counts)**: 
   - **NEVER** force a uniform or fixed number of sections per chapter (e.g., forcing 2 sections). A chapter might need 2 sections, or 5, or 10+, depending entirely on the breadth and complexity of the subject matter.
   - **NEVER** force a uniform or fixed number of subsections per section (e.g., forcing 2 subsections). A section may have 1 focused subsection or 6+ detailed subtopics.
   - Each chapter and section must have its own tailored, independent breakdown reflecting the natural mathematical and conceptual structure of the material.
3. **First-Principles Scaffolding**: Every chapter must have clear prerequisites, learning goals, and companion project goals.
4. **Deterministic Structure**: Always produce the canonical folder hierarchy:
   - `curriculum/syllabus.md` & `curriculum/PROGRESS.md`
   - `tickets/` with markdown files for every subsection (`SEC-XX-YY-ZZ.md`), chapter paper review (`PAPER-XX.md`), and chapter project (`PROJ-XX.md`).
   - `notes/chXX-.../secYY-.../`
   - `papers/chXX-.../`
   - `projects/chXX-.../{proposal,docs,notes,src}/`
5. **Environment Isolation**: Initialize the shared notes environment (`.venv-notes`) using `setup_notes_env.sh` and register `scinotes-kernel`.

---

## Step-by-Step Procedure

### Step 1: Intake & Level Diagnostic (HITL)
Interview the user via the `question` tool across the key axes:
1. **Subject & Target Destination**: Exact field, specific topics of interest, and ultimate goal.
2. **Curriculum Topology & Breadth**: 
   - How deep and broad should the curriculum be?
   - Inquire about the desired breakdown: highlight that chapters can vary in weight (e.g., core foundational chapters may have 6-12 sections, while introductory or concluding chapters may only have 2-4 sections).
   - Let the user specify or confirm the varied section breakdown per chapter and subsection breakdown per section.
3. **Mathematical Background**: Comfort level with calculus, linear algebra, probability, and proofs.
4. **Computational Background**: Python fluency, scientific packages (NumPy, PyTorch, SciPy).

### Step 2: Build Syllabus Spec
Synthesize the user's responses into a JSON specification where each chapter and section has its own organically sized breakdown. For example:
```json
{
  "topic": "Quantum Computing & Quantum Algorithms",
  "level": "First-Principles to Advanced",
  "description": "Comprehensive theoretical notes, simulations, and companion papers.",
  "parts": [
    {
      "title": "Mathematical Foundations",
      "chapters": [
        {
          "number": 1,
          "title": "Hilbert Spaces and Quantum States",
          "project_title": "Quantum State Vector Simulator",
          "paper_topics": ["Quantum state tomography", "Bra-ket notation and density operators"],
          "sections": [
            {
              "number": 1,
              "title": "Complex Vector Spaces",
              "subsections": [
                {
                  "number": 1,
                  "title": "Inner Products and Dirac Notation",
                  "goals": ["Master bra-ket notation", "Derive Cauchy-Schwarz inequality", "Implement inner products in NumPy"]
                },
                {
                  "number": 2,
                  "title": "Cauchy-Schwarz and Triangle Inequalities",
                  "goals": ["Formal algebraic proofs of foundational inequalities"]
                },
                {
                  "number": 3,
                  "title": "Gram-Schmidt Orthogonalization",
                  "goals": ["Orthonormal basis construction and numerical implementation"]
                }
              ]
            },
            {
              "number": 2,
              "title": "Linear Operators on Hilbert Spaces",
              "subsections": [
                {
                  "number": 1,
                  "title": "Hermitian, Unitary, and Normal Operators",
                  "goals": ["Spectral theorem and matrix representations"]
                }
              ]
            },
            {
              "number": 3,
              "title": "Tensor Products and Composite Systems",
              "subsections": [
                {
                  "number": 1,
                  "title": "Kronecker Products and State Spaces",
                  "goals": ["Multiqubit state space representations"]
                },
                {
                  "number": 2,
                  "title": "Entanglement and Non-Separability Criteria",
                  "goals": ["Schmidt decomposition and entanglement entropy"]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

Save this temporary spec file to `/tmp/opencode/curriculum_spec.json`.

### Step 3: Run Ticket Generator
Execute `scripts/ticket_tool.py`:
```bash
python3 /home/mahan/Work/scinote-skills/scripts/ticket_tool.py init-curriculum \
  --spec /tmp/opencode/curriculum_spec.json \
  --base-dir .
```

### Step 4: Provision Shared Notes Environment
Run `setup_notes_env.sh` to ensure Python packages (`numpy`, `scipy`, `matplotlib`, `sympy`, `ipykernel`) are installed and registered under the kernel `scinotes-kernel`:
```bash
/home/mahan/Work/scinote-skills/setup_notes_env.sh .venv-notes scinotes-kernel "Python (Scientific Notes)"
```

### Step 5: Report Roadmap & Next Prompt
Print a summary of the scaffolded curriculum, display the path to `curriculum/syllabus.md`, and give the user the exact copy-paste prompt for the first frontier ticket:
```text
Curriculum scaffolded successfully!
Next step: In a fresh OpenCode chat, run:
scinote-section-writer tickets/SEC-01-01-01.md
```
