#!/usr/bin/env python3
"""
One-shot bootstrap: reads SOTA_DLxSAT.xlsx, builds canonical paper records
with stable kebab-case IDs, creates notes/<id>.md sidecar per paper,
renames already-downloaded PDFs into library/<id>.pdf.

Idempotent: re-running preserves existing note content (only updates frontmatter
header), and won't re-rename PDFs already in library/.
"""
from __future__ import annotations
import json
import re
import shutil
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent  # papers/
EXCEL = ROOT / "SOTA_DLxSAT.xlsx"
LIBRARY = ROOT / "library"
NOTES = ROOT / "notes"

# Manual ID + author + tags + relevance mapping for the 26 curated Excel entries.
# Keyed by the Excel row's title prefix (first ~50 chars, lowercased) for stable matching.
# This is one-time curation — addresses inferred from prior work and READING_LIST.
EXCEL_MAP = {
    "a deep learning pipeline for solid waste detection": {
        "id": "gibellini-2025-pipeline",
        "authors": ["Gibellini", "Torres", "Fraternali"],
        "venue": "Waste Management Bulletin",
        "doi": "10.1016/j.wmb.2025.100246",
        "arxiv": "2502.06607",
        "tags": ["waste", "baseline", "swin-t", "rsp", "aerialwaste"],
        "relevance": "critical",
        "existing_pdf": "gibellini_2025_waste_pipeline.pdf",
        "in_slides": ["baseline", "approach"],
    },
    "solid waste detection, monitoring and mapping in remote sensing": {
        "id": "fraternali-2024-survey",
        "authors": ["Fraternali", "Castelli", "Torres"],
        "venue": "arXiv",
        "doi": None,
        "arxiv": "2402.09066",
        "tags": ["waste", "survey", "gap-analysis"],
        "relevance": "critical",
        "existing_pdf": "fraternali_2024_waste_survey.pdf",
        "in_slides": ["gap-analysis", "intro"],
    },
    "aerialwaste: a dataset for illegal landfill discovery": {
        "id": "torres-2023-aerialwaste",
        "authors": ["Torres", "Fraternali"],
        "venue": "Scientific Data",
        "doi": "10.1038/s41597-023-01976-9",
        "arxiv": None,
        "tags": ["waste", "dataset", "aerialwaste"],
        "relevance": "critical",
        "existing_pdf": "torres_2023_aerialwaste.pdf",
        "in_slides": ["dataset"],
    },
    "revisiting pre-trained remote sensing model benchmarks": {
        "id": "corley-2024-resizing",
        "authors": ["Corley", "et al."],
        "venue": "arXiv",
        "doi": None,
        "arxiv": "2305.13456",
        "tags": ["foundation-model", "benchmark", "normalization"],
        "relevance": "high",
        "existing_pdf": "corley_2024_resizing_normalization.pdf",
        "in_slides": [],
    },
    "satmae: pre-training transformers for temporal and multi-spectral": {
        "id": "cong-2022-satmae",
        "authors": ["Cong", "et al."],
        "venue": "NeurIPS",
        "doi": None,
        "arxiv": "2207.08051",
        "tags": ["foundation-model", "multispectral", "pretraining"],
        "relevance": "high",
        "existing_pdf": None,
        "in_slides": ["foundation-models"],
    },
    "prithvi-eo-2.0": {
        "id": "szwarcman-2024-prithvi-eo2",
        "authors": ["Szwarcman", "et al."],
        "venue": "arXiv",
        "doi": None,
        "arxiv": "2412.02732",
        "tags": ["foundation-model", "nasa-ibm", "multi-temporal"],
        "relevance": "high",
        "existing_pdf": "szwarcman_2024_prithvi_eo2.pdf",
        "in_slides": ["foundation-models"],
    },
    "neural plasticity-inspired foundation model for observing the earth": {
        "id": "xiong-2024-dofa",
        "authors": ["Xiong", "et al."],
        "venue": "arXiv",
        "doi": None,
        "arxiv": "2403.15356",
        "tags": ["foundation-model", "dofa", "cross-modal", "any-bands"],
        "relevance": "critical",
        "existing_pdf": "xiong_2024_dofa.pdf",
        "in_slides": ["foundation-models", "approach"],
    },
    "ssl4eo-s12": {
        "id": "wang-2023-ssl4eo-s12",
        "authors": ["Wang", "et al."],
        "venue": "arXiv",
        "doi": None,
        "arxiv": "2211.07044",
        "tags": ["foundation-model", "ssl", "sentinel-1-2"],
        "relevance": "high",
        "existing_pdf": None,
        "in_slides": ["foundation-models"],
    },
    "softcon": {
        "id": "wang-2024-softcon",
        "authors": ["Wang", "et al."],
        "venue": "arXiv",
        "doi": None,
        "arxiv": "2405.20462",
        "tags": ["foundation-model", "contrastive", "multilabel"],
        "relevance": "high",
        "existing_pdf": "wang_2024_softcon.pdf",
        "in_slides": ["foundation-models"],
    },
    "critical wavelengths for construction and demolition": {
        "id": "cdw-2025-critical-wavelengths",
        "authors": ["(unknown)"],
        "venue": "arXiv",
        "doi": None,
        "arxiv": "2501.02239",
        "tags": ["construction-demolition", "wavelengths", "materials"],
        "relevance": "medium",
        "existing_pdf": None,
        "in_slides": [],
    },
    "mapping terrestrial macroplastics and polymer-coated materials": {
        "id": "aguilar-2025-macroplastics-wv3",
        "authors": ["Aguilar", "Sousa", "Uhrin", "Gudino-Elizondo", "Biggs"],
        "venue": "Environmental Monitoring and Assessment",
        "doi": "10.1007/s10661-025-14125-z",
        "arxiv": None,
        "tags": ["wv-3", "swir", "plastic", "high-resolution", "high-res-survey"],
        "relevance": "high",
        "existing_pdf": None,
        "in_slides": ["high-res-survey"],
        "relates_to": ["ndpi-2020-wv3", "tasseron-2021-plastic-classifier"],
    },
    "spectralwaste": {
        "id": "spectralwaste-2024-dataset",
        "authors": ["(unknown)"],
        "venue": "arXiv",
        "doi": None,
        "arxiv": "2403.18033",
        "tags": ["waste", "dataset", "hyperspectral", "sorting"],
        "relevance": "medium",
        "existing_pdf": None,
        "in_slides": [],
    },
    # marrocco-2024-microdumps: REMOVED 2026-05-25 (user: "chi se ne frega, non serve")

    # --- ASBESTOS / ABLATION anchors added 2026-05-25 ---
    "detection of asbestos-based cement rooftops in conflict-affected": {
        "id": "shepherd-2025-asbestos-enmap",
        "authors": ["Shepherd", "Sagi", "Zagron", "Aharoni-Mack", "et al."],
        "venue": "Scientific Reports",
        "doi": "10.1038/s41598-025-09738-w",
        "arxiv": None,
        "tags": ["asbestos", "enmap", "hyperspectral", "satellite", "sam", "low-res-survey"],
        "relevance": "critical",
        "existing_pdf": None,
        "in_slides": ["low-res-survey", "asbestos-anchor"],
        "relates_to": ["cilia-2015-ac-weathering", "bonifazi-2026-ac-python"],
    },
    "mapping of asbestos cement roofs and their weathering": {
        "id": "cilia-2015-ac-weathering",
        "authors": ["Cilia", "Panigada", "Rossini", "Candiani", "Pepe", "Colombo"],
        "venue": "ISPRS Int. J. Geo-Information",
        "doi": "10.3390/ijgi4020928",
        "arxiv": None,
        "tags": ["asbestos", "hyperspectral", "mivis", "sam", "weathering", "italian"],
        "relevance": "high",
        "existing_pdf": None,
        "in_slides": ["asbestos-anchor"],
        "relates_to": ["shepherd-2025-asbestos-enmap", "bonifazi-2026-ac-python"],
    },
    "a python-based workflow for asbestos roof mapping": {
        "id": "bonifazi-2026-ac-python",
        "authors": ["Bonifazi", "Aurigemma", "Salas-Cáceres", "Lorenzo-Navarro", "Serranti", "Paglietti", "Bellagamba", "Malinconico"],
        "venue": "Geomatics",
        "doi": "10.3390/geomatics6030041",
        "arxiv": None,
        "tags": ["asbestos", "wv-3", "vnir", "swir", "python", "open-source", "multi-temporal", "italian"],
        "relevance": "critical",
        "existing_pdf": None,
        "in_slides": ["asbestos-anchor", "high-res-survey"],
        "relates_to": ["cilia-2015-ac-weathering", "aguilar-2021-wv3-ablation"],
    },
    "evaluation of object-based greenhouse mapping using worldview-3": {
        "id": "aguilar-2021-wv3-ablation",
        "authors": ["Aguilar", "Jiménez-Lao", "Aguilar"],
        "venue": "Remote Sensing",
        "doi": "10.3390/rs13112133",
        "arxiv": None,
        "tags": ["wv-3", "vnir", "swir", "ablation", "obia", "ndpi", "methodology-canonical"],
        "relevance": "critical",
        "existing_pdf": None,
        "in_slides": ["approach", "high-res-survey"],
        "notes": "Material = plastic greenhouses, NOT asbestos. But the VNIR vs SWIR vs All-Features ablation methodology (90.85/96.79/97.38 OA) is THE canonical benchmark for 'spectral added value on WV-3'. Cite as methodological precedent in the thesis approach slide.",
        "relates_to": ["ndpi-2020-wv3", "aguilar-2025-macroplastics-wv3"],
    },
    "waste detection and change analysis based on multispectral": {
        "id": "tisza-2023-waste-change",
        "authors": ["(Hungarian Tisza team)"],
        "venue": "arXiv",
        "doi": None,
        "arxiv": "2303.14521",
        "tags": ["waste", "change-detection", "multispectral", "sentinel-2", "planetscope"],
        "relevance": "medium",
        "existing_pdf": None,
        "in_slides": [],
    },
    "foundation models for remote sensing and earth observation": {
        "id": "fm-rs-survey-2024",
        "authors": ["(unknown)"],
        "venue": "arXiv",
        "doi": None,
        "arxiv": "2410.16602",
        "tags": ["foundation-model", "survey", "earth-observation"],
        "relevance": "high",
        "existing_pdf": None,
        "in_slides": ["foundation-models"],
    },
    "mapping plastic materials in an urban area": {
        "id": "guo-li-2020-ndpi-wv3",
        "authors": ["Guo", "Li"],
        "venue": "ISPRS J. Photogr. & Remote Sensing",
        "doi": "10.1016/j.isprsjprs.2020.09.009",  # CORRECTED 2026-05-25: was 08.027 (Hovi-photon-tree, wrong paper)
        "arxiv": None,
        "tags": ["wv-3", "swir", "plastic", "spectral-index", "urban", "ndpi"],
        "relevance": "high",
        "existing_pdf": None,
        "in_slides": ["high-res-survey"],
        "notes": "DOI corrected 2026-05-25: previous DOI 10.1016/j.isprsjprs.2020.08.027 was Hovi et al. photon-recollision (wrong paper). True NDPI = Guo & Li 2020, ISPRS JPRS 169:214-226. Elsevier closed access — VPN PoliMi required.",
        "relates_to": ["aguilar-2025-macroplastics-wv3", "zhou-2021-plastic-classifier"],
    },
    "deflect: parameter-efficient adaptation of geospatial": {
        "id": "thoreau-2025-deflect",
        "authors": ["Thoreau", "Marsocci", "Derksen"],
        "venue": "ICCV 2025",
        "doi": None,
        "arxiv": "2503.09493",
        "tags": ["vit", "parameter-efficient", "multispectral-adapter", "geospatial-fm", "peft"],
        "relevance": "medium",
        "existing_pdf": None,
        "in_slides": [],
        "relates_to": ["xiong-2024-dofa", "szwarcman-2024-prithvi-eo2"],
    },
    # fusionsort-2025: REMOVED 2026-05-25 (user: "ignoriamo fusionsort", primary source non trovato)
    "anysat: an earth observation model for any resolutions": {
        "id": "anysat-2024",
        "authors": ["Astruc", "et al."],
        "venue": "arXiv",
        "doi": None,
        "arxiv": "2412.14123",
        "tags": ["foundation-model", "any-resolution", "any-modality"],
        "relevance": "high",
        "existing_pdf": None,
        "in_slides": ["foundation-models"],
    },
    "spectralgpt: spectral remote sensing foundation model": {
        "id": "spectralgpt-2024",
        "authors": ["Hong", "et al."],
        "venue": "TPAMI",
        "doi": None,
        "arxiv": "2311.07113",
        "tags": ["foundation-model", "spectral", "transformer"],
        "relevance": "high",
        "existing_pdf": None,
        "in_slides": ["foundation-models"],
    },
    "marida": {
        "id": "marida-2022-marine-debris",
        "authors": ["Kikaki", "et al."],
        "venue": "PLOS ONE",
        "doi": "10.1371/journal.pone.0262247",
        "arxiv": None,
        "tags": ["marine-debris", "sentinel-2", "benchmark", "low-res-survey"],
        "relevance": "high",
        "existing_pdf": None,
        "in_slides": ["low-res-survey"],
    },
    "global-scale detection of plastic from space with the emit": {
        "id": "emit-2025-plastic",
        "authors": ["(unknown)"],
        "venue": "Geophys. Res. Lett.",
        "doi": "10.1029/2024GL112416",
        "arxiv": None,
        "tags": ["plastic", "hyperspectral", "emit", "global-scale"],
        "relevance": "high",
        "existing_pdf": None,
        "in_slides": ["high-res-survey"],
    },
    "revealing influencing factors on global waste distribution": {
        "id": "global-dumpsites-2023",
        "authors": ["(unknown)"],
        "venue": "Nature Comms",
        "doi": "10.1038/s41467-023-37136-1",
        "arxiv": None,
        "tags": ["waste", "global", "deep-learning", "dumpsites"],
        "relevance": "high",
        "existing_pdf": None,
        "in_slides": ["low-res-survey"],
    },
    "hyperspectral uv to swir characteristics of marine-harvested": {
        "id": "plastics-uv-swir-2020",
        "authors": ["Knaeps", "et al."],
        "venue": "ESSD",
        "doi": "10.5194/essd-12-77-2020",
        "arxiv": None,
        "tags": ["plastic", "hyperspectral", "uv-swir", "signature-library"],
        "relevance": "high",
        "existing_pdf": None,
        "in_slides": ["spectral-signatures"],
    },
    "usgs spectral library version 7": {
        "id": "kokaly-2017-splib07a",
        "authors": ["Kokaly", "et al."],
        "venue": "USGS Data Series",
        "doi": "10.3133/ds1035",
        "arxiv": None,
        "tags": ["signature-library", "usgs", "splib07a"],
        "relevance": "critical",
        "existing_pdf": None,
        "in_slides": ["spectral-signatures"],
    },
    "a knowledge-based, validated classifier for the identification of aliphatic": {
        "id": "zhou-2021-plastic-classifier",
        "authors": ["Zhou", "Kuester", "Bochow", "Bohn", "Brell", "Kaufmann"],
        "venue": "Remote Sensing of Environment",
        "doi": "10.1016/j.rse.2021.112598",
        "arxiv": None,
        "tags": ["plastic", "hyperspectral", "classifier", "aliphatic-aromatic", "wv-3", "gfz"],
        "relevance": "high",
        "existing_pdf": None,
        "in_slides": ["high-res-survey"],
        "notes": "Authors corrected 2026-05-25: Excel/memory attribuiva a 'Tasseron' — actual paper è Zhou et al. (GFZ Potsdam). Stesso DOI, PDF corretto.",
    },
}


