---
name: scinote-scaffold
description: "Scaffold an adaptive, comprehensive scientific notes curriculum on any topic. Conducts HITL intake diagnostics, performs deep academic domain taxonomy decomposition, plans naturally sized Parts -> Chapters -> Sections -> Subsections without artificial constraints, scaffolds folder structures, sets up shared notes virtual environments, and creates an unblocked dependency graph of markdown tickets."
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

Plan and scaffold an authoritative, comprehensively structured scientific curriculum with companion research papers, hands-on chapter projects, and runnable Jupyter notebooks.

## When to Use

- Use when starting a new study or research curriculum on any scientific, mathematical, or engineering subject (e.g. quantum computing, deep learning, algebraic topology, statistical mechanics, computational neuroscience).
- Trigger when the user mentions "scaffold notes", "create curriculum", "plan scientific notes", or invokes `scinote-scaffold`.
- Do NOT use for writing an individual subsection note (use `scinote-section-writer` instead).
- Do NOT use for finding papers for an existing chapter (use `scinote-paper-finder` instead).

---

## Operating Invariants

1. **HITL Diagnostic First**: Always use the OpenCode `question` tool to interview the user regarding learning outcomes, mathematical background, and target scope. Assume nothing.
2. **Anti-Toy Invariant & Dynamic Topology (STRICT)**:
   - **Banned Anti-Pattern**: NEVER fall into the LLM "Rule of Twos" (e.g. defaulting to 2 parts, 2 chapters, 2 sections, 2 subsections). Real scientific fields cannot be crammed into a toy outline.
   - **Topic-Driven Natural Topology**: The number of chapters, sections, and subsections must reflect the true academic depth of the subject matter:
     - Foundational or mathematically dense chapters often demand **5 to 12 distinct sections** (e.g., separating distinct theorems, operators, and algorithms into individual sections rather than lumping them together).
     - Individual sections naturally decompose into **1 to 6+ subsections**, where each subsection corresponds to a single, focused notebook study session.
     - Introductory or review chapters may only need 2-4 sections, while advanced or algorithmic chapters need extensive coverage.
   - Structure the curriculum like an authoritative graduate textbook (e.g. Nielsen & Chuang, Boyd & Vandenberghe, Goodfellow, or Goldstein).
3. **Interactive Syllabus Review Gate (HITL)**: Before generating any files or tickets, present the full drafted breakdown of Parts, Chapters, Sections, and Subsections to the user. Get explicit user confirmation or adjustments.
4. **First-Principles Scaffolding**: Every chapter must have clear prerequisites, learning goals, companion research paper topics, and companion project goals.
5. **Deterministic File & Ticket Hierarchy**:
   - `curriculum/syllabus.md` & `curriculum/PROGRESS.md`
   - `tickets/` with markdown files for every subsection (`SEC-XX-YY-ZZ.md`), chapter paper review (`PAPER-XX.md`), and chapter project (`PROJ-XX.md`).
   - `notes/chXX-.../secYY-.../`
   - `papers/chXX-.../`
   - `projects/chXX-.../{proposal,docs,notes,src}/`
6. **Environment Isolation**: Initialize the shared notes environment (`.venv-notes`) using `setup_notes_env.sh` and register `scinotes-kernel`.

---

## Step-by-Step Procedure

### Step 1: Intake Diagnostic Interview (HITL)
Interview the user via the OpenCode `question` tool across the 4 key axes:
1. **Target Subject & Destination**: What exact topic are we mastering? What is the end goal (research-readiness, implementing production systems, passing qualifying exams, or deep intellectual curiosity)?
2. **Target Depth & Scope**:
   - Comprehensive Masterclass (exhaustive multi-part graduate treatise covering every mathematical derivation, algorithmic variant, edge case, and physical simulation).
   - Focused Research Monograph (deep dive into specific subfields, skipping elementary prerequisites).
   - Applied Practitioner Suite (rigorous intuition + production-grade code implementations and benchmarks).
3. **Mathematical Baseline**: Linear algebra, multivariate calculus, differential equations, real/functional analysis, probability/measure theory, abstract algebra.
4. **Computational Baseline**: Python, vectorized NumPy/SciPy, autograd frameworks (PyTorch/JAX), hardware acceleration (GPU/TPU).

### Step 2: Academic Domain Decomposition
Analyze the chosen field and break it down according to genuine academic rigor:
- **Pillars / Parts**: Map out the high-level thematic trajectory (typically 3 to 5 Parts: e.g., Part 1: Mathematical Foundations; Part 2: Core Mechanics & Dynamics; Part 3: Advanced Architectures & Algorithms; Part 4: Frontier Applications & Open Problems).
- **Chapters**: Divide each Part into cohesive chapters (typically 3 to 6 chapters per Part).
- **Sections**: For each chapter, identify EVERY distinct mathematical structure, physical law, operator, or algorithmic family. Ensure no complex topics are glossed over or combined artificially.
- **Subsections**: Each subsection represents **one runnable Jupyter notebook** (~one study session):
  - Motivation & mental model
  - Step-by-step rigorous LaTeX derivation
  - Mermaid system diagram
  - Python computational experiment & visualization
  - Literature citations & self-assessment exercises

