# SOTA — high-resolution material discrimination from remote sensing

*Focused state-of-the-art for the PERIVALLON thesis, re-scoped after the advisor's 2026-06-15 directive.* Companion to [`datasets_catalog.md`](datasets_catalog.md) and [`datasets_guide.md`](datasets_guide.md). The point is **not** "everything on waste from satellites" — it is **how the literature discriminates MATERIALS at a spatial resolution that is actually useful to us**.

*Last revised 2026-06-16: open `(confirm)` cells closed against primary sources via four targeted verification agents; corrections applied (see §11); master comparison table added (§2bis); foundation-model section rebuilt on verified evidence (§8).*

---

## 1. Scope & criteria (read this first)

**The task we care about:** identifying / separating **what a surface is made of** (material-level), per-pixel, per-object (OBIA), or per-region. Works on *other* materials (minerals, roofing, urban surfaces) count, because the question is material *discrimination*, not waste detection.

**Inclusion — a work must satisfy ALL three:**
1. **Task = material discrimination** (not scene classification, not binary waste/no-waste, not land-use/land-cover).
2. **Spatial resolution GSD ≤ ~5 m** — sub-metre VHR (WorldView-3 1.24 m, Pléiades ~2 m, aerial, drone cm-scale) **and** ~3 m PlanetScope/SuperDove class. *Criterion is the GSD, not the sensor:* fine-GSD airborne/drone hyperspectral is IN.
3. **Multispectral or hyperspectral** input (≥4 bands).

**Exclusion (deliberate):**
- **GSD ≥ ~10 m** — Sentinel-2 (10 m), EnMAP / PRISMA / EMIT (30–60 m) — **even with SWIR or material labels**.
- Scene classification / binary presence; pure land-use/land-cover.

**Known but excluded by resolution** (so the panel sees we know them, not that we missed them): **Shepherd / Aharoni-Mack 2025** (EnMAP asbestos, 30 m), **EMIT plastic** (Estrela 2025, 60 m), **MARIDA / MADOS** (S-2, 10 m), **Tisza / Magyar 2023** (S-2 primary), **Sun 2023 dumpsites** (binary detection). These set the *upper bound of what SWIR buys*, but at a resolution we have ruled out.

> **The honest tension this scoping exposes:** the strongest material discrimination uses **SWIR**, which on satellites comes either at high cost & limited access (**WorldView-3**, 3.7 m SWIR native) or at **low resolution** (EnMAP/PRISMA, 30 m). Our sensor (**SuperDove, 8 VNIR bands @ 3 m, no SWIR**) sits in a sparsely-studied corner. The SOTA below makes that corner explicit — and, importantly, surfaces a growing body of **VNIR-only high-resolution** material work that is the closest precedent we have.

---

## 2. Reading the tables
Per entry: **platform / GSD · bands (SWIR?) · task · key metric · public data.** **[NEW]** = surfaced by the June-2026 deep-research pass and fact-checked individually against primary sources; un-tagged = established library. Numbers were taken from primary text where reachable; cells still behind a paywall are marked *(confirm)*. Confidence notes in §11.

**Two cross-cutting eligibility caveats:**
- **WV-3 SWIR GSD is dual.** Native SWIR is **3.7 m** (at nadir; eoPortal/Maxar) → qualifies as ≤5 m. But under the old US Dept. of Commerce restriction, commercial WV-3 SWIR was **resampled to 7.5 m** for distribution; the native 3.7 m product was released only later. **So any WV-3-SWIR work must be checked for which product it used.** WV-3 *VNIR* (1.24 m) always qualifies.
- **"Airborne hyperspectral" ≠ our sensor.** Most VNIR-only successes are at 0.25–2.5 m; SWIR successes are airborne/WV-3. The 3 m VNIR-only point (SuperDove) is the unfilled cell — see §9.

---

## 2bis. MASTER COMPARISON TABLE (thesis Related-Work backbone)

Single consolidated view of §3–§6. Sorted by domain, then by closeness to our setting. **SWIR? ✅/❌** is the column that matters most for "what SuperDove loses". **Conf** = our verification confidence (H/M/U). Full citations & per-row notes in §3–§6 and §11.

