# papers/scripts/

Scopus literature-search tool, adapted from Thomas Martinoli's reference script.

## Setup

1. API key — already saved in `api_key.txt` (gitignored). To rotate, replace its content with a new key from https://dev.elsevier.com/apikey/manage, or export `SCOPUS_API_KEY=...` (env var wins over file).
2. Dependencies: `pip install requests pandas` (already in `waste/`'s env if you reuse it).

## Usage

```bash
cd papers
python3 scripts/scopus_search.py waste             # only waste filone (140 queries)
python3 scripts/scopus_search.py asbestos          # only asbestos filone (175 queries)
python3 scripts/scopus_search.py all               # both

python3 scripts/scopus_search.py waste --max-results 200    # Polimi network
python3 scripts/scopus_search.py waste --skip-search        # only reprocess raw JSON to CSV
```

## Outputs (`papers/literature_search/`)

| File | Content |
|---|---|
| `<topic>_raw.json` | Every (query, title) hit — one row per (paper × matching query) |
| `<topic>_unique.json` | Deduplicated by normalized title, with merged source/subject/task lists |
| `<topic>_unique.csv` | Same as above, flattened — open in Excel/pandas |

## Profiles

Defined in `scopus_search.py`:

- **waste** — 7 SOURCE × 5 SUBJECT × 5 TASK = 175 queries
  - SUBJECT: illegal waste, landfill, dumping site, solid waste, waste detection
  - TASK: detection, classification, segmentation, mapping, monitoring
- **asbestos** — 7 SOURCE × 5 SUBJECT × 5 TASK = 175 queries
  - SUBJECT: asbestos, asbestos cement, asbestos roof, cemento amianto, eternit
  - TASK: detection, mapping, identification, spectral signature, classification
- Shared SOURCE: remote sensing, satellite imagery, aerial imagery, multispectral, hyperspectral, UAV, VHR

Tune the lists at the top of the script before running.

## Notes

- Sort is `relevancy` so the top hits are most-cited / best-matched per query — useful on public-network tier (25 results/req).
- Rate limit: ~5 req/s; `429` triggers exponential backoff (2/4/8/16/32 s).
- The script resumes: if `<topic>_raw.json` already exists, new rows are appended. Delete the file to start fresh.
- Quota: 20,000 results/week on the standard key — both topics combined typically stay under 10k.
