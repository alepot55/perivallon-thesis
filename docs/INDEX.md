# docs/ — guida di lettura

Mappa dei documenti di tesi PERIVALLON. I file sono numerati per **ordine di lettura** consigliato a un nuovo collaboratore (o a una sessione futura senza memoria).

## Ordine di lettura

1. `00_context/thesis_overview.md` — cosa è la tesi, perché esiste, chi c'è dietro
2. `00_context/technical_foundations.md` — fondamenti tecnici (telerilevamento, satelliti, da 3 a N canali, fine-tuning, FM, pipeline PoliMi, stack)
3. `01_calls/2026-04-24_pivot_superdove.md` — **cambio di rotta**: Sentinel-2 → SuperDove
4. `01_calls/call_sota_revision.md` — feedback Thomas sulle slide SOTA, slide-per-slide
5. `02_research/research_compendium.md` — panoramica completa (sensori, FM, baseline, stack)
6. `02_research/gap_analysis.md` — cosa manca nella reading list, top citation da aggiungere
7. `02_research/spectral_signatures.md` — firme spettrali per materiale (plastica/metalli/cemento/...)
8. `02_research/datasets_catalog.md` — 42 dataset multispettrali con label di materiale
9. `03_papers/gibellini_polimi_waste.pdf` — paper PoliMi baseline (Gibellini 2025)

## Indice per domanda

| Domanda | Apri |
|---|---|
| Qual è il problema della tesi e perché conta? | `00_context/thesis_overview.md` |
| Perché SuperDove e non Sentinel-2? | `01_calls/2026-04-24_pivot_superdove.md` §"Cambio di rotta" |
| Workflow Fase 1 amianto (clustering firme)? | `01_calls/call_sota_revision.md` slide 17 + `01_calls/2026-04-24_pivot_superdove.md` §"Pre-esperimento" |
| Quali bande servono per discriminare materiali? | `02_research/spectral_signatures.md` |
| Plastica PE vs PP vs PET — dove si distinguono? | `02_research/spectral_signatures.md` §1 |
| Asbesto-cemento — quali bande SWIR diagnostiche? | `02_research/spectral_signatures.md` + `02_research/gap_analysis.md` B.4 |
| RGB vs multispettrale — ablation canonica? | `02_research/gap_analysis.md` C.4 (Aguilar 2021, Kaur 2024) |
| Quale foundation model scegliere? | `02_research/research_compendium.md` §5 + `02_research/gap_analysis.md` A.1 |
| DOFA, Prithvi, SpectralGPT — chi accetta cosa? | `02_research/research_compendium.md` §5 |
| Confronto sensori (SuperDove/WV-3/Pléiades/S2)? | `02_research/research_compendium.md` §3 (tabella) |
| Dataset multispettrali con label materiale? | `02_research/datasets_catalog.md` |
| Baseline PoliMi (Swin-T + RSP, 92% F1)? | `03_papers/gibellini_polimi_waste.pdf` + `02_research/research_compendium.md` §6 |
| Cosa Thomas vuole cambiato nelle slide SOTA? | `01_calls/call_sota_revision.md` (slide-per-slide) |
| Quali paper assolutamente da citare? | `02_research/gap_analysis.md` §Recommendations + tabella finale |

## Note sui contenuti

- **`call_sota_revision.md`**: è il feedback più recente — i contenuti delle slide vanno allineati a questo, non al compendio.
- **`gap_analysis.md`**: contiene il competitor diretto (Aharoni-Mack 2025, EnMAP + asbesto-cemento, ACE OA 91.4%). Da benchmarcare.
- **`research_compendium.md`**: scritto **prima** del pivot a SuperDove → alcune raccomandazioni (es. SWIR centrico) sono superate. La rotta corrente è in `01_calls/2026-04-24_pivot_superdove.md`.
- **`spectral_signatures.md`**: knowledge base per interpretare cosa SuperDove **può** (VNIR + red edge) e **non può** (SWIR) vedere.

## Cosa non c'è qui

- La tesi LaTeX è su Overleaf, non in repo
- Le slide tecniche (deck minimale) sono altrove (`/asbestos/`, slide deck specifiche)
- Bibliografia in PDF intera → `../papers/` (top-level)