| # | Work (year) | Domain | Platform / **GSD** | Bands · SWIR? | Task / method | Headline metric | Public | Conf |
|---|---|---|---|---|---|---|---|---|
| 1 | **Aguilar 2025** | plastics | WV-3 / **~3.7 m SWIR** | 8 SWIR ✅ | matched-filter, 5 polymers (HDPE/LDPE/PET/PS/PVC) | **precision 92.5%** | no | M |
| 2 | **Zhou 2021** | plastics | WV-3 / **3.7 m** | 8 SWIR ✅ | knowledge-based pixel class., 3 polymer clusters | OA >80% | no | M |
| 3 | **Alboody 2023** | plastics | aquatic drone / **~cm** | 143–164 b, 900–1700 nm ✅ | supervised class., up to 10 polymers | **OA ≈89%** (≤92% val) | on req. | H |
| 4 | **Balsi 2023/24** | plastics | drone / **1–4 cm** | VNIR 400–1000 + SWIR 900–1700 ✅ | real-time push-broom detection (PE/PET) | **none (proof-of-concept)** | no | H |
| 5 | **Agronomy 2026** (Pika L) | plastics | UAV / **cm** | 150 b, 400–1000 nm VNIR ❌ | semantic seg: mulch/soil/cotton | **mIoU 85.9%** (PSPNet) **> RGB 83.4%** | no | M |
| 6 | **Bonifazi 2026** | asbestos | WV-3 / **1.24 m VNIR + 3.7 m SWIR** | 16 b ✅ | Py6S + MLC, building-level | **F1 0.87**, multi-year | code | H |
| 7 | **Cartagena / Martínez 2024** | asbestos | airborne HySpex Mjolnir / **0.8 m** | 490 b, 400–2500 nm ✅ | **SAM** (SAM only — *not* MLC), AC vs clay vs steel | **OA 96%**, AC PA/UA **98%** | no | H |
| 8 | **Saba 2026** | asbestos | WV-3 / **1.24 m** | 8 **VNIR** ❌ | 32 classifiers, multiclass + AC/non-AC | **Macro-F1 97.6%** (Fine-KNN); binary ~99–100% | no | H |
| 9 | **Saba 2025** **[NEW]** | asbestos | WV-3 MS 3.7 m + airborne HS / **1.2 m** | MS ❌ / HS ✅ | 6 supervised + 2 unsupervised | **HS 97.3% vs MS 74.4%** (Mahalanobis best) | no | H |
| 10 | **Hikuwai 2023** | asbestos | WV-3 VNIR 1.24 m + aerial 7.5 cm | VNIR ❌ | Mask R-CNN instance seg | aerial **94%** vs sat **~63%** prec | no | M |
| 11 | **Raczko 2022** | asbestos | airborne orthophoto / **25 cm** | 4 b (RGB+NIR) ❌ | CNN (Inception), AC binary | **OA ~88–93%** | no | H |
| 12 | **Abriha & Szabó 2018/23** | asbestos | WorldView-2 / **0.5 m** | 8 VNIR ❌ | Random Forest / DFA | high OA *(exact confirm)* | no | M |
| 13 | **Widipaminto 2021** | asbestos | **Pléiades / 2 m** (pansharp 0.5 m) | 4 VNIR ❌ | SVM, 5 roof materials incl. asbestos | **OA 92.92%, κ 0.9069** | no | H |
| 14 | **Abbasi 2024** | asbestos | Nearmap aerial / **cm** (RGB) | RGB ❌ | OBIA + DL (DenseNet+LSTM), multi-temporal | **OA 95.8–96.0%**, AC 94% | no | M |
| 15 | **Xu 2022** **[NEW]** | inert/C&D | UAV GaiaSky-mini2 / **cm** *(GSD confirm)* | 176 b, 400–1000 nm VNIR ❌ | decision-tree, 4 C&D-waste classes | **OA 85.91%, κ 0.845** | no | H |
| 16 | **Vitek/Krauz 2025** | inert/C&D | close-range / lab | RGB + narrowbands | band selection for C&D | **RGB + 2 bands ≈ HSI 768 b** | dataset | M |
| 17 | **Wang 2022** (=Liu/Ye HySpex) | minerals | HySpex airborne / **1 m VNIR + 1.2 m SWIR** | 504 b, 400–2500 nm ✅ | RF, 7 alteration minerals → 3 assemblages | **OA 73.08%, κ 0.657** | on req. | H |
| 18 | **Karimzadeh 2021** | minerals | WV-3 / **1.2 m VNIR + 3.7 m SWIR** | 16 b ✅ | SVM, lithologies | **OA 88.36%, κ 0.86** (top band = **SWIR-7**) | no | H |
| 19 | **Huang & Zheng 2018** **[NEW]** | minerals | airborne CASI+SASI / **~1–2.5 m** *(confirm)* | 32+88 b VNIR–SWIR ✅ | MTMF, alteration minerals | qualitative maps | no | M |
| 20 | **Huaniushan CASI/SASI 2020/21** **[NEW]** | minerals | airborne CASI+SASI / **~1–2.4 m** *(confirm)* | 137 b VNIR–SWIR ✅ | SAM + MTMF, lithology + alteration | qualitative maps | no | M |
| 21 | **Toulouse / Thoreau 2024** | urban | airborne / **1 m** | 310 b VNIR+SWIR ✅ | 32 urban-material classes (seg) | benchmark | **yes** | H |
| 22 | **Banolia 2022** | metals/urban | Pavia 1.3 m / HYDICE ~2 m | VNIR ❌ | rule-based metal-roof detection | **F1 0.44, OA 99%** (low F1 = GT noise) | benchmarks | H |
| 23 | **Ma 2023** | urban | airborne CASI / **2.5 m** | 144 b, 380–1050 nm VNIR ❌ | improved 3D-CNN, 15 urban classes | **OA 96.3%** (>SVM +24, RF +11) | **yes** | M |
| 24 | **MCubeS** | urban | close-range / cm | RGB+NIR+polarisation | 20-class material seg | NIR+pol adds **+2.7–8.7% mIoU** | **yes** | H |

