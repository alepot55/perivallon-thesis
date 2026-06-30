# Risk & Prioritization Framing of Illegal Waste / Hazardous Materials from Remote Sensing — Literature Review

*Primary-source-verified. Confidence tags: HIGH (verified against primary/authoritative source), MEDIUM (verified secondary or partial), UNCERTAIN (inference / needs confirmation). Autonomous research loop, iteration 1, 2026-06-27.*

This review covers a thread the existing thesis research does not: not *detecting* waste, but *tiering detected sites by risk* to assign intervention priority. The literature splits cleanly into (a) RS/GIS risk-scoring methods, (b) the regulatory material→hazard mapping, (c) Italian/ARPA operational prioritization, and (d) the PERIVALLON crime-enforcement framing.

---

## 1. Waste-site risk/hazard scoring from RS or GIS

The most directly relevant primary source is **Fazzo et al. (2020)**, a GIS-based waste-risk indicator built for 38 municipalities of the Campania "Land of Fires" (Naples/Caserta) — the canonical illegal-dumping health crisis in Italy. **(HIGH)** Their **Municipal Risk Index** operationalizes risk as a composite:

- a per-site **Hazard Index** = a *numeric* score 1–5 for **disposal modality** (5 = burning, 1 = controlled storage) crossed with a *letter* score A–G for **waste-type hazard** (A = highly hazardous/non-visible, G = inert with no release potential);
- a **Hazard Risk Level** converting that to powers of ten so one high-hazard site outranks many low-hazard ones;
- **population exposure** via 100 m buffers intersected with census tracts;
- combined as `RI = S × HRL × (S/Sc) × P` and binned into four risk classes.

This is the cleanest published precedent for "material/disposal type + proximity → tiered risk," and it is Italian. It does *not*, however, derive material from spectral RS — hazard is assigned from inspection records. That gap is the thesis's opening. **(HIGH for the method; inference that MS could feed the hazard term — UNCERTAIN)**

Two newer RS+GIS prioritization frameworks confirm the pattern: the **Dumpsite Inspection Priority Index (DIPI)** for CALABARZON, Philippines (DEMATEL + GIS + remote sensing, 2025) produces an inspection-priority ranking; and a **Dakar susceptibility map** (MDPI *Sustainability*, 2025) fuses RS, GIS, citizen science and **AHP**. **(MEDIUM — secondary verification)** Across the broader MCDA literature, **AHP is the dominant operationalization** (also fuzzy-AHP, ANP, TOPSIS, Best-Worst), with criteria recurring as: proximity to surface water/drainage, slope/flood-proneness, land cover, distance to population/schools/agriculture, and economic feasibility. **(HIGH — consistent across multiple Springer/Frontiers/MDPI sources)** Note these are mostly *siting* studies (where to put a landfill) repurposable as *risk* studies (how dangerous an existing dump is) — the exposure criteria are identical, the sign is flipped.

**How "risk" is operationalized, synthesized:** `risk ≈ hazard(material × disposal type) × exposure(distance to receptors: water, population, agriculture) × magnitude(area/quantity)`. This is the load-bearing equation for the thesis.

---

## 2. Material → hazard mapping (the regulatory backbone)

The hazard term above is not invented — it is **legally codified** in the **European List of Waste (LoW) / European Waste Catalogue**, established by **Commission Decision 2000/532/EC** and operative under the **Waste Framework Directive 2008/98/EC**. **(HIGH — EUR-Lex primary source)** Mechanics:

- 20 chapters, six-digit codes (EWC codes).
- An **asterisk (\*)** marks **"absolute" hazardous entries** — hazardous *without further assessment*.
- **"Mirror entries"** are hazardous only if a dangerous substance exceeds threshold (assessed against **hazard properties HP1–HP15**, Annex III).
- Recently amended (e.g. Delegated Decision (EU) **2025/934** for battery wastes). **(MEDIUM)**

