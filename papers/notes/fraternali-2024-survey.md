---
id: "fraternali-2024-survey"
title: "Solid waste detection, monitoring and mapping in remote sensing images: A survey"
authors: ["Fraternali", "Castelli", "Torres"]
year: 2024
venue: "arXiv"
doi: null
arxiv: "2402.09066"
link: "arXiv:2402.09066"
tags: ["waste", "survey", "gap-analysis"]
relevance: "critical"
status: "downloaded"
pdf: "library/fraternali-2024-survey.pdf"
in_slides: ["gap-analysis", "intro"]
relates_to: []
---

## Obiettivo
Mappare sistematicamente lo stato dell'arte sulla waste detection da RS, identificare gap e direzioni future.

## Metodo
Literature review sistematica. Tassonomia per tecniche (visual interpretation, ML tradizionale, DL), dataset, sensori.

## Risultati
Identificati gap chiave: limite RGB esplicito, assenza benchmark standardizzato, material classification non affrontata. NIR indicato come banda più informativa mancante.

## Riassunto
Survey del gruppo PoliMi. Mappa il campo e identifica esplicitamente il limite RGB come gap principale, motivando l'estensione multispettrale.

## Cosa riutilizzare (tesi)
Motivazione della tesi (gap RGB), tassonomia delle tecniche, bibliography strutturata come punto di partenza.

## Note Claude

**Punti chiave**
- Survey sistematica PRISMA su 50 lavori (1987–2023) di waste detection da RS, classificati in 3 obiettivi (Detection, Monitoring, Mapping) e 6 task. Identifica esplicitamente i gap che la tesi attacca.
- Tassonomia tecniche: visual interpretation, descriptive indices, multi-factor, feature extraction+ML, traditional CV, Deep Learning CV, other. Solo 11/50 lavori usano DL e quasi tutti su immagini RGB/pansharpened.
- Italia = paese più attivo; PERIVALLON (grant 101073952) è il contesto Horizon Europe della tesi stessa. Survey è il razionale di partenza diretto.

**Figure/tabelle usabili in slide** (numero fig + cosa mostra)
- Fig. 1: trend pubblicazioni 2008–2023 (picco 2022, 11 paper) — mostra crescita interesse.
- Fig. 2: distribuzione geografica per continente/paese — Italia domina in Europa.
- Fig. 3: tassonomia 50 lavori in 3 obiettivi (Detection 27, Monitoring 11, Mapping 12) + 6 task.
- Tab. 5: tecniche × input data × task — utile per posizionare il proprio contributo.

**Numeri forti** (metriche concrete: OA, F1, # bande, GSD)
- 1235 paper iniziali → 50 finali dopo PRISMA. 23 satelliti coperti, 4 dataset pubblici. 75% lavori in Europa+Asia. Solo Lavender 2022, Sun 2023, Rajkumar 2022 testano generalizzazione globale.

**Limite onesto** (terminologia: "generalizzazione" non "OOD", "classificare per rischio" non "rilevare")
- Gap dichiarati: (1) assenza benchmark standardizzato globale; (2) generalizzazione geografica scarsa (case study locali); (3) waste material identification non affrontata — serve risoluzione ≤30 cm e MS per discriminare rubble/tires/metal/wood; (4) RS visivo non distingue legale da illegale (manca site risk assessment); (5) Foundation Models RS (Prithvi-100M) inesplorati per waste; (6) court-proof evidence collection aperta.

**Cross-link**
- `torres-2023-aerialwaste`: dataset PoliMi citato come l'unico con waste classes ampie ma geographic-limited (motiva tesi MS).
- `xiong-2024-dofa` / `szwarcman-2024-prithvi-eo2`: FM-RS citati esplicitamente come direzione futura.
- `fm-rs-survey-2024`: complementare per Foundation Models RS.
- `global-dumpsites-2023` (Sun 2023): tra i pochi a testare generalizzazione globale.
