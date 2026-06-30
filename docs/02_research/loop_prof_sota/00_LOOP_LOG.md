# Loop log — autonomous SOTA/direction research for the prof presentation

Bridges context between iterations (read at iteration start, update at iteration end).

## Objective
Deliver a clear, study-ready SOTA + thesis-direction panorama for the advisor presentation (next week), re-centred on the confirmed data **WorldView-3 + Pléiades Neo (sub-metre VHR)**, with **datasets** as the priority. Stay inside Thomas's scope (risk-classification framing; MS-vs-RGB added value). Work autonomously; surface only the decisions that genuinely need Thomas.

## Operating facts (confirmed this session)
- Data = **WV-3** (8 VNIR @1.24 m, 8 SWIR @3.7 m, pan 0.31 m) **+ Pléiades Neo** (6 VNIR @1.2 m, pan 0.3 m). Both sub-metre. → updates the SuperDove-primary assumption.
- Problem = **classify sites by risk for ARPA priority**, material is the hazard term. Core measurement = added value of multiband (MS) over RGB.
- AerialWaste **coordinates are withheld** (ARPA) → re-imaging bridge needs an in-group agreement. Asbestos **WFS is public** → immediate pilot label source.

## Iteration 1 — 2026-06-27 ✅ DONE
**Did:** read the full existing research base; ran 3 parallel verified research agents (Pléiades Neo; cross-sensor + pansharpening; risk framing); reconciled the data reality; produced the panorama.
**Produced:** `01_synthesis_direction.md`, `02_datasets_usable.md`, `research_pleiades_neo.md`, `research_crosssensor_pansharpening.md`, `research_risk_framing.md`, `README.md`.
**Key new findings:**
- SWIR re-enters experimental scope (WV-3); strongest precedents (Aguilar, Saba, Bonifazi, CascadeDumpNet) become *direct benchmarks*.
- Pléiades Neo = VNIR-only; Red Edge is the value band; Deep Blue ≈ atmospheric; **no peer-reviewed Pléiades-Neo material benchmark** (gap/opportunity); only 2 satellites operational.
- Classify on **native MS**, pansharpen for **texture only** (MRA/MTF, never GS/IHS); surface reflectance + SBAF mandatory; **pansharpened-vs-native control is itself publishable**.
- Risk framing has a citable Italian backbone: Fazzo 2020 + EWC/List of Waste + PRAL/Indice di Degrado; novelty = MS-derived hazard feeding the risk tier.
- Dataset bridge: asbestos WFS (open) + AerialWaste (gated on coords).

## Iteration 2 — 2026-06-27 ✅ DONE (background workflow, 9 agents)
**Did:** 5 parallel finders (archive coverage, Lombardy label layers, AerialWaste WV-3 recoverability, new-datasets sweep, FM/baseline fit) → adversarial verify → 2 design agents → synthesis.
**Produced:** `03_dataset_verification.md`, `04_experimental_design.md`; README upgraded to master panorama.
**Key new findings / corrections:**
- ESA TPM = free path for BOTH sensors (proposal ~9 wk + 1-yr consumption) → submit ASAP.
- **Correction:** WV-3 SWIR available at native **3.7 m** (7.5 m cap relaxed ~2018); real risk = archive availability over AOI, not resolution.
- **Correction:** Microsoft building footprints are ODbL (share-alike), not permissive → use regional **DBT `edificato`** (CC-BY).
- Lombardy label stack (all EPSG:32632, ArcGIS REST): asbestos WFS (hard positives) + DUSAF 131–134 (weak pos / clean neg) + AGISCO contaminated-site points (risk priors) + DBT footprints.
- AerialWaste MS recovery blocked without ARPA (no public scene IDs) → 2 concrete questions specified.
- 2025–26 sweep: only RoofNet + RoofSense new (optical-only, no SWIR, no asbestos) → thesis angle intact; verified negatives logged.
- DOFA = structurally-fair ablation spine; band ladder R0→R3 + center wavelengths defined; asbestos pilot = de-risking anchor; regulatory risk chain (EWC 17 06 05* → Indice di Degrado thresholds 25/44/45 → exposure → magnitude) concrete.

## Iteration 3 — 2026-06-27 ✅ DONE (background workflow, 4 agents)
**Did:** live-verified Lombardy layer field/code metadata via ArcGIS REST `?f=json`; drafted the prof-presentation narrative.
**Produced:** `05_field_metadata.md`, `06_presentation_outline.md`; corrected `04` re Indice di Degrado.
**Key results / corrections (all HIGH, from raw service JSON):**
- Real endpoint host = `/expo/rest/services/gpt/...` (not `/arcgis/rest/...`); asbestos service is a group tree → GT layers are **layer 1 (Mappatura 2020, 10,903)** and **layer 4 (Mappature precedenti, 50,131)**, all EPSG:32632.
- Layer 1 = presence-only (only COD_ISTATN). Layer 4 status codes **1/2/3/4 CONFIRMED** (present/removed/+PV/demolished) as per-year columns F1999..F2018 → use to filter by imagery date.
- **CORRECTION: Indice di Degrado is ABSENT from the WFS** → must be estimated remotely (SWIR Mg-OH + VNIR weathering) or sourced separately; the remote estimator is now framed as a contribution.
- DUSAF: class code `COD_TOT` is renderer-only/not-queryable → **filter on `DESCR`**; classes 131/132/133/134 present; CC-BY 4.0.
- AGISCO (PSC) = points, 5,813 features, fields ANA_CLAS_2 {bonificato,contaminato} + TIP_TIPOLO (incl. "smaltimenti non autorizzati - abbandono rifiuti", "discariche abusive o incontrollate"); CC-BY 4.0.

