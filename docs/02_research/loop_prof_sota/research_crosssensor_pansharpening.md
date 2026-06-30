# Methods Review: Combining & Preparing WorldView-3 + Pléiades Neo VHR Imagery for Material Classification

*Scope: data-engineering and fusion methodology for the PERIVALLON illegal-waste / material-risk classification thesis. Foundation models, the Aguilar-2021 VNIR/SWIR ablation, and asbestos/waste SOTA are deliberately excluded. Confidence tags: HIGH / MEDIUM / UNCERTAIN. Autonomous research loop, iteration 1, 2026-06-27.*

## 1. Pansharpening vs spectral fidelity for material classification (the central question)

**The core tension is real and quantified.** Pansharpening fuses the panchromatic detail (0.31 m WV-3 / 0.3 m PNeo) into the MS bands (1.24 m / 1.2 m) but *always* perturbs the per-pixel spectrum to some degree. The community measures this with the Wald protocol and standard distortion metrics: **SAM** (spectral angle — the metric that matters most for material signatures, since it captures shape/angle distortion of the reflectance vector), **ERGAS** (global relative error), and **Q2n** (joint spectral-spatial quality). **(HIGH)**

The decisive finding for a *material* task is the **CS-vs-MRA split** (Vivone et al. survey; arXiv:2405.18900): **Component-Substitution methods (Gram-Schmidt/GS, IHS, Brovey, PCA) give sharper images but the largest spectral/colour distortion**, whereas **Multi-Resolution-Analysis methods (à-trous wavelet, ATWT, MTF-GLP) preserve spectral fidelity far better and are relatively insensitive to radiometric mismatch between sources.** For material discrimination, where the classifier keys on the *shape* of the spectrum rather than RGB appearance, GS/IHS are the wrong default despite being the GIS-software defaults. **(HIGH)**

DL pansharpening (PNN, PanNet, and spatial-spectral transformers) typically achieves the best ERGAS/Q2n on benchmark scenes and PanNet explicitly adds a high-pass / spectral-preservation term. **But two caveats are load-bearing here:** (a) they are trained at *reduced resolution* (Wald protocol) and generalisation to full-resolution real material spectra is not guaranteed — they can hallucinate plausible-but-wrong detail; (b) they are trained per-sensor and would need retraining/fine-tuning to behave on WV-3+PNeo. For a thesis whose dependent variable is "does the spectrum carry material information", an injected-detail DL method adds an uncontrolled confound. **(MEDIUM)**

On the literature's **net classification effect**: results are genuinely mixed. Several LULC studies report pansharpening *raising* overall accuracy (Chen 2015 on WV-2 reports pansharpening mattering more than atmospheric correction, ~12% gains in some object-based settings) — but those gains come from **spatial context / texture / better object delineation**, not from improved spectral purity. Other studies find pansharpening *lowers per-class spectral separability* even while raising spatial accuracy. **(HIGH that results are mixed; MEDIUM on the mechanism.)**

**Recommendation for a material task: classify on native-MS reflectance as the spectral source of truth, and treat pansharpening as a *spatial-context add-on*, not a substitute.** The single most defensible design is: extract spectral features at native 1.2 m and use 0.3 m pan only for object/segment boundaries (object-based) or as a separate texture channel — never melt the two and assume the resulting per-pixel spectrum is physically valid. If pansharpening for the full pipeline is unavoidable, use an **MRA/MTF-matched method (MTF-GLP-HPM)** and **report SAM/ERGAS/Q2n** so distortion is auditable. **(MEDIUM — this is a judgement call, but well-supported.)**

## 2. Cross-sensor harmonization WV-3 ↔ Pléiades Neo

**Band correspondence (verified centres):**

