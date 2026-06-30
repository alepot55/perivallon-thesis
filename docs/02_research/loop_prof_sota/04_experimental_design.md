# Experimental Design — Added Value of Multiband (MS) over RGB at VHR for Waste Material & Risk Classification

*Autonomous research loop, iteration 2 (2026-06-27). Merged & de-duplicated from the experimental protocol and the asbestos risk-tier demonstrator. Sensors: WorldView-3 (8 VNIR @1.24 m, 8 SWIR @3.7 m, pan 0.31 m) + Pléiades Neo (6 VNIR @1.2 m, pan 0.30 m) over a Lombardia AOI. Imagery is unlabeled → self-paired with external geolocated labels.*

**Core hypothesis** — H0: RGB is sufficient · H1: added bands (RedEdge/NIR → full VNIR → SWIR) improve **material/risk** discrimination — tested by controlled band ablation with everything else held fixed.

---

## 0. Guiding design principles

- **One variable at a time.** Backbone, input GSD, augmentation, optimizer, label set frozen across an ablation axis; only the band subset changes. Report Δ vs the RGB anchor with CIs, not absolute numbers alone.
- **Resolution confound is the enemy.** SWIR (3.7 m) and pansharpened products differ from native VNIR (1.24 m) in *both* spectra and GSD. Every "added-band" claim is paired with a resolution control (§3) so a gain is not silently a resolution artefact — the most common reviewer objection in VHR-MS waste work.
- **Generalization is first-class.** Per Thomas ("generalizzazione fa schifo"), report ID-vs-OOD gap for every band cell (§5).
- **Pre-register.** Freeze splits, ≥3 seeds, and the metric table before looking at test results; report mean ± std (rung-to-rung deltas are small).
- **Spectra vs texture must be separable.** Always include a spatial-context-free spectral baseline so an MS gain can be attributed to material chemistry vs object/colour cues (§4, §6).

---

## 1. The band ladder (the independent variable)

Center wavelengths (µm) for wavelength-conditioned models. WV-3 ranges **[HIGH]** (Maxar radiometric note, centers = midpoints); PNeo centers **[MEDIUM]** (vendor ranges).

**WV-3 VNIR:** Coastal 0.425 · Blue 0.480 · Green 0.545 · Yellow 0.605 · Red 0.660 · RedEdge 0.725 · NIR1 0.833 · NIR2 0.950.
**WV-3 SWIR:** 1.21 · 1.57 · 1.66 · 1.73 · 2.16 · 2.20 · 2.26 · 2.33.
**PNeo VNIR:** DeepBlue 0.425 · Blue 0.483 · Green 0.562 · Red 0.655 · RedEdge ~0.725 · NIR ~0.840.

**Canonical rungs (nested ladder, same definition for both sensors):**
| Rung | WV-3 | PNeo | Note |
|---|---|---|---|
| **R0 RGB** | B,G,R | B,G,R | anchor / null hypothesis |
| **R1 +RedEdge/NIR** | R0 + RedEdge,NIR1 | R0 + RedEdge,NIR | cheap bands most sensors have |
| **R2 full VNIR** | all 8 | all 6 | coastal/yellow/NIR2 extras |
| **R3 +SWIR** | 16-band | — (no SWIR) | WV-3 only; the **headline test**. The PNeo asymmetry is itself a finding |

**Literature prior (sanity, not target) [MEDIUM transferability]:** Aguilar 2021 WV-3 plastic-greenhouse ablation — VNIR ≈ 90.85, VNIR+SWIR ≈ 96.79, +pansharpen ≈ 97.38 — SWIR adds the largest single jump.

---

## 2. Three-axis ablation

- **Axis A — spectral content (primary):** R0→R1→R2→R3 on WV-3; R0→R2 on PNeo. Identical model, common working grid.
- **Axis B — sensor comparison (VNIR-only, matched):** WV-3 VNIR (R2) vs PNeo VNIR (R2) on the *same physical sites*. Resample both to common GSD; treat PNeo DeepBlue ≈ WV-3 Coastal; note PNeo lacks Yellow/NIR2. Isolates DeepBlue/SNR effects independent of SWIR.
- **Axis C — native vs pansharpened (resolution control):** for each spectral cell produce **C-native** (bands at native GSD, bilinear to working grid, no pan injection) and **C-pansharp** (pansharpened to ~0.3 m via a fixed documented algorithm). **Critical control: pansharpened SWIR** — "SWIR helps" is only credible if it helps in C-native too, not only after pan injection. Use ≥2 fusion algorithms (one component-substitution e.g. GS/Brovey, one MRA/CNN e.g. ATWT/PNN); select the operational one by §7.3 metrics; report the alternative in an appendix.

