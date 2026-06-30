# Professor Q&A Pack — Likely Hard Questions & Defensible Answers

*Autonomous research loop, iteration 4 (2026-06-28). ~20 anticipated questions with crisp, honest, confidence-aware answers. Terminology: "generalizzazione" (not OOD in speech), "classificare per rischio" (not "rilevare"), "multiband" (not spectral cube), GSD untranslated.*

---

**Q1 — What is the task, exactly?**
Two separable sub-problems. (1) **Detection** of illegal-waste sites from VHR satellite — already largely solved on RGB (Gibellini F1 92.0%). (2) **Classification by risk** of an already-detected site, by inferring the **material** (asbestos, plastics, C&D, slag…). The contribution lives in (2): the **added value of multiband over RGB for material discrimination**, via a band-ablation ladder R0 RGB → R1 +RedEdge/NIR → R2 full VNIR → R3 +SWIR. `HIGH`

**Q2 — If RGB already detects waste at F1 92%, why bother with multiband?**
Detection ≠ risk. RGB wins on **morphology + context**, not chemistry — Gibellini's own stated limit is "RGB-only, no spectral added value, does not distinguish materials". ARPA must *prioritize* by hazard, and hazard is defined by **material**. Of 13 classes, ~5 are chemistry-bound (asbestos, plastic-type, slag, sludge, scrap composition) where RGB is blind. Multiband is for the part RGB cannot do. `HIGH`

**Q3 — Why not Sentinel-2? It's free and has SWIR.**
GSD. S-2 is **10–20 m**; a dump is decimetre-to-metre. At 20 m a whole site is 1–4 mixed pixels. Every VNIR material success in the literature is at **0.25–2.5 m**, none ≥3 m. S-2 SWIR at 20 m integrates an entire site → the feature is diluted below detectability. So S-2 is out for material; WV-3 (1.24 m VNIR / 3.7 m SWIR) + Pléiades Neo (1.2 m) are the operating point. `HIGH`

**Q4 — What exactly does SWIR buy, and what does Pléiades Neo lose without it?**
SWIR (1.0–2.5 µm) holds molecular vibration overtones: **chrysotile Mg-OH ~2.32** (asbestos), **C-H 1.215/1.730** (plastics), **carbonate ~2.34** (concrete/C&D), clay Al-OH ~2.2. These are *the* material fingerprints. PNeo has **no SWIR** → loses all direct material-chemistry confirmation; asbestos/plastics collapse to shape + VNIR-colour proxy. WV-3 keeps SWIR but at 3.7 m / ~40 nm bands → *detects* "something absorbs near 2.33" rather than cleanly *resolving* which material. `HIGH`

**Q5 — So is WV-3 SWIR actually useful, or too coarse?**
Honest: **probably partially useful, possibly weak.** Analogy = Aguilar 2021 WV-3 (OA 90.85 VNIR → 96.79 SWIR → 97.38 all) — but that's greenhouse *plastic-film* (NDPI), a plastic-class analogy only. For asbestos, 3.7 m + atmospheric water + ~40 nm bands attenuate the narrow Mg-OH feature → expect modest, possibly non-significant SWIR contribution. Measuring this honestly **is** part of the contribution (R3 quantifies it). `MEDIUM`→`UNCERTAIN`

**Q6 — Mixed pixels: at 1.2–3.7 m no pixel is pure. Doesn't that kill the material claim?**
It sets the **ceiling**, doesn't kill it. WV-3 VNIR ~1.5 m², SWIR ~14 m² — over a dump, a mixture of waste+soil+shadow+vegetation. Lab/library numbers (pure endmembers) are **upper bounds**; on-satellite is a realistic **mixed-pixel lower bound**. The cited SOTA detectors (Aguilar matched-filter, EMIT) are **already sub-pixel**. Unmixing is out of my experimental scope but I discuss it as the ceiling and contrast mixed-pixel results vs the pure-endmember bound. `HIGH`