### Step 3: HITL Syllabus Review Gate
Present the proposed syllabus structure to the user via the `question` tool:
- Show the complete outline with chapter titles, section breakdowns, and estimated subsection count.
- Ask: *"Does this decomposition cover the full scope of your desired curriculum, or should we add/expand specific chapters or subtopics?"*
- Incorporate any feedback, added sections, or deeper subsections requested by the user.

### Step 4: Compile Spec & Initialize Curriculum
Once the user approves the outline, serialize the structure into `/tmp/opencode/curriculum_spec.json`.
The JSON must reflect the natural, varied topology:
```json
{
  "topic": "Geometric Deep Learning & Gauge Equivariant Neural Networks",
  "level": "Graduate / Research Monograph",
  "description": "Comprehensive theoretical notes, group actions, manifold representations, and equivariant architectures.",
  "parts": [
    {
      "title": "Mathematical Foundations: Groups, Manifolds, and Fibres",
      "chapters": [
        {
          "number": 1,
          "title": "Lie Groups, Lie Algebras, and Representations",
          "project_title": "Lie Group SO(3) & SE(3) Representation Engine",
          "paper_topics": ["Representation theory for neural networks", "Lie algebra exponential maps"],
          "sections": [
            {
              "number": 1,
              "title": "Topological Groups and Matrix Lie Groups",
              "subsections": [
                {
                  "number": 1,
                  "title": "Definition and Axioms of Matrix Lie Groups",
                  "goals": ["General linear group GL(n, R)", "Topological properties and compactness", "Implement matrix exponentials"]
                },
                {
                  "number": 2,
                  "title": "Orthogonal Group O(n) and Special Orthogonal Group SO(n)",
                  "goals": ["Isometries and rotations", "Orientation preservation", "Numerical orthogonalization"]
                },
                {
                  "number": 3,
                  "title": "Special Euclidean Group SE(n) and Rigid Motions",
                  "goals": ["Semidirect products", "Homogeneous coordinate representations", "SE(3) kinematics in Python"]
                }
              ]
            },
            {
              "number": 2,
              "title": "Lie Algebras and the Exponential Map",
              "subsections": [
                {
                  "number": 1,
                  "title": "Tangent Spaces at the Identity and Lie Brackets",
                  "goals": ["Infinitesimal generators", "Commutator brackets and Jacobi identity"]
                },
                {
                  "number": 2,
                  "title": "Exponential and Logarithmic Coordinates on SO(3)",
                  "goals": ["Rodrigues rotation formula", "Hat and vee isomorphism", "Lie algebra vector space basis"]
                },
                {
                  "number": 3,
                  "title": "Baker-Campbell-Hausdorff (BCH) Formula and Curvature",
                  "goals": ["Non-commutative additions", "Series expansion and truncation error bounds"]
                },
                {
                  "number": 4,
                  "title": "Adjoint Representation and Invariant Metrics",
                  "goals": ["Killing form", "Bi-invariant Riemannian metrics on compact Lie groups"]
                }
              ]
            },
            {
              "number": 3,
              "title": "Group Representation Theory for Deep Learning",
              "subsections": [
                {
                  "number": 1,
                  "title": "Linear Representations, Invariant Subspaces, and Irreps",
                  "goals": ["Schur's Lemma", "Complete reducibility (Maschke's theorem)"]
                },
                {
                  "number": 2,
                  "title": "Wigner D-Matrices and Spherical Harmonics",
                  "goals": ["SO(3) irreps decomposition", "Spherical harmonics expansion algorithms"]
                },
                {
                  "number": 3,
                  "title": "Clebsch-Gordan Coefficients and Tensor Products of Irreps",
                  "goals": ["Coupling angular momenta", "Tensor product decomposition into irreps", "NumPy Clebsch-Gordan tensor contraction"]
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

Run `ticket_tool.py`:
```bash
python3 /home/mahan/Work/scinote-skills/scripts/ticket_tool.py init-curriculum \
  --spec /tmp/opencode/curriculum_spec.json \
  --base-dir .
```

### Step 5: Provision Shared Notes Environment
Run `setup_notes_env.sh` to ensure Python packages (`numpy`, `scipy`, `matplotlib`, `sympy`, `ipykernel`) are installed and registered under the kernel `scinotes-kernel`:
```bash
/home/mahan/Work/scinote-skills/setup_notes_env.sh .venv-notes scinotes-kernel "Python (Scientific Notes)"
```

### Step 6: Present Roadmap & Next Frontier Prompt
Display the generated roadmap summary, reference `curriculum/syllabus.md`, and give the user the exact copy-paste prompt for the first frontier ticket:
```text
Curriculum scaffolded successfully!
Syllabus: curriculum/syllabus.md
Progress: curriculum/PROGRESS.md

First frontier ticket ready:
scinote-paper-finder tickets/PAPER-01.md
(or: scinote-section-writer tickets/SEC-01-01-01.md)
```