---

## 3. Stem strategy (itself a confound — report it)

Two fairness protocols; pick per model family:
- **(A) Re-instantiate stem per rung** — patch-embed resized to `in_chans = len(rung)`, downstream identical. Cleanest "is the information there?" Use for CNN-scratch, SpectralFormer, DOFA, and supervised Swin adapters.
- **(B) Fixed N-channel stem + band masking** — build the 16-ch stem once, zero absent channels. Confounds capacity with information → **secondary sanity check only**; required for the fixed-template FMs (Prithvi).

For Swin-T+RSP report all three adapter strategies for R1–R3 (`weight_inflation` headline, `late_fusion` for R3, `random_init_extra` robustness) since the stem strategy is a confound. Keep the two-step TL→FT Gibellini schedule unchanged across rungs.

---

## 4. Tasks

| Task | Label source | Output | Notes |
|---|---|---|---|
| **T1 Binary detection** | AerialWaste v3 positives (coords withheld → §6) + DroneWaste; AOI negatives | waste / no-waste, tile | detection floor; mirrors existing Swin-T+RSP 95.2% F1 RGB |
| **T2 Material multi-class** | AerialWaste 22 categories → coarse risk-relevant groups (plastic, C&D/inert, organic, metal, hazardous/asbestos, mixed) | per-tile/region class | **core MS-value task** — material is where extra bands pay off |
| **T2-risk Risk tier** | derived material → ARPA priority (high/med/low) | ordinal | the deliverable Thomas/ARPA cares about; ordinal-aware metrics |
| **T3 Asbestos pilot** | Lombardy WFS `Mappatura_2020` (10,903) + `Mappature_precedenti` (50,131), EPSG:32632 | AC-roof / not + weathering | **anchor experiment** — public pixel-accurate labels, unambiguous self-pairing |

**T3 is run FIRST and in full.** It is the only sub-problem where geolocated public labels coincide with the confirmed VHR imagery, on a material with a textbook SWIR diagnostic. It validates the entire self-pairing→spectra→classify→risk pipeline before AerialWaste coordinates are ever needed, and is a publishable mini-result in itself.

---

## 5. Self-pairing & splits

**Self-pairing (the hard data problem):**
- **T3:** direct spatial join — WFS polygons (EPSG:32632) ∩ imagery footprints; buffer-erode roofs ~1 px (avoid mixed edges), rasterize to masks, tile. Straightforward, no reprojection.
- **T1/T2:** AerialWaste coordinates **withheld (ARPA confidentiality)**. Routes: (a) ~250 WV-3-origin positives are RGB-pansharpened tiles → bound T1 only, not the MS ablation; (b) negotiate an ARPA coordinate-bridge for a matched held-out subset. **Flag as an open dependency: the general-waste MS ablation is only as strong as the geolocated label coverage obtained.**
- **DroneWaste (RGB, 20 materials):** label-space definition + RGB-only material sanity set; not in the MS ablation.

**Splits — make generalization a reported axis:**
1. **ID:** spatially-blocked (grid/cluster, **never random tile** — adjacent tiles leak), 60/20/20, stratified by class and source sensor.
2. **Cross-region (spatial OOD):** train provinces A, test held-out province B, zero overlap — the headline generalization number.
3. **Cross-time (temporal OOD):** train date D1, test D2 (different season/illumination) — directly probes the robustness Thomas flagged.
4. **Cross-sensor (transfer):** train WV-3 VNIR, test PNeo VNIR (and reverse) at matched bands — does an MS model transfer or overfit one instrument's calibration?

**Report ID-vs-OOD ΔF1 for every band cell.** Whether added bands *narrow or widen* the generalization gap is a publishable finding either way (physically-grounded transferable features vs sensor-calibration overfit).

---

## 6. Honest caveats (instrument the experiments to expose them)

