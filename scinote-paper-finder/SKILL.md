---
name: scinote-paper-finder
description: "Discover, download, and synthesize scientific papers for a chapter paper ticket. Queries arXiv/Semantic Scholar, downloads official PDFs into papers/chXX/, generates clean BibTeX citations, and authors an in-depth analytical reading guide."
category: development
risk: safe
source: self
author: OpenCode Scientific Suite
tags:
  - research
  - arxiv
  - literature-review
  - bibtex
  - pdf-download
tools:
  - opencode
  - question
  - shell
  - write
  - read
  - websearch
  - webfetch
---

# Scinote Paper Finder

Discover and curate complementary academic literature for any chapter paper ticket, downloading PDFs and building deep pedagogical reading guides.

## When to Use

- Use when working on a `tickets/PAPER-XX.md` ticket.
- Trigger when the user requests finding, downloading, or analyzing scientific papers for a curriculum chapter.
- Can be invoked in a fresh OpenCode chat session.

---

## Operating Invariants

1. **HITL Literature Preference**: Use the `question` tool to ask if the user prefers foundational breakthrough papers (classic citations) or recent state-of-the-art preprints.
2. **Download Physical PDFs**: Always download actual PDF files into `papers/chXX-<slug>/` so the user has offline access to the primary sources.
3. **BibTeX Standardization**: Always generate or update `papers/chXX-<slug>/papers.bib` with standardized citation keys for use in subsection notebooks.
4. **Analytical Reading Guide**: Never output just a list of abstracts. The `reading-guide.md` must provide deep mathematical synthesis, explaining how each paper connects to the chapter's concepts and practical project.

---

## Step-by-Step Procedure

### Step 1: Read the Paper Ticket
Read `tickets/PAPER-XX.md` to retrieve:
- Chapter number and title
- Suggested search keywords
- Destination directory `papers/chXX-<slug>/`

### Step 2: HITL Preference Check
Ask the user via the `question` tool:
- Foundational classic papers (established consensus, seminal proofs)
- Modern state-of-the-art advances (latest preprints, empirical breakthroughs)
- Balanced mix (1 classic foundation + 2 recent developments)

### Step 3: Search and Download via `paper_tool.py`
Run `paper_tool.py fetch` with the chapter topics:
```bash
python3 /home/mahan/Work/scinote-skills/scripts/paper_tool.py fetch \
  --query "<search_query>" \
  --output-dir "papers/chXX-<slug>" \
  --chapter-title "<chapter_title>" \
  --limit 3 \
  --download
```

If specific additional papers are needed, use `websearch` and `paper_tool.py` to retrieve them directly.

### Step 4: Expand the Analytical Reading Guide
Read the generated `papers/chXX-<slug>/reading-guide.md` and enrich it with:
1. **Mathematical Bridge**: How the notation in the papers maps to the notation in your chapter notes.
2. **Key Theorems**: Step-by-step breakdown of the core theorems, loss functions, or experimental proofs from the papers.
3. **Implementation Hooks**: Specific algorithms or techniques from the papers that can be incorporated into the chapter's practical project.
4. **Critical Discussion Questions**: 3 probing questions challenging the assumptions, scalability, or limitations of the papers.

### Step 5: Resolve the Ticket
Execute `ticket_tool.py resolve`:
```bash
python3 /home/mahan/Work/scinote-skills/scripts/ticket_tool.py resolve \
  --id "PAPER-XX" \
  --summary "Discovered and downloaded 3 papers on <topics>. Generated papers.bib and synthesized reading-guide.md with notation bridges and project implementation hooks." \
  --tickets-dir tickets
```
Print confirmation and prompt for the next ticket.
