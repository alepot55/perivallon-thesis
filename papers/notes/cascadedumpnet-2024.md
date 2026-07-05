---
id: "cascadedumpnet-2024"
title: "CascadeDumpNet: open dumpsite detection via deep learning + AutoML on high-resolution satellite imagery"
authors: ["Zhang", "Ma"]
year: 2024
venue: "Remote Sensing of Environment"
doi: "10.1016/j.rse.2024.114349"
arxiv: null
link: "https://www.sciencedirect.com/science/article/abs/pii/S0034425724003754"
tags: ["waste", "dumpsite", "pleiades", "object-detection", "automl", "vhr"]
relevance: "high"
status: "pending"
pdf: null
in_slides: ["vhr-13classes"]
relates_to: []
---

## Target class
1 rubble / dumpsites

## Riassunto
Dual-stage CNN object detection + AutoML on Pléiades 0.5 m; 84.6% mAP; Context-Fusion module cuts false alarms; transferable Shenzhen→Shanghai/Guangzhou. Newer than Sun-2023 for VHR dumpsite scenes.

## Cosa riutilizzare (tesi)
Anchor for the VHR-satellite dumpsite branch; the context-fusion idea against false alarms is directly relevant.

## Note Claude
Aggiunto 2026-06-23 nella ricerca VHR 30-50 cm sui 13 materiali (vedi `docs/02_research/sota_vhr_13classes.md`). Claim verificati nel run deep-research.
