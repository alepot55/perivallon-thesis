# PERIVALLON — Prof Presentation Narrative Outline (draft)

*Autonomous research loop, iteration 3 (2026-06-27). A DRAFT narrative integrating the loop docs — to be reconciled with the existing slide-by-slide directives in `../../01_calls/call_sota_revision.md` and confirmed with Thomas (sensors/AOI/scope still open).*

**Audience:** non-specialist professor · **Register:** didactic, colorful (Fraternali) · **Language:** English
**Backbone:** (1) what is the problem → (2) why → (3) what exists → (4) what is missing → (5) what I propose & why

*Define on first use: EO = Earth Observation · MS = multispectral · GSD = ground sampling distance (keep untranslated) · VNIR = visible + near-infrared · SWIR = short-wave infrared.*

---

### PART 1 — WHAT IS THE PROBLEM

**Slide 1 — Illegal waste dumps are a hidden, widespread environmental crime**
- Lombardia/Italy face thousands of unauthorized dumping sites; many are never reported, only stumbled upon.
- ARPA must find them and decide where to send limited inspectors first.
- The operational question is not only *"where is the waste?"* but *"how dangerous is it?"* — **classify by risk** (`classificare per rischio`), not merely detect.
- *Visual:* a real satellite tile of a dump beside a clean field — how similar they look from above.

**Slide 2 — Not all waste is equal: risk = hazard × exposure × magnitude**
- The hazard depends on the **material**: inert rubble vs plastics vs asbestos-cement are worlds apart.
- "Material" carries the **hazard**; the European Waste Catalogue (EWC) assigns codes, asterisked = hazardous (asbestos **17 06 05\***).
- Priority risk = **hazard** (material) × **exposure** (who/what is nearby) × **magnitude** (how much).
- *Visual:* risk-equation graphic → ARPA priority dial.

**Slide 3 — From pixels to an intervention priority for ARPA**
- Goal: a pipeline turning imagery into an **actionable priority list** — reframing computer vision as **decision support**.
- Chain: image → material → EWC hazard → degradation/risk index (Lombardia `Indice di Degrado`, d.d.g. 13237/2008) × exposure × magnitude → ARPA priority.
- *Visual:* horizontal flow diagram of the full chain.

### PART 2 — WHY IS IT A PROBLEM

**Slide 4 — The human way does not scale**
- Today: citizen reports, ground patrols, manual photo-interpretation — slow, partial, reactive.
- Territory is vast; inspector time is the scarce resource; without **ranking**, agencies inspect blindly.
- *Visual:* map of Lombardia peppered with sites vs a handful of inspectors — the scale mismatch.

**Slide 5 — Ordinary RGB is not enough: materials need information beyond the visible**
- An RGB photo captures only what the eye sees — three broad bands.
- Many dangerous materials look almost identical in plain color (grey asbestos ≈ grey concrete ≈ grey roof).
- Telling **materials** apart often needs information **outside** the visible.
- *Visual:* side-by-side RGB crops of asbestos vs concrete, near-identical to the eye.

**Slide 6 — Materials have spectral "fingerprints" — the core scientific bet**
- Each material reflects light differently across wavelengths; diagnostic clues sit in **NIR and especially SWIR** (chemistry).
- Core bet: **multiband** imagery can discriminate materials RGB cannot — but the added value must be **measured, not assumed**, and it has limits.
- *Visual:* reflectance-curve plot (splib07a) asbestos vs concrete vs vegetation, VNIR/SWIR shaded.

### PART 3 — WHAT EXISTS TODAY

**Slide 7 — The data reality: two very-high-resolution satellites**
- **WorldView-3:** 8 VNIR @ ~1.24 m + **8 SWIR @ ~3.7 m** + pan ~0.31 m — rare civilian SWIR at high resolution.
- **Pléiades Neo:** 6 VNIR @ ~1.2 m + pan ~0.3 m — sharp, but **VNIR-only** (no SWIR).
- Access feasible **for free** via ESA Third Party Missions (~9-week proposal lead).
- *Visual:* two satellite "spec cards" side by side (bands, GSD, SWIR yes/no).

**Slide 8 — Honest caveat: resolution is split between texture and chemistry**
- Material **spectra** are sampled coarsely — VNIR ~1.2 m, SWIR ~3.7 m.
- The **pan** band gives fine **texture/shape** ~0.3 m but no material info alone.
- A small dump can be *seen* (texture) more easily than *chemically identified* (spectra) — a real tension.
- *Visual:* same scene at 0.3 m pan (crisp) vs 3.7 m SWIR (blurry but spectrally rich).

**Slide 9 — Direct precedents to benchmark against**
- **Aguilar 2021** — WV-3 VNIR vs +SWIR ablation (SWIR adds discriminative power).
- **Saba / Bonifazi** — WV-3 for asbestos roof detection.
- **CascadeDumpNet** — waste-dump detection on **Pléiades**.
- From vague inspiration to **direct comparison points**.
- *Visual:* 3-card "precedents" row (sensor + task + what it proves).