**Q7 — How do you prove multiband-CNN beats RGB because of *chemistry*, not extra texture channels?**
Core safeguard. A CNN has a receptive field, so MS-CNN > RGB-CNN could be texture. **Four-cell design**: {RGB, MS} × {spatial-context-free per-pixel, full CNN}. **B−A** (MS−RGB, both per-pixel, RF=1 px) isolates **pure spectral gain** — no spatial info to either, only the spectrum changed. B−A>0 ⇒ MS value = chemistry. B−A≈0 but D−C>0 ⇒ gain is texture (honest negative). The ablation alone can't separate the two; pairing with the per-pixel row makes the claim defensible. `HIGH`

**Q8 — Why a per-pixel baseline at all? Deployment uses a CNN.**
Two reasons: scientifically it's the only way to attribute gain to chemistry vs texture (Q7); empirically it works — Saba's Fine-KNN on WV-3 VNIR pixel features reaches Macro-F1 97.6% for asbestos with no spatial kernel. Both an instrument and a credible model. `HIGH`

**Q9 — Generalization: existing work generalizes badly. True? How bad?**
True and quantifiable. **Cross-region** (same sensor, new territory) mild: Gibellini −5.1% F1 (92.0→86.9; GR 85.4 / SE 83.8 / RO 91.5). **Cross-sensor with band mismatch** catastrophic: GeoCrossBench **2–4× drop** (no overlap), **5–25%** even with a superset. Asbestos transfer (Shepherd EnMAP) ACE 91.4→86% vs field GT. Severity scales with band-set change — the crux of a multiband thesis. `HIGH`

**Q10 — Does multiband make generalization better or worse than RGB?**
Genuinely mixed — which makes it publishable. **Narrows** the gap for cross-region/cross-time on a *fixed* sensor (physical absorptions more invariant than colour/texture). **Widens** it cross-sensor (extra bands are exactly where center/bandwidth/SNR/calibration mismatch lives; RGB is the lowest common denominator and ports trivially). Defensible claim: MS helps within-sensor generalization, hurts cross-sensor *unless* you harmonize reflectance and handle the band gap. `HIGH`/`MEDIUM`

**Q11 — How will you test generalization so a reviewer accepts it?**
Hold out **entire provinces** (never random tiles — spatial autocorrelation leaks and inflates). Report ID + OOD side-by-side with the **gap (ID−OOD) as a first-class metric**. Three axes: cross-region, cross-sensor (WV-3→PNeo under both band-intersection and superset), cross-time. **Match preprocessing across domains and say so** (Corley 2024). ≥3 seeds, per-class. For ARPA, report precision@k of high-risk sites — ranking can survive OOD even when F1 drops. `HIGH`

**Q12 — Is the contribution actually novel, or re-running known experiments?**
Novelty = the **2-D table: band-ablation (R0→R3) × generalization axis**, ID−OOD gap per cell, per-class, at the VHR-satellite material operating point the literature leaves empty (no published per-class 13-material risk classifier at this GSD), plus the chemistry-vs-texture decomposition (B−A) and the remote asbestos-degradation proxy. Individual pieces have precedent; the *combination + honest attribution* is the contribution. `MEDIUM`

**Q13 — DOFA / wavelength-conditioned FMs — aren't those the obvious cross-sensor fix?**
Right *mechanism*, not a guaranteed fix. DOFA's wavelength-conditioned patch-embedding is built for variable band sets. But GeoCrossBench found it did **not** beat a simple channel-sampling ViT (χViT), and even a general vision model (DINOv3) beat DOFA there. So I treat DOFA as a strong baseline, prioritizing the cheaper high-ROI fixes first (reflectance harmonization + resize/normalization + band-dropout). `HIGH` mechanism / `MEDIUM` efficacy.