| Role | WV-3 VNIR (nm range) | Pléiades Neo (centre nm) | Match |
|---|---|---|---|
| Coastal / Deep Blue | Coastal 397–454 | Deep Blue 436 | close |
| Blue | 445–517 | 483 | good |
| Green | 507–586 | 562 | good |
| Yellow | 580–629 | — | **WV-3 only** |
| Red | 626–696 | 654 | good |
| Red Edge | 698–749 | 723 | **near-identical** |
| NIR | NIR1 765–899 | 828 | good |
| NIR2 | 857–1039 | — | **WV-3 only** |
| SWIR ×8 | 1184–2373 | — | **WV-3 only** |

So the two sensors share ~6 broadly-corresponding VNIR bands (Red-Edge and NIR are almost coincident, a lucky break); WV-3 additionally supplies Yellow, NIR2 and the 8 SWIR bands that PNeo entirely lacks. **(HIGH)**

**Harmonization practice:** (a) **co-registration** to a common AOI grid via orthorectification against the same DEM and image-to-image tie-pointing — VHR cross-sensor mis-registration of even 1–2 px corrupts per-pixel spectra, so sub-pixel alignment is mandatory; (b) **radiometric cross-calibration** to surface reflectance (Section 3) so DN differences vanish; (c) **spectral band adjustment factors (SBAF)** — the same linear band-pass harmonization used for Landsat↔Sentinel — to correct residual centre/FWHM differences for the "matching" bands; the differences here are small (≤15 nm for most pairs) so SBAF corrections are minor but should be applied for the Coastal/Deep-Blue pair where the gap is largest. **(HIGH for the approach; MEDIUM for exact SBAF values, which must be derived from spectral response functions, not assumed.)**

**Joint vs parallel use — the honest answer:** because PNeo has no SWIR and no Yellow/NIR2, a single fused stack would be inhomogeneous (some pixels carry SWIR, some do not). The cleanest experimental design treats them as **two co-registered but separable strata**: PNeo gives the dense-VNIR + 0.3 m pan layer; WV-3 supplies the SWIR (and Yellow/NIR2) increment. Use them jointly only at the *feature/decision* level over a shared grid, not as one melted cube. **(MEDIUM — design recommendation.)**

## 3. Atmospheric correction / surface reflectance

