# Related work (Chapter 2) — draft, post-pivot

Draft of thesis Chapter 2 for the post-pivot task (call 2026-07-17): binary illegal-landfill
detection in very-high-resolution satellite imagery under resolution degradation, with
weakly-supervised localization. Target ~5 LaTeX pages, article format (`indice_tesi_v0.md`).
Written 2026-07-22. Citations as [Author Year], to reconcile with the thesis `.bib` (verified
entries in `loop_prof_sota/11_references.md`). All numbers come from locally verified sources
(`baseline_gibellini_frozen.md`, `wsol_mini_sota.md`, the verified bibliography).

---

This chapter reviews three bodies of work: the detection of waste sites in remote sensing
imagery, which provides the task definition and the baseline this thesis builds on (Section
2.1); weakly-supervised object localization (WSOL) and its evaluation protocol (Section 2.2);
and the effect of spatial resolution on detection (Section 2.3). The closing section states the
gap at their intersection and the position of this work.

Throughout, GSD (ground sampling distance) denotes the on-ground size of one image pixel, VHR
(very high resolution) denotes sub-metre to metre-class imagery, and CAM denotes the class
activation map of a classifier.

## 2.1 Waste detection from remote sensing

The automated analysis of overhead imagery for solid waste has grown into a distinct research
line. The survey by [Fraternali et al. 2024] reviews about fifty studies published between 1987
and 2023 and organizes them by task, sensor, and method. Two observations from that survey frame
this chapter. First, published work relies almost entirely on RGB imagery, aerial or satellite.
Second, the dominant task is locating candidate sites, not characterizing their content. Site
detection supports a concrete workflow: environmental agencies such as the Italian ARPAs screen
large territories by photointerpretation, and a model that ranks image tiles by confidence
reduces the area an operator must inspect.

The reference dataset for the Italian setting is AerialWaste [Torres and Fraternali 2023], built
from ARPA Lombardia records over 487 municipalities. Images come from three sources at different
GSDs: AGEA orthophotos (20 cm), WorldView-3 (30 cm, pansharpened RGB), and Google Earth. Labels
are binary at the tile level (waste present or absent); 22 fine-grained material tags annotated
by experts cover about 72% of the positives, but are released as metadata rather than as a
benchmark. Site coordinates are withheld for enforcement reasons. For localization studies, the
dataset includes segmentation masks on 169 test images (841 polygons); the original paper shows
CAMs on these images qualitatively and reports no localization metric.

The baseline this thesis starts from is the pipeline of [Gibellini et al. 2025]. An input VHR
image is tiled; each georeferenced tile passes through a binary scene classifier that outputs a
confidence score and a Grad-CAM saliency map; scores and maps are overlaid in a GIS to guide
photointerpretation. The experimental design spans 36 configurations: two architectures
(ResNet-50, Swin-T), three GSDs (20, 30, 50 cm), three context sizes (100, 150, 210 m), and two
pretraining sources (ImageNet, RSP). The best configuration, Swin-T with RSP pretraining at
20 cm GSD and 100 m context, reaches an F1 of 92.02% (precision 90.02, recall 94.13) on
AerialWaste; remote-sensing pretraining gives a modest but consistent gain over ImageNet
(+1.62 percentage points on the best configuration). Tested on sites from Greece, Sweden, and
Romania, the model loses 5.10 F1 points on average against the Lombardy test set, which
quantifies the geographic generalization cost. On the operational side, at a confidence
threshold of 0.2 screening with the pipeline finds 63.2% more sites than manual
photointerpretation alone while reducing the inspected area by 60.2% [Gibellini et al. 2025].
Localization, however, is only shown qualitatively through Grad-CAM figures.

Detection has also been demonstrated on satellite imagery alone and at wider scale.
[Sun et al. 2023] map dumpsites globally with a deep detection model and use the results to
study the factors that influence waste distribution; the paper shows CAMs for illustration, not
evaluation. CascadeDumpNet [Zhang and Ma 2024] reports 84.6% mAP for open dumpsite detection on
Pléiades imagery at about 0.5 m GSD, and [Marrocco et al. 2024] detect illegal microdumps in
Campania from Pléiades and GeoEye-1 imagery, confirming that spaceborne VHR sensors support the
task. On the aerial side, lightweight and ensemble architectures benchmarked on
AerialWaste reach binary F1 up to 92.41% [Sharmily et al. 2025], confirming the strength of the
RGB classification baseline.

