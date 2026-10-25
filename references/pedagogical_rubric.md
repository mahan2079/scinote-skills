# Pedagogical Rubric & Authoring Standards

## 1. Prime Directive: Assume Nothing, Derive from First Principles
- **No Unexplained Jargon**: Never introduce a technical term without defining it immediately in plain English, followed by its formal mathematical notation.
- **Mental Models First**: Before writing an abstract equation, describe the intuitive physical or geometric mental model.
- **Step-by-Step Derivations**: When presenting a proof or derivation, show intermediate algebraic steps rather than skipping to "it is easily seen that".

## 2. The 3 Diagnostic Tiers (Calibrated via HITL Checkpoints)

### Tier 1: Intuitive Foundation (Novice / Refresher)
- **Focus**: Concrete analogies, 2D/3D visualizations, geometric intuition, code-first experimentation.
- **Math Depth**: High school algebra through introductory single-variable calculus and basic vectors.
- **Code Style**: Explicit variables, line-by-line comments, interactive matplotlib plots.

### Tier 2: Applied Rigor (Undergraduate / Practitioner)
- **Focus**: Algorithmic implementation, vectorization (NumPy/PyTorch), efficiency tradeoffs, standard mathematical proofs.
- **Math Depth**: Multivariate calculus, linear algebra (eigenspaces, SVD), probability theory, differential equations.
- **Code Style**: Vectorized array operations, modular classes/functions, benchmark timing.

### Tier 3: Advanced Theory (Graduate / Researcher)
- **Focus**: Formal axiomatic frameworks, convergence guarantees, edge-case theorems, frontier open questions.
- **Math Depth**: Real/functional analysis, measure theory, differential geometry, modern statistical learning theory.
- **Code Style**: High-performance implementations, custom autograd / solvers, rigorous numerical stability safeguards.

## 3. Subsection Notebook Checklist
Every subsection `.ipynb` must fulfill:
- [ ] Title with chapter/section context
- [ ] First-principles intuitive motivation
- [ ] Rigorous LaTeX mathematical formulation
- [ ] At least one Mermaid workflow/architecture diagram (with interactive loader + markdown fallback)
- [ ] Executable Python code cells with NumPy / SciPy / Matplotlib
- [ ] Clear visualizations with labeled axes, titles, and legends
- [ ] Proper academic citations with arXiv/DOI links
- [ ] Self-assessment exercises with step-by-step worked solutions
- [ ] Clean headless execution with 0 errors via `nb_tool.py execute`

## 4. Natural Scientific Topology & Sizing (Strict Anti-Toy Invariant)
- **Strict Anti-Toy Rule**: The LLM "Rule of Twos" (defaulting to 2 parts, 2 chapters, 2 sections, 2 subsections) is strictly forbidden. Real scientific domains are rich, nuanced, and uneven.
- **Natural Chapter Sizing**:
  - A chapter must cover a complete, coherent scientific pillar (e.g. "Chapter 3: Spectral Graph Theory & Graph Laplacians" or "Chapter 5: Continuous Normalizing Flows and Neural ODEs").
  - Do NOT artificially split or compress chapters to fit arbitrary counts.
- **Natural Section Sizing**:
  - Every distinct mathematical structure, physical law, operator, or algorithmic family belongs in its own dedicated section.
  - A complex chapter will naturally feature **5 to 12 sections**. Lumping distinct concepts together creates shallow, unreadable notes.
  - An introductory or review chapter may only need 2 to 4 sections.
- **Natural Subsection Sizing (Cognitive Unit of Study)**:
  - Each individual subsection notebook represents **one focused study session** (one coherent mathematical concept, its step-by-step derivation, an executable Python experiment with visualization, and self-assessment exercises).
  - An intricate section (e.g., proving convergence of optimization algorithms) may demand **4 to 8 subsections**, while a self-contained definition needs only 1 or 2.
  - If a topic introduces more than 3 distinct code experiments or 4 major theorems, split it into multiple subsections.