Material signatures are only physically meaningful at **bottom-of-atmosphere surface reflectance**, so TOA-radiance → SR is mandatory before any cross-sensor comparison. Established tooling: **FLAASH** (runs MODTRAN internally, handles WV-3 sensor geometry; multiple WV-2/WV-3 studies find it the best VNIR performer, <4% deviation vs field spectra in VIS, <0.5% in NIR), **ATCOR** (comparable, strong terrain/BRDF handling), and **6S/MODTRAN** as first-principles radiative-transfer engines. Maxar publishes WV-3 abscal gains/offsets and ESUN values needed for radiance→TOA-reflectance; **6SV with WV-3 spectral response functions is the standard route for the SWIR bands**, which FLAASH also supports. For PNeo, Airbus delivers a "Reflectance" product option, but for cross-sensor parity the safest path is to run **the same engine (FLAASH or 6S) on both** with matched aerosol/water-vapour inputs rather than mixing vendor-SR with self-computed-SR. **(HIGH; "FLAARE" appears to be a niche/typo'd tool — not corroborated. UNCERTAIN.)**

## 4. Practical pipeline recommendation for this thesis

To enable a clean **RGB → +RedEdge/NIR → +full-VNIR → +SWIR** ablation:

1. **Order/obtain both as ortho-ready; co-register** to one AOI grid (common DEM, sub-pixel tie-pointing).
2. **TOA-reflectance → surface reflectance** with one engine (FLAASH or 6S) on both sensors; matched atmospheric inputs.
3. **Apply SBAF** to the corresponding VNIR pairs; keep WV-3 SWIR/Yellow/NIR2 as the unique increment.
4. **Keep native resolutions as the spectral source**: build the ablation on native-MS reflectance (1.2 m VNIR; 3.7 m SWIR). Resample by **area-weighted averaging when down-sampling, never bilinear up-sampling of SWIR into VNIR grid for the spectral features** (up-sampling fabricates sub-pixel reflectance).
5. **Pansharpen only for the spatial/context branch**, with an MRA/MTF method, and log SAM/ERGAS/Q2n. Run a **pansharpened-vs-native control** so the thesis can *quantify* pansharpening's effect on material accuracy — this directly answers Section 1 with your own data and is a strong contribution.

**Pitfalls to flag explicitly:** mixed pixels at 1–4 m (a 1.2 m pixel over a waste pile is already a mixture — material "endmembers" are rarely pure); the **SWIR 3.7 m vs VNIR 1.2 m resolution mismatch** means SWIR adds spectral depth but at ~9× coarser footprint, so SWIR features describe a neighbourhood, not the VNIR pixel; pansharpening artefacts (edge ringing, spectral bleeding) that masquerade as material edges; and CS-pansharpening colour distortion that would silently inflate or deflate band-ablation deltas.

## What this means for the thesis

- **Treat native-MS reflectance as the spectral ground truth; pansharpening is a spatial aid, not a spectral one.** Build the RGB→VNIR→SWIR ablation on native bands.
- **Default to MRA/MTF-matched pansharpening (MTF-GLP-HPM), avoid GS/IHS/Brovey** — CS methods maximise the very spectral distortion (high SAM) that kills material discrimination.
- **Run a pansharpened-vs-native control experiment** and report SAM/ERGAS/Q2n: this *measures* pansharpening's harm on your task and is a publishable result.
- **The two sensors are best used as co-registered parallel strata, not one melted cube:** PNeo = dense VNIR + 0.3 m pan; WV-3 = the SWIR (+Yellow/NIR2) increment. Fuse at feature/decision level.
- **Surface reflectance is mandatory and must use one consistent engine** (FLAASH or 6S) across both sensors; don't mix vendor-SR with self-computed-SR.
- **Apply SBAF on the matching VNIR pairs**; the Red-Edge and NIR bands are near-identical, so the VNIR ablation transfers cleanly between sensors — exploit this for cross-sensor robustness checks.
- **Frame SWIR honestly as a coarse-footprint spectral-depth gain (3.7 m)**, not a per-pixel feature; expect mixed-pixel dilution at 1–4 m for waste piles.
- **Co-registration quality is a first-order experimental risk** — budget effort there; sub-pixel mis-alignment silently corrupts every per-pixel spectral comparison the thesis depends on.

**Sources:** [Chen 2015 AC+pansharpening on WV-2 (PDF)](https://skclivinglandscapes.org/remote_sensing/resources/Section6Resources/Chinsu2015EffectsofAtmosphericCorrectionPansharpenin.pdf) · [Effects of AC & pansharpening on LULC, ScienceDirect](https://www.sciencedirect.com/science/article/pii/S221431731500013X) · [Spectral fidelity & cascading of pansharpening techniques, arXiv:2405.18900](https://arxiv.org/html/2405.18900v1) · [Survey of image-fusion/pansharpening methods, ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1566253521001998) · [WorldView-3 datasheet (band ranges)](https://www.spaceimagingme.com/downloads/sensors/datasheets/DG_WorldView3_DS_2014.pdf) · [Radiometric Use of WorldView-3 (Maxar)](https://dg-cms-uploads-production.s3.amazonaws.com/uploads/document/file/207/Radiometric_Use_of_WorldView-3_v2.pdf) · [Pléiades Neo band specs, Disasters Charter](https://docs.disasterscharter.org/missions/opt/pleiades-neo/) · [Pléiades Neo User Guide (Airbus/Apollo)](https://wp-cdn.apollomapping.com/web_assets/user_uploads/2021/11/08103301/2021.10_PleiadesNeo_UserGuide-EarlyRelease_20211015.pdf) · [Sentinel-2 & WorldView-3 AC vs ground spectra, ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0924271621000095) · [FLAASH vs ATCOR on WorldView-2, ResearchGate](https://www.researchgate.net/publication/215896687)
