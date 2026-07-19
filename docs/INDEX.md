# docs/ — guida di lettura

Mappa dei documenti di tesi PERIVALLON. I file sono numerati per **ordine di lettura** consigliato a un nuovo collaboratore (o a una sessione futura senza memoria).

> ⚠️ **Pivot 2026-07-17**: la rotta corrente è **binary detection satellite-only, asse risoluzione**. Tutto ciò che parla di material classification / SuperDove / SWIR è **pre-pivot**: resta valido come knowledge base, non come direzione. Fonte di verità sullo stato: `../STATO.md`.

## Ordine di lettura

1. `../STATO.md` — stato corrente, TODO, log decisioni (**parti da qui**)
2. `01_calls/2026-07-17_pivot_binary_detection.md` — **rotta corrente** (binary satellite-only, asse GSD)
3. `01_calls/2026-07-17_punteggio_strategia.md` — punteggio (≈5 vs 8) e strategia base+upgrade
4. `04_planning/2026-07-19_piano_7_punti.md` — piano operativo ≥7 punti (angoli innovazione, timeline, gating)
5. `00_context/server_eagle_howto.md` — infra: server eagle, Docker, storage, GPU, tmux
6. `04_planning/EXPERIMENTS_LOG.md` + `04_planning/CLAIMS.md` — registro esperimenti e ledger dei claim
7. `03_papers/gibellini_polimi_waste.pdf` — paper baseline (Gibellini 2025): la reference dei numeri
8. `00_context/thesis_overview.md` — origine della tesi, contesto PERIVALLON *(pre-pivot: RQ materiali superata)*
9. `00_context/technical_foundations.md` — fondamenti (telerilevamento, bande, FM, fine-tuning)
10. `02_research/loop_prof_sota/README.md` + `02_research/loop_prof_sota/10_related_work_draft.md` + `02_research/loop_prof_sota/11_references.md` — SOTA materiali completa: da **riorientare su detection**, bib verificata riusabile

## Indice per domanda

| Domanda | Apri |
|---|---|
| Qual è la rotta corrente e perché? | `01_calls/2026-07-17_pivot_binary_detection.md` |
| Cosa serve per ≥7 punti e qual è il piano? | `04_planning/2026-07-19_piano_7_punti.md` + `01_calls/2026-07-17_punteggio_strategia.md` |
| Come accedo al server / lancio un training? | `00_context/server_eagle_howto.md` |
| Come scrivo un messaggio a Thomas (stile, processo)? | `00_context/chat_thomas_log.md` |
| Quali numeri deve battere/avvicinare la tesi? | `03_papers/gibellini_polimi_waste.pdf` (F1 92.02 @20 cm) + `../papers/notes/gibellini-2025-pipeline.md` |
| Cosa è già stato fatto nel gruppo su CAM/localizzazione? | Gibellini pipeline (Grad-CAM→GIS) + Mazzola 2024 (`../asbestos/reference/Mazzola_2024_Thesis.pdf`) — vedi anche CLAIMS C-7 |
| Quali esperimenti sono pianificati/fatti? | `04_planning/EXPERIMENTS_LOG.md` |
| Che claim vuole difendere la tesi? | `04_planning/CLAIMS.md` |
| Formato tesi (article ~30 pp, executive summary)? | `../STATO.md` §Fatti chiave + pagina IngIndInf "Modelli formato tesi" |
| Related work / bibliografia verificata? | `02_research/loop_prof_sota/10_related_work_draft.md` + `11_references.md` + `references.bib` |
| Quale foundation model accetta cosa? | `02_research/research_compendium.md` §5 *(pre-pivot ma tecnico, valido)* |
| Fondamenti: bande, GSD, pansharpening, FM? | `00_context/technical_foundations.md` |
| Firme spettrali per materiale? *(filone in pausa)* | `02_research/spectral_signatures.md` |
| Dataset MS con label materiale? *(filone in pausa)* | `02_research/datasets_catalog.md` |
| Storia delle decisioni pre-pivot? | `01_calls/` in ordine di data (2026-04-24 SuperDove → 2026-05-22/26 slide → 2026-06-30 deck) |

## Note sui contenuti

- **`01_calls/`**: una call = un doc datato `YYYY-MM-DD_slug.md`. **Il più recente vince** su compendi, piani e draft precedenti. (`01_calls/call_sota_revision.md` è senza data nel filename: è del periodo maggio, pre-pivot.)
- **`02_research/`** (incluso `loop_prof_sota/`): costruito per la RQ materiali. La bib è verificata e riusabile; il framing va riorientato su detection prima di finire in tesi.
- **`02_research/research_compendium.md`**: scritto prima ancora del pivot SuperDove — doppio strato di staleness sul framing, sezioni tecniche (sensori, FM) ancora utili.
- **`00_context/thesis_overview.md`**: fotografia dell'inizio (febbraio), utile per l'introduzione storica, non per lo stato.

## Cosa non c'è qui

- La tesi LaTeX è su Overleaf, non in repo
- Il codice esperimenti del gruppo è su GitLab PoliMi e gira su eagle (`00_context/server_eagle_howto.md`)
- Le slide sono in `../assets/` (deck_v7 = ultimo); il codice personale in `../waste/`, `../asbestos/`, `../spectral/`
- Bibliografia completa e sistema note → `../papers/`