This directly supports the material→tier mapping: **asbestos (EWC 17 06 05\* "materials containing asbestos", absolute hazardous) and other starred hazardous waste = urgent tier; inert construction & demolition rubble (EWC 17 01 / 17 05, non-starred) = low tier.** **(HIGH for the codes existing and asterisk semantics; the specific tier assignment is the thesis's framing — defensible inference, MEDIUM)** ARPA and Italian operators classify waste using exactly these EWC codes (transposed via D.Lgs 152/2006), so the framing is operationally native, not academic.

---

## 3. ARPA Lombardia / Italian operational prioritization

**Two distinct Italian regimes** already prioritize by risk, giving the thesis concrete institutional grounding.

**(a) Asbestos roofs — Piano Regionale Amianto Lombardia (PRAL).** Approved by **DGR 8/1526 of 22 Dec 2005**, PRAL's strategic objective is census + mapping to quantify risk from friable/compact asbestos and prioritize remediation. **(HIGH)** Critically, conservation state — and therefore remediation priority — is scored by the **Indice di Degrado (Degradation Index)**, established for Lombardy by **d.d.g. 13237 of 18 Nov 2008** (the national instrument is **D.M. 6 settembre 1994**). **(HIGH for the Lombardy decree; D.M. 1994 MEDIUM)** **ARPA Lombardia** executed the mapping in two phases under the "AMIANTO" project — Phase 1 updating >2,400 km², Phase 2 (2020) mapping ~1,300 km² of never-before-mapped territory. **(HIGH — this is the exact `Mappatura_2020` WFS layer in `asbestos/data`, closing the loop with the thesis's own dataset.)** So: an RS/GIS asbestos map already exists *and* a risk-index (degradation) drives intervention order — the thesis sits squarely inside an established prioritization workflow.

**(b) Contaminated sites — D.Lgs 152/2006, Part IV, Title V.** Italy's environmental code mandates **site-specific risk analysis (Analisi di Rischio sanitario-ambientale)** as the decision tool, implemented via the **RBCA / ASTM** framework and **ISPRA/SNPA methodological criteria** (ISS-INAIL database). **(HIGH)** Risk here is quantitative exposure-to-receptor modelling — the same hazard × exposure logic, institutionalized.

**Synthesis:** Italian authorities *do not* intervene on detection alone — they triage by a risk/degradation index. The thesis's risk-tiering objective therefore mirrors how ARPA actually works, which is a strong "operational relevance" argument. **(HIGH)**

---

## 4. PERIVALLON / EU environmental-crime context

The parent project frames the domain as **organised environmental crime enforcement**, not pollution monitoring. **PERIVALLON** (Horizon Europe **101073952**, started Dec 2022) explicitly lists, alongside automatic satellite waste detection, **"real-time risk assessment"** and **"optimal inspection and characterisation of sites of interest"** as platform capabilities, serving **Police Authorities and Border Guards**. **(HIGH — CORDIS)** The end-user need is *triage of finite inspection capacity* — i.e. priority ranking — which is precisely the value the thesis adds on top of detection. **(HIGH for project goals; the explicit "material→priority" link as a stated PERIVALLON deliverable — UNCERTAIN, infer from the "characterisation"/"risk assessment" language.)**

---

## 5. Framing this as a citable thesis contribution

Existing RS work is **detection-only** (PERIVALLON's CV tool, the thesis's own Swin-T baseline) or **risk-scoring with externally-supplied hazard** (Fazzo et al. assign hazard from records, not pixels). MCDA studies operationalize exposure but treat material as known. **No published pipeline derives material/hazard class *from multispectral RS* and feeds it into a risk tier.** That junction is the novelty.

**Positioning statement (citable):** "Prior art either detects waste sites (PERIVALLON, RGB DL baselines) or ranks known sites by GIS exposure criteria (Fazzo 2020; AHP siting literature), with the hazard term supplied by ground records. This work closes the loop: **multispectral material discrimination → EWC-aligned hazard class → exposure-weighted risk tier → ARPA intervention priority**, the first step of which (spectral material info) is exactly the term every prior risk index takes as a given." **(MEDIUM — defensible given the surveyed literature; absence-of-prior-art claims should be hedged.)**

---

## What this means for the thesis

