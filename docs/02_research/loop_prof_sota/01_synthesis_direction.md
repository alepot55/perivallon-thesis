---
title: "SOTA & thesis direction under the WorldView-3 + Pléiades Neo data reality"
subtitle: "Autonomous research loop — iteration 1 synthesis (for the advisor presentation)"
author: "PERIVALLON thesis · Politecnico di Milano"
date: "2026-06-27"
status: "working synthesis — open questions flagged for Thomas/Fraternali"
---

# 0. Why this document exists

The advisor will provide the experimental data as **WorldView-3 + Pléiades Neo, both sub-metre VHR**, over a Lombardia AOI. The existing research base (two SOTA docs, 42-dataset catalog, gap analysis, 47 paper notes) is strong but was written around two *older* operating-point assumptions:

- `sota_highres_material.md` is framed around **SuperDove (3 m, VNIR-only)** as "the unstudied frontier".
- `sota_vhr_13classes.md` correctly uses the **30–50 cm VHR satellite** operating point, but treats WV-3 SWIR mostly as an *out-of-scope upper bound*.

Neither fully matches the confirmed data. This synthesis **re-centres the SOTA and the thesis direction on the actual sensors**, and folds in three research threads run in this iteration that the prior docs did not cover:

1. **Pléiades Neo** as a first-class sensor (it was a single vendor footnote before).
2. **Cross-sensor preparation & pansharpening** for material classification (the data-engineering reality).
3. **Risk / intervention-prioritization framing** (Thomas's reframe: classify sites *by risk*, not just detect them).

> Companion raw research (with full source lists) in this folder: `research_pleiades_neo.md`, `research_crosssensor_pansharpening.md`, `research_risk_framing.md`. Loop status in `00_LOOP_LOG.md`.

---

# 1. The reconciled data reality (state this clearly to the prof)

| Sensor | Pan | MS | Bands | SWIR | Role in the thesis |
|---|---|---|---|---|---|
| **WorldView-3** | 0.31 m | 1.24 m | 8 VNIR (+ Yellow, NIR2) | **8 SWIR @ 3.7 m** | the **spectral-evidence** sensor — only source of true material fingerprints |
| **Pléiades Neo** | 0.30 m | 1.2 m | 6 VNIR (Deep Blue, Red Edge) | none | the **high-fidelity VNIR / texture** sensor (12-bit, clean Red Edge) |

**What changes vs the old SuperDove framing:**

- **SWIR is back *inside* the experimental scope** (via WV-3), not just a theoretical upper bound. This is the single biggest shift — the band-ablation can run all the way to `+SWIR` on the *real* AOI, not only as a literature citation.
- The closest precedents are **no longer "finer than us"** — they are *at our operating point*: Aguilar 2021 (WV-3 VNIR/SWIR ablation), Saba 2026 / Bonifazi 2026 (WV-3 asbestos), Widipaminto (Pléiades 2 m), CascadeDumpNet (Pléiades 0.5 m). They become **direct benchmarks**, not distant analogues.
- **Pléiades Neo is half the data and is essentially unstudied for material work** — no peer-reviewed Pléiades-Neo material-classification benchmark exists (only the Disaitek vendor claim). That is both a real gap and a clean contribution surface.

**Honest caveat to keep:** *both* VHR sensors sample material spectra at **1.2 m (VNIR)** and WV-3 SWIR at **3.7 m**. The 0.3 m panchromatic gives *texture*, not *spectrum*. So at the pixel a waste pile is already a **mixture** — "material discrimination" here means broadband/coarse-spectral material classes, not lab-grade polymer identity. Say this before the prof says it.

---

# 2. Sharpened thesis direction (within Thomas's scope)

## 2.1 The problem (Thomas's reframe, now literature-backed)

Not "detect more sites" — **identify sites and classify them by risk to give ARPA intervention priority.** Knowing *what a site is made of* (material) drives the risk tier. This is now anchored, not rhetorical:

- **Risk is an established, Italian, regulatory construct.** Fazzo et al. 2020 ("Land of Fires", Campania) gives the citable template: `risk = hazard(material × disposal type) × exposure(proximity to water/population/agriculture) × magnitude(area)`. Every prior risk index **takes the hazard term as given (from ground records)** — none derives it from imagery.
- **The hazard term is legally codified**: European List of Waste (Decision 2000/532/EC, Directive 2008/98/EC). Asbestos = `17 06 05*` (absolute hazardous); inert C&D = `17 01 / 17 05` (non-hazardous). So "asbestos/hazardous = urgent, inert = low" is **regulatory**, not arbitrary.
- **ARPA already triages this way**: PRAL (Piano Regionale Amianto Lombardia) ranks asbestos roofs by the *Indice di Degrado*; D.Lgs 152/2006 mandates site-specific risk analysis for contaminated sites. The thesis's asbestos pilot literally feeds the same `Mappatura_2020` workflow ARPA uses.
- **PERIVALLON lists "real-time risk assessment" and "characterisation of sites of interest"** as platform capabilities → the end-user pull is *triage*, and the missing input is *characterisation*, which is exactly what MS material classification supplies.

**The contribution junction (citable):** *prior art either detects sites (RGB DL baselines, PERIVALLON CV tool) or ranks known sites by GIS exposure (Fazzo 2020, AHP siting literature) with hazard supplied externally. This work closes the loop — **multispectral material discrimination → EWC-aligned hazard class → exposure-weighted risk tier → intervention priority** — supplying the hazard term every prior risk index assumes.* (Hedge as "to our knowledge".)

## 2.2 The core measurement (Thomas's "added value of MS vs RGB")

The data hands us a **clean, three-step ablation** that *is* the research question, now extended:

```
RGB  →  +RedEdge/NIR (VNIR-MS)  →  full VNIR (8-band WV-3)  →  +SWIR (WV-3 3.7 m)
```

Two extra axes the data makes possible:

- **WV-3 (full VNIR+SWIR) vs Pléiades Neo (VNIR-only)** at near-identical GSD → quantifies the *marginal value of SWIR* directly, on the same task. This is a stronger, harder-to-dismiss version of "RGB vs MS".
- **Native-MS vs pansharpened control** → measures whether resolution-enhancement helps or hurts *material* accuracy (see §3). This is itself a publishable result.

The yardstick from the literature for "what SWIR buys": **Aguilar 2021** (WV-3, OA 90.85% VNIR / 96.79% SWIR / 97.38% all) and **Saba 2025** (asbestos, HS 97.3% vs MS 74.4%). These are now *comparable*, not aspirational.

## 2.3 The honest object-vs-material split (keep — it governs feasibility)

At sub-metre broadband VNIR, a class is feasible if its identity is in **shape/context**, weak if in **spectral chemistry**:

- **Detectable by shape (VHR-friendly):** vehicles/ELV, tanks/cisterns, containers, rubble/C&D heaps, bulky items, firewood, tyres, big bags.
- **Need SWIR or finer spectral (where WV-3 SWIR earns its place):** asbestos-cement, plastic polymer type, foundry slag, sludge, scrap composition.

This split is the bridge between "detection" (shape) and "risk/material" (chemistry) — and it's exactly where SWIR (WV-3) is the experimental differentiator.

---

# 3. Data-engineering reality (the part that protects the result)

These are decisions that, if wrong, silently corrupt the MS-vs-RGB deltas. From `research_crosssensor_pansharpening.md`:

1. **Classify on native-MS reflectance, not pansharpened bands.** Pansharpening injects pan *space*, not *spectrum*; per-pixel material decisions on pansharpened bands trust radiometry that was interpolated. Use 0.3 m pan for **texture / object boundaries** only.
2. **If pansharpening is used, use MRA/MTF methods (MTF-GLP-HPM), never GS/IHS/Brovey** — component-substitution methods maximise spectral-angle (SAM) distortion, the exact thing material classification keys on. Report SAM/ERGAS/Q2n so distortion is auditable.
3. **Surface reflectance is mandatory and must use one consistent engine** (FLAASH or 6S) on *both* sensors — don't mix vendor-SR with self-computed-SR, or cross-sensor comparisons are meaningless.
4. **Co-registration to a shared AOI grid is a first-order risk.** Neo (0.3 m) and WV-3 SWIR (3.7 m) differ >10× in footprint; sub-pixel mis-alignment corrupts every per-pixel spectral comparison. Budget real effort here.
5. **Use the two sensors as co-registered parallel strata, not one melted cube:** PNeo = dense VNIR + 0.3 m pan; WV-3 = the SWIR (+Yellow/NIR2) increment. Fuse at the *feature/decision* level. The Red-Edge and NIR bands are near-identical across the two sensors (lucky), so the VNIR ablation transfers cleanly and enables a cross-sensor robustness check.
6. **Down-sample by area-weighted averaging; never bilinear up-sample SWIR into the VNIR grid** for spectral features (it fabricates sub-pixel reflectance).

**Band correspondence (verified centres):** Coastal/Deep-Blue, Blue, Green, Red, Red-Edge, NIR match across both; **WV-3 only**: Yellow, NIR2, and the 8 SWIR bands. Apply SBAF on the matching pairs (largest correction on the Coastal/Deep-Blue pair).

---

# 4. What to change in the prof deck (concrete)

Mapped to the existing deck-rework directive (`docs/01_calls/call_sota_revision.md`):

- **Problem slide (S2):** lead with the **risk-tiering** framing + the `risk = hazard × exposure × magnitude` equation; cite Fazzo 2020 + EWC + PRAL so it reads as operational, not academic. "Material is the hazard term every risk index currently assumes."
- **Sensors slide (S12):** replace the "SuperDove sweet spot" message with the **two-sensor reality** — WV-3 (spectral evidence, incl. SWIR) + Pléiades Neo (VNIR fidelity/texture). Honest: both sample spectra at 1.2 m; SWIR at 3.7 m.
- **"Beyond RGB" split (S4a/S4b):** S4b (commercial VHR) now includes our *actual* sensors as benchmarks — Aguilar/Saba/Bonifazi (WV-3), CascadeDumpNet/Widipaminto (Pléiades).
- **Gaps slide (S16):** keep "material-level labels missing" first; **add** "no peer-reviewed Pléiades-Neo material benchmark" and "no pipeline derives EWC hazard from MS for risk tiering".
- **Proposed direction (S17):** the three-axis ablation (RGB→VNIR→+SWIR; WV-3 vs PNeo; native vs pansharpened) → material → risk tier. Phase-1 asbestos pilot = the **risk-tier demonstrator** (feeds PRAL/Indice di Degrado).
- **New micro-slide (optional):** the data-prep guardrails (native-MS, MRA pansharpening, surface reflectance) — shows methodological maturity the prof rewards.

---

# 5. Open questions for Thomas / Fraternali (need answers before locking the design)

1. **WV-3 product:** VNIR-only, or **VNIR + 8 SWIR bands**? (Decides whether the `+SWIR` ablation axis is real — the strongest part of the design.)
2. **Pléiades Neo product:** native Bundle (1.2 m MS + 0.3 m pan) or pansharpened only? (Decides whether we *can* classify on native MS.)
3. **AOI:** which Lombardia municipality/extent — and does it overlap **AerialWaste** positives and/or the **`Mappatura_2020`** asbestos roofs? (No overlap = no labels = no supervised experiment.)
4. **SuperDove:** still in the picture (free, near-daily, 3 m) as a third/cheaper sensor or a temporal layer, or dropped in favour of the two VHR sensors?
5. **Risk-tier scope:** does the thesis go all the way to a *risk tier* output (material → EWC hazard → tier), or stop at material classification and frame risk as the motivation only?
6. **Labels:** do we get any material-level labels with the imagery, or is it self-annotation against AerialWaste object categories + the asbestos WFS?

---

# 6. One-paragraph summary (for the weekly report to Fraternali)

> Con i dati confermati (WorldView-3 + Pléiades Neo, entrambi sub-metro), la SOTA è stata ri-centrata sui sensori reali: lo SWIR rientra nello scope sperimentale (via WV-3), i precedenti più forti (Aguilar, Saba, Bonifazi, CascadeDumpNet) diventano benchmark diretti, e Pléiades Neo — metà dei dati — risulta privo di benchmark material peer-reviewed (gap + opportunità). La domanda "valore aggiunto del multiband sul RGB" diventa un'ablazione a tre assi (RGB→VNIR→+SWIR; WV-3 vs Pléiades Neo; nativo vs pansharpened) che alimenta la classificazione del materiale e, da lì, una **classificazione per rischio** ancorata al quadro normativo (List of Waste / EWC) e alla pratica ARPA (PRAL, Indice di Degrado) — il termine "hazard" che ogni indice di rischio oggi dà per scontato.
