# Reading List — 12 must-read papers

Curato dalla survey Scopus (`combined_unique.csv` → 699 paper). Selezione ponderata su: pertinenza diretta ai tuoi due filoni (WV3 / hyperspectral / CNN-transformer / temporale 2020↔post), citazioni, recency, open-access.

**Download tip:**
- **Polimi VPN attiva** → clicca il link DOI, l'editore ti dà direttamente il PDF (funziona per Elsevier, IEEE, Taylor & Francis, T&F).
- **OA puro (MDPI, Sensors, RS, Sustainability)** → il link DOI ti porta alla pagina con bottone "Download PDF". I download automatici falliscono per Akamai/Cloudflare; dal tuo browser funzionano normalmente.
- Per gli Elsevier `j*.j*` (Hazard Materials / Env Management): solo via Polimi.

---

## 🟢 ASBESTOS — 7 picks

Filoni mirati: WorldView-3 VNIR (il tuo sensore!), hyperspectral SWIR signature, CNN deep learning, change detection temporale, classificazione urbana supervised/unsupervised.

### 1. ⭐ Satellite-based detection of asbestos-cement roofs using WorldView-3 VNIR data
- **2026** · *Journal of Hazardous Materials* · closed-access
- **Perché**: usa **esattamente il tuo sensore (WV3)**, banda VNIR. Probabilmente il match più diretto al pilot Fase 1.
- DOI: https://doi.org/10.1016/j.jhazmat.2026.141864
- ⚠️ Polimi VPN richiesta.

### 2. ⭐ Affordable risk mapping and detection of asbestos-cement roofs via remote sensing
- **2026** · *Journal of Environmental Management* · closed-access
- **Perché**: top score (32.30) della survey. Approccio "low-cost" → utile per il piano operativo.
- DOI: https://doi.org/10.1016/j.jenvman.2026.128908
- ⚠️ Polimi VPN richiesta.

### 3. Mapping of asbestos cement roofs and their weathering status using hyperspectral
- **2015** · *ISPRS IJGI* · 43 citazioni · **OA (MDPI)**
- **Perché**: probabilmente **Frassy/Bassani** — il riferimento per la firma SWIR a 2.31 µm (Mg-OH bending) citata nel tuo notebook amianto. Indispensabile per giustificare la scelta del sensore SWIR vs SuperDove.
- DOI: https://doi.org/10.3390/ijgi4020928

### 4. Asbestos-cement roofing identification using remote sensing and convolutional neural networks
- **2020** · *Remote Sensing* (MDPI) · 45 citazioni · **OA**
- **Perché**: il **CNN baseline classico** per asbestos roof detection. Comparator obbligato.
- DOI: https://doi.org/10.3390/rs12030408

### 5. Mapping Asbestos-Cement Corrugated Roofing Tiles with Imagery Cube via Machine Learning
- **2022** · *Remote Sensing* (MDPI) · 10 citazioni · **OA**
- **Perché**: approccio "imagery cube" (multispettrale ricco), ML. Buon match con la tua pipeline multispettrale.
- DOI: https://doi.org/10.3390/rs14143418

### 6. Multi-temporal change detection of asbestos roofing: A hybrid object-based deep
- **2024** · *RS Applications: Society and Environment* (Elsevier) · 11 citazioni · OA
- **Perché**: affronta **direttamente il problema temporale** (GT 2020 vs imagery 2023+) che hai nel pilot. Hybrid object-based + deep.
- DOI: https://doi.org/10.1016/j.rsase.2024.101167

### 7. Analysis of asbestos-cement roof classification in urban areas: Supervised and unsupervised
- **2025** · *RS Applications: Society and Environment* (Elsevier) · 5 citazioni · closed
- **Perché**: comparison **supervised vs unsupervised** in contesti urbani — utile per decidere lo stack del pilot.
- DOI: https://doi.org/10.1016/j.rsase.2025.101464
- ⚠️ Polimi VPN richiesta.

---

## 🟢 WASTE — 5 picks

(I 7 paper già in `papers/` coprono il grosso. Queste 5 aggiungono ciò che manca.)

### 8. ⭐ Development and application of an analytical framework for mapping probable illegal landfills
- **2022** · *Waste Management* (Elsevier) · 46 citazioni · closed
- **Perché**: top citation della survey waste (46). Framework analitico end-to-end — utile come blueprint operativo.
- DOI: https://doi.org/10.1016/j.wasman.2022.02.031
- ⚠️ Polimi VPN richiesta.

### 9. Satellite Data Potentialities in Solid Waste Landfill Monitoring: Review and Case Study
- **2023** · *Sensors* (MDPI) · 46 citazioni · **OA**
- **Perché**: **review recente** (≠ Fraternali 2024 che hai già). Survey complementare con case-study.
- DOI: https://doi.org/10.3390/s23083917

### 10. Litter on the streets — solid waste detection using VHR images
- **2023** · *European Journal of Remote Sensing* (T&F) · 20 citazioni · OA
- **Perché**: focus **VHR** (matcha tuo WV3), task waste detection. Recente e citato.
- DOI: https://doi.org/10.1080/22797254.2023.2176006

### 11. Multi-Scale Context Fusion Network for Urban Solid Waste Detection in Remote Sensing
- **2024** · *Remote Sensing* (MDPI) · 3 citazioni · **OA**
- **Perché**: metodo **multi-scale fusion network** — direttamente confrontabile col tuo Swin-T+RSP. Architettura concorrente.
- DOI: https://doi.org/10.3390/rs16193595

### 12. A Practical Deep Learning Architecture for Large-Area Solid Wastes Monitoring
- **2024** · *Applied Sciences* (MDPI) · 9 citazioni · **OA**
- **Perché**: "practical" architecture su large area — perspective operativa, non solo accademica.
- DOI: https://doi.org/10.3390/app14052084

---

## Summary OA status

| Status | Count | Action |
|---|---|---|
| 🟢 MDPI OA (clicca DOI da browser) | 6 | #3, #4, #5, #9, #11, #12 |
| 🟡 OA via Elsevier/T&F (preprint o landing) | 2 | #6, #10 |
| 🔴 Closed (Polimi VPN required) | 4 | #1, #2, #7, #8 |

## Bulk batch — copia-incolla in browser

```
https://doi.org/10.1016/j.jhazmat.2026.141864
https://doi.org/10.1016/j.jenvman.2026.128908
https://doi.org/10.3390/ijgi4020928
https://doi.org/10.3390/rs12030408
https://doi.org/10.3390/rs14143418
https://doi.org/10.1016/j.rsase.2024.101167
https://doi.org/10.1016/j.rsase.2025.101464
https://doi.org/10.1016/j.wasman.2022.02.031
https://doi.org/10.3390/s23083917
https://doi.org/10.1080/22797254.2023.2176006
https://doi.org/10.3390/rs16193595
https://doi.org/10.3390/app14052084
```

Apri tutti con `xdg-open URL` da terminale o trascinali sul browser. Una volta scaricati, mettili in `papers/literature_search/pdfs/` con il nome `<topic>_<year>_<slug>.pdf` come da MANIFEST.json.