A complementary research line asks what a detected site contains rather than where it is. The
closest precedent inside the same group is [Alari 2024], a multi-label material classification
study over a 13-category taxonomy built on the AerialWaste annotations, reaching weighted F1
69.21% on a 5-category subset and 59.42% on 10 categories, on RGB imagery. Outside the waste
domain, material-specific spectral work shows that some target materials are separable with
more than three bands: asbestos-cement roofs from WorldView-3 VNIR data
[Saba et al. 2026; Bonifazi et al. 2026] and plastic-covered surfaces through VNIR and SWIR band
combinations [Aguilar et al. 2021]. These results concern roofs and greenhouses, not waste
deposits. The gap between site-level and material-level scores shows that material
characterization remains a harder, open problem; this thesis keeps it out of scope and
concentrates on detection, where the satellite-only and resolution questions are unanswered.

In summary, waste-site detection is well developed on aerial RGB imagery at 20 to 50 cm GSD.
Coverage is thinner for satellite-only data, for GSDs above 50 cm, and above all for the
quantitative evaluation of localization, which the waste literature treats only qualitatively.

## 2.2 Weakly-supervised localization

Weakly-supervised object localization is the problem of localizing objects using only
image-level labels at training time, without bounding boxes or masks. The standard approach
derives a class activation map from a trained classifier [Zhou et al. 2016], typically through
gradient-based variants such as Grad-CAM [Selvaraju et al. 2017] and its successors
(Grad-CAM++, LayerCAM); the heatmap is thresholded and converted into a box or a mask. A known
limitation is that CAMs tend to cover the most discriminative parts of an object rather than its
full extent [Zhang et al. 2021].

Evaluation is a central issue in this literature. [Choe et al. 2020] show that earlier WSOL
comparisons were confounded by inconsistent threshold and model selection, and propose a
protocol based on GT-known metrics: MaxBoxAcc (fraction of images where the predicted box
reaches IoU at least 0.5 with the ground truth, maximized over the CAM threshold), MaxBoxAccV2
(the same averaged over IoU thresholds 0.3, 0.5, 0.7), and PxAP where pixel masks exist; the
protocol was later extended in a journal version (IEEE TPAMI, 2023). The pointing game, which
checks whether the heatmap maximum falls inside the ground-truth region, is a common
complementary metric. The survey of [Zhang et al. 2021] covers the WSOL and weakly-supervised
detection literature on natural images and standardizes the metric definitions.

In remote sensing, weak supervision is attractive because dense annotation of overhead imagery
is expensive. The survey by [Fasana et al. 2022], from the same group as this thesis, reviews
weakly-supervised object detection for remote sensing images and its evaluation practices
(mAP, CorLoc). [Bai et al. 2023] propose a self-directed WSOL method for remote sensing images
in which Grad-CAM++ activations guide an auxiliary loss, and introduce dedicated benchmarks
(C45V2, PN2). More recent work generates pseudo masks from the Segment Anything Model to
supervise a detector [SAM-induced WSOD 2024, authors to confirm]. Across these works the
evaluation is carried out at the fixed native GSD of each benchmark; the robustness of
localization to resolution is not an axis of study.

In the waste literature specifically, CAM-based localization appears in several works but is
never evaluated quantitatively. [Torres and Fraternali 2023] provide test masks and show CAMs
without reporting a metric; [Sun et al. 2023] use CAMs as illustration; [Gibellini et al. 2025]
put Grad-CAM maps in front of photointerpreters but evaluate only the classification.