**Q14 — The Indice di Degrado has thresholds 25/44/45. Can you predict it remotely?**
Not fully, and I'm explicit. ID = (A+…+H)×I is a *site-inspection* score, **not in the public WFS**. Only **D (fibre exposure)** has a spectral handle (SWIR chrysotile, weak at WV-3); **B (large cracks)** partial at pan 0.3 m; **A, C invisible**. Exposure E–H + age I are GIS/registry (H = ≤300 m to sensitive sites is pure GIS). I propose a **two-tier Remote Degradation Proxy**: ordinal spectral surface-class × GIS overlay, a **screening pre-filter**, not a substitute for on-site ID. I output an ordinal class, not a fake continuous ID — matching what Cilia (2 classes) and Martínez (HIP/LIP) achieved. `HIGH`

**Q15 — Where do you get ground truth for the degradation proxy?**
Best: request filed ID surveys from ATS/ARPA via the supervisory team. Fallbacks: small field campaign scoring A–D per the questionnaire (clean, small N); HIP/LIP binary proxy (Martínez 149 roofs); photo-interpretation (cheap, risks circularity). The WFS gives locations + possibly install-year for stratified sampling but no condition field. `HIGH`

**Q16 — Is the data feasible? Can you actually get WV-3 SWIR?**
WV-3 + Pléiades Neo archive imagery is free to PoliMi via **ESA Third Party Missions** (proposal ~9 wk + 1-yr quota). The asbestos pilot already has public GT (Mappatura_2020, 10,903 roofs, EPSG:32632). The real risk is **SWIR archive availability over the specific AOI** (SWIR is tasked separately, may be sparse) and SWIR co-registration/atmospheric correction at 3.7 m — not access in general. `MEDIUM`

**Q17 — Three diagnostic features (asbestos 2.32, concrete 2.34, plastic 2.31) all fall in one WV-3 SWIR band. Doesn't that make WV-3 useless for telling them apart?**
WV-3 cannot *resolve* them within SWIR8 — correct. Discrimination then comes from the **shoulders** (S5 2.16, S6 2.20 clay; S7 2.26; S1 1.21 + S4 1.73 plastic) + VNIR context (asbestos = corrugated shape + moss/lichen; concrete heaps differ morphologically). So I don't claim WV-3 SWIR "identifies material" in isolation — the *full multiband stack + shape* does, and I measure each band's contribution. Hyperspectral (~6.5 nm) would resolve the triplet; WV-3 won't, and I state that limit. `HIGH`

**Q18 — Why not just use hyperspectral (EnMAP/PRISMA)?**
Spectral-vs-spatial trade-off. EnMAP/PRISMA give ~6.5 nm bands that cleanly resolve the 2.3 µm triplet but at **30 m GSD** — useless over decimetre-scale waste (Q3/Q6). No sensor today has both hyperspectral resolution and sub-metre GSD over wide areas. The thesis works precisely in the realistic gap: VHR multiband (broad bands, fine GSD) — what can it do for material/risk, and how much does each band buy. `HIGH`

**Q19 — Your strongest single number for "RGB isn't enough for material"?**
Saba 2026: Fine-KNN on **WV-3 VNIR pixel features** → Macro-F1 97.6% for asbestos *without* a spatial kernel — spectral features alone carry material identity. The "HS 97.3% vs MS 74.4%" penalty figure is suggestive but **unverified (paywalled)** — I won't lean on it. Aguilar's SWIR jump (90.85→96.79 OA) is my plastic-class analogy, with "+14% kappa" dropped as unverified. `HIGH` + honest caveats.

**Q20 — What's your honest biggest risk of a null result?**
That at WV-3 SWIR's 3.7 m the asbestos Mg-OH feature is too diluted to add significant discrimination over VNIR — i.e. R3 ≈ R2 for asbestos. If so, that is *still a publishable, honest finding*: it quantifies that satellite-SWIR is below the threshold needed, motivating airborne/hyperspectral or temporal approaches. The four-cell design protects against the opposite failure (claiming chemistry value that is really texture). Either way the experiment is informative. `MEDIUM`
