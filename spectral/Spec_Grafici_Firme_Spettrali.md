# Specifiche per grafici firme spettrali — Claude Code Sprint

## Obiettivo
Generare grafici di riflettanza (wavelength vs. reflectance) per tutti i materiali rilevanti al progetto di tesi, usando esclusivamente dati misurati da librerie spettrali pubbliche. Ogni grafico deve essere citabile in tesi con fonte esatta.

---

## 1. Fonte dati principale: USGS splib07a

**Download:** già scaricato da ScienceBase  
**URL:** `https://www.sciencebase.gov/catalog/file/get/586e8c88e4b0f5ce109fccae?f=__disk__a7%2F4f%2F91%2Fa74f913e0b7d1b8123ad059e52506a02b75a2832`  
**File:** `ASCIIdata_splib07a.zip` (21 MB)  
**Citazione:** Kokaly, R.F., et al., 2017, USGS Spectral Library Version 7: U.S. Geological Survey Data Series 1035, 61 p., https://doi.org/10.3133/ds1035

### Formato dati
- **Wavelength file:** `ASCIIdata_splib07a/splib07a_Wavelengths_ASD_0.35-2.5_microns_2151_ch.txt`
  - Riga 1: header testuale (skip)
  - Righe 2–2152: wavelength in **microns** (0.35 → 2.50), un valore per riga
- **Spectrum files (ASDFRa):** stesso layout — riga 1 header, righe 2–2152 reflectance (0–1 scale, fractional)
- **Valori = -1.23e+34** sono **no-data** (flag SPECPR) → trattare come NaN
- **Spectrum files (BECKa):** range diverso (0.2–3.0 µm), ~480 canali — usare il wavelength file corrispondente: `splib07a_Wavelengths_BECK_Beckman_0.2-3.0_microns.txt`

### Parsing pseudocode
```python
import numpy as np

def load_usgs_spectrum(zip_path, spectrum_file, wavelength_file):
    """Load a USGS splib07a spectrum from zip archive."""
    with zipfile.ZipFile(zip_path) as z:
        # Load wavelengths
        wvl_raw = z.read(wavelength_file).decode().strip().split('\n')
        wavelengths = np.array([float(x) for x in wvl_raw[1:]])  # skip header
        
        # Load reflectance
        ref_raw = z.read(spectrum_file).decode().strip().split('\n')
        reflectance = np.array([float(x) for x in ref_raw[1:]])  # skip header
        
        # Handle no-data flag
        reflectance[reflectance < -1e30] = np.nan
        
        # Convert wavelength µm → nm
        wavelengths_nm = wavelengths * 1000
        
    return wavelengths_nm, reflectance
```

---

## 2. File da estrarre — selezione per ogni materiale

Per ogni categoria, selezionare **1–2 campioni rappresentativi** (colore neutro, opaco preferito).

### Plastics
| Label grafico | File | Rationale |
|---|---|---|
| HDPE (white opaque) | `ChapterA.../splib07a_Plastic_HDPE_GDS384_Wht_Opaq_ASDFRa_AREF.txt` | Bianco opaco = firma più pulita senza effetti colore |
| HDPE (black) | `ChapterA.../splib07a_Plastic_HDPE_GDS351_BlkSheet_ASDFRa_AREF.txt` | Confronto con campione scuro |
| LDPE (white translucent) | `ChapterA.../splib07a_Plastic_LDPE_GDS404_WhTrnslu_ASDFRa_AREF.txt` | |
| PET (clear) | `ChapterA.../splib07a_Plastic_PETE_GDS380_Clear_ASDFRa_AREF.txt` | Firma PET standard |
| PET (translucent brown) | `ChapterA.../splib07a_Plastic_PETE_GDS379_TrnslBrn_ASDFRa_AREF.txt` | Bottiglie colorate |
| Polystyrene (blue) | `ChapterA.../splib07a_Polystyrene_GDS345_BluInsul_ASDFRa_AREF.txt` | |
| ABS (black) | `ChapterA.../splib07a_Plastic_ABS_GDS341_BlackPipe_ASDFRa_AREF.txt` | |

