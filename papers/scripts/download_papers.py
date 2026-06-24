#!/usr/bin/env python3
"""
For each note in papers/notes/ without an existing PDF:
- Try arXiv (if arxiv ID present): https://arxiv.org/pdf/<id>.pdf
- Try DOI-based OA endpoints (Unpaywall fallback for MDPI, PLOS, Copernicus, Nature OA)
- Try USGS direct (for splib07a)
- Update the note's `status` field accordingly.

Closed-access (Elsevier jhazmat/jenvman/wasman/rsase, Wiley GRL, Springer): flagged
status=vpn-required so user knows to fetch via PoliMi VPN.
"""
from __future__ import annotations
import re
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
LIBRARY = ROOT / "library"
NOTES = ROOT / "notes"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}
TIMEOUT = 30


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    out = {}
    for line in m.group(1).split("\n"):
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        v = v.strip()
        if v == "null":
            out[k.strip()] = None
        elif v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            out[k.strip()] = (
                [x.strip().strip('"') for x in inner.split(",") if x.strip()]
                if inner else []
            )
        else:
            out[k.strip()] = v.strip('"')
    return out


def update_frontmatter_field(text: str, field: str, value: str) -> str:
    pattern = rf'^({field}: )(.*)$'
    return re.sub(pattern, rf'\g<1>"{value}"', text, count=1, flags=re.MULTILINE)


def download_pdf(url: str, dst: Path, allow_html_check: bool = True) -> bool:
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True, stream=True)
        if r.status_code != 200:
            return False
        ct = r.headers.get("Content-Type", "").lower()
        if allow_html_check and "pdf" not in ct and not url.lower().endswith(".pdf"):
            return False
        first = next(r.iter_content(chunk_size=8192))
        if not first.startswith(b"%PDF"):
            return False
        dst.parent.mkdir(parents=True, exist_ok=True)
        with open(dst, "wb") as f:
            f.write(first)
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return dst.stat().st_size > 10_000
    except Exception:
        return False


def try_arxiv(arxiv_id: str, dst: Path) -> bool:
    if not arxiv_id or arxiv_id == "null":
        return False
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    return download_pdf(url, dst, allow_html_check=False)


