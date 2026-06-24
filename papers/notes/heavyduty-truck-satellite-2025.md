---
id: "heavyduty-truck-satellite-2025"
title: "A deep-learning approach to detect and classify heavy-duty trucks in satellite images"
authors: ["et al."]
year: 2025
venue: "PMC (open access)"
doi: null
arxiv: null
link: "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12302943/"
tags: ["vehicles", "containers", "object-detection", "vhr"]
relevance: "medium"
status: "pending"
pdf: null
in_slides: ["vhr-13classes"]
relates_to: []
---

## Target class
3 vehicles / 6 containers

## Riassunto
CenterNet + Mask R-CNN ensemble; classifies container size/status and trucks from satellite. Vehicles/containers detectable by shape; no ELV-specific detector exists.

## Cosa riutilizzare (tesi)
Container/vehicle object detection from satellite; flags the ELV sub-gap.

## Note Claude
Aggiunto 2026-06-23 nella ricerca VHR 30-50 cm sui 13 materiali (vedi `docs/02_research/sota_vhr_13classes.md`). Claim verificati nel run deep-research.
