---
id: "fclipseg-debris-2025"
title: "Post-hurricane debris segmentation using fine-tuned foundational vision models"
authors: ["et al."]
year: 2025
venue: "arXiv"
doi: null
arxiv: "2504.12542"
link: "https://arxiv.org/abs/2504.12542"
tags: ["debris", "foundation-model", "clipseg", "segmentation", "aerial"]
relevance: "medium"
status: "downloaded"
pdf: "library/fclipseg-debris-2025.pdf"
in_slides: ["vhr-13classes"]
relates_to: []
---

## Target class
1 rubble / debris

## Riassunto
Fine-tunes CLIPSeg ('fCLIPSeg') for debris segmentation on aerial RGB; Dice 0.70, event-agnostic across three hurricanes. The SAM/CLIP-family route for data-thin shape classes.

## Cosa riutilizzare (tesi)
Foundation-model adaptation recipe for debris/rubble with small annotated sets.

## Note Claude
Aggiunto 2026-06-23 nella ricerca VHR 30-50 cm sui 13 materiali (vedi `docs/02_research/sota_vhr_13classes.md`). Claim verificati nel run deep-research.
