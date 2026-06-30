# Deck revision — 2026-06-30 (WV-3 + Pléiades Neo direction)

**Base:** `ultime_slide.pptx` (19 slides, 16:9) · **Target:** the confirmed experimental data
**WorldView-3 + Pléiades Neo** (sub-metre VHR, SWIR back in scope) with the
**risk-classification** framing Thomas asked for. Backed by `docs/02_research/loop_prof_sota/`.

Register: B/N, didactic, English. "generalizzazione" (not "OOD"). Define EO/MS/HSI/VNIR/SWIR/GSD on first use.
This is paste-ready content for Google Slides — verdict per slide: **KEEP / EDIT / REPLACE / NEW / CUT**.

---

## Why this revision (the one-line diagnosis)

The current deck makes **SuperDove the chosen sensor** (VNIR-only) and treats **SWIR as a future horizon**.
Thomas confirmed (27 Jun) the real experimental data is **WV-3 (8 VNIR @1.24 m + 8 SWIR @3.7 m) + Pléiades Neo
(6 VNIR @1.2 m, no SWIR)**. So: **SWIR is now IN scope**, the experiment becomes a **cross-sensor** comparison,
and the spine adds **material → hazard → ARPA priority**. Slides 1-8 survive; the sensor/experiment half (9, 12, 14, 15, 18, 19) is rebuilt.

