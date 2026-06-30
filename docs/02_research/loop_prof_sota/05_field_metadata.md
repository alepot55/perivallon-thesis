# Lombardy Layer Field-Schema Report — Verified Field Metadata

*Autonomous research loop, iteration 3 (2026-06-27). All findings verified against the LIVE ArcGIS REST endpoints (`?f=json`, distinct-value and count queries) + Geoportale/INSPIRE metadata. **HIGH** = parsed from raw service JSON or live query · **RESOLVED** = previously-UNCERTAIN assumption now settled · **UNCERTAIN** = still not exposed by these services. This is the implementation reference for the asbestos pilot (`04_experimental_design.md` Part II).*

---

## 1. Asbestos-cement roofs — `coperture_amianto`

**Service (live):** `https://www.cartografia.servizirl.it/expo/rest/services/gpt/coperture_amianto/MapServer`
ArcGIS Server 10.81 · units esriMeters · maxRecordCount 1000 · SR `{wkid:32632}`.

- **RESOLVED — host path.** Real path is `/expo/rest/services/gpt/...`; the guessed `/arcgis/rest/...` 404s. (HIGH)
- **RESOLVED — layer numbering.** Group-layer tree, NOT flat 0/1. Ground-truth feature layers = **layer 1** and **layer 4**. (HIGH)

| ID | Name | Type | Geom | SR |
|----|------|------|------|----|
| 0 | Coperture rilevate nel 2020 | group | — | — |
| **1** | **Mappatura 2020** | feature | polygon | 32632 |
| 2 | Aree mappature 2020 | feature | polygon | 32632 |
| 3 | Coperture già esistenti 2007-2012-2015-2018 | group | — | — |
| **4** | **Mappature precedenti** | feature | polygon | 32632 |
| 5 | Aree mappature | feature | polygon | 32632 |
| 6–9 | Limiti amministrativi (Comuni/Province/ATS) | feature | polygon | 32632 |

### Layer 1 — Mappatura 2020 (positive ground truth)
Count: **10,903** (matches `Mappatura_2020.gpkg`). Fields: `OBJECTID`, `Shape`, `COD_ISTATN` (Istat code, str16), `Shape_Length`, `Shape_Area`.
- **RESOLVED — NO status field, NO Indice di Degrado.** Simple renderer; every polygon = an AC covering present at the 2020 survey, carrying only the ISTAT municipality code. The `1=present/2=removed/…` code does **NOT** exist here. (HIGH)

### Layer 4 — Mappature precedenti (temporal history)
Count: **50,131** (matches `Mappature_precedenti.gpkg`). Fields: `OBJECTID`, `Shape`, **`F1999` `F2012` `F2013` `F2015` `F2018`** (per-year integer status), `FONTE` (str10), `COD_ISTATN`, `decodifica` (str254 free text), `Shape_Length/Area`.
- **RESOLVED — status-code semantics** (no coded-value domain; status = per-year integer columns; verified via distinct values + `decodifica` + `F2018` renderer):

| Code | Meaning |
|------|---------|
| **1** | covering present / "non variato" at that year |
| **2** | variato / rimossa in that epoch |
| **3** | variato con installazione fotovoltaico (removed + PV) |
| **4** | variato con demolizione edificio (demolished) |
| **0** | no change in *that* epoch (change in an earlier F-year column) |

  → The earlier briefing mapping (1=present/2=removed/3=removed+PV/4=demolished) is **CONFIRMED**, on **layer 4 only**. `FONTE` ∈ {Milanese, Monzese, Pavese, PRAL}.