**How to read this table in one breath:** the only rows that are simultaneously (a) material-discrimination, (b) ≤3 m, and (c) **VNIR-only like SuperDove** are **#8 Saba (1.24 m), #13 Widipaminto (2 m), #15 Xu (cm)** — all *finer* than 3 m. Every row with a strong polymer-identity or mineral result has a ✅ in the SWIR column. **No row sits at our exact operating point (3 m, 8-band VNIR, no SWIR).** That empty cell is the thesis.

---

## 3. Domain 1 — Plastics & polymers

Two lessons: (a) **polymer-TYPE discrimination needs NIR–SWIR** (C–H features ~1215/1730 nm); (b) but a **VNIR-only** sensor can still separate *plastic presence/extent* from soil and vegetation, and multiband still beats RGB there.

| Work | Platform / GSD | Bands (SWIR?) | Task | Result | Public |
|---|---|---|---|---|---|
| **Aguilar 2025** (Los Laureles) | WV-3 / ~3.7 m SWIR | 8 SWIR ✅ | matched-filter detection, 5 polymers (HDPE/LDPE/PET/PS/PVC) | **precision 92.5%** | no |
| **Zhou 2021** | WV-3 / 3.7 m | 8 SWIR ✅ | knowledge-based pixel class., 3 polymer clusters | OA >80% | no |
| **[NEW] Alboody 2023** (ROV-ULCO aquatic drone) | proximal ~45 cm, cm-scale | 143–164 b, **900–1700 nm** ✅ | supervised class., up to 10 polymers (HDPE/LDPE/PET/PP/PVC/PS/PUR/POM/ABS) | **OA ≈89%** (≤92% val) | on request |
| **[NEW] Balsi 2023/2024** (DJI M600, Sapienza) | drone / **1–4 cm** | VNIR 400–1000 + SWIR 900–1700 ✅ | real-time push-broom detection (PE, PET) | **NO quantitative metric** — proof-of-concept; really a 2023 WHISPERS paper (IEEE Xplore 10431217, indexed 2024) | no |
| **[NEW] Plastic-mulch — Agronomy 2026** (Pika L, Alar/Xinjiang) | UAV / cm (40 m alt) | 150 b, **400–1000 nm VNIR** ❌ | semantic seg: mulch / soil / cotton | **mIoU 85.9%** (PSPNet) **> RGB U-Net 83.4%** | no |
| **Tasseron 2021** | lab spectroradiometer | VNIR–SWIR ✅ | reference spectra (iso-chromaticity) | — | yes |

*(Also noted, RGB-only so out of the spectral argument: Zhai 2022 / Qiu 2022 cotton residual-film UAV segmentation — same domain, but 3-band RGB.)*

**Takeaways:** every *polymer-type* success uses bands **beyond 1000 nm** (Alboody, Balsi, Aguilar, Zhou) → **resolution does not substitute for SWIR** when the question is "which polymer". **But** the Agronomy-2026 plastic-mulch study is the key VNIR-only datapoint: at 400–1000 nm it still **beats RGB by ~2.5 mIoU** and cleanly separates plastic-presence from soil/vegetation. **Conclusion for SuperDove:** plausible for *plastic presence/extent*, not for *polymer identity*. (Balsi confirms the SWIR route works qualitatively but gives us no number to cite.)

---

## 4. Domain 2 — Asbestos-cement & roofing materials

The domain closest to the Phase-1 pilot — and, after this pass, the **best external evidence that a VNIR-only sensor can classify asbestos**. Splits into a SWIR "pure" route and a now-well-populated VNIR/RGB route.

