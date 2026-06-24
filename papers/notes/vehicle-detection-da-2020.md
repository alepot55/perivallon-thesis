---
id: "vehicle-detection-da-2020"
title: "Vehicle detection in high-resolution satellite images using a region-based detector and unsupervised domain adaptation"
authors: ["Koga", "Miyazaki", "Shibasaki"]
year: 2020
venue: "Remote Sensing"
doi: "10.3390/rs12030575"
arxiv: null
link: "https://www.mdpi.com/2072-4292/12/3/575"
tags: ["vehicles", "object-detection", "domain-adaptation", "vhr"]
relevance: "medium"
status: "pending"
pdf: null
in_slides: ["vhr-13classes"]
relates_to: []
---

## Target class
3 vehicles

## Riassunto
Region-based vehicle detector on ~30–50 cm VHR; CORAL + adversarial domain adaptation give +10% in the target domain without labels. Vehicles recognisable by shape at VHR.

## Cosa riutilizzare (tesi)
Object-side anchor for vehicles + a cross-region generalization technique.

## Note Claude
Aggiunto 2026-06-23 nella ricerca VHR 30-50 cm sui 13 materiali (vedi `docs/02_research/sota_vhr_13classes.md`). Claim verificati nel run deep-research.