## Iteration 4 — 2026-06-28 ✅ DONE (background workflow, 6 agents)
**Did:** 4 parallel deep-dives (spectral physics↔bands; remote AC-degradation; generalization; object-vs-material) → adversarial verify → synthesis into study aids.
**Produced:** `07_technical_foundations.md`, `08_prof_qa_defense.md` (20 Q&A), `09_master_cheatsheet.md`.
**Key new knowledge / corrections:**
- Material↔feature↔band master table for all 13 classes; **SWIR-8 bottleneck** (asbestos 2.32 + concrete 2.34 + plastic 2.31 all in one WV-3 band).
- Remote AC-degradation proxy (two-tier spectral×GIS) since the Indice di Degrado is absent from the WFS; only ID factors A–D are imaging-targetable, D weakly.
- Generalization quantified (cross-region −5.1%; cross-sensor 2–4×/5–25%); **multiband narrows within-sensor, widens cross-sensor** → 2-D ablation×generalization table is the novel experiment.
- **Four-cell chemistry-vs-texture decomposition (B−A vs D−C)** = the safeguard that makes any MS gain attributable to material not texture.
- Corrections: dropped Aguilar "+14% kappa" & chrysotile "5 nm width"; downgraded Saba HS/MS, Bonifazi 0.87, Cilia figures to UNCERTAIN; fixed glossary EWC = European Waste Catalogue.

## Iteration 5 — 2026-06-28 ✅ DONE (background workflow, 4 agents)
**Did:** drafted the thesis Related-Work / SOTA chapter (intro + 6 sections + gaps/positioning + references) consolidating the loop knowledge into thesis-usable English prose.
**Produced:** `10_related_work_draft.md`.

## Iteration 6 — 2026-06-28 ✅ DONE (background workflow, 4 agents)
**Did:** web-verified DOIs/citations for the key anchors → annotated bibliography + ready-to-paste BibTeX.
**Produced:** `11_references.md`, `references.bib`.
**Corrections captured:** CascadeDumpNet = **Zhang & Ma 2024** (not Marrocco); AerialWaste real title; Shepherd 2nd author = Sagi; full Gibellini author list + DOI; "Garaba & Dierssen 2021 Sci.Rep." was a conflation (use Moshtaghi 2021 or Garaba&Dierssen 2018). TODOs: full author lists for GeoCrossBench/Fazzo/Estrela/Prithvi.

## LOOP STATUS — 2026-06-28 ~01:15: comprehensive panorama complete (6 iterations)
Deliverables: README + `01`–`11` + `references.bib` + 3 raw reports. Covers direction, datasets+usability, acquisition/verification, experimental design, verified field metadata, presentation outline, scientific foundations, prof Q&A, cheat-sheet, Related-Work draft, verified bibliography. The autonomous research space is now thoroughly covered; further substantive progress is **gated on Thomas/ARPA decisions** (see Blockers) rather than more search.
**Resume points when answers arrive:** deck integration (`06` + synthesis §4 into slides); lock experimental scope; ESA TPM proposal; asbestos-pilot T3 against the verified endpoints in `05`.

## LOOP STATUS: deep & well-organized; remaining empirical work gated on Thomas/ARPA
The knowledge base is now comprehensive (README → 01→09 + 6 raw reports + Related-Work draft). Decisions still needed from Thomas (AOI, ESA TPM submission, WV-3 SWIR confirmation, AerialWaste coordinate bridge, risk-chain scope) — see §"Blockers". Resume points when answers arrive:
- Deck integration: fold `06` + synthesis §4 into the actual slides (apply `../../01_calls/call_sota_revision.md`).
- Lock experimental scope; draft ESA TPM proposal; build asbestos-pilot T3 against the verified endpoints in `05`.

## Blockers / decisions needed from Thomas
1. AerialWaste coordinates obtainable? (gates the waste dataset)
2. WV-3 product includes SWIR? (gates the +SWIR axis)
3. AOI extent + overlap with AerialWaste positives / Mappatura_2020? (gates labels)
4. Material labels provided or self-annotate?
5. SuperDove still in (cheap/temporal layer) or dropped?
6. Risk-tier output in scope, or material classification only + risk as motivation?