| Work | Platform / GSD | Bands (SWIR?) | Task | Result | Public |
|---|---|---|---|---|---|
| **Bonifazi 2026** (Mantova) | WV-3 / 1.24 m VNIR + 3.7 m SWIR | 16 b ✅ | Py6S + MLC, building-level | **F1 0.87**, multi-year | code |
| **Cilia 2015** | WV-3 / airborne SWIR | ✅ | SAM + lab endmembers | pilot AC roofs ID'd | no |
| **[NEW] Cartagena / Martínez 2024** (Heliyon 10(3):e25612) | airborne HySpex Mjolnir VS-620 / **0.4→0.8 m** | 490 b (200 VNIR + 290 SWIR), 400–2500 nm ✅ | **SAM** classification, AC vs clay vs steel + deterioration indices | **OA 96%**; AC producer/user acc. **98%** (146/149) | no |
| **Saba 2026** (J. Haz. Mat., S0304389426008423) | WV-3 / 1.24 m | 8 **VNIR** ❌ | 32 classifiers, multiclass + AC/non-AC binary | **Macro-F1 97.6%** (Fine-KNN); binary ~99–100% (Subspace-KNN) | no |
| **[NEW] Saba 2025** (RSASE, S2352938525000175) | WV-3 MS 3.7 m + airborne HS / **1.2 m** | MS ❌ / HS ✅ | 6 supervised (incl. SAM, SVM, SID) + 2 unsupervised | **HS 97.3% vs MS 74.4%**; Mahalanobis best on HS | no |
| **Hikuwai 2023** (Sustainability, su15054276) | WV-3 VNIR 1.24 m + aerial 7.5 cm | VNIR (ceiling ~920 nm) ❌ | Mask R-CNN instance seg | aerial **94%** vs sat **~63%** prec | no |
| **[NEW] Raczko 2022** (Bldg & Env 217:109092) | airborne orthophoto / **25 cm** | 4 b (RGB+NIR) ❌ | CNN (Inception) AC binary | **OA ~88–93%** | no |
| **[NEW] Abriha & Szabó 2018 / 2023** (Debrecen, Heliyon) | WorldView-2 / **0.5 m** | 8 VNIR ❌ | Random Forest / DFA, AC class. | high OA *(confirm exact)* | no |
| **[NEW] Widipaminto 2021** (TELKOMNIKA 19(2):690) | **Pléiades / 2 m** (pansharp 0.5 m) | 4 VNIR ❌ | SVM (C-SVC, RBF), 5 roof materials incl. **asbestos** | **OA 92.92%, κ 0.9069** | no |
| **[NEW] Abbasi 2024** (RSASE 35:101167) | Nearmap aerial / cm (RGB) | RGB ❌ | OBIA + DL (DenseNet+LSTM), multi-temporal | **OA 95.8–96.0%**, AC 94% | no |
| **RoofNet / RoofSense / Nacala** | EO / aerial+LiDAR / drone | RGB(+) ❌ | roof-material class./seg (Nacala has explicit AC class) | — | yes |

**Takeaways:** the diagnostic asbestos feature (**Mg-OH 2.31 µm**) is SWIR → the "physically pure" route needs WV-3 (Bonifazi) or airborne (Cartagena, Saba-2025 HS). **But the VNIR/RGB line is now strong and quantified**: **Widipaminto (Pléiades VNIR, OA 92.9%)**, **Saba-2026 (WV-3 VNIR, Macro-F1 0.98)**, **Raczko/Abriha/Abbasi (RGB-VNIR, OA 88–96%)**. → This is the **strongest external argument that the SuperDove VNIR-only asbestos pilot is viable**. Two caveats: (1) all operate at **0.25–2 m (12–25× finer than 3 m SuperDove)** — *our open question is whether the result survives the coarser GSD*; (2) **Saba-2025 directly quantifies the VNIR penalty in this exact domain — HS 97.3% vs MS 74.4%** — a ~23-point drop that is the most honest single number for "what SuperDove leaves on the table" for asbestos.

> **Note on the Saba cluster.** Saba 2026 (JHM, WV-3 VNIR), Saba 2025 (RSASE, MS vs HS), and the Gil/Martínez 2026 *Geomatics* Python workflow are the **same author group** as Cartagena/Martínez 2024. They are *distinct papers* but cite each other — present them as one coherent line, not four independent confirmations.

---

## 5. Domain 3 — Inert / C&D waste, minerals, soils

