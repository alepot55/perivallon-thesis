# Paper synthesis — organizzazione per sezione slide

Generato 2026-05-25 dopo deep-read di 28 paper (`papers/library/`). Single point of access per la struttura della presentazione: ogni sezione slide è ancorata a 2–5 paper con take-away esatti e numeri citabili.

Fonte: `papers/INDEX.md` (machine-readable: `papers/index.json`). Dettagli per-paper: `papers/notes/<id>.md` sezione `## Note Claude`.

---

## Stat di partenza

- **28 paper** totali letti (27 con PDF + 1 placeholder Guo&Li 2020 in attesa VPN)
- **Critical** (anchor della tesi): 8 — `gibellini-2025-pipeline`, `fraternali-2024-survey`, `torres-2023-aerialwaste`, `xiong-2024-dofa`, `kokaly-2017-splib07a`, `shepherd-2025-asbestos-enmap`, `bonifazi-2026-ac-python`, `aguilar-2021-wv3-ablation`
- **High** (comparatori diretti / SOTA da battere): 14
- **Medium** (contesto + survey): 5
- **Low** (nice-to-have): 1

---

## Through-line della tesi

**Research question**: *qual è il valore aggiunto della classificazione di materiali via dati multispettrali satellitari vs RGB?*

**Evidenza quantitativa più forte (da citare letteralmente nelle slide):**

> **WV-3 ablation (Aguilar et al. 2021, `aguilar-2021-wv3-ablation`):** OA = 90.85% (VNIR) → 96.79% (SWIR) → 97.38% (All Features) per detection di plastica. Salto VNIR→All = **+6.7% OA, +14% kappa**. SWIR domina grazie al Normalized Difference Plastic Index (NDPI).

Questo singolo paper risponde quantitativamente alla research question per il setting plastica/WV-3. La tesi estende la stessa logica al setting waste/SuperDove (no SWIR ma 8 bande VNIR vs 3 RGB).

**Asse complementare (materiale-specifico):**

> **Knowledge-based classifier (Zhou et al. 2021, `zhou-2021-plastic-classifier`):** decision tree su 8 bande SWIR WV-3 discrimina 3 cluster di polimeri (alifatici PE/PVC/PP/POM vs aromatici PET/PS/PC vs PBAT/ABS/PU). Nessun training data — feature engineering basata su firme spettrali pure.

Esempio concreto di **classificazione di materiali** (non solo detection), che è l'asse mancante nei lavori RGB-only.

---

## Mapping per sezione slide

### Slide 2-3 — Problem + research context
**Anchor:** `fraternali-2024-survey` (gap analysis del gruppo PoliMi, 50 paper survey)

**Gap dichiarati nel paper, da citare letteralmente nella slide:**
1. Assenza di benchmark globale unificato per waste detection
2. **Generalizzazione geografica scarsa** dei modelli (cross-country drops di 5-10pp F1)
3. **Material identification non affrontata** (tutti i lavori = binary waste/no-waste, nessuno discrimina cosa)
4. RS non distingue waste **legale vs illegale**
5. Foundation models per RS inesplorati nel dominio waste
6. Manca **court-proof evidence** per uso operativo

**Da fare nelle slide:** lasciare la RQ aperta ("qual è il valore aggiunto della classificazione di materiali"), non pre-rispondere.

---

### Slide 4 — Stack di bande / cos'è un dato satellitare
**Anchor:** `torres-2023-aerialwaste` per il setup tecnico (8 bande VNIR vs 3 RGB) + `kokaly-2017-splib07a` per concettualizzazione (firma spettrale = vettore di riflettanze).

**Numeri da slide:**
- USGS splib07a: 2151 canali da 350 a 2500 nm
- WorldView-3: 8 bande VNIR (400-1040 nm) + 8 bande SWIR (1100-2400 nm)
- SuperDove: 8 bande VNIR @3 m (no SWIR)
- Sentinel-2: 13 bande @10/20/60 m

---

### Slide 4.1 — Visualizzazioni (RGB / false-color IR / NDVI)
**Anchor:** Generazione personale da QGIS o matplotlib. Nessun paper specifico, ma scene single-material da `kokaly-2017-splib07a` (USGS spectral library) per il plot delle firme.

---

### Slide 5 — Spectral signatures (pedagogica)
**Anchor:** `kokaly-2017-splib07a` (USGS library, fonte autoritativa) + `plastics-uv-swir-2020` (firme polimeri specifici)

**Plot consigliato:** 3-4 firme spettrali singolo-materiale (vegetazione, suolo, cemento, asbestos) sovrapposte. Da `kokaly-2017-splib07a` Note Claude: convoluzioni S2 e WV-3 sono **già disponibili nella libreria** — usare direttamente.