def slugify(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:80]


def lookup_excel(title: str) -> dict | None:
    if not title:
        return None
    t = title.lower().strip()
    for key, meta in EXCEL_MAP.items():
        if t.startswith(key) or key in t[:120]:
            return meta
    return None


def load_excel() -> list[dict]:
    wb = openpyxl.load_workbook(EXCEL, data_only=True)
    ws = wb["Literature Review"]
    rows = list(ws.iter_rows(values_only=True))
    out = []
    for r in rows[1:]:
        if not any(c is not None and str(c).strip() for c in r):
            continue
        out.append({
            "titolo": (r[0] or "").strip(),
            "anno": int(float(r[1])) if r[1] else None,
            "obiettivo": r[2] or "",
            "metodo": r[3] or "",
            "risultati": r[4] or "",
            "riassunto": r[5] or "",
            "cosa_riutilizzare": r[6] or "",
            "link": (r[7] or "").strip(),
        })
    return out


def write_note(meta: dict, excel_row: dict):
    """Write notes/<id>.md preserving any existing 'Note Claude' section."""
    note_path = NOTES / f"{meta['id']}.md"
    existing_claude_notes = ""
    if note_path.exists():
        text = note_path.read_text()
        m = re.search(r"## Note Claude\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
        if m:
            existing_claude_notes = m.group(1).rstrip() + "\n"

    pdf_rel = f"library/{meta['id']}.pdf"
    # PDF presence on disk wins — VPN hint applies only when file is missing.
    if (ROOT / pdf_rel).exists():
        pdf_status = "downloaded"
    elif "vpn" in str(meta.get("notes", "")).lower():
        pdf_status = "vpn-required"
    else:
        pdf_status = "pending"

    fm = {
        "id": meta["id"],
        "title": excel_row["titolo"],
        "authors": meta.get("authors", []),
        "year": excel_row["anno"],
        "venue": meta.get("venue"),
        "doi": meta.get("doi"),
        "arxiv": meta.get("arxiv"),
        "link": excel_row["link"],
        "tags": meta.get("tags", []),
        "relevance": meta.get("relevance", "medium"),
        "status": pdf_status,
        "pdf": pdf_rel if (ROOT / pdf_rel).exists() else None,
        "in_slides": meta.get("in_slides", []),
        "relates_to": meta.get("relates_to", []),
    }

    def yaml_dump(d: dict) -> str:
        lines = []
        for k, v in d.items():
            if v is None:
                lines.append(f"{k}: null")
            elif isinstance(v, list):
                if not v:
                    lines.append(f"{k}: []")
                else:
                    items = ", ".join(f'"{x}"' for x in v)
                    lines.append(f"{k}: [{items}]")
            elif isinstance(v, (int, float)):
                lines.append(f"{k}: {v}")
            else:
                sv = str(v).replace('"', '\\"')
                lines.append(f'{k}: "{sv}"')
        return "\n".join(lines)

    body = f"""---
{yaml_dump(fm)}
---

## Obiettivo
{excel_row['obiettivo']}

## Metodo
{excel_row['metodo']}

## Risultati
{excel_row['risultati']}

## Riassunto
{excel_row['riassunto']}

## Cosa riutilizzare (tesi)
{excel_row['cosa_riutilizzare']}

## Note Claude
{existing_claude_notes}"""

    note_path.write_text(body)


def relocate_existing_pdf(meta: dict):
    """Move existing PDF from papers/ root into papers/library/<id>.pdf."""
    src_name = meta.get("existing_pdf")
    if not src_name:
        return
    src = ROOT / src_name
    dst = LIBRARY / f"{meta['id']}.pdf"
    if not src.exists() and dst.exists():
        return  # already moved
    if src.exists():
        if dst.exists():
            src.unlink()  # already in library, drop the duplicate at root
        else:
            shutil.move(str(src), str(dst))


def main():
    NOTES.mkdir(exist_ok=True)
    LIBRARY.mkdir(exist_ok=True)

    excel_rows = load_excel()
    matched = 0
    unmatched = []
    for row in excel_rows:
        meta = lookup_excel(row["titolo"])
        if not meta:
            unmatched.append(row["titolo"])
            continue
        matched += 1
        relocate_existing_pdf(meta)
        write_note(meta, row)

    print(f"Matched & wrote notes for {matched}/{len(excel_rows)} Excel rows")
    if unmatched:
        print(f"\nUNMATCHED ({len(unmatched)}):")
        for t in unmatched:
            print(f"  - {t[:100]}")


if __name__ == "__main__":
    main()