| Work | Platform / GSD | Bands (SWIR?) | Task | Result | Public |
|---|---|---|---|---|---|
| **[NEW] Xu 2022** (Spectrosc. Spectral Anal. 42(12):3927) | UAV (DJI M600 + GaiaSky-mini2) / cm *(exact GSD unconfirmed)* | 176 b, **400–1000 nm VNIR** ❌ | decision-tree pixel class., construction waste (white plastic, dust cloth, foundation residue, rubble sand) | **OA 85.91%, κ 0.845** | no |
| **Vitek/Krauz 2025** (CDW critical wavelengths) | close-range / lab | RGB + narrowbands | band selection for C&D materials | **RGB + 2 bands ≈ HSI 768 b** | dataset |
| **[NEW] Wang 2022** (Front. Earth Sci. 10:871529; = Liu/Ye HySpex, Yudai/Kalatag NW China) | HySpex airborne / **1 m VNIR + 1.2 m SWIR** | 504 b, **400–2500 nm** ✅ | RF, 7 alteration minerals → 3 assemblages | **OA 73.08%, κ 0.657** | on request |
| **[NEW] Karimzadeh & Tangestani 2021** (Adv. Space Res.; *vol/issue: 67:2421 vs 68(6):2421 — resolve before citing*) | WV-3 / 1.2 m VNIR + 3.7 m SWIR | 16 b ✅ | SVM, lithologies (*8-class count unconfirmed*) | **OA 88.36%, κ 0.86** (most discriminating = **SWIR-7**, +4.81% OA) | no |
| **[NEW] Huang & Zheng 2018** (ISPRS Archives XLII-3:601; Wuyi belt, China) | airborne CASI (32 b) + SASI (88 b) / **~1–2.5 m** *(confirm)* | VNIR–SWIR ✅ | MTMF, alteration minerals (silicification/sericite/pyrite/chlorite) | qualitative maps | no |
| **[NEW] Huaniushan Au-Ag-Pb-Zn 2020/2021** (Sci.Rep. s41598-020-79864-0; Geologia Croatica 74:73) | airborne CASI/SASI, 137 b / **~1–2.4 m** *(confirm)* | VNIR–SWIR ✅ | SAM + MTMF, lithology + alteration zones | qualitative maps | no |
| **Toulouse 2024** | airborne / 1 m | 310 b VNIR+SWIR ✅ | 32 urban-material classes (seg) | benchmark | yes |

**Takeaways:** **Xu 2022 is the closest sensor-analogue** — VNIR-only, *inert/C&D* materials, OA 85.91% with a simple decision tree → encouraging that the inert family is partly separable without SWIR (caveat: it is drone-cm, not 3 m). The "few well-chosen bands suffice" result (Vitek/Krauz) is the strongest enabler for 8-band VNIR. The mineral works **quantify the VNIR penalty**: Karimzadeh finds the single most informative band is **SWIR-7**, and Wang's mineral mapping depends on 1.0–2.5 µm — exactly what SuperDove lacks. **The Chinese mineral cluster (Wang, Huang, Huaniushan) is the answer to the advisor's "go check the Chinese" point:** China has a substantial fine-GSD material-discrimination literature, but it is **airborne hyperspectral *with SWIR* for mineral mapping** — *none* at the 3 m VNIR-only point, and *none* on waste/asbestos materials (see §7).

---

## 6. Domain 4 — Metals / e-waste & general urban materials (confusers & benchmarks)

| Work | Platform / GSD | Bands (SWIR?) | Task | Result | Public |
|---|---|---|---|---|---|
| **[NEW] Banolia 2022** (SPIE 12269, 122690A) | airborne HSI: Pavia 1.3 m / "Urban" (HYDICE-class) ~2 m | VNIR ❌ | rule-based **metal-roof** detection (reflectance + spectral-flatness) | **F1 0.44, OA 99%** (low F1 = GT noise) | benchmarks public |
| **[NEW] Ma 2023** (Remote Sens. 15(4):992) | airborne CASI / **2.5 m** (Houston) | 144 b, **380–1050 nm VNIR** ❌ | improved 3D-CNN, 15 urban classes | **OA 96.3%** (>SVM +24, RF +11) | yes (GRSS) |
| **MCubeS** | close-range / cm | RGB+NIR+polarisation | 20-class material seg | NIR+pol adds **+2.7–8.7% mIoU** | yes |
| **Toulouse / Pavia** | airborne / 1–1.3 m | HSI (Toulouse VNIR+SWIR) | urban-material seg | benchmark | yes |

**Takeaways:** metal's **high-reflectance + flat-spectrum** cue survives in VNIR (Banolia) — relevant because *metal sheeting* is a common waste/roof confuser. **Ma 2023** confirms a **VNIR 3D-CNN reaches OA 96% on urban surfaces at 2.5 m** — a direct methodological analogue for a 3 m VNIR SuperDove CNN baseline. Caveat: Ma's 15 classes lean land-use, not a pure asphalt/concrete/tile material split.