def try_doi_oa(doi: str, dst: Path) -> bool:
    if not doi or doi == "null":
        return False
    # MDPI: www.mdpi.com /pdf endpoint hits Akamai (403). Use mdpi-res.com mirror.
    # DOI 10.3390/<journal_short><vol_padded><art_padded> — but mapping is non-trivial,
    # so try DOI resolver, follow redirect, then translate to mdpi-res.com pattern.
    if doi.startswith("10.3390/"):
        landing = f"https://doi.org/{doi}"
        try:
            r = requests.get(landing, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
            final = r.url  # e.g. https://www.mdpi.com/2072-4292/13/11/2133
            m = re.search(r"mdpi\.com/(\d{4}-\d{4})/(\d+)/(\d+)/(\d+)", final)
            if m:
                issn, vol, issue, art = m.groups()
                # Find journal short name from DOI: 10.3390/<jshort><vol>0<iss>0<art>
                jshort_m = re.match(r"10\.3390/([a-z]+)\d+", doi)
                if jshort_m:
                    jshort = jshort_m.group(1)
                    # mdpi-res pattern: <jshort>-<vol_padded4>-<art_padded4 or 5>
                    for art_pad in (str(art).zfill(5), str(art).zfill(4)):
                        for vol_pad in (str(vol).zfill(2), str(vol).zfill(4)):
                            for ver in ("v2", "v1", ""):
                                suffix = f"-{ver}" if ver else ""
                                url = (
                                    f"https://mdpi-res.com/d_attachment/{jshort}/"
                                    f"{jshort}-{vol_pad}-{art_pad}/article_deploy/"
                                    f"{jshort}-{vol_pad}-{art_pad}{suffix}.pdf"
                                )
                                if download_pdf(url, dst, allow_html_check=False):
                                    return True
        except Exception:
            return False
    # PLOS ONE
    if doi.startswith("10.1371/"):
        pdf_url = f"https://journals.plos.org/plosone/article/file?id={doi}&type=printable"
        return download_pdf(pdf_url, dst, allow_html_check=False)
    # Copernicus / ESSD
    if doi.startswith("10.5194/"):
        landing = f"https://doi.org/{doi}"
        try:
            r = requests.get(landing, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
            final = r.url.rstrip("/")
            if "copernicus.org" in final:
                pdf_url = final + ".pdf"
                return download_pdf(pdf_url, dst, allow_html_check=False)
        except Exception:
            return False
    # Nature OA (s41467 = Nature Comms, s41598 = Sci Rep, etc.)
    if doi.startswith("10.1038/s41"):
        landing = f"https://doi.org/{doi}"
        try:
            r = requests.get(landing, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
            final = r.url
            if "nature.com" in final:
                pdf_url = final.rstrip("/") + ".pdf"
                return download_pdf(pdf_url, dst, allow_html_check=False)
        except Exception:
            return False
    # USGS DS
    if doi.startswith("10.3133/"):
        ds_id = doi.split("/")[-1]
        url = f"https://pubs.usgs.gov/ds/1035/{ds_id}.pdf"
        if download_pdf(url, dst, allow_html_check=False):
            return True
    # IEEE Access OA: try Xplore stamp endpoint
    if doi.startswith("10.1109/ACCESS"):
        # Resolve DOI to grab the arnumber
        try:
            r = requests.get(f"https://doi.org/{doi}", headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
            m = re.search(r"/document/(\d+)", r.url)
            if m:
                arnum = m.group(1)
                pdf_url = f"https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber={arnum}"
                if download_pdf(pdf_url, dst, allow_html_check=False):
                    return True
        except Exception:
            return False
    # Springer OA (EMA, etc.): try landing then /pdf
    if doi.startswith("10.1007/"):
        landing = f"https://link.springer.com/article/{doi}"
        pdf_url = f"https://link.springer.com/content/pdf/{doi}.pdf"
        if download_pdf(pdf_url, dst, allow_html_check=False):
            return True
    return False


def is_closed_access_doi(doi: str | None) -> bool:
    if not doi:
        return False
    closed_prefixes = [
        "10.1016/j.jhazmat",
        "10.1016/j.jenvman",
        "10.1016/j.wasman",
        "10.1016/j.rsase",
        "10.1016/j.rse",
        "10.1016/j.isprsjprs",
        "10.1029/",
        "10.1080/",
        "10.1109/ACCESS",  # IEEE Access is OA but stamp.jsp often blocks scripted access
    ]
    return any(doi.startswith(p) for p in closed_prefixes)


def main():
    notes = sorted(NOTES.glob("*.md"))
    print(f"Processing {len(notes)} notes\n")

    results = {"downloaded": [], "vpn-required": [], "failed": []}

    for note in notes:
        text = note.read_text()
        fm = parse_frontmatter(text)
        pid = fm.get("id")
        if not pid:
            continue
        pdf = LIBRARY / f"{pid}.pdf"
        if pdf.exists():
            results["downloaded"].append(pid)
            continue

        # try arxiv first
        ok = try_arxiv(fm.get("arxiv"), pdf)
        # then DOI OA
        if not ok:
            ok = try_doi_oa(fm.get("doi"), pdf)

        if ok:
            new = update_frontmatter_field(text, "status", "downloaded")
            new = update_frontmatter_field(new, "pdf", f"library/{pid}.pdf")
            note.write_text(new)
            results["downloaded"].append(pid)
            print(f"✓ {pid}")
        elif is_closed_access_doi(fm.get("doi")):
            new = update_frontmatter_field(text, "status", "vpn-required")
            note.write_text(new)
            results["vpn-required"].append(pid)
            print(f"⚠ {pid}  (closed access — needs PoliMi VPN)")
        else:
            new = update_frontmatter_field(text, "status", "failed")
            note.write_text(new)
            results["failed"].append(pid)
            print(f"✗ {pid}")
        time.sleep(0.5)

    print(f"\n=== SUMMARY ===")
    print(f"Downloaded: {len(results['downloaded'])}")
    print(f"VPN required: {len(results['vpn-required'])}")
    print(f"Failed: {len(results['failed'])}")
    if results["vpn-required"]:
        print(f"\nVPN-required (fetch manually via PoliMi):")
        for pid in results["vpn-required"]:
            print(f"  - {pid}")
    if results["failed"]:
        print(f"\nFailed (need investigation):")
        for pid in results["failed"]:
            print(f"  - {pid}")


if __name__ == "__main__":
    main()