### Textiles
| Label | File |
|---|---|
| Polyester (black) | `ChapterA.../splib07a_Polyester_Pile_GDS434_Blk_ASDFRa_AREF.txt` |
| Nylon (olive drab) | `ChapterA.../splib07a_Nylon_Webbing_GDS428_OlvDrab_ASDFRa_AREF.txt` |
| Cotton (white) | `ChapterA.../splib07a_Cotton_Fabric_GDS437_White_ASDFRa_AREF.txt` |

### Construction
| Label | File |
|---|---|
| Concrete (light grey road) | `ChapterA.../splib07a_Concrete_GDS375_Lt_Gry_Road_ASDFRa_AREF.txt` |
| Brick (paving red) | `ChapterA.../splib07a_Brick_GDS349_Paving_Red_ASDFRa_AREF.txt` |
| Asphalt (black road old) | `ChapterA.../splib07a_Asphalt_GDS376_Blck_Road_old_ASDFRa_AREF.txt` |
| Asphalt tar (black roof) | `ChapterA.../splib07a_Asphalt_Tar_GDS346_Blck_Roof_ASDFRa_AREF.txt` |

### Wood
| Label | File |
|---|---|
| Cedar (fresh) | `ChapterA.../splib07a_Cedar_Shake_GDS357_Fresh_ASDFRa_AREF.txt` |
| Cedar (heavily weathered) | `ChapterA.../splib07a_Cedar_Shake_GDS361_HiWeather_ASDFRa_AREF.txt` |
| Pine beam (new) | `ChapterA.../splib07a_Wood_Beam_GDS363_Nw_Pine_2X4_ASDFRa_AREF.txt` |

### Iron oxides / minerals
| Label | File | Wavelength file |
|---|---|---|
| Goethite (pure) | `ChapterM.../splib07a_Goethite_GDS134_ASDFRb_AREF.txt` | ASD (0.35–2.5 µm) |
| Iron oxide (pigment) | `ChapterA.../splib07a_Iron_oxide_#4820_GDS782_ASDFRa_AREF.txt` | ASD |
| Kaolinite (pure) | `ChapterM.../splib07a_Kaolinite_CM3_BECKa_AREF.txt` | **BECK** (0.2–3.0 µm) |

### Organic compounds
| Label | File |
|---|---|
| Cellulose (pure) | `ChapterO.../splib07a_Cellulose_SA-C6288_ASDHRa_AREF.txt` |
| Lignin (alkali) | `ChapterO.../splib07a_Lignin_alkali_SA-370959_ASDHRa_AREF.txt` |

### Vegetation
| Label | File |
|---|---|
| Green vegetation (aspen leaf, top) | `ChapterV.../splib07a_Aspen_Aspen-1_green-top_ASDFRa_AREF.txt` |
| Dry grass (golden) | `ChapterV.../splib07a_Grass_Golden_Dry_GDS480_ASDFRa_AREF.txt` |
| Dry NPV (D. spicata) | `ChapterV.../splib07a_D.spicata_DWV6-0511_dryNPV.a_ASDFRa_AREF.txt` |
| Green grass (cheatgrass, field) | `ChapterV.../splib07a_Cheatgrass_ANPC1_field_calib_ASDFRa_AREF.txt` |

### Water
| Label | File |
|---|---|
| Water (slightly turbid) | `ChapterL.../splib07a_Water+Montmor_SWy-2+0.50g-l_ASDFRa_AREF.txt` |

---

## 3. Fonte dati supplementare: ECOSTRESS (solo per rubber)

**API endpoint:** POST `https://speclib.jpl.nasa.gov/ecospeclibinteractive`  
**Parametro:** `plotfile=<filename>`  
**Risposta:** HTML con URL CSV embedded (`https://speclib.jpl.nasa.gov/graphs/eco_inter_data_*.csv`)  
**Formato CSV:** `X,Y` → wavelength (µm), reflectance (%)  
**Citazione:** ECOSTRESS Spectral Library, JPL/NASA, sample [ID]

