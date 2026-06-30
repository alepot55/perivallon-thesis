# 🗺️ PANORAMA — SOTA, dataset & direzione per la presentazione al prof

**Obiettivo:** panorama chiaro e study-ready per la presentazione al prof (prossima settimana), ri-centrato sulla realtà-dati confermata **WorldView-3 + Pléiades Neo (sub-metro VHR)**, con focus **dataset**. Prodotto da un loop di ricerca autonomo (2026-06-27, 2 iterazioni).

## ⚡ Ripasso veloce (se hai poco tempo)
Parti da **[09_master_cheatsheet.md](09_master_cheatsheet.md)** (tutto in una pagina) + **[08_prof_qa_defense.md](08_prof_qa_defense.md)** (20 domande del prof con risposte). Poi torna qui per l'approfondimento.

## 📖 Percorso di studio (leggi in quest'ordine)

1. **[01_synthesis_direction.md](01_synthesis_direction.md)** — il punto di partenza. Realtà-dati riconciliata, direzione affilata (rischio + ablazione MS-vs-RGB), cosa cambiare nel deck, domande aperte.
2. **[02_datasets_usable.md](02_datasets_usable.md)** — **i dataset che possiamo usare** (priorità): matrice di usabilità per ruolo, il "ponte di etichette", le 8 cose da studiare per prime.
3. **[03_dataset_verification.md](03_dataset_verification.md)** — verifica/fattibilità: accesso gratis ESA TPM (entrambi i sensori), rischio-SWIR (disponibilità, non risoluzione), **stack di layer-etichette Lombardia** (DUSAF/AGISCO/DBT, tutti EPSG:32632), recupero WV-3 dietro AerialWaste, backbone per l'ablazione (DOFA spina dorsale).
4. **[04_experimental_design.md](04_experimental_design.md)** — il protocollo sperimentale completo (ladder bande R0→R3, 3 assi, split + generalizzazione) + il **demonstrator amianto** end-to-end (il pezzo subito fattibile).
5. **[05_field_metadata.md](05_field_metadata.md)** — schema-attributi **verificato live** dei layer Lombardia (endpoint reali, codici-stato amianto, DUSAF, AGISCO) → reference d'implementazione del pilot.
6. **[06_presentation_outline.md](06_presentation_outline.md)** — bozza narrativa slide-by-slide (18 slide) per il prof, da riconciliare con `../../01_calls/call_sota_revision.md`.
7. **[07_technical_foundations.md](07_technical_foundations.md)** — **la scienza**: tabella materiale↔feature↔banda, stima remota degrado amianto, generalizzazione, object-vs-material (il decompositore B−A = chimica vs texture).
8. **[08_prof_qa_defense.md](08_prof_qa_defense.md)** — **20 domande probabili del prof + risposte** difendibili e oneste.
9. **[09_master_cheatsheet.md](09_master_cheatsheet.md)** — **cheat-sheet una pagina** + glossario (ripasso veloce).
10. **[10_related_work_draft.md](10_related_work_draft.md)** — **bozza capitolo Related Work/SOTA** in inglese, pronta da rifinire su Overleaf (+ reference list).
11. **[11_references.md](11_references.md)** + **[references.bib](references.bib)** — **bibliografia verificata** (DOI controllati, correzioni) pronta per il `.bib` della tesi.
12. Ricerca grezza con tutte le fonti: [research_pleiades_neo.md](research_pleiades_neo.md) · [research_crosssensor_pansharpening.md](research_crosssensor_pansharpening.md) · [research_risk_framing.md](research_risk_framing.md)
13. **[00_LOOP_LOG.md](00_LOOP_LOG.md)** — stato del loop, iterazioni, prossimi passi.

