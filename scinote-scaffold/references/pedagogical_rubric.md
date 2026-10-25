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
- [ ] 2 Self-assessment questions with expandable/worked answers
- [ ] Clean headless execution with 0 errors via `nb_tool.py execute`

## 4. Variable Topology: Dynamic Chapter, Section & Subsection Sizing
- **No Uniformity Enforced**: Never force a rigid count of sections (e.g. 2 per chapter) or subsections (e.g. 2 per section).
- **Topic-Driven Granularity**:
  - Foundational, sprawling, or mathematically dense chapters should have as many sections as needed (e.g., 5 to 12+ sections).
  - Compact, review, or introductory chapters may only need 2 or 3 sections.
  - Similarly, an intricate section (e.g., proving convergence of optimization algorithms) may demand 4 to 8 subsections, while a self-contained concept needs only 1.
- **Cognitive Sizing**: Each individual subsection notebook should represent approximately one focused study session (one coherent concept, its derivation, a code experiment, and exercises). If a topic requires more than 3 distinct code experiments or 4 major theorems, split it into multiple subsections.