### File ECOSTRESS da scaricare
| Label | Filename ECOSTRESS |
|---|---|
| Rubber (roofing) | `manmade.roofingmaterial.rubber.solid.all.0795uuurbr.jhu.becknic.spectrum.txt` |

### Workflow download ECOSTRESS
```python
import requests, re

def download_ecostress_spectrum(plotfile):
    """Download spectrum CSV from ECOSTRESS via interactive viewer."""
    resp = requests.post(
        "https://speclib.jpl.nasa.gov/ecospeclibinteractive",
        data={"plotfile": plotfile},
        headers={"Content-type": "application/x-www-form-urlencoded"}
    )
    # Extract CSV URL from response
    match = re.search(r'https://speclib\.jpl\.nasa\.gov/graphs/eco_inter_data_[^"]+\.csv', resp.text)
    if match:
        csv_url = match.group()
        csv_resp = requests.get(csv_url)
        # Parse: skip header "X,Y", then wavelength(µm), reflectance(%)
        lines = csv_resp.text.strip().split('\n')[1:]  # skip "X,Y" header
        data = [line.strip().split(',') for line in lines]
        wavelengths_um = [float(d[0]) for d in data]
        reflectance_pct = [float(d[1]) for d in data]
        return np.array(wavelengths_um) * 1000, np.array(reflectance_pct) / 100  # nm, fractional
    return None, None
```

---

## 4. PP (polipropilene) — fonte mancante

PP non è presente né in USGS né in ECOSTRESS. Opzioni:

1. **Moshtaghi et al. 2021** (Sci. Rep. 11:5436) — hanno misurato PP con ASD FieldSpec (350–2500 nm). Verificare se i dati raw sono nei supplementary materials del paper.
2. **Garaba & Dierssen 2020** (ESSD 12:77–86) — dataset pubblico di plastiche marine vergini e raccolte, include PP pellets. DOI: 10.5194/essd-12-77-2020. Dati probabilmente su Zenodo/PANGAEA.
3. **Fallback:** usare solo HDPE e PET per il confronto PE-vs-PET. PP è comunque spettralmente molto simile a PE (stessi C-H features, shift minore) e la discriminazione PE/PP richiede risoluzione iperspettrale. Per la tesi multispettrale, il confronto PE-vs-PET è più rilevante.

**Raccomandazione:** procedere senza PP per ora. Il confronto HDPE vs PET è il discriminante chiave (1730 nm vs 1660 nm) e quello che WorldView-3 può risolvere. PP vs PE è irrisolvibile con multispettrale.

---

## 5. Specifiche grafici matplotlib

### Stile generale
- **Figure size:** 12×5 inches (landscape, slide-friendly)
- **DPI:** 300 (per export PNG ad alta risoluzione)
- **Font:** sans-serif (DejaVu Sans o Helvetica)
- **Axis labels:** "Wavelength (nm)" vs "Reflectance" (0–1 scale)
- **X range:** 350–2500 nm (full VNIR-SWIR)
- **Grid:** light grey, dashed
- **Legend:** outside plot area (right) or inside top-right, fontsize 9
- **No background color** (transparent/white)

### Annotazioni obbligatorie su ogni grafico
1. **Bande di assorbimento diagnostiche:** frecce verticali tratteggiate con label (es. "C-H 1st overtone, 1730 nm")
2. **Barre colorate orizzontali** in alto che indicano le regioni spettrali dei sensori:
   - Sentinel-2 bands (B1–B12): barre sottili con label
   - SuperDove (8 bands): barre separate
   - WorldView-3 SWIR (8 bands): barre separate
   - Evidenziare la zona "SWIR gap" dove SuperDove/Pléiades Neo non hanno copertura (>885 nm)