**One open flag for Thomas (was open question #5):** SuperDove is here **demoted** to an optional *free wide-area
screening layer*, not the thesis sensor. If Thomas wants it dropped entirely, cut every SuperDove mention — trivial.

---

## New structure at a glance (20 slides)

| # | Title | vs current |
|---|---|---|
| 1 | Title | KEEP |
| 2 | The problem: priority, not just presence — *classify by risk, not only detect* | EDIT |
| 3 | Not all waste is equal: risk = hazard × exposure × magnitude | **NEW** |
| 4 | Today's paradigm: RGB deep learning detects sites, not materials | EDIT (was S3) |
| 5 | A satellite pixel is a spectrum, not just a colour | EDIT (was S4) |
| 6 | From bands to information: three views of the same scene | KEEP (was S5) |
| 7 | Every material has a spectral fingerprint | KEEP (was S6) |
| 8 | RGB fails in two distinct ways (iso-chromaticity + sub-pixel mixing) | MERGE S7+S8 |
| 9 | The sensor trade-off: spatial × spectral × revisit | EDIT (was S9) |
| 10 | Low/medium resolution (10-30 m): too coarse for material | EDIT (was S10+S11) |
| 11 | **The chosen data: WorldView-3 + Pléiades Neo** | **REPLACE** (was S12) |
| 12 | Spectral added value, measured: direct precedents to benchmark | EDIT (was S13) |
| 13 | More bands ≠ more — SWIR carries the jump, and WV-3 has it | EDIT (was S14) |
| 14 | Honest caveat: resolution is split between texture and chemistry | **REPLACE** (was S15 SuperDove) |
| 15 | Foundation models for EO: a new lever | KEEP (was S16) |
| 16 | DOFA: a band-agnostic backbone that makes the comparison fair | EDIT (was S17) |
| 17 | Gaps in the literature — and the test that matters | EDIT (was S18) |
| 18 | **The experiment: a 3-axis band ablation** | **NEW** |
| 19 | From material to risk tier — and the asbestos pilot | REPLACE (was S19) |
| 20 | What's novel · what to confirm with Thomas | **NEW** |

---

## Slide-by-slide content

### S1 — Title · KEEP
No change. (Optional subtitle tweak: "State of the art and thesis direction — WV-3 + Pléiades Neo".)

### S2 — The problem: priority, not just presence · EDIT
- Illegal waste dumping is an environmental crime and a public-health issue.
- Agencies such as ARPA cannot inspect everything — they must **prioritise**, and priority depends on the **material** (the hazard).
- Today's automated pipelines find sites well; they classify **presence, not what is there**.
- **Research question:** *what is the added value of multispectral (MS) data, vs RGB only, for waste **material** classification from satellite imagery?*
- *Footer:* Framing distilled from Fraternali et al. 2024 (PoliMi survey, arXiv:2402.09066).

### S3 — Not all waste is equal: risk = hazard × exposure × magnitude · NEW
- The danger is **material-bound**: inert rubble vs plastics vs **asbestos-cement** are worlds apart.
- "Material" carries the **hazard**; the European Waste Catalogue (EWC) flags hazardous codes with `*` — asbestos = **17 06 05\***.
- Priority **risk = hazard (material) × exposure (who/what is nearby) × magnitude (how much)**.
- Goal: turn imagery into an **actionable ARPA priority list** — computer vision as **decision support**.
- *Footer:* EWC List of Waste (Dec. 2000/532/EC); Indice di Degrado d.d.g. 13237/2008; Fazzo et al. 2023.

### S4 — Today's paradigm: RGB deep learning detects sites, not materials · EDIT (was S3)
- Pipeline: VHR RGB tile → CNN/Transformer → EO pretraining → two-step fine-tune → binary waste.
- Accurate **within the geographic context it was trained on** (Gibellini 2025: F1 **92.0%**).
- But: classifies **presence, not material**; tied to **colour only**; **generalizzazione** collapses across a new region (**-5.1% F1**) or a new sensor.
- These limits motivate looking at the **spectrum**.
- *Footer:* Gibellini et al. 2025; Fraternali et al. 2024.

### S5 — A satellite pixel is a spectrum, not just a colour · EDIT (was S4)
- Each pixel is a vector of reflectance values — the material's **spectral signature**.
- **RGB:** 3 broad visible bands (colour only). **MS (multispectral):** 4-15 chosen bands. **HSI (hyperspectral):** hundreds of contiguous narrow bands.
- Our sensors: **WorldView-3 = 8 VNIR + 8 SWIR**; **Pléiades Neo = 6 VNIR**. *(was "SuperDove records 8")*
- This vector is the raw input from which any classifier reasons.
- *Footer:* Spectrum schema after USGS splib07a (Kokaly et al. 2017).

### S6 — From bands to information: three views of the same scene · KEEP (was S5)
No change (RGB / false-colour IR / NDVI).

### S7 — Every material has a spectral fingerprint · KEEP (was S6)
No change — USGS splib07a curves (asbestos vs concrete vs vegetation), VNIR/SWIR shaded.

### S8 — RGB fails in two distinct ways · MERGE (was S7 + S8)
- **(1) Iso-chromaticity:** same colour, different materials — HDPE plastic ≈ asbestos-cement roof ≈ light concrete slab.
- **(2) Sub-pixel mixing:** a 10-30 m pixel rarely holds one pure material; a mix of two endmembers can land on the magnitude of a third.
- Both are **invisible without spectral information**; only SWIR features (C-H, Mg-OH, C-O-C) keep the materials separable.
- *Footer:* Tasseron 2021 · Aguilar/Uhrin 2025 · USGS splib07a.

### S9 — The sensor trade-off: spatial × spectral × revisit · EDIT (was S9)
- Three axes, one photon budget — no satellite maximises all three. **(Keep the radar chart.)**
- **WorldView-3** — 1.24 m VNIR + **3.7 m SWIR**, 16 bands · tasked, commercial — *our chemistry sensor*.
- **Pléiades Neo** — 1.2 m, 6 VNIR, no SWIR · tasked, commercial — *our cross-sensor (VNIR-only) control*.
- *Sentinel-2* — 10-20 m, 13 bands, free — too coarse for material. *EnMAP/PRISMA* — 30 m hyperspectral — resolves the 2.3 µm triplet but too coarse.
- *SuperDove* — 3 m, 8 VNIR, near-daily, free — optional **wide-area screening** layer.
- *Footer:* Specs: Maxar, Airbus, ESA, ASI, DLR, Planet (mission docs).

### S10 — Low/medium resolution (10-30 m): too coarse for material · EDIT (was S10 + S11)
- Keep the table (Sentinel-2 / EnMAP). Detection works where the signal fits 10-30 m pixels; **material identity stays out of reach**.
- **MARIDA** (Kikaki 2022): marine debris confused with natural organic matter where pixels mix.
- **Sun 2023**: dumpsite *locations* across 28 cities detected — but material identity unknown.
- **Tisza** (Magyar 2023): change detection works; per-tile post-processing still needed.
- *Takeaway:* low-res answers "where", not "what" → we need VHR.
- *Footer:* Kikaki 2022 PLOS ONE · Sun 2023 Nat. Commun. 14:1565 · Magyar 2023 · Shepherd 2025 Sci. Rep.

### S11 — The chosen data: WorldView-3 + Pléiades Neo · REPLACE (was S12)
**Two spec cards side by side (this is the new core sensor slide):**

| | **WorldView-3** | **Pléiades Neo** |
|---|---|---|
| VNIR | 8 bands @ **1.24 m** | 6 bands @ **1.2 m** |
| SWIR | **8 bands @ 3.7 m** ✓ | none ✗ |
| Pan | ~0.31 m | ~0.30 m |
| Unique bands | Yellow, NIR2 | Deep Blue |
| Role in thesis | **full ladder incl. chemistry (R3)** | **VNIR-only cross-sensor axis** |

- Both **sub-metre VHR**; access feasible **for free** via ESA Third-Party Missions (~9-week proposal lead + 1-yr quota).
- WV-3 is **rare civilian SWIR at high resolution**; Pléiades Neo tests *how far VNIR-only gets*.
- *Footer:* Maxar WV-3 spec; Airbus Pléiades Neo spec; ESA TPM.

### S12 — Spectral added value, measured: direct precedents · EDIT (was S13)
- **Aguilar 2021** — WV-3 VNIR vs +SWIR ablation (greenhouse plastic): OA **90.85 → 96.79 → 97.38** — SWIR carries the jump.
- **Saba / Bonifazi** — WV-3 for **asbestos-cement** roof detection (Saba VNIR Macro-F1 ~97.6%, per-pixel).
- **CascadeDumpNet (Zhang & Ma 2024)** — waste-dump detection on **Pléiades**.
- From vague inspiration to **direct comparison points**.
- *Footer:* Aguilar et al. 2021 RS 13(11):2133 · Saba/Bonifazi 2026 · Zhang & Ma 2024.

### S13 — More bands ≠ more — SWIR carries the jump, and WV-3 has it · EDIT (was S14)
- **Aguilar 2021** (WV-3 plastic): VNIR 90.85 → All 97.38 — **SWIR carries the jump**.
- **Vitek 2025** (C&D waste): RGB + 2 narrowbands ≈ HSI 768 bands.
- **Zhou 2021** (WV-3 plastic): 8 SWIR bands separate 3 polymer clusters.
- *Flip vs old deck:* what matters is **which** bands. SWIR is the most informative region — and **WV-3 gives us SWIR**; **Pléiades Neo (VNIR-only) measures how far we get without it.**
- *Footer:* Vitek et al. 2025 (CTU Prague) · Aguilar et al. 2021 · Zhou et al. 2021.

### S14 — Honest caveat: resolution is split between texture and chemistry · REPLACE (was S15 SuperDove)
- Material **spectra** are sampled coarsely — VNIR ~1.24 m, **SWIR ~3.7 m** (~14 m² pixels, no pure pixels over a dump).
- The **pan** band gives fine texture/shape ~0.3 m — but **no material information alone**.
- A small dump can be *seen* (texture) more easily than *chemically identified* (spectra) — a real tension.
- ⚠ **SWIR-8 bottleneck:** asbestos 2.32 + concrete 2.34 + plastic 2.31 crowd into one WV-3 band → discrimination leans on shoulders (2.16/2.20/2.26, 1.21/1.73) + VNIR shape.
- *Honest:* at 3.7 m + atmosphere, the SWIR feature is attenuated — **R3 may ≈ R2; that is itself a valid finding.**
- *Footer:* Maxar radiometric note; USGS splib07a.

### S15 — Foundation models for EO: a new lever · KEEP (was S16)
No change. (2024-25 wave; most pretrained at 10-30 m → transfer to VHR not guaranteed; sensor-agnostic vs adapters.)

### S16 — DOFA: a band-agnostic backbone that makes the comparison fair · EDIT (was S17)
- **Dynamic-One-For-All** (Xiong et al. 2024): a hypernetwork generates patch-embedding weights from each band's **central wavelength**.
- One backbone fairly ingests **WV-3 (16 b)**, **Pléiades Neo (6 b)**, S-2, or HSI — so **RGB vs VNIR vs SWIR is apples-to-apples, not apples-to-oranges**.
- Natural fit for the band-ablation study; pairable with a **DEFLECT** adapter (<1% params) for cheap spectral fine-tune.
- RGB-era reference baseline: **Swin-T + RSP**.
- *To verify:* does 10-30 m pretraining close the gap to ~1.2 m? — open, empirical.
- *Footer:* Xiong et al. 2024 (arXiv:2403.15356) · Thoreau et al. 2025 (DEFLECT, ICCV).

### S17 — Gaps in the literature — and the test that matters · EDIT (was S18)
- **No public VHR dataset** pairing waste sites with **material labels**; **no peer-reviewed Pléiades-Neo material benchmark** exists.
- RGB pipelines **conflate iso-colour, chemically distinct materials**.
- No pipeline goes from **spectra to a regulatory hazard class** (material → EWC → risk tier).
- The **object-vs-material** split is unaddressed; **generalizzazione** (cross-region/sensor/time) is rarely shown.
- **The test that matters:** *how much does multiband actually beat RGB for material — and where does it stop helping?*
- *Footer:* Gap list distilled from Fraternali et al. 2024 (arXiv:2402.09066).

### S18 — The experiment: a 3-axis band ablation · NEW
**The core novelty — a cube/matrix:**
- **Axis A — spectral content:** R0 RGB → R1 +RedEdge/NIR → R2 full VNIR → **R3 +SWIR** (WV-3 only; the headline test).
- **Axis B — sensor:** WorldView-3 (with SWIR) vs Pléiades Neo (VNIR-only), on the **same physical sites**.
- **Axis C — resolution handling:** **native** bands vs **pansharpened** (the control: "SWIR helps" must hold in *native* too, not only after pan injection).
- Same **DOFA** backbone throughout; **Swin-RSP** as the RGB reference. Run each rung on a **per-pixel** baseline *and* the full CNN → **B-A = pure chemistry gain; D-C = total MS gain.**
- Report **ΔF1 vs R0** with CIs, **and the ID-vs-OOD gap per cell** (generalizzazione is first-class).
- *Footer:* Design in `loop_prof_sota/04_experimental_design.md`. Prior: Aguilar 2021 (sanity, not target).

### S19 — From material to risk tier — and the asbestos pilot · REPLACE (was S19)
**Phase 1 — asbestos pilot (run first, in full):**
- Public pixel-accurate ground truth: Lombardy WFS **Mappatura_2020 (10,903 roofs)**, EPSG:32632.
- Textbook **SWIR diagnostic** (Mg-OH ~2.30-2.33 µm) on **WV-3 SWIR-7** → the single most defensible reason WV-3 is in scope.
- Self-pair roofs → surface reflectance → per-roof signatures → **unsupervised clustering (no labels)** → **decision gate:** do AC clusters form *only* when SWIR is included? Then supervised RF/GBM ablation (RGB / VNIR / VNIR+SWIR).
- **Map positive → EWC 17 06 05\* → risk = hazard × exposure × magnitude → ARPA priority.** (Note: Indice di Degrado is **not** in the WFS → estimated remotely = a contribution.)

**Phase 2 — multispectral waste benchmark:**
- Co-register AerialWaste polygons with the VHR archive *(coordinate bridge with ARPA = open dependency)*; material-level labels where available.
- The **3-axis ablation** (S18) + cross-region / cross-time / cross-sensor splits; DOFA backbone.
- *Footer:* Pilot GT: Mappatura_2020 (Lombardia WFS) · Backbone: DOFA (Xiong 2024) · Baseline ref.: Gibellini 2025.

### S20 — What's novel · what to confirm with Thomas · NEW
**Novel contributions (map each gap → contribution):**
- First to **measure** RGB vs VNIR vs SWIR added value for **waste material at VHR**.
- First **WV-3 vs Pléiades Neo** head-to-head for this task.
- First to connect **spectra → EWC hazard → ARPA risk tier**; confidence-aware (reports where MS helps *and where it doesn't*, incl. generalizzazione).

**To confirm with Thomas (the decision checklist):**
- Trigger the **ESA TPM** proposal now (~9-wk lead)? AOI / scene selection over Lombardia?
- Risk-chain depth: full Indice di Degrado / PRAL formalization, or stop at material + EWC?
- **SuperDove:** kept as a free wide-area screening layer, or dropped?
- Ablation depth: 3 axes as designed, or trim for time?
- Backbone: **DOFA primary + Swin-RSP RGB reference** — agreed?

---

## Honesty guardrails (keep audible throughout)
- Multiband value is **measured, not assumed** — and explicitly **bounded** (SWIR earns its keep on chemistry; detection may need little beyond RGB).
- Spectra at 1.24 m / 3.7 m vs pan at 0.3 m = **texture, not chemistry**; SWIR carries chemistry but **Pléiades Neo has none**.
- No public VHR+waste+material dataset; **no peer-reviewed Pléiades-Neo material benchmark**.
- "generalizzazione", not "OOD". Unmixing = out of scope (it sets the ceiling).

## Don't-quote-as-fact (downgraded in research)
- Aguilar "+14% kappa" (use OA only) · Saba "HS 97.3 vs MS 74.4" (paywalled) · Bonifazi AC F1 0.87 · Cilia "40/86/89%" · chrysotile "~5 nm" (it's tens of nm).
