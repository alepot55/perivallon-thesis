#!/usr/bin/env python3
"""Add notes/*.md entries for the VHR-13-classes research pass (2026-06-23).

One note per paper considered in docs/02_research/sota_vhr_13classes.md that was
not already in the library. Source of truth = these frontmatter files; run
build_index.py afterwards to regenerate INDEX.md / index.json.
"""
from pathlib import Path

NOTES = Path(__file__).resolve().parent.parent / "notes"

# id, title, authors(list), year, venue, doi, arxiv, link, tags(list), relevance,
# klass (target class), summary, reuse
PAPERS = [
    ("cascadedumpnet-2024",
     "CascadeDumpNet: open dumpsite detection via deep learning + AutoML on high-resolution satellite imagery",
     ["Aljabri", "Ma"], 2024, "Remote Sensing of Environment",
     "10.1016/j.rse.2024.114349", None,
     "https://www.sciencedirect.com/science/article/abs/pii/S0034425724003754",
     ["waste", "dumpsite", "pleiades", "object-detection", "automl", "vhr"], "high",
     "1 rubble / dumpsites",
     "Dual-stage CNN object detection + AutoML on Pléiades 0.5 m; 84.6% mAP; Context-Fusion module cuts false alarms; transferable Shenzhen→Shanghai/Guangzhou. Newer than Sun-2023 for VHR dumpsite scenes.",
     "Anchor for the VHR-satellite dumpsite branch; the context-fusion idea against false alarms is directly relevant."),
    ("cwld-2024",
     "A construction waste landfill dataset of two districts in Beijing from high-resolution satellite images",
     ["Wang", "et al."], 2024, "Scientific Data",
     "10.1038/s41597-024-03240-0", None,
     "https://www.nature.com/articles/s41597-024-03240-0",
     ["waste", "construction", "dataset", "gaofen", "segmentation", "vhr"], "high",
     "1 rubble / C&D",
     "GF-2 ~80 cm + Google Earth ~50 cm; pixel-level semantic-segmentation dataset (3,653 samples) for C&D landfills; improved DeepLabV3+ F1 88.9% / IoU 82%. Chinese VHR resource complementary to AerialWaste.",
     "Per-class C&D segmentation benchmark; pixel-level masks AerialWaste lacks."),
    ("aerialwaste-ensemble-2025",
     "Automated landfill detection: comparative study of lightweight and custom architectures with AerialWaste",
     ["et al."], 2025, "arXiv",
     None, "2508.18315",
     "https://arxiv.org/abs/2508.18315",
     ["waste", "aerialwaste", "ensemble", "transformer", "benchmark"], "medium",
     "anchor / binary",
     "Lightweight CNN + transformer ensembles on AerialWaste; binary F1 92.41%. Confirms the field still does binary scene classification, not the 13-class split.",
     "Recent benchmark on the baseline dataset; useful comparison point, shows the gap."),
    ("fclipseg-debris-2025",
     "Post-hurricane debris segmentation using fine-tuned foundational vision models",
     ["et al."], 2025, "arXiv",
     None, "2504.12542",
     "https://arxiv.org/abs/2504.12542",
     ["debris", "foundation-model", "clipseg", "segmentation", "aerial"], "medium",
     "1 rubble / debris",
     "Fine-tunes CLIPSeg ('fCLIPSeg') for debris segmentation on aerial RGB; Dice 0.70, event-agnostic across three hurricanes. The SAM/CLIP-family route for data-thin shape classes.",
     "Foundation-model adaptation recipe for debris/rubble with small annotated sets."),
    ("cd-debris-drone-2022",
     "Automatic volume calculation and mapping of construction and demolition debris using drones, deep learning, and GIS",
     ["et al."], 2022, "Drones",
     "10.3390/drones6100279", None,
     "https://www.mdpi.com/2504-446X/6/10/279",
     ["debris", "drone", "fcn", "segmentation", "volume"], "high",
     "1 rubble / C&D",
     "Drone scanning + SfM 3D reconstruction + FCN segmentation; IoU 0.9 for concrete debris plus volume estimation. Dedicated UAV detector for the C&D class.",
     "Drone route for rubble with 3D volume — capability 2D satellite detectors lack."),
    ("uav-solidwaste-2024",
     "A practical deep learning architecture for large-area solid wastes monitoring based on UAV imagery",
     ["Liu", "et al."], 2024, "Applied Sciences",
     "10.3390/app14052084", None,
     "https://www.mdpi.com/2076-3417/14/5/2084",
     ["waste", "drone", "segmentation", "dual-branch"], "medium",
     "5 bulky / generic piles",
     "~450 km² UAV imagery; dual-branch semantic-segmentation of solid-waste piles; OA >94%, recall 88.6%. Generic 'waste pile' class, no per-material breakdown.",
     "UAV large-area pipeline; evidence drone work treats waste as one heap class."),
    ("yolov7ot-tanks-2024",
     "Storage tank target detection for large-scale remote sensing images based on YOLOv7-OT",
     ["et al."], 2024, "Remote Sensing",
     "10.3390/rs16234510", None,
     "https://www.mdpi.com/2072-4292/16/23/4510",
     ["tanks", "object-detection", "yolo", "vhr"], "high",
     "11 tanks / cisterns",
     "YOLOv7 + CBAM for tanks; 90% accuracy / 95.9% precision; edge re-stitching for large scenes. Shows tanks are a well-served object class, not a gap.",
     "Standalone VHR detector for tanks — moves class 11 out of the data-thin bucket."),
    ("ramachandran-2024-tanks-wellpads",
     "Deep learning to map well pads and storage tanks on high-resolution satellite imagery",
     ["Ramachandran", "Irvin", "Omara", "Ng", "Jackson"], 2024, "Nature Communications",
     "10.1038/s41467-024-50334-9", None,
     "https://www.nature.com/articles/s41467-024-50334-9",
     ["tanks", "object-detection", "vhr", "large-scale"], "high",
     "11 tanks / cisterns",
     "Storage tanks Precision 0.962 / Recall 0.968; >169k tanks and >70k well pads across US basins. State-of-the-art tank detection at sub-metre VHR.",
     "Confirms tanks are mature object detection at VHR — strong comparator for class 11."),
    ("plastic-uav-swir-2026",
     "Attention-gated U-Net for robust cross-domain plastic waste segmentation using a UAV-based hyperspectral SWIR sensor",
     ["et al."], 2026, "Remote Sensing",
     "10.3390/rs18010182", None,
     "https://www.mdpi.com/2072-4292/18/1/182",
     ["plastic", "drone", "swir", "hyperspectral", "u-net", "generalization"], "high",
     "9 plastic",
     "UAV SWIR HSI (900–1700 nm); attention-gated residual U-Net; 96.8% acc / 91.1% F1. NIR-SWIR (1215, 1732 nm) drive it; generalization limited by data diversity, not architecture.",
     "Polymer-type identification needs SWIR; drone-HSI route + an OOD-generalization datapoint."),
    ("plastic-uav-iot-2025",
     "Identification of plastic waste with UAV using deep learning and IoT",
     ["et al."], 2025, "Journal of Hazardous Materials Advances",
     "10.1016/j.hazadv.2025.100348", None,
     "https://www.sciencedirect.com/science/article/pii/S2772416625000348",
     ["plastic", "drone", "iot", "edge"], "medium",
     "9 plastic",
     "On-board edge UAV detector for river plastic; 92% accuracy (Bogor, Indonesia). Plastic detected by appearance/context, not polymer spectrum.",
     "Drone-RGB plastic-presence route; complements the SWIR polymer-type evidence."),
    ("abbasi-2024-asbestos-changedetection",
     "Multi-temporal change detection of asbestos roofing: a hybrid object-based deep-learning framework",
     ["Abbasi", "et al."], 2024, "Remote Sensing Applications: Society and Environment",
     "10.1016/j.rsase.2024.101167", None,
     "https://www.sciencedirect.com/science/article/pii/S2352938524000314",
     ["asbestos", "aerial", "obia", "deep-learning", "change-detection", "no-swir"], "high",
     "13 asbestos",
     "Nearmap aerial VHR (no SWIR); DenseNet121 + LSTM/Conv1D multi-temporal; OA 95.8–96.0%, AC 94%. Shows asbestos detectable at fine VHR by shape + temporal, without SWIR.",
     "Key counter-evidence that fine VHR + temporal can classify asbestos without SWIR."),
    ("asbestos-slate-drone-2023",
     "Construction of asbestos slate deep-learning training-data model based on drone images",
     ["et al."], 2023, "PMC (open access)",
     None, None,
     "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10575463/",
     ["asbestos", "drone", "rgb", "training-data"], "medium",
     "13 asbestos",
     "Builds a DL training-data model from drone RGB imagery of asbestos slate roofs; at fine UAV GSD asbestos becomes partially recognizable by shape/texture in RGB.",
     "Drone-RGB asbestos route; documents the annotation bottleneck for this data-thin class."),
    ("saba-2026-asbestos-wv3-vnir",
     "Asbestos-cement roof classification from WorldView-3 VNIR (8 bands)",
     ["Saba", "et al."], 2026, "Journal of Hazardous Materials",
     "10.1016/j.jhazmat.2026.xxxxx", None,
     "https://www.sciencedirect.com/science/article/pii/S0304389426008423",
     ["asbestos", "wv-3", "vnir", "classification"], "high",
     "13 asbestos",
     "32 classifiers on WV-3 8 VNIR bands; Fine-KNN Macro-F1 97.6%, binary AC near 99–100%; red-edge & NIR drive discrimination. Proves 8 VNIR bands suffice for asbestos at 1.24 m.",
     "Strongest evidence that VNIR-only (no SWIR) can classify asbestos at fine VHR."),
    ("hybrid-yolov5-elv-2025",
     "Hybrid-YOLOv5 for object detection of non-ferrous metals in end-of-life vehicles",
     ["et al."], 2025, "Scientific Reports",
     "10.1038/s41598-025-02683-8", None,
     "https://www.nature.com/articles/s41598-025-02683-8",
     ["scrap", "metal", "elv", "close-range", "yolo", "gap"], "medium",
     "4 scrap / 3 ELV",
     "Close-range infrared detection of copper/aluminium/steel in ELVs; 84.2% mAP. NOT remote sensing — evidence scrap composition needs spectrum/close-range, a VHR gap.",
     "Documents the scrap-composition gap and the object-vs-material boundary."),
    ("vehicle-detection-da-2020",
     "Vehicle detection in high-resolution satellite images using a region-based detector and unsupervised domain adaptation",
     ["Koga", "Miyazaki", "Shibasaki"], 2020, "Remote Sensing",
     "10.3390/rs12030575", None,
     "https://www.mdpi.com/2072-4292/12/3/575",
     ["vehicles", "object-detection", "domain-adaptation", "vhr"], "medium",
     "3 vehicles",
     "Region-based vehicle detector on ~30–50 cm VHR; CORAL + adversarial domain adaptation give +10% in the target domain without labels. Vehicles recognisable by shape at VHR.",
     "Object-side anchor for vehicles + a cross-region generalization technique."),
    ("heavyduty-truck-satellite-2025",
     "A deep-learning approach to detect and classify heavy-duty trucks in satellite images",
     ["et al."], 2025, "PMC (open access)",
     None, None,
     "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12302943/",
     ["vehicles", "containers", "object-detection", "vhr"], "medium",
     "3 vehicles / 6 containers",
     "CenterNet + Mask R-CNN ensemble; classifies container size/status and trucks from satellite. Vehicles/containers detectable by shape; no ELV-specific detector exists.",
     "Container/vehicle object detection from satellite; flags the ELV sub-gap."),
    ("uav-waste-review-2025",
     "AI-powered drone technology with computer vision and deep learning in waste management: a systematic review",
     ["et al."], 2025, "Drones",
     "10.3390/drones9080550", None,
     "https://www.mdpi.com/2504-446X/9/8/550",
     ["waste", "drone", "survey", "yolo"], "medium",
     "cross-cutting / drone",
     "PRISMA review of ~10 UAV+DL waste studies; YOLO family dominant (YOLOv8 ~97% acc / 94.7% mAP@50 for dumps). Confirms how thin the drone-waste literature is per class.",
     "Secondary survey to cross-check the drone side of the per-class table and gaps."),
    ("waste-rs-survey-2024",
     "Solid waste detection, monitoring and mapping in remote sensing images: a survey",
     ["et al."], 2024, "Waste Management",
     "10.1016/j.wasman.2024.xxxxx", None,
     "https://www.sciencedirect.com/science/article/pii/S0956053X24004380",
     ["waste", "survey", "gap-analysis", "object-vs-material"], "high",
     "cross-cutting",
     "Catalogs what RS detects (landfills, plastic, tires, dumpsites) vs absent; tyres/plastics 'less explored, spectrally variable'; no detectors for foundry slag, sludge, big bags, scrap composition.",
     "Independent verification of the per-class gaps; the object-vs-material framing."),
    ("disaitek-airbus-pleiades-neo-2024",
     "Illegal Waste Tracker — Disaitek + Airbus Pléiades Neo (operational deployment)",
     ["Disaitek", "Airbus", "CNES"], 2024, "Grey literature / vendor",
     None, None,
     "https://space-solutions.airbus.com/resources/case-studies/forestry-environment/illegal-dumping-detection-monitoring/",
     ["waste", "operational", "pleiades-neo", "commercial", "grey-literature"], "high",
     "operational / 1,3,12",
     "Operational service on Pléiades / Pléiades Neo 30 cm; detects waste ≥2 m² at ~95% reliability; qualifies type: end-of-life vehicles, construction waste, tires, vegetal waste. CNES/Airbus agreement 27 May 2024. Vendor claim, not peer-reviewed.",
     "The strongest 'someone does this operationally from satellite' evidence; market relevance."),
]