- **Object-vs-material confound.** A VHR model can "detect waste" from object/context cues (piles, tarps, vehicles) not material spectra. The per-pixel spectral baseline (§7.1) measures material separability with spatial context removed; if MS gains survive there, the gain is chemistry — if only the spatial CNN benefits, it is texture/colour. Say which.
- **Mixed pixels.** Even at 1.24 m, waste sites are spectral mixtures; SWIR at 3.7 m is strongly mixed. Keep unmixing **out of experimental scope** (per project principles) but acknowledge it bounds material purity; for SWIR cells report native 3.7 m vs upsampled; use USGS splib07a / asbestos endmembers only for **interpretation** (band-importance/SHAP), not as a classifier.
- **Label noise & scale mismatch.** WFS polygons and AerialWaste tile labels live at different scales than 1.24 m pixels — document rasterization/buffer choices and run a buffer ±1 px sensitivity check.

---

## 7. Baselines, backbones, metrics

### 7.1 Backbones (run R0–R3 on all, so the conclusion is not backbone-specific)
- **Swin-T + RSP (extended)** — existing baseline, strong VHR prior; `swin_ms_adapter` strategies per §3.
- **DOFA** — wavelength-conditioned; feed actual centre wavelengths per cell; the structurally-fair FM spine.
- **CNN from scratch** — unbiased info-content control (RGB & MS start equal).
- **SpectralFormer (Band-Embedding mode)** — fine spectral structure; spectra-only argument.
- **Per-pixel spectral baseline (RF/SVM on band vectors, no spatial context)** — the lower bound that isolates pure spectral separability. **Mandatory** — it directly answers "signal in spectra or in texture?".
- *(R3 SWIR specialist point:* Prithvi-EO-2.0 via fixed 6-band mapping, WV-3 only.)

### 7.2 Downstream metrics
- **T1:** F1, P/R, mAP (if boxes), AUROC.
- **T2 / T2-risk:** macro-F1 **and per-class F1** (mandatory — MS value concentrates in 1–2 hard materials, washed out by OA), OA, confusion matrices; for risk tiers add **quadratic-weighted κ** and ordinal MAE.
- **Headline:** **ΔF1 / Δmacro-F1 vs R0**, per backbone, bootstrap 95% CI + paired significance (McNemar binary, paired bootstrap macro-F1) so "MS helps" is statistically defensible.

### 7.3 Pansharpening quality gate (before classification, Axis C)
Reduced-resolution (Wald protocol) + full-resolution: **SAM** (spectral fidelity — key for material work), **ERGAS**, **Q2n**, SCC, and full-res **QNR / Dλ / Ds**. Only the algorithm passing the low-SAM bar is used for C-pansharp downstream, since spectral distortion would corrupt a material conclusion.

---

# Part II — Asbestos Risk-Tier Demonstrator (T3 in detail)

The Phase-1 pilot. The clean, regulator-relevant testbed with a textbook SWIR diagnostic. Local assets ready: `asbestos/data/mappatura_2020.gpkg`, `mappature_precedenti.gpkg`, `aree_mappature_2020.gpkg`; reference signatures `spectral/`; notebook `asbestos/notebooks/05_amianto_briefing.ipynb`.

## 8. Pipeline

```
Mappatura_2020 polygons (EPSG:32632, 10,903 roofs)
  │ spatial filter to imagery footprint + geometry QA (drop slivers <~4–9 px on SWIR,
  │ fix invalid geoms, buffer-erode ~1 px, log positional-accuracy flag)
  ▼
Self-pairing: clip each roof onto WV-3 (8 VNIR @1.24m + 8 SWIR @3.7m) & PNeo (6 VNIR @1.2m)
  │ convert DN → SURFACE REFLECTANCE (vendor SR / empirical-line / dark-object) — MANDATORY
  │ keep SWIR native; do NOT upsample before computing stats
  ▼
Per-roof spectral feature vector (median[primary]/mean/std per band + indices)
  ├─► (A) UNSUPERVISED: SAM vs reference endmembers + k-means/HDBSCAN
  │        → does the AC cluster separate ONLY when SWIR is included?
  └─► (B) SUPERVISED: RF / gradient-boost (XGBoost/LightGBM) + shallow MLP, label = WFS
           → asbestos vs non-asbestos (+ weathering / predicted-ID head)
  ▼
Map positive → EWC 17 06 05* (mirror-hazardous)
  ▼
Risk tier = Hazard × Exposure × Magnitude → ARPA intervention priority
```