3. **Citazione fonte:** testo piccolo in basso a destra: "Data: USGS splib07a, [Sample ID] (Kokaly et al., 2017)"

### Grafici da produrre (9 pannelli)

**Grafico 1 — Plastics comparison**
- Curva HDPE (white opaque), PET (clear), LDPE (white translucent) sullo stesso plot
- Annotare: 1660 nm (PET aromatic C-H), 1730 nm (PE aliphatic C-H), 2310 nm (C-H combination)
- Titolo: "Spectral Reflectance of Common Packaging Plastics"

**Grafico 2 — PET vs PE discrimination zoom**
- Stesso dato del Grafico 1, ma X range 1500–1900 nm (zoom sulla regione critica)
- Evidenziare il crossover 1660/1730 nm
- Annotare le bande WorldView-3 SWIR-3 (1660) e SWIR-4 (1730)

**Grafico 3 — Construction materials**
- Concrete (road), brick (red), asphalt (black road), asphalt tar
- Annotare: 870 nm (Fe³⁺ in brick), 1940 nm (H₂O in concrete), 2340 nm (CO₃²⁻ in concrete), 1730 nm (hydrocarbon in asphalt)
- Titolo: "Spectral Reflectance of Construction Materials"

**Grafico 4 — Wood (fresh vs weathered)**
- Cedar fresh, cedar heavily weathered, pine beam
- Annotare: 1450 nm (H₂O), 1940 nm (H₂O), 2100 nm (cellulose), 2340 nm (lignin/cellulose)
- Titolo: "Spectral Reflectance of Wood (Fresh vs Weathered)"

**Grafico 5 — Textiles**
- Polyester (black), nylon (olive drab), cotton (white)
- Annotare: 1500 nm (N-H, nylon), 1660 nm (aromatic C-H, polyester), 2050 nm (amide, nylon), 2100 nm (cellulose, cotton)
- Titolo: "Spectral Reflectance of Textile Fibers"

**Grafico 6 — Natural backgrounds**
- Green vegetation (aspen), dry grass (golden), bare soil proxy (use iron oxide or find soil), water
- Annotare: 670 nm (chlorophyll red absorption), 870 nm (NIR plateau), 1450/1940 nm (H₂O), red edge
- Titolo: "Spectral Reflectance of Natural Background Materials"

**Grafico 7 — Confusion pair: plastic vs dry vegetation**
- HDPE (white) vs dry grass (golden) vs cellulose (pure)
- Annotare: 1730 nm (plastic-only), 2100 nm (cellulose-only)
- Titolo: "Plastic vs Dry Vegetation: SWIR Discrimination"

**Grafico 8 — Confusion pair: rust vs iron-rich soil**
- Iron oxide (pigment) vs goethite (mineral) vs brick (red)
- Annotare: 480, 535, 670, 870 nm (shared Fe³⁺ features), 2200 nm (clay Al-OH — absent in rust)
- Titolo: "Iron Oxide Features: Rust vs Soil Minerals"

**Grafico 9 — Pure biochemicals**
- Cellulose, lignin sovrapposti
- Annotare: 1200, 1450, 1730, 1780, 2100, 2270, 2340 nm
- Titolo: "Spectral Signatures of Plant Biochemical Components"

### Output
- PNG files: `spectral_plot_01_plastics.png` ... `spectral_plot_09_biochemicals.png`
- Un PDF unico con tutti i 9 pannelli: `spectral_signature_library.pdf`
- CSV estratti per ogni materiale (per riuso): `spectra_data/[material]_[sampleID].csv` con colonne `wavelength_nm, reflectance`

---

## 6. Nota sulla copertura PP

Se durante il lavoro in Claude Code si trova il dataset Garaba & Dierssen 2020 (ESSD), aggiungere PP al Grafico 1. Altrimenti, annotare nel grafico: "PP not shown — spectrally similar to PE, requires hyperspectral resolution for discrimination". Questo è coerente con l'argomento della tesi (multispettrale non risolve PE vs PP).