The closest quantitative precedent is [Mazzola 2024], a thesis from the same group on binary
asbestos-roof classification from WorldView-3 and Pléiades Neo multispectral imagery
(pansharpened to 0.3 m), with ImageNet-pretrained CNNs and an RGB-versus-multispectral
comparison. The work computes the IoU between predicted and ground-truth bounding boxes as a
localization measure, and finds that the multispectral input improves IoU by about 4 points over
RGB in its best setting (EfficientNetB0 on Pléiades Neo). It also compares pansharpened 0.3 m
against native 1.2 m data, with better precision, recall, and IoU at 0.3 m. Four limitations
matter for the present work. The evaluation does not follow the standard WSOL protocol: no
MaxBoxAcc, no pointing game, no analysis across CAM thresholds, and the procedure that extracts
the predicted box from the heatmap is not described. The resolution comparison has two points
and conflates the GSD change with the pansharpening process. The target is a compact,
regularly-shaped object (a roof), whereas waste deposits are diffuse and multi-material.
Finally, the method is vanilla Grad-CAM, with no refinement. These points define the deltas that
Section 2.4 turns into requirements for this thesis.

## 2.3 Resolution effects in remote sensing detection

Spatial resolution is the main cost axis of VHR satellite imagery, and operational programmes
for environmental monitoring point toward metre-class rather than sub-metre data. Whether
detection and localization survive coarser GSD is therefore an operational question as well as a
scientific one.

Within the waste literature, the most direct evidence is the GSD ablation in
[Gibellini et al. 2025]. By resampling all image sources to target GSDs of 20, 30, and 50 cm,
the study finds that classification F1 is nearly flat across this range, and that the context
size (100 to 210 m) has a minor effect, penalizing ResNet-50 at large contexts while Swin-T
stays stable. Two bounds of this result matter here. The ablation stops at 50 cm, below the
metre-class regime of interest; and it measures classification only, so it says nothing about
what happens to localization as resolution degrades. [Mazzola 2024] reaches 1.2 m but, as
discussed above, with a two-point comparison confounded by pansharpening.

The sensor context explains why the 0.3 m to 1.2 m range is the relevant one. Free
medium-resolution missions such as Sentinel-2 (10 to 20 m GSD) are too coarse to resolve
individual waste sites [Fraternali et al. 2024]. Current VHR satellites bracket the range
studied here: WorldView-3 provides multispectral bands at 1.24 m with a 0.31 m panchromatic
channel, and Pléiades Neo provides 1.2 m multispectral with 0.3 m panchromatic. Pansharpening
converts between the two ends of this range but alters the multispectral signal, one reason to
prefer controlled resampling of the same images when resolution is the variable under study.

Two methodological cautions from the literature apply to any resolution-degradation protocol.
[Corley et al. 2024] show that resizing and input-normalization choices alone materially change
the measured performance of pretrained remote sensing models, so the resampling procedure must
be fixed and reported as part of the experimental design. Separately, geospatial foundation
models are pretrained mostly at decametric GSD and become plausible candidates only near the
metre scale [Xiong et al. 2024; Astruc et al. 2025; Szwarcman et al. 2024]; their value on this
task is untested and treated as an open experimental question.

The gap in this section is symmetric to the one in Section 2.2. Resolution studies in the waste
domain measure classification or detection accuracy; WSOL studies evaluate localization at fixed
GSD. No work in either line measures how localization quality degrades as GSD degrades in a
controlled way.

## 2.4 Positioning

To our knowledge, no published study quantitatively evaluates weakly-supervised localization
under controlled resolution degradation in remote sensing, in the waste domain or elsewhere; a
targeted search on this intersection returned no direct precedent, so the claim is stated with
that caveat. The individual ingredients all exist: strong binary waste classifiers with
qualitative CAM output [Gibellini et al. 2025; Sun et al. 2023], a standard quantitative WSOL
protocol [Choe et al. 2020], WSOL methods for remote sensing at fixed GSD [Bai et al. 2023], a
GSD ablation limited to classification and to 50 cm [Gibellini et al. 2025], and a single-column
IoU evaluation at two confounded resolutions [Mazzola 2024]. This thesis combines them. It
trains a binary illegal-landfill classifier on satellite-only multispectral imagery, following
the two-step recipe of [Gibellini et al. 2025], and evaluates two quantities along a controlled
GSD axis obtained by resampling the same images (0.3 m, about 0.7 m, 1.2 m): detection F1, and
localization quality measured with the protocol of [Choe et al. 2020] (MaxBoxAcc, pointing
game, box IoU) on an object-level bounding-box subset of the dataset. Against [Mazzola 2024],
the deltas are explicit: a diffuse multi-material target instead of roofs, a standard and
reproducible localization protocol instead of a single undocumented IoU column, a multi-point
degradation of the same images instead of a pansharpened-versus-native pair, and, if the method
track matures, a refinement beyond vanilla Grad-CAM. Against [Gibellini et al. 2025], the thesis
extends the resolution axis beyond 50 cm to satellite metre-class data and adds the localization
measurement that the published pipeline shows only qualitatively.