## 9. Labels, negatives, features

- **Positives:** WFS AC-roof polygons (layer 1 "Mappatura 2020", 10,903, presence-only; layer 4 "Mappature precedenti", 50,131, with verified per-year status codes 1/2/3/4 — use these to drop roofs removed/demolished/PV-converted before the imagery date). **CORRECTION (verified, see `05_field_metadata.md`): the WFS carries NO Indice di Degrado attribute** — the degradation/condition term must be **estimated remotely** (SWIR Mg-OH depth + VNIR weathering proxy) or sourced separately. This makes the remote weathering estimator a thesis *contribution*, not a lookup; an external ID ground-truth for validation is an open item.
- **Negatives (not in WFS):** sample DBT `edificato` footprints (regional, CC-BY) not intersecting any asbestos polygon, same AOI/imagery footprint to control sensor/atmosphere; ~2:1 neg:pos.
- **Per-roof features:** **median** reflectance per band (primary — robust to mixed-edge/shadow), mean, std (heterogeneity/weathering proxy); indices: SWIR Mg-OH continuum-removed depth ~2300 nm (WV-3 only), VNIR weathering proxy (Cilia ISD), NDVI/brightness to flag vegetated/shadowed roofs for exclusion. Output `roof_id | sensor | band_stats… | indices… | wfs_label | id_degrado`.

## 10. Why this tests SWIR cleanly (the physics)

Asbestos-cement (chrysotile + Portland cement) has a **diagnostic SWIR signature**: Mg-OH ~2300 nm (chrysotile 2300–2350 nm), Fe-OH 2280–2343 nm; AC composite sits between pure chrysotile and bare cement. **WV-3 SWIR-7 (~2.33 µm) sits on this feature** — the single most defensible reason WV-3 is in scope. In VNIR/RGB, AC is separable only *indirectly* via weathering (moss/lichen greening), which is climate/age-dependent and **fails on clean/painted/new roofs** (Cilia 2015 limitation). A 2025 paper claims AC detection from **WV-3 VNIR alone** [MEDIUM, single-source — verify] — useful as the RGB-arm upper bound to beat. **[HIGH on physics; SWIR is at native 3.7 m — the old 7.5 m export cap no longer applies.]**

## 11. Modeling arms & decision gate

**Unsupervised (exploratory):** SAM each roof vs {chrysotile, cement, AC-mix, clay tile, metal, bitumen} endmembers (splib07a + project `spectral/`, convolved to each sensor SRF); cluster separately for VNIR-only vs VNIR+SWIR; quantify with silhouette / purity vs WFS labels.

**Supervised (deliverable):** RF/gradient-boost primary (interpretable importances → *which bands* carry the signal), shallow MLP secondary. **Ablation arms:** (1) PNeo VNIR, (2) WV-3 VNIR, (3) WV-3 VNIR+SWIR, (4) RGB-only floor. Identical spatially-blocked CV (group by tile/comune — non-negotiable). Compare arms *within WV-3* (VNIR vs VNIR+SWIR) to hold the sensor constant so atmospheric/BRDF differences can't masquerade as SWIR value.

> **Decision gate:** train RGB/VNIR and VNIR+SWIR arms under identical CV; compare F1/balanced-acc/AUROC and MAE/rank-corr for predicted Indice di Degrado.
> - If VNIR/RGB already separates AC well (F1 ≥ ~0.9), SWIR's *marginal* gain (ΔF1, Δ on clean/painted roofs, Δ on degradation grading) is exactly what the thesis measures.
> - If VNIR/RGB fails on clean/young roofs but VNIR+SWIR succeeds (2300 nm Mg-OH), that is the **strong positive result**: physically-grounded, transferable multiband value, not a climate-dependent shortcut.
> - The gate result determines whether SWIR is *necessary* or merely *helpful* for the broader waste-by-risk task → informs sensor/cost choices for AerialWaste-scale work.

## 12. Hazard → risk tier