### ⚠️ Indice di Degrado — ABSENT from the service (key correction)
**RESOLVED (negative): the d.d.g. 13237/2008 degradation index (thresholds 25/44/45) is NOT present on any asbestos layer.** It is a derived/field-survey attribute, not exposed in the public WFS/REST. **Implication for the risk chain:** the condition/weathering term must be **estimated remotely from the imagery** (SWIR Mg-OH continuum depth ~2300 nm + VNIR weathering proxy / Cilia ISD) or sourced separately — i.e. the *remote degradation estimator becomes a thesis contribution*, not a lookup. (HIGH that it's absent; the means of obtaining a ground-truth ID for validation remains open.)

### Exact URLs
`…/coperture_amianto/MapServer?f=json` · `…/MapServer/1?f=json` · `…/MapServer/4?f=json` · `…/MapServer/1/query?where=1=1&returnCountOnly=true&f=json` → 10903 · `…/MapServer/4/query?where=1=1&returnCountOnly=true&f=json` → 50131 · WFS `…/coperture_amianto/MapServer/WFSServer?` · INSPIRE `r_lombar:6857dc92-76cb-4c56-8837-123e9370dcda`.

**Pilot takeaway:** layer 1 (10,903) = presence-only positive GT; layer 4 (50,131, codes 1/2/3/4) = filter roofs removed/demolished/PV-converted before the imagery date (avoids label-date mismatch). Neither carries the Indice di Degrado.

---

## 2. DUSAF 7.0 — Land use / land cover 2021

**Service:** `https://www.cartografia.servizirl.it/arcgis1/rest/services/territorio/dusaf7/MapServer` · LULC polygons = **layer 1** ("DUSAF 2021 (7.0)"; layer 0 = hedgerow polylines). Geometry polygon · EPSG:32632.

- **RESOLVED — ⚠️ class code is NOT queryable.** The numeric code `COD_TOT` exists only in the renderer (`uniqueValueInfos`), **not** in the queryable `fields[]` (only `OBJECTID`, `Shape`, `DESCR`). **Filter on the `DESCR` string, not the code.** (HIGH)
- **RESOLVED — 4 waste-relevant classes present:** 131 *Cave* · 132 *Discariche* · 133 *Cantieri* · 134 *Aree degradate non utilizzate e non vegetate*.
- **License: CC-BY 4.0** (Regione Lombardia; metadata `r_lombar:7cd05e9f-...`; scale 1:10,000, AGEA 2021). Service `copyrightText` is empty → cite the metadata sheet. (HIGH)
- Query: `where=DESCR IN ('Cave','Discariche','Cantieri','Aree degradate non utilizzate e non vegetate')`.

---

## 3. Contaminated / remediated sites — PSC-AGISCO

**Service:** `https://www.cartografia.servizirl.it/expo/rest/services/gpt/siti_bonificati_contaminati/MapServer/0` ("Siti bonificati e contaminati"; published layer of the ARPA PSC-AGISCO registry `agiscopsc.arpalombardia.it`).
Geometry **point** · EPSG:32632 · **5,813 features** · snapshot 31/12/2024.

Fields: `OBJECTID`, `SHAPE`, `COD_SITO`, `ANA_DENOM_` (name), `ANA_COMUNE`, `ANA_PROV_S`, **`ANA_CLAS_2`** (status), **`TIP_TIPOLO`** (activity type).
- **`ANA_CLAS_2`** ∈ {`bonificato`, `contaminato`}. (HIGH)
- **`TIP_TIPOLO`** = 16 free strings; waste-relevant: **"smaltimenti non autorizzati - abbandono rifiuti"** and **"discariche abusive o incontrollate"** (also: impianti stoccaggio rifiuti, discariche autorizzate, operazioni di recupero/gestione rifiuti, aree industriali in attività/dismesse, rilasci accidentali/dolosi, …). (HIGH)
- **License: CC-BY 4.0** (INSPIRE noLimitations; `r_lombar:c5ac536b-...`); `copyrightText` empty → cite metadata. (HIGH)

---

## Pipeline flags
1. **DUSAF: filter on `DESCR`, not `COD_TOT`** (code is renderer-only). Keep a local label→code lookup if codes are needed.
2. **DUSAF & AGISCO `copyrightText` are empty** — the CC-BY 4.0 attribution is in the Geoportale/INSPIRE metadata; cite that in the thesis, not the REST service.
3. **Asbestos: use layer 1 for positives, layer 4 for temporal status filtering**; compute degradation remotely (no ID in service).

## Status summary
- **RESOLVED:** asbestos host path; layer numbering (1 & 4); EPSG:32632 everywhere; layer-1 has no status/ID; layer-4 status codes 0/1/2/3/4 (briefing mapping confirmed); DUSAF `COD_TOT`-not-queryable; DUSAF 4 target classes; DUSAF & AGISCO licenses CC-BY 4.0; AGISCO geometry/fields/domains/count.
- **STILL OPEN:** Indice di Degrado absent from the service → estimate remotely or source separately (open for risk-chain validation).