---

## 7. Cross-cutting synthesis

1. **SWIR is the discriminator; resolution is the locator.** *Material identity* is carried by SWIR features; *spatial resolution* decides whether you can place them. High-res + SWIR (WV-3, airborne HySpex) is the gold standard — expensive/scarce. The cleanest single number: **Saba 2025, same asbestos task, HS 97.3% vs MS 74.4%**.
2. **VNIR-only at high resolution genuinely works for several material problems** — now quantified: asbestos (Widipaminto OA 92.9%, Saba-2026 Macro-F1 0.98, Raczko/Abriha/Abbasi 88–96%), inert/C&D (Xu OA 85.9%), urban surfaces (Ma OA 96.3%), plastic-presence (Agronomy-2026 mIoU 85.9% > RGB). It **fails** for polymer-type identity (needs SWIR).
3. **"Which bands, not how many"** (Vitek/Krauz: RGB + 2 bands ≈ 768-band HSI) is the strongest theoretical enabler for SuperDove's 8 VNIR bands.
4. **The catch is GSD, not bands.** Almost every VNIR-only success above is at **0.25–2.5 m**; *none* is at 3 m. SuperDove's open question is whether these results survive a 3 m pixel.
5. **3 m is the frontier, not the comfort zone** — the ~3 m VNIR setting is essentially unstudied → the thesis's contribution space.
6. **The Chinese literature does NOT pre-empt us** (advisor's explicit concern, now checked). China's fine-GSD material work is real and substantial but is **airborne HSI + SWIR mineral mapping** (Wang/Huang/Huaniushan). Chinese *waste* remote sensing is **detection/scene-level, not material-level** (GF-2 construction-waste-landfill *zones*; SWAD dumpsite detection — both excluded). **No Chinese group operates at 3 m VNIR-only, and none targets waste/asbestos materials** — the gap and the generalization framing survive the check.

---

## 8. Foundation models at high resolution — the honest assessment (rebuilt, verified)

The advisor's skepticism (FMs pretrained at 10–30 m won't transfer to ≤3 m) is **supported by recent evidence**, with partial, testable mitigations. All claims below were verified against primary sources (arXiv / CVF / IEEE) on 2026-06-16.

### 8.1 The DOFA "gap question" — answered
The advisor's sharp question was: *if DOFA already ingests arbitrary bands, hasn't it already solved "10–30 m FMs don't transfer to 3 m"?* **No — and this is now precise:**
- DOFA (Xiong et al. 2024, arXiv:2403.15356, **still a preprint** — do not cite as journal-published) uses a **wavelength-conditioned hypernetwork**: it generates patch-embedding weights *from each band's central wavelength*. **Wavelength is the ONLY physical conditioning variable — there is no GSD/resolution conditioning.**
- **What it closes:** the *band-mismatch* gap — SuperDove's 8 VNIR centres are exactly the kind of input DOFA accepts natively.
- **What it does NOT close:** the *spatial-frequency / object-scale (GSD) gap*. Two sensors with identical band centres but different GSD get the *same* nominal embedding while their texture/scale statistics differ. DOFA's own pretraining mix (S2 10–60 m, EnMAP 30 m, Gaofen, NAIP RGB sub-m, S1) has fine GSD **only in RGB** — an 8-band sensor at 3 m sits in an under-represented corner.
- **Thesis framing:** DOFA reduces the problem from *two* gaps to *one*. The band gap is architecturally closed; the **GSD gap stays an open empirical question** — i.e. a legitimate thesis measurement (DOFA fine-tuned on 3 m SuperDove vs. a from-scratch / RGB-pretrained supervised baseline), not an assumption.

### 8.2 Evidence FM-transfer to high-res is hard / oversold
- **PANGAEA (Marsocci et al. 2024, arXiv:2412.04204)** — global GFM benchmark across 9 models, **0.1–30 m**: geospatial FMs **do not consistently beat supervised baselines** (U-Net, vanilla ViT); the FM edge appears mainly under label scarcity. **This is our single strongest skeptic-supporting citation, and it explicitly spans high-res.**
- **GEO-Bench (Lacoste et al., NeurIPS 2023)** — companion evidence that GFM ranking is task-dependent and supervised baselines stay competitive (mixed resolutions incl. high-res; verify the exact rows quoted).
- **"Specialized FMs struggle to beat supervised baselines" (2024)** — same direction across domains incl. RS.