- **Hazard (regulatory anchor):** AC-positive roof → **EWC `17 06 05*`** (mirror-hazardous, "construction materials containing asbestos"). **[HIGH]**
- **Risk tier = Hazard × Exposure × Magnitude:**
  - **Hazard/condition:** Regione Lombardia **Indice di Degrado** (d.d.g. 13237/2008): ID ≤25 → biennial re-eval; 26–44 → remediate within 3 yr; ≥45 → total removal within 12 mo. The RS weathering proxy (SWIR Mg-OH depth + VNIR ISD) is the remote estimator → output a **predicted-ID band**. **[HIGH thresholds]**
  - **Exposure:** buffer distance to receptors (schools/hospitals/residences, pop. density). Grounded in Fazzo et al. (residential-proximity mesothelioma risk) — **[HIGH epidemiology; the composite tiering formula is ours, informed-not-prescribed, MEDIUM]**.
  - **Magnitude:** roof area (≈ fibre-release potential) from polygon geometry.
- **Output:** Low/Medium/High/Urgent → ARPA action windows → ranked intervention list.

## 13. Demonstrator metrics
Detection: balanced-acc, F1(asbestos), P/R, AUROC, per-class PA/UA (Cilia 2015 benchmark PA 86%/UA 89%). **Added-value (primary):** ΔF1 & ΔAUROC (VNIR+SWIR − VNIR), bootstrap CIs, per-stratum (weathered vs clean, large vs small). Weathering: MAE & Spearman ρ predicted vs WFS ID, confusion across the 3 regulatory bands. Operational: sample attrition vs roof size (SWIR 3.7 m under-resolves small roofs — report and stratify); spatial-CV variance across comuni. Feature attribution: RF/SHAP confirm SWIR-7 carries the signal when SWIR helps.

## 14. What each outcome means
- **Positive:** validates the multiband thesis on a clean regulator-relevant case; transferable mechanism (Mg-OH 2300 nm), not a weathering shortcut; deployable ARPA priority map tied to EWC + legal ID windows.
- **Null (VNIR ≈ VNIR+SWIR):** still publishable — at sub-metre VHR, AC detection may ride spatial/weathering cues, SWIR's 3.7 m penalty cancelling its spectral edge; sharpens the resolution–spectral tradeoff argument and redirects waste-risk work toward sub-pixel/chemically-ambiguous materials, avoiding a costly SWIR commitment on weak evidence.
- **Either way:** the pipeline is the reusable skeleton for the AerialWaste-by-risk task once coordinates arrive.

---

## 15. Execution checklist (student-runnable)
1. Build T3 asbestos masks from WFS ↔ imagery footprints; tile at common grid. **Verify status-code semantics first.**
2. Implement §2 native/pansharp variant generator (≥2 fusion algos) + §7.3 quality metrics; pick operational pansharpener.
3. Freeze splits (ID + 3 OOD), seeds ×3, augmentation, optimizer.
4. Run **R0→R3 × {Swin-RSP, DOFA, SpectralFormer, spectral-baseline} × {native, pansharp}** on **T3 first**.
5. Tabulate ΔF1 vs R0 with CIs + significance; per-class confusion matrices; ID-vs-OOD gap table; map predicted-ID → risk tier.
6. Extend to T1/T2 to the extent geolocated labels allow (§5 dependency).
7. Run Axis B (WV-3 vs PNeo VNIR) on co-covered sites.
8. Write up: (i) does MS beat RGB and by how much; (ii) where (materials/risk tiers); (iii) survives resolution control?; (iv) helps or hurts generalization?; (v) spectral or spatial?

---

**Confidence:** design/metrics (SAM, ERGAS, Q2n, QNR, McNemar, spatial-block, Wald) = **HIGH** (standard practice). DOFA/SpectralFormer = **HIGH**. Aguilar-2021 as waste prior = **MEDIUM** (different target). EWC code + ID thresholds = **HIGH**. AerialWaste coordinate-bridge = **UNCERTAIN — open dependency, confirm with ARPA/Thomas before committing T1/T2 to the MS ablation**. WFS status-code semantics = **UNCERTAIN — verify field metadata**.

**Sources:** [DOFA 2403.15356](https://arxiv.org/abs/2403.15356) · [EWC 17 06 05*](https://dsposal.uk/ewc-codes/17/17-06/17-06-05star/) · [d.d.g. 13237/2008](https://www.regione.lombardia.it/) · [Cilia 2015, MDPI IJGI 4(2):928](https://www.mdpi.com/2220-9964/4/2/928) · [Fazzo et al. Front. Public Health 2023](https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2023.1243261/full).
