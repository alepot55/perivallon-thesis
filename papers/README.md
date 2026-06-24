# papers/ — Reference bibliography

Sistema organizzato di gestione paper, ottimizzato per essere navigabile sia dall'utente sia da Claude attraverso sessioni multiple.

## Layout

```
papers/
├── SOTA_DLxSAT.xlsx       ← Excel del team (sorgente autoritativo, sync via script)
├── INDEX.md               ← tabella human-readable [AUTO-GENERATA, non editare]
├── index.json             ← tabella machine-readable [AUTO-GENERATA, Claude la legge]
├── README.md              ← questo file
├── library/               ← tutti i PDF, naming: <id>.pdf (kebab-case)
├── notes/                 ← un .md per paper, frontmatter YAML + sezioni
│   └── <id>.md
├── scripts/
│   ├── scopus_search.py       ← survey Scopus broad-net (≠ Excel curato)
│   ├── bootstrap_papers.py    ← legge Excel → crea/aggiorna notes/, sposta PDF in library/
│   ├── download_papers.py     ← tenta download (arXiv + OA: MDPI, PLOS, Copernicus, Nature, USGS, Springer)
│   ├── sync_excel.py          ← notes/ → Excel (reverse-sync: Claude aggiorna l'Excel da solo)
│   └── build_index.py         ← notes/ → INDEX.md + index.json
└── literature_search/     ← survey Scopus 699 paper (≠ Excel curato)
```

## Convenzione ID

Ogni paper ha un ID stabile `kebab-case`: `<first-author-lastname>-<year>-<slug>` (es. `gibellini-2025-pipeline`, `aharoni-mack-2026-wv3-vnir`).

L'ID è la **chiave primaria** di tutto il sistema:
- File PDF: `library/<id>.pdf`
- Nota: `notes/<id>.md`
- Riferimenti incrociati: `relates_to: [<id1>, <id2>]` nel frontmatter
- Memoria Claude: `reference_key_papers.md` cita ID, non duplica contenuto

## Frontmatter delle note (`notes/<id>.md`)

```yaml
---
id: gibellini-2025-pipeline
title: A deep learning pipeline for solid waste detection in remote sensing images
authors: [Gibellini, Torres, Fraternali]
year: 2025
venue: Waste Management Bulletin
doi: 10.1016/j.wmb.2025.02.003
arxiv: 2502.06607
link: arXiv:2502.06607
tags: [waste, baseline, swin-t, rsp, aerialwaste]
relevance: critical    # critical | high | medium | low
status: downloaded     # downloaded | vpn-required | failed | pending
pdf: library/gibellini-2025-pipeline.pdf
in_slides: [baseline, approach]   # quali sezioni della presentazione lo citano
relates_to: [torres-2023-aerialwaste, fraternali-2024-survey]
---
## Obiettivo
## Metodo
## Risultati
## Riassunto
## Cosa riutilizzare (tesi)
## Note Claude       ← spazio per appunti Claude tra sessioni (preservato dal bootstrap)
```

## Workflow tipico

### Aggiungi un nuovo paper
1. Aggiungi riga all'Excel `SOTA_DLxSAT.xlsx` (titolo + anno + link minimi).
2. Apri `scripts/bootstrap_papers.py`, aggiungi entry in `EXCEL_MAP` con ID stabile + metadata corretti.
3. Esegui:
   ```bash
   cd papers
   python3 scripts/bootstrap_papers.py   # crea/aggiorna nota
   python3 scripts/download_papers.py    # tenta download
   python3 scripts/sync_excel.py         # riporta info corrette dall'Excel
   python3 scripts/build_index.py        # rigenera indici
   ```

### Correggere/rinominare un paper esistente
1. Aggiorna la entry corrispondente in `EXCEL_MAP` (titolo prefix come chiave, nuovo ID nel value).
2. Cancella la vecchia nota `notes/<old-id>.md` e il PDF `library/<old-id>.pdf`.
3. Rilancia la pipeline (4 comandi sopra).
4. L'Excel viene sincronizzato automaticamente da `sync_excel.py` — **non editare l'Excel a mano.**

### Aggiungi un appunto a un paper
Edita direttamente `notes/<id>.md`, sezione `## Note Claude`. Bootstrap re-run preserva il contenuto di quella sezione.

### Trova paper per tema
Apri `INDEX.md` → sezioni "By topic" e "By slide section". Oppure leggi `index.json` programmaticamente.

### Status legenda
- ✅ `downloaded` — PDF in `library/`
- 🔒 `vpn-required` — closed-access (Elsevier jhazmat / jenvman / wasman / rsase, Wiley GRL, RSE). Scaricalo dal browser con VPN PoliMi attiva, salva in `library/<id>.pdf`, poi `python3 scripts/build_index.py`.
- ❓ `failed` — link Excel ambiguo o sorgente non risolvibile. Da investigare manualmente (cercare arXiv/DOI corretto, aggiornare `notes/<id>.md`).
- ⏳ `pending` — non ancora tentato.

## Stato corrente

Vedi `INDEX.md` per il totale aggiornato. La sezione `literature_search/` contiene il survey Scopus più ampio (699 paper) con `READING_LIST.md` di 12 picks aggiuntivi — quelli non sono stati ancora integrati nel sistema di note, sono backlog secondario.