### 8.3 Mitigations that target the GSD/scale gap (testable, not magic)
- **Scale-MAE (Reed et al., ICCV 2023)** — **GSD-based positional encoding** (encodes real ground footprint) + Laplacian-pyramid reconstruction; +5.0% avg kNN, +0.9–3.8 mIoU vs SatMAE; evaluated across GSDs incl. high-res. **The most directly relevant scale-aware-pretraining baseline.**
- **USat / USatMAE (Irvin et al. 2023, arXiv:2312.02199)** — per-band patching where finer-GSD bands get more patches; jointly models S2 + NAIP (sub-m). **Closest existing template for a mixed-GSD multispectral encoder.**
- **AnySat (Astruc et al., CVPR 2025, Highlight)** — JEPA + **scale-adaptive spatial encoders**; one model over 11 sensors incl. sub-metre aerial; "resolution is an explicit model input" precedent.
- **Panopticon (Waldmann et al., CVPR-W 2025 EarthVision)** — any-sensor via cross-attention over channels; strong on S1/S2, **weaker high-res evidence** (treat as supporting, not load-bearing for 3 m).
- **GFM continual pretraining (Mendieta et al., ICCV 2023)** — supports "continue-pretrain on your domain" over training from scratch.

### 8.4 Cheap adaptation (PEFT) — most actionable for our methods
- **DEFLECT (Thoreau et al., ICCV 2025, arXiv:2503.09493)** — additive PEFT to adapt an **RGB-pretrained GFM to multispectral**: keeps frozen weights for RGB geometry/radiometry, injects only the new-band radiometry ("new bands = informative radiometry but redundant geometry"). **The single most relevant recipe for "RGB-pretrained FM → 8-band SuperDove", and it dovetails with the two-branch idea below.**
- **PEFT of multispectral FMs for HSI (arXiv:2505.15334, 2025)** — LoRA/KronA/LoKr/**KronA+** adapt SpectralGPT; KronA+ ≈ full fine-tuning at a fraction of params. Evidence PEFT cheaply bridges spectral-domain gaps.

### 8.5 Two-branch RGB + MS fusion (the advisor's "two rami che si uniscono")
Concrete prior art for a high-res-RGB branch fused with a spectral branch:
- **FusAtNet (Mohla et al., CVPR-W 2020)** — spectral-attention + spatial-attention branches with **cross-attention**; the canonical two-attentive-branches-that-cross-talk.
- **CCFormer (2024/25)** — cross-modal cross-attention Transformer, multi-scale token exchange.
- **LoGoCAF (arXiv:2406.17679, 2024)** — two-branch HSI-X encoder; the "X" branch can be the high-res RGB.
- **DSSFN (Remote Sensing 2023)** — dual-stream self-attention (spectral + spatial).
- **Pansharpening line (Attention-FPNet, CDFAN, HetSSNet)** — the most battle-tested "high-spatial PAN + high-spectral MS merge" prior art.
- **Dual-Branch ConvNeXt (2025)** — separate encoders for visible (RGB) vs non-visible (NIR/MS) channels + CBAM fusion decoder — cleanest exact match to "RGB branch + MS branch".

**Verdict for the thesis:** treat high-res FM adaptation as a **bounded, honest experiment, not a pillar** (aligned with the advisor). The **band-ablation** (RGB → +NIR → +RedEdge → 8 b) on a well-tuned supervised baseline is the more defensible core; FM adaptation is the *side* test, framed as: *use DOFA / an RGB-or-MS FM as init, then explicitly bridge the GSD gap (Scale-MAE / DEFLECT / PEFT) and benchmark against a supervised baseline — because PANGAEA says the FM is not guaranteed to win.* The two-branch architecture is a credible alternative init worth one experiment.

---

## 9. Where the thesis sits & the test that matters

- **Setting:** SuperDove, 8 VNIR bands, **3 m**, no SWIR — between sub-metre VHR and 10 m Sentinel-2, and essentially unstudied.
- **The gap (re-scoped):** no high-res material-discrimination study operates at *exactly* VNIR-only 3 m; the closest precedents (Widipaminto Pléiades 2 m, Saba/Hikuwai WV-3 VNIR 1.24 m, Xu UAV cm) are all finer. Confirmed by the June-2026 completeness sweep: **zero** public works at the ~3 m VNIR PlanetScope/SuperDove material-classification point, and **no public terrestrial MS/HS waste-material benchmark at RS resolution** (material-labelled HS datasets exist only at lab/conveyor scale — DeepHS-Debris, TECNALIA WEEE, bulky-waste THz).
- **The test that matters:** *how much of the SWIR/VHR material-discrimination performance can VNIR-only 3 m recover* — quantified by the band ablation and benchmarked against the VNIR competitors above. The most honest yardstick for "what SWIR buys" is **Saba 2025's 97.3% (HS) vs 74.4% (MS)** on the asbestos task.

---

## 10. Datasets — pointer
Full catalog in [`datasets_catalog.md`](datasets_catalog.md) (42 public sets + June-2026 addendum). The structural finding holds: **no public *multispectral-satellite + terrestrial-waste + material-label* dataset.** Closest usable references for the pilot: **Toulouse 2024** (public, 32 urban materials, VNIR+SWIR, 1 m), **Ma 2023 / GRSS Houston** (public, VNIR 2.5 m), **WaRM / KLUM** roof-material spectral libraries, and **Nacala** (public, explicit asbestos class, RGB cm). WV-3 SWIR raw imagery is obtainable **free to PoliMi via ESA eoGateway** (no labels — self-annotate) for the SWIR validation track.

---

## 11. Provenance & confidence

Built from the established `papers/` library (re-scoped to ≤5 m material discrimination) + the **June-2026 deep-research pass** + a **2026-06-16 four-agent verification pass** that read primary sources for every `(confirm)` cell, ran a Chinese-literature completeness sweep, a non-Chinese 2023–2026 sweep, and a foundation-model deep-dive.

**Cells closed (HIGH confidence, primary-source read):** Xu 2022 (OA 85.91%, κ 0.845; Spectrosc. Spectral Anal. 42(12):3927); Cartagena/Martínez 2024 (Heliyon 10(3):e25612, SAM-only, OA 96%, AC 98%); Banolia 2022 (SPIE 12269, F1 0.44/OA 99%); Widipaminto 2021 (TELKOMNIKA 19(2):690, OA 92.92%, κ 0.9069); Saba 2026 (JHM, Macro-F1 97.6% Fine-KNN); Karimzadeh 2021 (OA 88.36%, κ 0.86, SWIR-7 top).

**Corrections made during verification (do not repeat the old errors):**
- **Cartagena/Martínez 2024 uses SAM only**, *not* "SAM/MLC" — MLC appears only in its related-work discussion.
- **Xu 2022** exact κ is **0.845** (not 0.85); sensor is GaiaSky-mini2 (176 b nominal); **exact GSD still unconfirmed** (Chinese full-text paywalled).
- **Balsi** reports **no quantitative metric** (proof-of-concept) and is really a **2023 WHISPERS** paper indexed 2024.
- **Karimzadeh 2021**: the **8-lithology count is unverified**, and the **volume/issue is ambiguous** (67:2421 vs 68(6):2421–2440) — resolve before citing.
- The aquatic-drone plastic work is **Alboody et al. 2023** (*Remote Sensing* 15:3455), *not* "Tasseron". The Inception-net aerial asbestos CNN is **Raczko, Krówczyńska & Wilk 2022**, *not* "Abriha & Szabó" (the real Abriha & Szabó WorldView-2 RF works, Debrecen 2018 & 2023, are separate rows).
- **Wang 2022** (Front. Earth Sci. 10:871529) and the agent-surfaced "Liu/Ye HySpex Yudai/Kalatag" paper are the **same work** — not a new find.

**New, genuinely additive since last revision:** Saba 2025 (RSASE — MS-vs-HS asbestos, the cleanest VNIR-penalty number); the **Chinese airborne CASI/SASI mineral-mapping cluster** (Huang & Zheng 2018; Huaniushan 2020/2021) — material discrimination at fine GSD but **always with SWIR**; the verified FM evidence base (PANGAEA, Scale-MAE, USat, AnySat, DEFLECT, KronA+) and the two-branch fusion family (FusAtNet, CCFormer, LoGoCAF, DSSFN, pansharpening nets, Dual-Branch ConvNeXt).

**Still unconfirmed — confirm from full text before citing a number:** Xu 2022 exact GSD; Abriha & Szabó exact OA; Karimzadeh class-count + volume; Huang/Huaniushan exact GSD (CASI/SASI class ~1–2.5 m, not stated per-study); WV-3 SWIR product GSD per WV-3-SWIR paper (native 3.7 m vs distributed 7.5 m); DOFA venue (preprint as of v3 — do not cite as journal-published); exact venues for Attention-FPNet and Dual-Branch ConvNeXt (ResearchGate-indexed).

*Done: §3–§6 collapsed into the §2bis master comparison table for the Related-Work chapter; `(confirm)` cells closed where reachable. Remaining manual step before the chapter is final: pull PoliMi-library full-text for the few `(confirm)` cells above (Xu GSD, Abriha OA, Karimzadeh metadata) and lock the Saba-cluster DOIs.*
