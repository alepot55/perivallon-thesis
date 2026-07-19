# STATO — snapshot corrente della tesi

> **Memoria di lavoro della repo.** Chi (umano o agente) inizia una sessione parte da qui; chi la chiude aggiorna questo file: sostituisci il contenuto superato (non appendere), aggiorna la data, tieni compatto. La cronologia fine sta in `docs/01_calls/` e nel git log. Se questo file contraddice l'ultima call in `docs/01_calls/`, **vince la call** — e va corretto qui.
>
> **Ultimo aggiornamento: 2026-07-19 (sera).**

## Stato in breve

Pivot del 17/7: da material classification MS a **binary landfill detection satellite-only**, asse sperimentale = **risoluzione** (30 cm → ~70 cm → 1.2 m). Obiettivo dichiarato di Ale: **≥7 punti a dicembre** → piano in `docs/04_planning/2026-07-19_piano_7_punti.md` (North Star: *weakly-supervised waste localization under GSD degradation*). Fase attuale: setup infra (eagle) + preparazione call con Enrico (mar/mer 21–22/7).

## Persone

| Chi | Ruolo |
|---|---|
| Prof. Piero Fraternali | Relatore (decide formato/impostazione; chiede sempre l'**indice**) |
| Thomas Martinoli | Supervisore operativo, revisor primario |
| **Enrico Targhini** (enrico.targhini@polimi.it) | Ricercatore, guida AI/codice waste (da 17/7); assegna repo GitLab |
| Federico Gibellini ("Fede") | Autore baseline binary (paper 2025) |
| Alari | Tesista 2024, material classification satellite (politesi 10589/230633, 11.477 annotazioni multi-label image-level) |
| Ale (Alessandro Potenza) | Tesista; remoto da Roma; contratto visiting fino a fine settembre |

## Fatti chiave correnti

- **Task**: binary detection su dataset satellite-only **~1.200 img → ~2.000 con WorldView** (vs ~10k AerialWaste). Annotazioni image-level; **non esistono maschere di segmentazione** per i dataset del gruppo (deck v7) → test-set di localizzazione da costruire (gating del piano).
- **Baseline riferimento**: Gibellini 2025 — Swin-T+RSP, 20 cm, context 100 m, **F1 92.02**; factorial 36 config (GSD 20/30/50); generalizzazione cross-country F1 86.92; la pipeline **include già Grad-CAM→GIS**. Replica personale in `waste/`: F1 0.9519 su AerialWaste v3.
- **Novelty bar** (per i +2 punti): Gibellini ha CAM in pipeline, **Mazzola 2024 ha già Grad-CAM + weakly supervised localization** su MS satellitare (asbestos). Delta obbligatorio: task waste + asse GSD + eval quantitativa + metodo oltre vanilla CAM.
- **Risoluzioni**: 30 cm pansharpened (start) → ~70 cm → 1.2 m nativo (a 1.2 m i FM diventano usabili). Razionale: IRIDE (best 1 m) + costi ARPA. PlanetScope 3 m: fuori.
- **FM in-house** del gruppo in preparazione → pesi ad hoc in arrivo (tempi ignoti).
- **Punteggio**: journal thesis ≤8 punti a contenuto; impostazione attuale ≈5; +2 solo con innovazione. Media Ale 28.7 → base ~105.
- **Formato tesi**: article/journal **≈30 pagine** + **Executive Summary ~6 pp** (errata di Thomas — in call si era detto ~10). Serve consenso scritto del relatore per il formato article. Template su pagina IngIndInf "Modelli formato tesi" (anche Overleaf). Strategia: scrivere lunga → condensare. Esempi: Alari (lunga), Merlo 10589/252150, Mazzola 10589/230433.
- **Infra**: server **eagle**, container **multispectralwaste**, porta **2212** — guida completa in `docs/00_context/server_eagle_howto.md`. Codice tesi del gruppo su **GitLab** (non GitHub), assegnato da Enrico.
- **Timeline**: sprint ferie **10–23/8**; checkpoint +2 con Thomas **~metà settembre**; contratto Ale finisce fine settembre; scrittura ott–nov; **deposito ~inizio-metà novembre (data esatta DA VERIFICARE — biblioteca PoliMi)**; laurea dicembre. Thomas via 1–15/8.

## TODO aperti

1. **Bloccanti infra**: (a) VPN PoliMi — attivazione via Thomas→IT (lead time!); (b) chiave SSH → `.pub` a Thomas; (c) ~~username GitLab a Enrico~~ → **msg a Enrico inviato (19/7)**, attesa risposta per call mar/mer.
2. **Msg a Thomas (lun 20/7)**: VPN + chiave SSH pubblica (+ PS: short "Asha" change detection, se esiste).
3. **Call Enrico (mar/mer 21–22/7)**: domande in `docs/04_planning/2026-07-19_piano_7_punti.md` §Domande — gating: poligoni per test-set localizzazione.
4. **Claude, in ordine**: (1) doc-baseline Gibellini congelato; (2) mini-SOTA WSOL/WSSS in RS (parte da Mazzola, `asbestos/reference/Mazzola_2024_Thesis.pdf`); (3) indice tesi v0 (formato article); (4) related work detection (riorienta `docs/02_research/loop_prof_sota/10_related_work_draft.md`); (5) tenere vivi `EXPERIMENTS_LOG.md` + `CLAIMS.md`.
5. Verificare **date deposito dicembre** (biblioteca PoliMi) + scaricare template Overleaf article.
6. In attesa: short "Asha" change detection (Thomas, se esiste); tempi pesi FM in-house; tempi campagna annotazione.

## Filone materiali (in pausa, non morto)

RQ pre-pivot: MS vs RGB per material classification (hazard/risk framing Fazzo 2020). Tutto il materiale resta valido come base: related work draft + bib verificata (`docs/02_research/loop_prof_sota/`), firme spettrali (`spectral/`), pilot amianto (`asbestos/`). L'angolo B del piano (risoluzione×spettro) lo ricicla dentro la nuova task.

## Log decisioni

- **2026-07-19**: obiettivo ≥7 dichiarato; piano operativo (`docs/04_planning/2026-07-19_piano_7_punti.md`); infra ricevuta (eagle/2212/multispectralwaste); errata formato (article ≈30 pp + exec summary); novelty alert Mazzola; repo riorganizzata per handoff agente (STATO.md, `.claude/commands/`, 04_planning). Sera: msg a Enrico inviato; root repo ripulita (build legacy → `assets/_legacy_builds/`, temp eliminati, `datasets_study_guide.pdf` → `docs/02_research/`).
- **2026-07-17 (pomeriggio)**: punteggio ≈5 vs 8; strategia base-poi-upgrade (`docs/01_calls/2026-07-17_punteggio_strategia.md`).
- **2026-07-17 (mattina)**: **pivot a binary detection satellite-only** (`docs/01_calls/2026-07-17_pivot_binary_detection.md`).
- **2026-06-30**: revisione deck direzione WV-3+Pléiades Neo. **2026-06-28**: loop SOTA materiali completo (`docs/02_research/loop_prof_sota/00_LOOP_LOG.md`).
- Storia precedente: `docs/01_calls/` (2026-04-24 pivot SuperDove, 2026-05-22/26 slide, ecc.).