---

## References (to reconcile with the thesis `.bib`)

- Aguilar et al. 2021. Object-based greenhouse mapping, WorldView-3 VNIR/SWIR. Remote Sensing 13(11):2133.
- Alari 2024. Multi-label waste-material classification. M.Sc. thesis, PoliMi (politesi 10589/230633). [Exact title from politesi.]
- Astruc et al. 2025. AnySat. CVPR 2025 (arXiv 2412.14123).
- Bai et al. 2023. Localizing From Classification: Self-Directed WSOL for Remote Sensing Images. IEEE (Xplore 10242056; venue to confirm).
- Bonifazi et al. 2026. Python-based workflow for asbestos roof mapping. Geomatics 6(3):41.
- Choe et al. 2020. Evaluating Weakly Supervised Object Localization Methods Right. CVPR 2020; extended in IEEE TPAMI (2023).
- Corley et al. 2024. Revisiting pre-trained RS model benchmarks: resizing and normalization. CVPR 2024 Workshops (PBVS).
- Fasana et al. 2022. Weakly Supervised Object Detection for Remote Sensing Images: A Survey. Remote Sensing (MDPI).
- Fraternali et al. 2024. Solid waste detection, monitoring and mapping in RS images: a survey. Waste Management 189:88-102.
- Gibellini et al. 2025. A Deep Learning Pipeline for Solid Waste Detection in Remote Sensing Images. Waste Management Bulletin. DOI 10.1016/j.wmb.2025.100246.
- Marrocco et al. 2024. Illegal microdumps detection in multi-mission satellite images. IEEE Access 12:79585-79601.
- Mazzola 2024. Deep Learning approaches for asbestos classification via Multispectral Satellite Images. M.Sc. thesis, PoliMi (politesi 10589/230433).
- Saba et al. 2026. Satellite-based detection of asbestos-cement roofs, WorldView-3 VNIR. J. Hazardous Materials 508:141864.
- SAM-induced WSOD 2024. SAM-Induced Pseudo Fully Supervised Learning for WSOD in RS Images. Remote Sensing (MDPI). [Authors to fetch.]
- Selvaraju et al. 2017. Grad-CAM. ICCV 2017. [To add to the verified bibliography.]
- Sharmily et al. 2025. Automated landfill detection with the AerialWaste dataset. arXiv 2508.18315 (venue to confirm).
- Sun et al. 2023. Global waste distribution via deep-learning based dumpsite detection. Nature Communications 14:1444.
- Szwarcman et al. 2024. Prithvi-EO-2.0. arXiv 2412.02732.
- Torres and Fraternali 2023. AerialWaste dataset for landfill discovery in aerial and satellite images. Scientific Data 10:63.
- Xiong et al. 2024. DOFA foundation model. arXiv 2403.15356.
- Zhang and Ma 2024. CascadeDumpNet. Remote Sensing of Environment 313:114349.
- Zhang et al. 2021. Weakly Supervised Object Localization and Detection: A Survey. IEEE TPAMI.
- Zhou et al. 2016. Learning Deep Features for Discriminative Localization (CAM). CVPR 2016. [To add to the verified bibliography.]

Open items before the `.bib` is final: authors of the SAM-induced WSOD paper; exact title of the
Alari thesis; venues of Bai et al. 2023 and Sharmily et al. 2025; add the standard CAM
references (Zhou 2016, Selvaraju 2017), which are not in the verified local bibliography yet.