**Slide 10 — DOFA: a backbone that makes the spectral comparison fair**
- Most models assume a fixed band set → RGB-vs-VNIR-vs-SWIR becomes apples-to-oranges.
- **DOFA** is wavelength-conditioned: it ingests bands by their actual wavelength, so the *same* model fairly takes RGB, VNIR, or SWIR.
- Strong RGB-era baseline: Swin-T + RSP (remote-sensing pretraining).
- *Visual:* schematic of DOFA accepting variable band sets keyed by wavelength.

### PART 4 — WHAT IS MISSING

**Slide 11 — No ready-made dataset for this exact problem**
- **No public VHR dataset** combining waste sites **with material labels**; **no peer-reviewed Pléiades-Neo material benchmark** exists.
- Existing waste datasets are RGB and detect *objects/sites*, not *materials/hazards*.
- *Visual:* gap matrix — rows = datasets, columns = {VHR? SWIR? material labels? waste?} — almost all cells empty.

**Slide 12 — No pipeline goes from spectra to a regulatory hazard class**
- Prior work stops at "waste / not waste" or "rooftop material"; **none derives an EWC hazard class** (and risk tier) from multiband imagery.
- The **object-vs-material split** is unaddressed (finding a pile ≠ knowing its material); the **generalizzazione** gap (transfer across area/sensor/condition) is rarely shown.
- *Visual:* the risk chain with a red "MISSING LINK" over material→EWC→risk.

### PART 5 — WHAT I PROPOSE & WHY

**Slide 13 — Core idea: measure the real, bounded added value of multiband**
- Central question: **how much does multiband actually beat RGB for material discrimination — and where does it stop helping?**
- Honest: the gain is **bounded** — detection may need little beyond RGB, while **material/chemistry is where SWIR earns its keep**; Pléiades Neo (VNIR-only) tests how far you get without SWIR.
- *Visual:* conceptual "accuracy vs spectral richness" curve with a plateau.

**Slide 14 — The experiment: a 3-axis band ablation**
- **Axis 1 — spectral content:** R0 RGB → R1 +RedEdge/NIR → R2 full VNIR → R3 +SWIR.
- **Axis 2 — sensor:** WorldView-3 (with SWIR) vs Pléiades Neo (VNIR-only).
- **Axis 3 — resolution handling:** native bands vs pansharpened.
- Same DOFA backbone throughout for fairness; Swin-RSP as RGB reference.
- *Visual:* 3-axis cube/matrix (R0–R3 × sensors × native/pansharpened).

**Slide 15 — Then: material → risk tier**
- Map predicted material → **EWC hazard** → **Indice di Degrado / PRAL** logic × exposure × magnitude → **ARPA priority tier**.
- Output = a **ranked intervention list**, each step transparent/auditable.
- *Visual:* worked example — one tile → "Priority: HIGH" with reasoning.

**Slide 16 — The asbestos pilot: the immediately-feasible demonstrator**
- Asbestos is the ideal first case: **public ground-truth labels** (Lombardy regional WFS, 10,903 mapped roofs), a **distinctive SWIR signature** (~2.3 µm Mg-OH), and a clear hazard code (17 06 05\*).
- De-risks the whole pipeline end-to-end before scaling — a clean first result against real labels.
- *Visual:* WFS asbestos-roof map overlaid on a WV-3 tile — predictions vs ground truth.

**Slide 17 — Why this matters & what's genuinely novel**
- First study to (a) **measure** RGB vs VNIR vs SWIR added value for **waste material** at VHR, (b) compare **WV-3 vs Pléiades Neo** head-to-head, (c) connect spectra to a **regulatory risk tier** for ARPA.
- Confidence-aware: reports where multiband helps **and where it doesn't**, incl. the **generalizzazione** test.
- Payoff: a transferable, free-data decision-support tool for environmental agencies.
- *Visual:* "contributions" panel mapping each gap to a contribution.

**Slide 18 — What to confirm with Thomas**
- **Data:** trigger the ESA TPM proposal now (~9-wk lead)? scene selection over Lombardia?
- **Risk-chain scope:** push to the full `Indice di Degrado`/PRAL formalization, or stop at material + EWC? (Note: the ID is **not** in the public WFS → must be estimated remotely or sourced separately.)
- **Ablation depth:** 3 axes as designed, or trim for time?
- **Pilot boundary:** asbestos-only demonstrator, others as outlook?
- **Backbone:** DOFA primary + Swin-RSP RGB reference — agreed?
- *Visual:* a decision checklist.

---

**Honesty guardrails kept throughout:** multiband value is *measured, not assumed* and explicitly *bounded*; material spectra at 1.2 m / 3.7 m while pan gives 0.3 m *texture only*; SWIR carries chemistry but Pléiades Neo has none; no public VHR+waste+material dataset and no peer-reviewed Pléiades-Neo material benchmark; "generalizzazione" (not "OOD") for the transfer gap.
