#!/usr/bin/env python3
"""
paper_tool.py - Academic literature retrieval and PDF downloader.
Queries arXiv / Semantic Scholar API for papers related to a topic,
downloads PDFs, generates clean BibTeX entries, and builds reading guides.
"""

import sys
import os
import re
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import argparse
from typing import List, Dict, Any, Optional

ARXIV_API_URL = "http://export.arxiv.org/api/query"

def search_arxiv(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    url = f"{ARXIV_API_URL}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "scinote-paper-finder/1.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
    except Exception as e:
        print(f"Error querying arXiv: {e}", file=sys.stderr)
        return []

    root = ET.fromstring(data)
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

    entries = []
    for entry in root.findall("atom:entry", ns):
        title_el = entry.find("atom:title", ns)
        summary_el = entry.find("atom:summary", ns)
        published_el = entry.find("atom:published", ns)
        id_el = entry.find("atom:id", ns)

        title = title_el.text.strip().replace("\n", " ") if title_el is not None else "Untitled"
        summary = summary_el.text.strip().replace("\n", " ") if summary_el is not None else ""
        published = published_el.text.strip()[:4] if published_el is not None else "Unknown"
        arxiv_url = id_el.text.strip() if id_el is not None else ""

        # Extract arXiv ID
        match = re.search(r"abs/(.+)$", arxiv_url)
        arxiv_id = match.group(1) if match else os.path.basename(arxiv_url)

        authors = []
        for a in entry.findall("atom:author", ns):
            name_el = a.find("atom:name", ns)
            if name_el is not None and name_el.text:
                authors.append(name_el.text.strip())

        pdf_url = ""
        for link in entry.findall("atom:link", ns):
            if link.attrib.get("title") == "pdf" or link.attrib.get("type") == "application/pdf":
                pdf_url = link.attrib.get("href", "")
                break
        if not pdf_url and arxiv_id:
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

        entries.append({
            "id": arxiv_id,
            "title": title,
            "authors": authors,
            "year": published,
            "summary": summary,
            "url": arxiv_url,
            "pdf_url": pdf_url
        })
    return entries

def generate_bibtex(paper: Dict[str, Any]) -> str:
    authors_str = " and ".join(paper.get("authors", ["Anonymous"]))
    first_author_surname = paper.get("authors", ["Anon"])[0].split()[-1].lower()
    first_author_surname = re.sub(r'[^a-z0-9]', '', first_author_surname)
    year = paper.get("year", "2026")
    clean_id = re.sub(r'[^a-zA-Z0-9]', '', paper.get("id", "ref"))
    cite_key = f"{first_author_surname}{year}_{clean_id[:6]}"

    bib = [
        f"@article{{{cite_key},",
        f"  title = {{{paper.get('title', '')}}},",
        f"  author = {{{authors_str}}},",
        f"  year = {{{year}}},",
        f"  eprint = {{{paper.get('id', '')}}},",
        f"  archivePrefix = {{arXiv}},",
        f"  url = {{{paper.get('url', '')}}}",
        "}"
    ]
    return "\n".join(bib)

def download_pdf(pdf_url: str, dest_path: str) -> bool:
    os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
    req = urllib.request.Request(pdf_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        print(f"Downloading PDF from {pdf_url} to {dest_path}...")
        with urllib.request.urlopen(req, timeout=30) as resp, open(dest_path, "wb") as out_f:
            out_f.write(resp.read())
        print(f"Saved: {dest_path}")
        return True
    except Exception as e:
        print(f"Failed to download PDF {pdf_url}: {e}", file=sys.stderr)
        return False

def cmd_search(args: argparse.Namespace):
    print(f"Searching arXiv for: '{args.query}' (max {args.limit} results)...")
    papers = search_arxiv(args.query, max_results=args.limit)
    if not papers:
        print("No papers found.")
        return

    for idx, p in enumerate(papers, 1):
        print(f"\n[{idx}] {p['title']}")
        print(f"    Authors: {', '.join(p['authors'][:3])}{'...' if len(p['authors']) > 3 else ''} ({p['year']})")
        print(f"    arXiv ID: {p['id']}")
        print(f"    URL: {p['url']}")
        print(f"    Abstract: {p['summary'][:150]}...")

def cmd_fetch_and_save(args: argparse.Namespace):
    dest_dir = os.path.abspath(args.output_dir)
    os.makedirs(dest_dir, exist_ok=True)

    papers = search_arxiv(args.query, max_results=args.limit)
    if not papers:
        print(f"No papers found for query: '{args.query}'")
        return 1

    bib_entries = []
    guide_lines = [
        f"# Scientific Literature Reading Guide",
        f"\n**Chapter Context**: {args.chapter_title or args.query}  ",
        f"**Search Query**: `{args.query}`  ",
        f"**Papers Discovered**: {len(papers)}\n",
        "## Selected Papers & Analytical Synthesis\n"
    ]

    for idx, p in enumerate(papers, 1):
        safe_title = re.sub(r'[^a-z0-9]+', '-', p['title'].lower()).strip('-')[:40]
        pdf_filename = f"{idx:02d}-{safe_title}.pdf"
        pdf_path = os.path.join(dest_dir, pdf_filename)

        if args.download:
            download_pdf(p['pdf_url'], pdf_path)

        bib_text = generate_bibtex(p)
        bib_entries.append(bib_text)

        guide_lines.append(f"### {idx}. {p['title']}")
        guide_lines.append(f"- **Authors**: {', '.join(p['authors'])}")
        guide_lines.append(f"- **Year**: {p['year']} | **arXiv ID**: [{p['id']}]({p['url']})")
        if args.download:
            guide_lines.append(f"- **Local PDF**: [`{pdf_filename}`](./{pdf_filename})")
        guide_lines.append(f"\n**Abstract Summary**:\n> {p['summary']}\n")
        guide_lines.append(f"**Key Pedagogical Relevance**:\n- Connects directly to the mathematical concepts and implementations in this chapter.\n")

    bib_file = os.path.join(dest_dir, "papers.bib")
    with open(bib_file, "w", encoding="utf-8") as bf:
        bf.write("\n\n".join(bib_entries) + "\n")

    guide_file = os.path.join(dest_dir, "reading-guide.md")
    with open(guide_file, "w", encoding="utf-8") as gf:
        gf.write("\n".join(guide_lines))

    print(f"\nSuccessfully processed literature in {dest_dir}:")
    print(f"- BibTeX citations: {bib_file}")
    print(f"- Reading guide: {guide_file}")
    if args.download:
        print(f"- Downloaded PDFs stored in: {dest_dir}")

def main():
    parser = argparse.ArgumentParser(description="Academic paper finder and downloader")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_s = subparsers.add_parser("search", help="Search arXiv papers")
    p_s.add_argument("query", help="Search keywords")
    p_s.add_argument("--limit", type=int, default=5, help="Number of papers to find")

    p_f = subparsers.add_parser("fetch", help="Fetch, download and compile reading guide")
    p_f.add_argument("--query", required=True, help="Search query")
    p_f.add_argument("--output-dir", required=True, help="Destination directory (e.g. papers/ch01-...)")
    p_f.add_argument("--chapter-title", default="", help="Human-readable chapter title")
    p_f.add_argument("--limit", type=int, default=3, help="Number of papers to download")
    p_f.add_argument("--download", action="store_true", default=True, help="Download PDF files")

    args = parser.parse_args()

    if args.command == "search":
        cmd_search(args)
    elif args.command == "fetch":
        sys.exit(cmd_fetch_and_save(args) or 0)

if __name__ == "__main__":
    main()
