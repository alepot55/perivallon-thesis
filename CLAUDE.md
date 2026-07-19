# CLAUDE.md

Guida per Claude Code su questa repo. **Prima azione di ogni sessione: leggi `STATO.md`** (memoria di lavoro), poi l'ultima call per data in `docs/01_calls/` — se divergono, vince la call e correggi STATO.md.

## Progetto

Tesi magistrale di Alessandro Potenza ("Ale") al PoliMi, dentro PERIVALLON (Horizon Europe, Grant 101073952). Relatore: Prof. Piero Fraternali. Supervisore operativo: Thomas Martinoli. Parte AI/codice: Enrico Targhini.

**Fase corrente (post-pivot 2026-07-17): binary landfill detection su imagery satellitare multispettrale, asse risoluzione (30 cm → 1.2 m). Obiettivo: ≥7 punti a dicembre 2026.** Dettagli e TODO: `STATO.md`. Piano: `docs/04_planning/2026-07-19_piano_7_punti.md`.

## Protocollo di sessione

1. `STATO.md` → ultima call in `docs/01_calls/` → (se serve) `docs/04_planning/`.
2. Lavora. Esperimenti → `/experiment` (log + claims). Nuove trascrizioni call → `/call`.
3. Chiudi aggiornando `STATO.md`: sostituisci il superato, data in testa, compatto.

Slash commands in `.claude/commands/`: `/catchup`, `/call`, `/experiment`.

## Mappa repo

```
Tesi/
├── STATO.md           ← memoria di lavoro (LEGGI PRIMA) — stato, TODO, decisioni
├── docs/              ← knowledge base testuale (INDEX.md = mappa e ordine di lettura)
│   ├── 00_context/    ← overview tesi, fondamenti tecnici, guida server eagle
│   ├── 01_calls/      ← UNA call = UN doc datato YYYY-MM-DD_slug.md; la più recente vince
│   ├── 02_research/   ← ricerca (loop_prof_sota/ = SOTA materiali pre-pivot, riusabile)
│   ├── 03_papers/     ← pdf chiave (Gibellini 2025 = baseline)
│   └── 04_planning/   ← piano 7 punti, EXPERIMENTS_LOG.md, CLAIMS.md
├── papers/            ← sistema bibliografico (README.md = regole; ID kebab-case = chiave primaria;
│                         INDEX.md/index.json AUTO-GENERATI — non editare a mano; usa gli script)
├── waste/             ← codice replica baseline AerialWaste (CLAUDE.md locale con comandi)
├── asbestos/          ← pilot amianto pre-pivot (in pausa; reference/Mazzola_2024_Thesis.pdf)
├── spectral/          ← firme spettrali USGS (in pausa, knowledge base)
└── assets/            ← deck slides (deck_v7 = ultimo)
```

**Non in repo**: tesi LaTeX (Overleaf) · codice esperimenti del gruppo (GitLab PoliMi, sul server eagle — vedi `docs/00_context/server_eagle_howto.md`) · checkpoint pesanti e imagery (`.gitignore`).

## Regole di lavoro

- **Gerarchia fonti**: (1) ciò che dice Ale → (2) call più recente in `docs/01_calls/` → (3) `STATO.md` → (4) resto dei docs (possono essere pre-pivot: verifica la data).
- **Rigore**: distingui fatto verificato / inferenza / speculazione; tag HIGH/MEDIUM/UNCERTAIN dove usati; novelty claims sempre hedged ("to our knowledge"); numeri solo con fonte riproducibile (EXP-ID, paper, path run).
- **Trascrizioni STT**: nomi propri spesso storpiati — verifica contro STATO.md/repo, flagga `[STT, da confermare]` se irrisolto.
- **Bibliografia**: usa i riferimenti verificati (`docs/02_research/loop_prof_sota/11_references.md` + `references.bib`); correzioni già registrate nei log — non reintrodurre errori corretti.
- **Stile con Ale**: italiano informale, termini tecnici in inglese, output scannable, zero preamboli. Deliverable di tesi in inglese. Slide: convenzioni nei doc call (B/N minimal, una idea per slide, refs su ogni slide).
- **Bozze messaggi (Teams/mail per Thomas, Enrico, prof)**: brevi, semplici, cortesi, tono naturale da telefono — niente elenchi, niente em dash, niente formattazione o struttura.
- **Punteggio**: la commissione riconosce contenuto, non volume — ogni contributo va reso difendibile via `docs/04_planning/CLAIMS.md`.

## Comandi rapidi (pillar codice)

```bash
# waste/ — replica baseline (dettagli in waste/CLAUDE.md)
cd waste && uv venv --python 3.11 && source .venv/bin/activate && uv pip install -e ".[dev]"
python scripts/train.py training.phase=both        # two-step TL→FT (Gibellini)
pytest tests/ -v && ruff check src/ scripts/ tests/

# papers/ — pipeline bibliografia (mai editare Excel/INDEX a mano)
cd papers && python3 scripts/bootstrap_papers.py && python3 scripts/build_index.py

# spectral/ — rigenera figure firme
cd spectral && python3 scripts/generate.py
```

Baseline personale: Swin-T+RSP su AerialWaste v3, val F1 **0.9519** (ckpt non in repo — vedi waste/CLAUDE.md §Checkpoints). Due-step training e convenzioni Hydra: `waste/CLAUDE.md`.

## Infra esperimenti tesi

Gli esperimenti della tesi girano sul **server eagle** del gruppo (container `multispectralwaste`, porta 2212), non in questa repo: setup, storage, regole GPU e tmux in `docs/00_context/server_eagle_howto.md`. Risultati e conclusioni tornano qui: `docs/04_planning/EXPERIMENTS_LOG.md` + `CLAIMS.md`.
