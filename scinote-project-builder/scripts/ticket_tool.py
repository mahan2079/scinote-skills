#!/usr/bin/env python3
"""
ticket_tool.py - Ticket lifecycle manager for scientific curriculum notes.
Handles ticket creation, frontier queries, status updates, and context propagation.
"""

import sys
import os
import re
import json
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional

def sanitize_slug(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def parse_frontmatter(content: str) -> (Dict[str, Any], str):
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    raw_fm = parts[1].strip()
    body = parts[2]
    meta = {}
    for line in raw_fm.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                meta[key] = [item.strip().strip('"').strip("'") for item in inner.split(",") if item.strip()]
            else:
                meta[key] = val
    return meta, body

def dump_frontmatter(meta: Dict[str, Any], body: str) -> str:
    lines = ["---"]
    for k, v in meta.items():
        if isinstance(v, list):
            items_str = ", ".join(f'"{i}"' for i in v)
            lines.append(f"{k}: [{items_str}]")
        else:
            lines.append(f'{k}: "{v}"')
    lines.append("---")
    return "\n".join(lines) + "\n" + body.lstrip()

def cmd_init_curriculum(args: argparse.Namespace):
    with open(args.spec, "r", encoding="utf-8") as f:
        spec = json.load(f)

    root = os.path.abspath(args.base_dir)
    curriculum_dir = os.path.join(root, "curriculum")
    tickets_dir = os.path.join(root, "tickets")
    notes_dir = os.path.join(root, "notes")
    papers_dir = os.path.join(root, "papers")
    projects_dir = os.path.join(root, "projects")

    for d in [curriculum_dir, tickets_dir, notes_dir, papers_dir, projects_dir]:
        os.makedirs(d, exist_ok=True)

    topic = spec.get("topic", "Scientific Notes")
    level = spec.get("level", "Comprehensive")
    parts = spec.get("parts", [])

    syllabus_lines = [
        f"# Syllabus & Curriculum: {topic}",
        f"\n**Level**: {level}  ",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  ",
        f"**Description**: {spec.get('description', '')}\n",
        "## Table of Contents\n"
    ]

    progress_lines = [
        f"# Progress Tracker: {topic}",
        f"\nLast Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
        "## Roadmap & Completion Checklist\n"
    ]

    all_tickets = []
    prev_ticket_id = None

    for part_idx, part in enumerate(parts, 1):
        part_title = part.get("title", f"Part {part_idx}")
        syllabus_lines.append(f"### Part {part_idx}: {part_title}\n")
        progress_lines.append(f"### Part {part_idx}: {part_title}\n")

        for ch_idx, ch in enumerate(part.get("chapters", []), 1):
            ch_num_str = f"{ch.get('number', ch_idx):02d}"
            ch_title = ch.get("title", f"Chapter {ch_num_str}")
            ch_slug = f"ch{ch_num_str}-{sanitize_slug(ch_title)}"
            
            syllabus_lines.append(f"#### Chapter {ch_num_str}: {ch_title}\n")
            progress_lines.append(f"#### Chapter {ch_num_str}: {ch_title}\n")

            # Create paper and project folder structures
            os.makedirs(os.path.join(papers_dir, ch_slug), exist_ok=True)
            proj_path = os.path.join(projects_dir, ch_slug)
            for subd in ["proposal", "docs", "notes", "src"]:
                os.makedirs(os.path.join(proj_path, subd), exist_ok=True)

            # 1. Paper Ticket
            paper_ticket_id = f"PAPER-{ch_num_str}"
            paper_ticket_file = os.path.join(tickets_dir, f"{paper_ticket_id}.md")
            paper_meta = {
                "id": paper_ticket_id,
                "type": "paper",
                "chapter": ch_num_str,
                "chapter_title": ch_title,
                "title": f"Literature & Key Papers: {ch_title}",
                "status": "pending",
                "blocked_by": [] if prev_ticket_id is None else [prev_ticket_id]
            }
            paper_body = f"""
## Mission
Discover, download, and review complementary scientific papers for Chapter {ch_num_str}: **{ch_title}**.

## Topics to Search
{chr(10).join(f"- {kw}" for kw in ch.get("paper_topics", [ch_title]))}

## Expected Deliverables
1. PDF downloads saved in `papers/{ch_slug}/`
2. Formatted BibTeX bibliography file `papers/{ch_slug}/papers.bib`
3. Comprehensive annotated reading guide in `papers/{ch_slug}/reading-guide.md`

## OpenCode Prompt Card
```bash
scinote-paper-finder tickets/{paper_ticket_id}.md
```
"""
            with open(paper_ticket_file, "w", encoding="utf-8") as pf:
                pf.write(dump_frontmatter(paper_meta, paper_body))
            progress_lines.append(f"- [ ] `tickets/{paper_ticket_id}.md` - Literature Review: {ch_title}")
            all_tickets.append(paper_ticket_id)
            prev_ticket_id = paper_ticket_id

            # 2. Section and Subsection Tickets
            for sec_idx, sec in enumerate(ch.get("sections", []), 1):
                sec_num_str = f"{sec.get('number', sec_idx):02d}"
                sec_title = sec.get("title", f"Section {sec_num_str}")
                sec_slug = f"sec{sec_num_str}-{sanitize_slug(sec_title)}"
                sec_dir = os.path.join(notes_dir, ch_slug, sec_slug)
                os.makedirs(sec_dir, exist_ok=True)

                syllabus_lines.append(f"- **Section {ch_num_str}.{sec_num_str}**: {sec_title}")

                for sub_idx, sub in enumerate(sec.get("subsections", []), 1):
                    sub_num_str = f"{sub.get('number', sub_idx):02d}"
                    sub_title = sub.get("title", f"Subsection {sub_num_str}")
                    sub_slug = f"{sub_num_str}-{sanitize_slug(sub_title)}.ipynb"
                    nb_rel_path = os.path.join("notes", ch_slug, sec_slug, sub_slug)

                    sub_ticket_id = f"SEC-{ch_num_str}-{sec_num_str}-{sub_num_str}"
                    sub_ticket_file = os.path.join(tickets_dir, f"{sub_ticket_id}.md")

                    sub_meta = {
                        "id": sub_ticket_id,
                        "type": "subsection",
                        "chapter": ch_num_str,
                        "chapter_title": ch_title,
                        "section": sec_num_str,
                        "section_title": sec_title,
                        "subsection": sub_num_str,
                        "title": sub_title,
                        "target_notebook": nb_rel_path,
                        "status": "pending",
                        "blocked_by": [prev_ticket_id] if prev_ticket_id else []
                    }

                    checkpoints = sub.get("diagnostic_questions", [
                        f"How comfortable are you with the mathematical foundations required for {sub_title}?",
                        f"Would you prefer this subsection to focus on geometric intuition or formal analytical proofs?"
                    ])

                    sub_body = f"""
## Mission & Learning Objectives
Author a standalone, fully runnable Jupyter notebook covering **{sub_title}**.
Target Path: `{nb_rel_path}`

### Learning Goals
{chr(10).join(f"- {goal}" for goal in sub.get("goals", [f"Master the core concept of {sub_title}", "Understand mathematical derivations from first principles", "Implement numerical experiments in Python"]))}

## Pedagogical Level Checkpoints (HITL)
Before writing, prompt the user with these checkpoints to calibrate explanation depth:
{chr(10).join(f"{i+1}. {q}" for i, q in enumerate(checkpoints))}

## Content Requirements
1. **First-Principles Theory**: Clear pedagogical exposition assuming no unexplained prior jargon.
2. **LaTeX Formulations**: Step-by-step rigorous mathematical definitions and derivations.
3. **Mermaid Flowchart**: Process, state machine, or data flow visualization.
4. **Interactive Code & Plots**: Python code blocks (NumPy, SciPy, Matplotlib) that execute and generate plots.
5. **Citations**: Citations referencing academic literature and papers from `papers/{ch_slug}/papers.bib`.
6. **Self-Assessment Exercises**: Comprehensive conceptual questions and hands-on exercises with worked step-by-step solutions.

## Previous Sections Review
*(Context from previous tickets will be appended here as they are completed)*

## OpenCode Prompt Card
```bash
scinote-section-writer tickets/{sub_ticket_id}.md
```
"""
                    with open(sub_ticket_file, "w", encoding="utf-8") as sf:
                        sf.write(dump_frontmatter(sub_meta, sub_body))

                    syllabus_lines.append(f"  - `{sub_num_str}`: {sub_title} (`{nb_rel_path}`)")
                    progress_lines.append(f"- [ ] `tickets/{sub_ticket_id}.md` - Note: {sub_title}")
                    all_tickets.append(sub_ticket_id)
                    prev_ticket_id = sub_ticket_id

            # 3. Chapter Project Ticket
            proj_ticket_id = f"PROJ-{ch_num_str}"
            proj_ticket_file = os.path.join(tickets_dir, f"{proj_ticket_id}.md")
            proj_meta = {
                "id": proj_ticket_id,
                "type": "project",
                "chapter": ch_num_str,
                "chapter_title": ch_title,
                "title": f"Chapter Project: {ch.get('project_title', ch_title + ' Practical Build')}",
                "project_dir": f"projects/{ch_slug}",
                "status": "pending",
                "blocked_by": [prev_ticket_id] if prev_ticket_id else []
            }
            proj_body = f"""
## Mission
Design, implement, and benchmark the hands-on companion project for Chapter {ch_num_str}: **{ch.get('project_title', ch_title + ' Practical Build')}**.
Project Directory: `projects/{ch_slug}/`

## Structure Requirements
- `proposal/proposal.md`: Formal specification, mathematical formulation, and architecture design.
- `docs/`: Technical guide and API reference.
- `notes/`: Research logs, experiment tracking, and analysis notes.
- `src/`: Production-ready, modular Python code with tests.
- `requirements.txt` / `pyproject.toml` with separate virtual environment.

## OpenCode Prompt Card
```bash
scinote-project-builder tickets/{proj_ticket_id}.md
```
"""
            with open(proj_ticket_file, "w", encoding="utf-8") as proj_f:
                proj_f.write(dump_frontmatter(proj_meta, proj_body))
            progress_lines.append(f"- [ ] `tickets/{proj_ticket_id}.md` - Project: {ch.get('project_title', ch_title + ' Build')}\n")
            all_tickets.append(proj_ticket_id)
            prev_ticket_id = proj_ticket_id

    with open(os.path.join(curriculum_dir, "syllabus.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(syllabus_lines))

    with open(os.path.join(curriculum_dir, "PROGRESS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(progress_lines))

    print(f"Curriculum initialized successfully under {root}:")
    print(f"- Total tickets created: {len(all_tickets)}")
    print(f"- Syllabus: {os.path.join(curriculum_dir, 'syllabus.md')}")
    print(f"- Progress tracker: {os.path.join(curriculum_dir, 'PROGRESS.md')}")
    if all_tickets:
        print(f"\nFirst frontier ticket to execute: tickets/{all_tickets[0]}.md")

def cmd_list(args: argparse.Namespace):
    tickets_dir = os.path.abspath(args.tickets_dir)
    if not os.path.exists(tickets_dir):
        print(f"Directory not found: {tickets_dir}", file=sys.stderr)
        return 1

    files = sorted(os.listdir(tickets_dir))
    tickets = []
    status_map = {}

    for fn in files:
        if not fn.endswith(".md"):
            continue
        p = os.path.join(tickets_dir, fn)
        with open(p, "r", encoding="utf-8") as f:
            meta, _ = parse_frontmatter(f.read())
            t_id = meta.get("id", fn[:-3])
            tickets.append((fn, meta))
            status_map[t_id] = meta.get("status", "pending")

    print(f"{'STATUS':<12} {'TICKET ID':<22} {'TYPE':<12} {'TITLE'}")
    print("-" * 75)

    frontier = []
    for fn, meta in tickets:
        t_id = meta.get("id", fn[:-3])
        status = meta.get("status", "pending")
        t_type = meta.get("type", "unknown")
        title = meta.get("title", "")
        blocked_by = meta.get("blocked_by", [])

        is_unblocked = True
        for blocker in blocked_by:
            if status_map.get(blocker) != "done":
                is_unblocked = False
                break

        status_str = f"[{status.upper()}]"
        if status == "pending" and is_unblocked:
            status_str = "[FRONTIER]"
            frontier.append((t_id, fn, title, t_type))

        print(f"{status_str:<12} {t_id:<22} {t_type:<12} {title}")

    print("\n" + "=" * 75)
    if frontier:
        print(f"Active Frontier ({len(frontier)} ticket(s) ready for execution):")
        for t_id, fn, title, t_type in frontier:
            print(f"  -> {t_id} ({t_type}): {title}")
            print(f"     Run: tickets/{fn}")
    else:
        print("No pending unblocked tickets on the frontier! All done or awaiting dependencies.")

def cmd_resolve(args: argparse.Namespace):
    tickets_dir = os.path.abspath(args.tickets_dir)
    target_id = args.id
    target_file = None

    for fn in os.listdir(tickets_dir):
        if fn.startswith(target_id) and fn.endswith(".md"):
            target_file = os.path.join(tickets_dir, fn)
            break

    if not target_file or not os.path.exists(target_file):
        print(f"Ticket with ID '{target_id}' not found in {tickets_dir}", file=sys.stderr)
        return 1

    with open(target_file, "r", encoding="utf-8") as f:
        meta, body = parse_frontmatter(f.read())

    meta["status"] = "done"
    meta["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    resolution_block = f"\n\n## Resolution Summary\n**Completed**: {meta['completed_at']}\n\n{args.summary.strip()}\n"
    new_target_content = dump_frontmatter(meta, body + resolution_block)

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(new_target_content)

    print(f"Marked {target_id} as DONE.")

    # Update PROGRESS.md
    root = os.path.dirname(tickets_dir)
    progress_file = os.path.join(root, "curriculum", "PROGRESS.md")
    if os.path.exists(progress_file):
        with open(progress_file, "r", encoding="utf-8") as f:
            prog_text = f.read()
        updated_prog = re.sub(
            rf"- \[ \] `tickets/{re.escape(os.path.basename(target_file))}`",
            f"- [x] `tickets/{os.path.basename(target_file)}`",
            prog_text
        )
        with open(progress_file, "w", encoding="utf-8") as f:
            f.write(updated_prog)
        print("Updated curriculum/PROGRESS.md.")

    # Propagate summary to the next ticket blocked by target_id
    propagated_count = 0
    for fn in sorted(os.listdir(tickets_dir)):
        if not fn.endswith(".md"):
            continue
        p = os.path.join(tickets_dir, fn)
        with open(p, "r", encoding="utf-8") as f:
            other_meta, other_body = parse_frontmatter(f.read())
        
        blocked_by = other_meta.get("blocked_by", [])
        if target_id in blocked_by:
            summary_addition = (
                f"\n### Recap from {target_id}: {meta.get('title', '')}\n"
                f"{args.summary.strip()}\n"
            )
            if "## Previous Sections Review" in other_body:
                other_body = other_body.replace(
                    "## Previous Sections Review",
                    f"## Previous Sections Review\n{summary_addition}"
                )
            else:
                other_body += f"\n## Previous Sections Review\n{summary_addition}"

            with open(p, "w", encoding="utf-8") as f:
                f.write(dump_frontmatter(other_meta, other_body))
            propagated_count += 1
            print(f"Propagated review recap into dependent ticket: {other_meta.get('id', fn)}")

    print(f"Resolution complete. Summary propagated to {propagated_count} dependent ticket(s).")

def main():
    parser = argparse.ArgumentParser(description="Ticket manager for scientific notes")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_init = subparsers.add_parser("init-curriculum", help="Initialize curriculum structure and tickets")
    p_init.add_argument("--spec", required=True, help="Path to syllabus specification JSON")
    p_init.add_argument("--base-dir", default=".", help="Root directory for the curriculum")

    p_list = subparsers.add_parser("list", help="List all tickets and current frontier")
    p_list.add_argument("--tickets-dir", default="tickets", help="Path to tickets directory")

    p_resolve = subparsers.add_parser("resolve", help="Mark ticket as done and propagate context")
    p_resolve.add_argument("--id", required=True, help="Ticket ID (e.g. SEC-01-01-01)")
    p_resolve.add_argument("--summary", required=True, help="Executive summary of what was completed")
    p_resolve.add_argument("--tickets-dir", default="tickets", help="Path to tickets directory")

    args = parser.parse_args()

    if args.command == "init-curriculum":
        cmd_init_curriculum(args)
    elif args.command == "list":
        sys.exit(cmd_list(args) or 0)
    elif args.command == "resolve":
        sys.exit(cmd_resolve(args) or 0)

if __name__ == "__main__":
    main()
