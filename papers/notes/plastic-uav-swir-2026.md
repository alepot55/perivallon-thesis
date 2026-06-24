---
id: "plastic-uav-swir-2026"
title: "Attention-gated U-Net for robust cross-domain plastic waste segmentation using a UAV-based hyperspectral SWIR sensor"
authors: ["et al."]
year: 2026
venue: "Remote Sensing"
doi: "10.3390/rs18010182"
arxiv: null
link: "https://www.mdpi.com/2072-4292/18/1/182"
tags: ["plastic", "drone", "swir", "hyperspectral", "u-net", "generalization"]
relevance: "high"
status: "pending"
pdf: null
in_slides: ["vhr-13classes"]
relates_to: []
---

## Target class
9 plastic

## Riassunto
UAV SWIR HSI (900–1700 nm); attention-gated residual U-Net; 96.8% acc / 91.1% F1. NIR-SWIR (1215, 1732 nm) drive it; generalization limited by data diversity, not architecture.

## Cosa riutilizzare (tesi)
Polymer-type identification needs SWIR; drone-HSI route + an OOD-generalization datapoint.

## Note Claude
Aggiunto 2026-06-23 nella ricerca VHR 30-50 cm sui 13 materiali (vedi `docs/02_research/sota_vhr_13classes.md`). Claim verificati nel run deep-research.
