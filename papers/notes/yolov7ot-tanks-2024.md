---
id: "yolov7ot-tanks-2024"
title: "Storage tank target detection for large-scale remote sensing images based on YOLOv7-OT"
authors: ["et al."]
year: 2024
venue: "Remote Sensing"
doi: "10.3390/rs16234510"
arxiv: null
link: "https://www.mdpi.com/2072-4292/16/23/4510"
tags: ["tanks", "object-detection", "yolo", "vhr"]
relevance: "high"
status: "pending"
pdf: null
in_slides: ["vhr-13classes"]
relates_to: []
---

## Target class
11 tanks / cisterns

## Riassunto
YOLOv7 + CBAM for tanks; 90% accuracy / 95.9% precision; edge re-stitching for large scenes. Shows tanks are a well-served object class, not a gap.

## Cosa riutilizzare (tesi)
Standalone VHR detector for tanks — moves class 11 out of the data-thin bucket.

## Note Claude
Aggiunto 2026-06-23 nella ricerca VHR 30-50 cm sui 13 materiali (vedi `docs/02_research/sota_vhr_13classes.md`). Claim verificati nel run deep-research.