- **Reframe the problem slide** around the operational reality: ARPA already triages (PRAL Indice di Degrado; D.Lgs 152/2006 risk analysis) — the bottleneck is not detection but *characterization for priority*. Detection-only output is low-value to the end user. **(HIGH)**
- **Justify material classification in risk terms:** material is the *hazard* term in `risk = hazard × exposure × magnitude`. MS adds value precisely where every risk index currently has a blind spot. This converts "does MS beat RGB on F1?" into "does MS supply the hazard input that detection alone cannot?" — a stronger, harder-to-dismiss claim.
- **Anchor hazard mapping to law, not opinion:** cite Decision 2000/532/EC + Directive 2008/98/EC (asterisk = absolute hazardous; asbestos 17 06 05\*) so the asbestos/hazardous=urgent vs inert/C&D=low tiering is *regulatory*, not arbitrary.
- **Use Fazzo et al. (2020) as the methodological template** — it is Italian, peer-reviewed, and already encodes "disposal-type + waste-type-hazard + population proximity." Adopt its `hazard × exposure × magnitude` structure; your contribution is replacing its record-based hazard with MS-derived material.
- **Leverage the asbestos pilot as proof-of-concept for tiering**, not just detection: PRAL + ARPA `Mappatura_2020` + Indice di Degrado show a real risk-index workflow your MS material layer could feed. Frame Filone 2 as "the risk-tier demonstrator."
- **Tie to PERIVALLON's stated "real-time risk assessment" capability** to show end-user pull — your output is the missing characterization input, not a parallel detector.
- **Hedge the novelty claim** ("to our knowledge, no RS pipeline derives EWC hazard class from MS to drive a risk tier") rather than asserting absolute first.
- **Add an exposure-proximity layer as cheap future work** (distance to water/population/agriculture from open GIS) to make the risk tier complete and visibly operational, even if material classification stays the experimental core.

---

### Sources
- [Fazzo et al. 2020, GIS waste-risk indicator, Land of Fires (PMC7459911)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7459911/)
- [Dumpsite Inspection Priority Index (DIPI), CALABARZON — DEMATEL/GIS/RS](https://www.researchgate.net/publication/400666653)
- [Mapping illegal dumping susceptibility, Dakar — RS/GIS/citizen science/AHP (MDPI 2025)](https://www.mdpi.com/2071-1050/17/24/11137)
- [Solid-waste site selection GIS+AHP (Frontiers 2025)](https://www.frontiersin.org/journals/sustainability/articles/10.3389/frsus.2025.1528851/full)
- [Commission Decision 2000/532/EC — List of Waste (EUR-Lex)](https://eur-lex.europa.eu/eli/dec/2000/532/oj/eng)
- [Piano Regionale Amianto Lombardia — DGR 8/1526, 2005 (Olympus/UniUrb)](https://olympus.uniurb.it/index.php?option=com_content&view=article&id=4561:2005lombamianto)
- [ARPA Lombardia AMIANTO mapping + Indice di Degrado (Certifico)](https://www.certifico.com/ambiente/legislazione-ambiente/legislazione-rifiuti/amianto-censimento-e-mappatura-dalla-regione-lombardia)
- [Regione Lombardia — Piano Regionale Amianto, official](https://www.regione.lombardia.it/wps/portal/istituzionale/HP/DettaglioServizio/servizi-e-informazioni/Cittadini/salute-e-prevenzione/Sicurezza-negli-ambienti-di-vita-e-di-lavoro/amianto-piano-regionale-flussi-informativi-bonifica/amianto-piano-regionale-flussi-informativi-bonifica)
- [D.Lgs 152/2006 risk analysis for contaminated sites (Title V) / ISPRA RBCA](https://www.wastezero.it/gestione-siti-contaminati-analisi-rischio/)
- [PERIVALLON project fact sheet (CORDIS 101073952)](https://cordis.europa.eu/project/id/101073952)
- [PERIVALLON — satellite + computer vision illicit waste detection](https://perivallon-he.eu/fighting-illicit-waste-dumping-using-satellite-images-and-computer-vision/)
