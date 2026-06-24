#!/usr/bin/env python3
"""Scopus literature search via Elsevier Scopus API — Thomas's cartesian approach, optimized.

Differences vs the reference script:
  * API key from env SCOPUS_API_KEY or file `papers/scripts/api_key.txt` (gitignored)
  * Pre-filtered queries: `PUBYEAR > MIN_YEAR AND DOCTYPE(ar OR cp OR re)` — kills editorials/notes
  * Rich metadata captured: DOI, year, citations, venue, first author, Scopus ID, link
  * Dedup by DOI first, then normalized title (catches punctuation variants)
  * Real resume: tracks done queries in `<topic>_done.json` — interrupt-safe
  * Real exponential backoff (2/4/8/16/32 s); 429 also respects Retry-After header if present
  * Ranking: score = n_query_hits + log10(1 + citations)
  * Combined CSV across topics with `topic` column
  * `--mode broad`: single OR-omnia query as cheap sanity check

Usage:
    cd papers
    python3 scripts/scopus_search.py waste                 # 175 queries, cartesian
    python3 scripts/scopus_search.py all                   # waste + asbestos
    python3 scripts/scopus_search.py asbestos --mode broad # 1 broad OR query
    python3 scripts/scopus_search.py all --skip-search     # reprocess existing raw files
    python3 scripts/scopus_search.py waste --min-year 2018 --max-results 200
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

import pandas as pd
import requests

# --------------------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
PAPERS = HERE.parent
OUT = PAPERS / "literature_search"
OUT.mkdir(parents=True, exist_ok=True)
API_KEY_FILE = HERE / "api_key.txt"

API_URL = "https://api.elsevier.com/content/search/scopus"
REQUEST_TIMEOUT = 30
SLEEP_BETWEEN_QUERIES = 0.2
MAX_RETRIES = 5
BACKOFF_BASE = 2.0
DEFAULT_MIN_YEAR = 2015
DEFAULT_MAX_RESULTS = 25
DOCTYPES = ["ar", "cp", "re"]                                # article, conf paper, review

SOURCE = [
    "remote sensing",
    "satellite imagery",
    "aerial imagery",
    "multispectral",
    "hyperspectral",
    "UAV",
    "VHR",
]

TOPICS: dict[str, dict[str, list[str]]] = {
    "waste": {
        "SUBJECT": [
            "illegal waste",
            "landfill",
            "dumping site",
            "solid waste",
            "waste detection",
        ],
        "TASK": [
            "detection",
            "classification",
            "segmentation",
            "mapping",
            "monitoring",
        ],
    },
    "asbestos": {
        "SUBJECT": [
            "asbestos",
            "asbestos cement",
            "asbestos roof",
            "cemento amianto",
            "eternit",
        ],
        "TASK": [
            "detection",
            "mapping",
            "identification",
            "spectral signature",
            "classification",
        ],
    },
}

# --------------------------------------------------------------------------------------
def load_api_key() -> str:
    key = os.environ.get("SCOPUS_API_KEY", "").strip()
    if key:
        return key
    if API_KEY_FILE.exists():
        key = API_KEY_FILE.read_text().strip()
        if key:
            return key
    sys.exit(f"ERROR: no Scopus API key. Set SCOPUS_API_KEY or write to {API_KEY_FILE}")


def filter_suffix(min_year: int) -> str:
    """Tail of the TITLE-ABS-KEY query: year + doctype filters."""
    doctype = " OR ".join(f"DOCTYPE({d})" for d in DOCTYPES)
    return f" AND PUBYEAR > {min_year - 1} AND ( {doctype} )"


def build_cartesian_query(src: str, subj: str, task: str, min_year: int) -> str:
    return f'TITLE-ABS-KEY ( "{src}" AND "{subj}" AND "{task}" ){filter_suffix(min_year)}'


def build_broad_query(topic: str, min_year: int) -> str:
    """OR-everything query — one shot, returns top-relevance papers across the keyword space."""
    profile = TOPICS[topic]
    src_or = " OR ".join(f'"{s}"' for s in SOURCE)
    subj_or = " OR ".join(f'"{s}"' for s in profile["SUBJECT"])
    task_or = " OR ".join(f'"{s}"' for s in profile["TASK"])
    return (
        f"TITLE-ABS-KEY ( ( {src_or} ) AND ( {subj_or} ) AND ( {task_or} ) )"
        + filter_suffix(min_year)
    )


# --------------------------------------------------------------------------------------
def safe_request(params: dict) -> dict | None:
    for attempt in range(MAX_RETRIES):
        try:
            res = requests.get(API_URL, params=params, timeout=REQUEST_TIMEOUT)
        except requests.RequestException as e:
            wait = BACKOFF_BASE * (2 ** attempt)
            print(f"    network error ({type(e).__name__}); retry in {wait:.0f}s")
            time.sleep(wait)
            continue

        if res.status_code == 429:
            retry_after = res.headers.get("Retry-After")
            wait = float(retry_after) if retry_after else BACKOFF_BASE * (2 ** attempt)
            print(f"    rate limited; sleeping {wait:.0f}s")
            time.sleep(wait)
            continue

        if res.status_code != 200:
            print(f"    HTTP {res.status_code}: {res.text[:200]}")
            return None

        try:
            data = res.json()
        except ValueError:
            print(f"    non-JSON response: {res.text[:200]}")
            return None

        if "search-results" not in data:
            print(f"    unexpected payload: {str(data)[:200]}")
            return None
        return data

    print(f"    giving up after {MAX_RETRIES} retries")
    return None


def extract_entry(entry: dict) -> dict:
    """Pull the fields we care about from a STANDARD-view Scopus entry."""
    cov = entry.get("prism:coverDate", "")
    year = ""
    if cov and re.match(r"^\d{4}", cov):
        year = cov[:4]
    cited = entry.get("citedby-count", "")
    try:
        cited_n = int(cited) if cited != "" else 0
    except ValueError:
        cited_n = 0
    return {
        "title": entry.get("dc:title", "") or "",
        "doi": entry.get("prism:doi", "") or "",
        "year": year,
        "venue": entry.get("prism:publicationName", "") or "",
        "first_author": entry.get("dc:creator", "") or "",
        "citations": cited_n,
        "scopus_id": entry.get("dc:identifier", "") or "",
        "type": entry.get("subtypeDescription", "") or "",
        "open_access": entry.get("openaccessFlag", False),
    }


# --------------------------------------------------------------------------------------
def normalize_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def dedup_key(row: dict) -> str:
    doi = (row.get("doi") or "").strip().lower()
    if doi:
        return f"doi:{doi}"
    return f"title:{normalize_title(row.get('title', ''))}"


# --------------------------------------------------------------------------------------
def search_topic_cartesian(topic: str, api_key: str, max_results: int, min_year: int) -> None:
    profile = TOPICS[topic]
    queries = list(itertools.product(SOURCE, profile["SUBJECT"], profile["TASK"]))
    n_queries = len(queries)

    raw_path = OUT / f"{topic}_raw.json"
    done_path = OUT / f"{topic}_done.json"

    raw_rows: list[dict] = json.loads(raw_path.read_text()) if raw_path.exists() else []
    done_set: set[str] = set(json.loads(done_path.read_text())) if done_path.exists() else set()
    if done_set:
        print(f"[{topic}] resuming — {len(done_set)}/{n_queries} queries already done")

    base_params = {
        "httpAccept": "application/json",
        "count": max_results,
        "apiKey": api_key,
        "sort": "relevancy",
        "view": "STANDARD",
    }

    start_time = time.time()
    for idx, (src, subj, task) in enumerate(queries, start=1):
        qkey = f"{src}|{subj}|{task}"
        if qkey in done_set:
            continue

        params = dict(base_params)
        params["start"] = 0
        params["query"] = build_cartesian_query(src, subj, task, min_year)

        total_results = 0
        n_titles_this_query = 0
        first_pass = True
        while first_pass or params["start"] < total_results:
            first_pass = False
            data = safe_request(params)
            if data is None:
                break
            total_results = int(data["search-results"].get("opensearch:totalResults", 0))
            for entry in data["search-results"].get("entry", []) or []:
                row = extract_entry(entry)
                if not row["title"]:
                    continue
                row.update({"source": src, "subject": subj, "task": task})
                raw_rows.append(row)
                n_titles_this_query += 1
            params["start"] += params["count"]
            time.sleep(SLEEP_BETWEEN_QUERIES)

        done_set.add(qkey)
        elapsed = time.time() - start_time
        done_count = idx - sum(1 for q in queries[:idx] if f"{q[0]}|{q[1]}|{q[2]}" not in done_set)
        # ETA based on this-session-only progress
        avg_per_query = elapsed / max(1, idx - (len(done_set) - 1 - done_count))
        remaining = sum(1 for q in queries[idx:] if f"{q[0]}|{q[1]}|{q[2]}" not in done_set)
        eta_min = (remaining * avg_per_query) / 60
        print(
            f"  [{idx:>3}/{n_queries}] total={total_results:>4}  new_rows={n_titles_this_query:>3}  "
            f"ETA={eta_min:>4.1f} min  ({src} × {subj} × {task})"
        )

        # checkpoint every 10 queries (interrupt-safe resume)
        if idx % 10 == 0:
            raw_path.write_text(json.dumps(raw_rows, indent=2, ensure_ascii=False))
            done_path.write_text(json.dumps(sorted(done_set), indent=2, ensure_ascii=False))

    # final flush
    raw_path.write_text(json.dumps(raw_rows, indent=2, ensure_ascii=False))
    done_path.write_text(json.dumps(sorted(done_set), indent=2, ensure_ascii=False))
    print(f"\n[{topic}] saved {len(raw_rows)} raw rows → {raw_path.relative_to(PAPERS)}")


def search_topic_broad(topic: str, api_key: str, max_results: int, min_year: int) -> None:
    raw_path = OUT / f"{topic}_broad_raw.json"
    params = {
        "httpAccept": "application/json",
        "count": max_results,
        "apiKey": api_key,
        "sort": "relevancy",
        "view": "STANDARD",
        "start": 0,
        "query": build_broad_query(topic, min_year),
    }
    print(f"[{topic}] broad query: {params['query'][:200]}...")

    rows: list[dict] = []
    total_results = 0
    first_pass = True
    while first_pass or params["start"] < total_results:
        first_pass = False
        data = safe_request(params)
        if data is None:
            break
        total_results = int(data["search-results"].get("opensearch:totalResults", 0))
        for entry in data["search-results"].get("entry", []) or []:
            row = extract_entry(entry)
            if row["title"]:
                row.update({"source": "(broad)", "subject": "(broad)", "task": "(broad)"})
                rows.append(row)
        params["start"] += params["count"]
        time.sleep(SLEEP_BETWEEN_QUERIES)
        print(f"  pagination: {len(rows)}/{total_results} so far")

    raw_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    print(f"[{topic}] broad: {total_results} total, {len(rows)} pulled → {raw_path.relative_to(PAPERS)}")


# --------------------------------------------------------------------------------------
def process_topic(topic: str, broad: bool = False) -> pd.DataFrame | None:
    suffix = "_broad" if broad else ""
    raw_path = OUT / f"{topic}{suffix}_raw.json"
    if not raw_path.exists():
        print(f"[{topic}] no raw file ({raw_path.name}) — skip processing")
        return None

    rows = json.loads(raw_path.read_text())
    if not rows:
        print(f"[{topic}] empty raw, skip")
        return None

    # group by dedup key
    grouped: dict[str, dict] = {}
    for r in rows:
        k = dedup_key(r)
        if k not in grouped:
            grouped[k] = {
                "title": r["title"],
                "doi": r.get("doi", ""),
                "year": r.get("year", ""),
                "venue": r.get("venue", ""),
                "first_author": r.get("first_author", ""),
                "citations": r.get("citations", 0),
                "scopus_id": r.get("scopus_id", ""),
                "type": r.get("type", ""),
                "open_access": r.get("open_access", False),
                "sources": set(),
                "subjects": set(),
                "tasks": set(),
            }
        # citations: keep max seen
        grouped[k]["citations"] = max(grouped[k]["citations"], r.get("citations", 0))
        grouped[k]["sources"].add(r["source"])
        grouped[k]["subjects"].add(r["subject"])
        grouped[k]["tasks"].add(r["task"])

    unique = []
    for v in grouped.values():
        n_hits = len(v["sources"]) * len(v["subjects"]) * len(v["tasks"])
        score = n_hits + math.log10(1 + v["citations"])
        unique.append(
            {
                "title": v["title"],
                "doi": v["doi"],
                "year": v["year"],
                "venue": v["venue"],
                "first_author": v["first_author"],
                "citations": v["citations"],
                "type": v["type"],
                "open_access": v["open_access"],
                "scopus_id": v["scopus_id"],
                "sources": sorted(v["sources"]),
                "subjects": sorted(v["subjects"]),
                "tasks": sorted(v["tasks"]),
                "n_query_hits": n_hits,
                "score": round(score, 3),
                "topic": topic,
            }
        )
    unique.sort(key=lambda p: p["score"], reverse=True)

    json_path = OUT / f"{topic}{suffix}_unique.json"
    json_path.write_text(json.dumps(unique, indent=2, ensure_ascii=False))

    df = pd.DataFrame(
        [
            {
                "topic": p["topic"],
                "score": p["score"],
                "citations": p["citations"],
                "year": p["year"],
                "title": p["title"],
                "first_author": p["first_author"],
                "venue": p["venue"],
                "doi": p["doi"],
                "type": p["type"],
                "open_access": p["open_access"],
                "n_query_hits": p["n_query_hits"],
                "sources": "; ".join(p["sources"]),
                "subjects": "; ".join(p["subjects"]),
                "tasks": "; ".join(p["tasks"]),
                "scopus_id": p["scopus_id"],
            }
            for p in unique
        ]
    )
    csv_path = OUT / f"{topic}{suffix}_unique.csv"
    df.to_csv(csv_path, index=False)

    print(f"\n[{topic}{suffix}] {len(rows)} raw → {len(unique)} unique papers")
    print(f"[{topic}{suffix}] saved → {json_path.name} + {csv_path.name}")

    if not broad and rows:
        all_sources = [r["source"] for r in rows]
        all_subjects = [r["subject"] for r in rows]
        all_tasks = [r["task"] for r in rows]
        print(f"[{topic}] hit-counts per axis (raw rows):")
        print(f"  SOURCE:  {dict(Counter(all_sources).most_common())}")
        print(f"  SUBJECT: {dict(Counter(all_subjects).most_common())}")
        print(f"  TASK:    {dict(Counter(all_tasks).most_common())}")

    return df


def write_combined(dfs: list[pd.DataFrame]) -> None:
    dfs = [d for d in dfs if d is not None and not d.empty]
    if not dfs:
        return
    combined = pd.concat(dfs, ignore_index=True).sort_values("score", ascending=False)
    out_csv = OUT / "combined_unique.csv"
    combined.to_csv(out_csv, index=False)
    print(f"\n[combined] {len(combined)} rows across {len(dfs)} topic(s) → {out_csv.name}")


# --------------------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("topic", choices=["waste", "asbestos", "all"])
    parser.add_argument("--mode", choices=["cartesian", "broad"], default="cartesian",
                        help="cartesian = SOURCE × SUBJECT × TASK (rigorous, ~175 q); broad = single OR query")
    parser.add_argument("--max-results", type=int, default=DEFAULT_MAX_RESULTS,
                        help="results per request (25 public, 200 Polimi)")
    parser.add_argument("--min-year", type=int, default=DEFAULT_MIN_YEAR,
                        help="filter PUBYEAR >= this")
    parser.add_argument("--skip-search", action="store_true",
                        help="reprocess existing raw files without hitting the API")
    args = parser.parse_args()

    api_key = load_api_key()
    targets = ["waste", "asbestos"] if args.topic == "all" else [args.topic]

    dfs = []
    for t in targets:
        if not args.skip_search:
            if args.mode == "broad":
                search_topic_broad(t, api_key, args.max_results, args.min_year)
            else:
                search_topic_cartesian(t, api_key, args.max_results, args.min_year)
        df = process_topic(t, broad=(args.mode == "broad"))
        dfs.append(df)
    write_combined(dfs)


if __name__ == "__main__":
    main()