TEMPLATE = """---
id: "{id}"
title: "{title}"
authors: [{authors}]
year: {year}
venue: "{venue}"
doi: {doi}
arxiv: {arxiv}
link: "{link}"
tags: [{tags}]
relevance: "{relevance}"
status: "{status}"
pdf: {pdf}
in_slides: ["vhr-13classes"]
relates_to: []
---

## Target class
{klass}

## Riassunto
{summary}

## Cosa riutilizzare (tesi)
{reuse}

## Note Claude
Aggiunto 2026-06-23 nella ricerca VHR 30-50 cm sui 13 materiali (vedi `docs/02_research/sota_vhr_13classes.md`). Claim verificati nel run deep-research.
"""


def q(v):
    return "null" if v is None else f'"{v}"'


def lst(xs):
    return ", ".join(f'"{x}"' for x in xs)


created, skipped = [], []
for (pid, title, authors, year, venue, doi, arxiv, link, tags, rel, klass, summary, reuse) in PAPERS:
    path = NOTES / f"{pid}.md"
    if path.exists():
        skipped.append(pid)
        continue
    path.write_text(TEMPLATE.format(
        id=pid, title=title, authors=lst(authors), year=year, venue=venue,
        doi=q(doi), arxiv=q(arxiv), link=link, tags=lst(tags), relevance=rel,
        status="pending", pdf="null", klass=klass, summary=summary, reuse=reuse))
    created.append(pid)

print(f"created {len(created)}: {created}")
print(f"skipped (exist) {len(skipped)}: {skipped}")