**Bande diagnostiche da evidenziare:**
- Mg-OH @ 2.31 µm → asbestos cement (citato in `cilia-2015-ac-weathering` e `shepherd-2025-asbestos-enmap`)
- C-H @ 1.73 µm e 1.66 µm → plastiche/idrocarburi (in tutti i paper plastic)
- λ=800 nm singola → discrimina C&D waste (`cdw-2025-critical-wavelengths`, finding bombshell)

---

### Slide 6 — Sensor landscape (radar/triangle chart)
**Anchor:** sintesi da `reference_sensor_tradeoffs.md` (memoria) — non un paper unico ma cheatsheet trasversale.

**Sensori da includere (assi: GSD spaziale, # bande spettrali, revisit time):**
- Sentinel-2 (10 m, 13 bande, 5 gg)
- SuperDove (3 m, 8 bande, daily)
- WorldView-3 (0.3 m PAN, 8 VNIR @1.2 m + 8 SWIR @3.7 m, 1 gg on-demand)
- PRISMA (30 m, 240 bande, 7 gg)
- EnMAP (30 m, 230 bande, ~4 gg) — citato in `shepherd-2025-asbestos-enmap`

---

### Slide 7-8 — Low/medium resolution survey (10-30 m, S2 + EnMAP)

**Anchor papers (3+1):**
1. `marida-2022-marine-debris` — MARIDA, S2 marine debris, 11 paesi 2015-2021
2. `global-dumpsites-2023` — Sun et al. Nature Comms, BCA-Net dumpsite globale 28 città
3. `tisza-2023-waste-change` — S2+PlanetScope river-waste Tisza
4. `shepherd-2025-asbestos-enmap` — EnMAP @30m asbestos (low-res hyperspectral, è la "frontiera" del low-res)

**Riga tabella formato `Titolo | Input | Metodo | Risultato`:**

| Titolo | Input | Metodo | Risultato |
|---|---|---|---|
| MARIDA (Kikaki 2022) | S2 13-band @10m | RF + U-Net pixel-level | F1 0.79 (RF best, multi-class 15) |
| Global dumpsites (Sun 2023) | VHR commercial | BCA-Net deep learning | Sensitivity 98% / Precision 70% su 4 tipologie waste, 28 città |
| Tisza river-waste (2023) | S2 + PlanetScope | RF + Plastic Index | Accuracy 96% change detection |
| Shepherd 2025 asbestos | EnMAP 230-band @30m | Cascade 8 classifier + manual verify | 86% positive match rate (823/2300 detection) |

**Visual per slide (Thomas: "cosa il SOTA becca / cosa manca a 10m"):**
- MARIDA Fig. 3 (firme spettrali MD vs NatM) + Fig. 4 (t-SNE) → mostra la confusione spettrale residua a 10m
- Global dumpsites Fig. 1d (esempi VHR su 4 città) → mostra DOVE il modello becca, e per contrasto dove perde
- Tisza Fig. 8-9 (post-processing morfologico) → mostra clustering/closing necessari per pulire detection
- Shepherd Fig. supplementary 5-14 (field spectra) → field-truth necessario per calibrazione

---

### Slide 9-10 — High resolution survey (WV-3, VHR commercial)

**Anchor papers (4):**
1. `aguilar-2025-macroplastics-wv3` — WV-3 SWIR macroplastics terrestri US-Mexico
2. `guo-li-2020-ndpi-wv3` — NDPI urbano (placeholder, PDF VPN)
3. `zhou-2021-plastic-classifier` — Knowledge-based classifier alifatici/aromatici
4. `bonifazi-2026-ac-python` — WV-3 VNIR+SWIR Python open-source Mantova asbestos

**Riga tabella:**

| Titolo | Input | Metodo | Risultato |
|---|---|---|---|
| Aguilar 2025 macroplastics | WV-3 SWIR 8-band @3.7m | Matched filter + 18 spettri lab | Precision 92.5% riparian watershed |
| Guo & Li 2020 NDPI | WV-3 SWIR 4-band | Spectral index `(B7-B8)/(B7+B8)` | (numeri post-VPN download) |
| Zhou 2021 KB-classifier | WV-3 SWIR 8-band | Decision tree knowledge-based | 3 cluster polimeri discriminati, OA >80% aromatic vs aliphatic |
| Bonifazi 2026 AC-Python | WV-3 VNIR+SWIR @1.2m | Py6S + MLC + threshold building-level | F1 0.87, 25319 edifici Mantova multi-temporale |

**Visual per slide:**
- Aguilar 2025 Fig. 4-5-7 → caso più forte per spectral added value urbano
- Zhou 2021 Fig. spettri → mostra le narrow bands SWIR che catturano polimeri specifici
- Bonifazi 2026 multi-temporal → rimozione asbestos visibile cross-year

**Argomento per slide (Thomas):** "VHR commercial + SWIR = il SOTA reale per classification di materiali, ma 1 strip = 1500 €/scena. La domanda: si può fare con SuperDove gratis-ish?"

---

### Slide 11 — Gap analysis
**Anchor:** `fraternali-2024-survey` (per i gap dichiarati) + sintesi cross-paper di seguito.

**Gap concreti che la tesi può attaccare:**

1. **Material classification gap** — TUTTI i paper waste-detection a 10m sono binari (waste/no-waste). Nessuno classifica COSA c'è. → Argomento: SuperDove 8-band può fare un primo passo.
2. **Generalizzazione cross-country** (`gibellini-2025-pipeline`: -5.10pp F1 mediamente da Italia a Grecia/Svezia/Romania).
3. **Gap di scala** — Bonifazi @1m raggiunge F1 0.87 sul SUO sito, MARIDA @10m raggiunge F1 0.79 su 11 paesi. La tesi sta nel mezzo (SuperDove @3m) — nessun benchmark coperto.
4. **Whitewash / paint-sealing failure mode** (Aguilar 2021 + Shepherd 2025): spectral feature mascherato da copertura artificiale → falso negativo. Pattern speculare al "waste covered" (telone su discarica).

---

### Slide 12 — Approach (la tesi)
**Anchor:** `gibellini-2025-pipeline` (baseline metodologica) + `xiong-2024-dofa` (l'opzione FM raccomandata) + `aguilar-2021-wv3-ablation` (precedente metodologico ablation VNIR/SWIR/All).

**Architettura proposta (da call note 2026-05-22):**
- Baseline = Swin-T + RSP su AerialWaste **RGB** (replica `gibellini-2025-pipeline`)
- Estensione MS = adapter su Swin per le 8 bande SuperDove (3 strategie da letteratura: weight-inflation / random-init-extra / late-fusion)
- Plus FM alternative = DOFA (`xiong-2024-dofa`) come sensor-agnostic baseline

**Ablation principale della tesi (modellata su `aguilar-2021-wv3-ablation`):**
- (i) RGB only (replica baseline)
- (ii) RGB + 5 bande aggiuntive SuperDove (Coastal, Yellow, Red-Edge, NIR2)
- (iii) 8 bande SuperDove via DOFA
- Confrontare gli OA/F1, *à la* Aguilar 90.85 → 96.79 → 97.38

---

### Slide 13 — Foundation models (slide dedicata DOFA, richiesta Thomas)

**Anchor:** `xiong-2024-dofa` (DOFA come scelta) + `thoreau-2025-deflect` (adapter PEFT per fine-tune efficiente) + comparator: `szwarcman-2024-prithvi-eo2`, `anysat-2024`, `wang-2024-softcon`.

**Take-away unico per slide (vedi Note Claude di xiong-2024-dofa):**

> DOFA è **sensor-agnostic via wavelength-conditioned hypernetwork**: basta passare le wavelength centrali delle 8 bande SuperDove e funziona plug-and-play, senza retraining. Alternativa PEFT efficiente: DEFLECT (Thoreau 2025) come adapter ortogonale su DOFA.

**Tabella comparativa FM** (da Note Claude `fm-rs-survey-2024`):

| FM | SuperDove-ready? | Verdetto |
|---|---|---|
| **DOFA** (Xiong 2024) | ✅ plug-and-play | **Scelta principale** |
| AnySat | parziale (fine-tune only) | Comparator alternativo |
| Prithvi-EO-2.0 | ❌ vincolato 6-band HLS | Escludere |
| SatMAE | ❌ rigido grouping S2 | Baseline storica solo |
| SSL4EO-S12 | parziale (no Yellow) | Baseline efficient |
| SpectralGPT | ❌ vincolato S2 12-band | Escludere |
| SoftCon | metodo riapplicabile | Ricetta (DINOv2 + random-init) |
| DEFLECT | ✅ adapter su qualsiasi ViT | Combina con DOFA |

---

### Slide 14 — Pilot Fase 1 amianto

**Anchor:** `shepherd-2025-asbestos-enmap` + `cilia-2015-ac-weathering` + `bonifazi-2026-ac-python` + `aguilar-2021-wv3-ablation` (asbestos triade).

**Take-away combinato:**
- Shepherd 2025: dimostra che asbestos detection da satellite **hyperspectral 30m** funziona (86% match) — quindi il segnale **esiste** anche in low-res
- Bonifazi 2026: stesso problema con WV-3 multispectral @1.2m, F1 0.87 — il SWIR multispectral basta
- Cilia 2015: workflow SAM + ISD index è il baseline storico riusabile
- Aguilar 2021: SWIR domina VNIR di 6 pp OA — quindi SuperDove (no SWIR) ha un *handicap noto*

**Domanda aperta per il pilot:** può SuperDove (no SWIR, 8 bande VNIR @3m) fornire signal sufficiente per asbestos? Workflow proposto (vedi `project_pilot_workflow_amianto.md` in memoria): firme da poligoni → SAM pairwise → clustering esplorativo.

---

### Slide 15 — Roadmap / conclusion
Sintesi finale. Nessun paper specifico, ma richiamo a `xiong-2024-dofa` (FM scelto), `aguilar-2021-wv3-ablation` (metric della tesi), `shepherd-2025-asbestos-enmap` (validazione pilot).

---

## Cross-paper themes

### Tema 1: "Few wavelengths suffice"
**Convergono:** `cdw-2025-critical-wavelengths` (RGB + 2 narrowband ≈ HSI 768-band per C&D), `aguilar-2021-wv3-ablation` (NDPI singolo cattura il 96% del segnale plastica), `kokaly-2017-splib07a` (convoluzioni S2/WV-3 già pre-fatte).

**Implication tesi:** SuperDove 8 bande (vs S2 13 vs WV-3 16) potrebbe essere "sufficiente" — empiricamente da verificare.

### Tema 2: "Spectral added value su SWIR domina, ma SuperDove non ha SWIR"
**Convergono:** `aguilar-2021-wv3-ablation` (+6.7% SWIR vs VNIR), `zhou-2021-plastic-classifier` (tutto SWIR), `aguilar-2025-macroplastics-wv3` (matched filter solo SWIR), `guo-li-2020-ndpi-wv3` (NDPI è SWIR).

**Implication tesi:** Il tema critico per giustificare SuperDove vs WV-3 è quanto il VNIR esteso (8 vs 3 bande) compensa la mancanza di SWIR. Risposta probabile: **parzialmente per detection coarse, non per classificazione fine di materiali**. Onestà richiesta nelle slide.

### Tema 3: "Foundation models cambiano il gioco"
**Convergono:** `xiong-2024-dofa` (sensor-agnostic), `anysat-2024` (any-modality), `thoreau-2025-deflect` (PEFT efficiente), `fm-rs-survey-2024` (panoramica), `wang-2024-softcon` (ricetta efficient pretrain).

**Implication tesi:** La domanda RGB-vs-MS non si gioca più sulla quantità di dati. DOFA permette di provare 8 bande SuperDove con pretraining gratis. La tesi ha leva inedita rispetto a Mazzola/Gibellini.

### Tema 4: "Generalizzazione = il gap operativo vero"
**Convergono:** `gibellini-2025-pipeline` (-5.1pp F1 cross-country), `fraternali-2024-survey` (gap esplicito), `bonifazi-2026-ac-python` (validazione site-specific stretta), `marida-2022-marine-debris` (multi-paese ma F1 0.79 medio basso).

**Implication tesi:** Anche se non è il focus primario, vale la pena dedicare 1-2 slide a "come la classificazione di materiali aiuta la generalizzazione" — l'argomento è: una firma spettrale di asbestos è più trasferibile geograficamente di un texture pattern RGB.

### Tema 5: "Failure mode comune: copertura artificiale"
**Convergono:** `aguilar-2021-wv3-ablation` (whitewash su serre maschera plastica), `shepherd-2025-asbestos-enmap` (paint-sealing su asbestos maschera Mg-OH).

**Implication tesi:** È il limite onesto da dichiarare. Speculare al problema "waste covered/burned" che vale anche per AerialWaste.

---

## Note tecniche operative

- **Sorgente di verità**: `papers/index.json` (machine-readable). Le note `.md` sono human-readable.
- **Aggiornamento**: dopo nuovo paper, `bootstrap_papers.py` → `download_papers.py` → `sync_excel.py` → `build_index.py`. La sezione `## Note Claude` è preservata su re-run.
- **Cross-link tra paper**: campo `relates_to:` nel frontmatter. Estensibile come graph.
- **Quando Thomas/Fraternali chiede "quale paper per X"**: prima cercare `papers/INDEX.md` (per topic) o `papers/notes/*.md` (per tag).
- **Aggiornare questo synthesis**: re-leggere ogni 3-4 paper aggiunti per mantenere coerente il through-line.