## 📅 Piano di studio per domani (suggerito)
1. **30 min** — `09_master_cheatsheet` + `08_prof_qa_defense` (quadro + difese).
2. **45 min** — `01_synthesis_direction` + `02_datasets_usable` (direzione + dati: le tue priorità).
3. **45 min** — `07_technical_foundations` (la scienza: tabella materiale↔banda, generalizzazione, B−A chimica-vs-texture).
4. **30 min** — `04_experimental_design` + `05_field_metadata` (cosa farai, con quali endpoint).
5. **30 min** — `10_related_work_draft` (la prosa per la tesi) + `06_presentation_outline` (per il prof).
6. Tieni a fianco le **domande per Thomas** (sotto) e segna le tue decisioni.

## 🎯 I messaggi chiave (in una schermata)

- **SWIR rientra nello scope** (WV-3, a **3.7 m nativi** — il vecchio cap a 7.5 m è decaduto): l'ablazione arriva fino a +SWIR su dati reali; Aguilar/Saba/Bonifazi diventano benchmark **diretti**.
- **Pléiades Neo** = VNIR-only, Red Edge = banda di valore, **nessun benchmark material peer-reviewed** → gap/opportunità.
- **Dati gratis via ESA Third Party Missions** per entrambi i sensori (proposal ~9 settimane + consumo entro 1 anno) → **sottomettere ASAP**.
- **Dataset usabili subito**: WFS amianto pubblico + geolocalizzato → pilot amianto fattibile ora. AerialWaste = etichette ottime ma **coordinate riservate (ARPA)** → serve accordo interno.
- **Stack etichette Lombardia** co-registrabile senza riproiezione (EPSG:32632): amianto (positivi) + DUSAF classi 131–134 (positivi deboli/negativi puliti) + siti contaminati AGISCO (prior di rischio) + footprint DBT.
- **Direzione**: MS material discrimination → hazard EWC (amianto `17 06 05*`) → tier di rischio (template Fazzo 2020; soglie Indice di Degrado) → priorità ARPA. Misurato dall'ablazione RGB→VNIR→+SWIR su etichette geolocalizzate.
- **Backbone**: DOFA (wavelength-conditioned = ablazione equa) + Swin-T+RSP esteso + CNN-from-scratch; Prithvi solo al gradino +SWIR.
- **Endpoint Lombardia verificati live** (vedi `05`): amianto layer 1 (10.903 positivi) + layer 4 (50.131, codici-stato 1/2/3/4 confermati) + DUSAF (filtra su `DESCR`, non sul codice) + AGISCO (punti, classi "abbandono rifiuti"/"discariche abusive"), tutti **CC-BY 4.0**. **Correzione**: l'**Indice di Degrado NON è nel WFS** → va stimato da imagery (lo stimatore remoto diventa un contributo).

## ❓ Domande da chiarire con Thomas/ARPA (sbloccano il design)

1. ARPA conserva i **deliverable WV-3 multiband originali** della campagna 2021 dietro AerialWaste? (la leva più alta)
2. Se no, può rilasciare **coordinate + date** dei ~250 positivi WV-3 → ri-pull 8-band gratis via ESA TPM?
3. Il prodotto WV-3 fornito include lo **SWIR**? Lo SWIR è in archivio sull'AOID scelta?
4. **AOI** condivisa che massimizzi overlap (WV-3 SWIR) ∩ (Pléiades Neo) ∩ (tetti amianto WFS densi).
5. Prodotti **Surface Reflectance** già disponibili o calibrazione empirical-line da fare noi?
6. **Sottomettere la proposal ESA TPM ORA** (9 sett + 1 anno vs target Ott/Dic 2026)?
7. Output fino al **tier di rischio**, o classificazione materiale + rischio come motivazione?

*Lista completa e dettagliata in `00_LOOP_LOG.md`. Documenti companion preesistenti (ancora validi): `../sota_vhr_13classes.md`, `../sota_highres_material.md`, `../datasets_catalog.md`, `../datasets_study_guide.md`, `../gap_analysis.md`, `../research_compendium.md`.*
