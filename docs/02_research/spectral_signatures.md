# Spectral signatures of waste materials for satellite-based illegal dump detection

**The ability to identify illegal waste from orbit depends fundamentally on shortwave infrared (SWIR) spectroscopy.** Every major waste material — plastics, construction debris, rubber, textiles — possesses diagnostic absorption features between 1200 and 2500 nm caused by molecular vibrations of C-H, O-H, C-O, and N-H bonds. Sensors lacking SWIR bands (Planet SuperDove, Pléiades Neo) can detect anomalous surface changes but cannot classify waste material type. Only WorldView-3, with eight narrow SWIR bands from 1195–2365 nm, provides the spectral resolution needed for material-level discrimination. Sentinel-2's two broad SWIR bands (B11 at 1610 nm, B12 at 2190 nm) offer partial capability. This reference document catalogues the spectral properties of all materials relevant to illegal waste detection, specifies which sensor bands capture diagnostic features, and identifies the spectral regions that resolve commonly confused material pairs.

---

## 1. Plastics: PE, PP, and PET have distinct SWIR fingerprints

All three common packaging polymers share C-H bond absorptions but differ in exact band positions due to their molecular structures. The SWIR region between 1600 and 1800 nm is the primary discriminating zone.

### Polyethylene (PE)

PE is a purely aliphatic hydrocarbon (–CH₂–CH₂–)ₙ with only C-H and C-C bonds. In the visible range (400–700 nm), reflectance is entirely colour-dependent and non-diagnostic. White/opaque PE reaches **0.5–0.8 reflectance** in VIS, rising to a broad NIR plateau at 850–1070 nm. The SWIR contains all diagnostic features:

| Wavelength (nm) | Assignment | Mechanism |
|---|---|---|
| ~930 | 3rd overtone C-H stretch (–CH₂–) | Anharmonic overtone of sp³ C-H |
| ~1210 | 2nd overtone C-H stretch | v=0→v=3 transition |
| ~1400 | C-H combination band (stretch + deformation) | Overlaps O-H 1st overtone |
| **~1730** | **1st overtone C-H stretch (–CH₂–)** | **v=0→v=2 of aliphatic C-H — strongest diagnostic feature** |
| ~1760 | 1st overtone asymmetric –CH₂– stretch | Shoulder on the 1730 nm feature |
| ~2310–2350 | C-H stretch + C-H deformation combination | Strong doublet in SWIR-2 |

The fundamental C-H stretch occurs at ~3.4 µm (mid-IR); SWIR features are overtones and combination bands. NASA's EMIT imaging spectrometer confirmed HDPE detection from orbit at **1200, 1710, and 2300 nm** (Estrela et al., 2025).

### Polypropylene (PP)

PP is (–CH₂–CH(CH₃)–)ₙ, sharing PE's C-H features but with additional –CH₃ methyl group contributions. Its absorption bands appear at **1192, 1394, and 1730 nm** (Moshtaghi et al., 2021). The key difference from PE lies in the **1700–1800 nm region**, where the –CH₃ asymmetric stretch fundamental (~2960 cm⁻¹ vs. –CH₂– at ~2920 cm⁻¹) produces a slightly different overtone profile. This ~40 cm⁻¹ shift propagates to subtle position and shape differences in the 1st overtone band. **Discriminating PE from PP requires hyperspectral resolution** in the 1600–1900 nm range; multispectral sensors cannot separate them.

### Polyethylene terephthalate (PET)

PET contains aromatic benzene rings, ester linkages (C=O, C-O-C), and aliphatic –CH₂– segments. This chemistry produces a **dramatically different** SWIR signature:

| Wavelength (nm) | Assignment | Mechanism |
|---|---|---|
| ~1130 | 2nd overtone aromatic C-H stretch (sp²) | Higher-frequency sp² C-H on benzene ring |
| **~1660** | **1st overtone aromatic C-H stretch** | **Key diagnostic — absent in PE/PP** |
| ~1908 | C=O stretch combination band | Unique to PET among common packaging plastics |
| ~2130–2150 | Aromatic ring C-H and C-C combination | Benzene ring vibrations |

The **~70 nm blue-shift** from PE's 1730 nm to PET's 1660 nm directly reflects sp³ vs. sp² carbon hybridisation — aromatic C-H fundamentals occur at ~3060 cm⁻¹ vs. aliphatic at ~2920 cm⁻¹. This is the single most important spectral discriminator among common plastics. The **R(1660)/R(1730) ratio** cleanly separates PET from PE/PP: low values indicate PE/PP (absorption at 1730), high values indicate PET (absorption at 1660).

### Plastic detection from sensors without SWIR

**VNIR-only sensors cannot identify polymer type.** No polymer-diagnostic absorption features exist below 1000 nm. VIS reflectance is entirely colour-dependent, not material-dependent. Schmidt et al. (2023) evaluated 22 satellite sensors and found that VNIR-only platforms (PlanetScope, Pléiades) produced the **lowest classification accuracy** for plastic type identification. Sequential forward selection confirmed features at **1215 nm and 1732 nm** (SWIR) as the most important spectral variables. On water, floating plastics can be detected via NIR brightness contrast (Biermann et al., 2020), but this detects "floating debris" generically, not plastic specifically.

---

## 2. Metals show free-electron reflectance until oxidation introduces iron features

### Bare ferrous and non-ferrous metals

Fresh metallic surfaces exhibit high, spectrally flat reflectance governed by the Drude free-electron model. Polished steel reflects **40–70%** across VIS-SWIR with no diagnostic absorption bands. Aluminium reaches **88–92%** in the visible. Copper shows an interband transition edge at ~560 nm (d-band to Fermi level), absorbing blue/green and producing its characteristic reddish colour. In satellite imagery, bare metals create specular glint or sensor saturation. The **absence** of any narrow absorption features is itself diagnostic — distinguishing metal from minerals and vegetation.

### Oxidised/rusted metal (iron oxides)

Rust transforms the featureless metal spectrum into one dominated by **Fe³⁺ crystal field transitions**:

| Wavelength (nm) | Transition | Mineral |
|---|---|---|
| ~480 | Electron pair transition 2(⁶A₁)→2(⁴T₁) | Goethite (FeOOH) |
| ~535 | Electron pair transition | Hematite (Fe₂O₃) |
| ~670 | ⁶A₁→⁴T₂ crystal field | Both (weak) |
| **~870** | **⁶A₁→⁴T₁ crystal field** | **Hematite (broad, diagnostic)** |
| ~920–950 | ⁶A₁→⁴T₁ crystal field | Goethite (shifted longer) |

These are spin-forbidden d-d transitions intensified by magnetic superexchange coupling between adjacent Fe³⁺ ions (Sherman & Waite, 1985). Goethite additionally shows O-H features at 1400 and 1900 nm from its hydroxyl structure (FeOOH), whereas anhydrous hematite (Fe₂O₃) lacks these. Importantly, **rusted metal shares identical VIS-NIR iron oxide features with lateritic/red soils** — discrimination requires SWIR analysis of clay mineral presence (see Section 6).

---

## 3. Construction debris has carbonate, clay, and hydrocarbon signatures

### Concrete

Concrete's spectrum rises from **~10–15%** at 400 nm to **~40–55%** in the NIR, with strong SWIR absorptions from its calcium carbonate and hydrated cement chemistry. The **CO₃²⁻ absorption at ~2310–2350 nm** (C-O combination/overtone vibration of calcite) is the primary diagnostic feature, complemented by molecular water absorption at **~1940 nm** (H-O-H bend + O-H stretch combination) and structural hydroxyl at **~1410 nm** from hydrated cement phases (portlandite, ettringite). Kotthaus et al. (2014) documented that all VIS-SWIR spectra of cement/concrete exhibit strong absorption around 1940–1970 nm. Fresh concrete has higher albedo (0.30–0.45); weathered concrete darkens and may develop iron staining.

### Asphalt

Fresh asphalt is extremely dark (**~3–8% reflectance**), dominated by bitumen's broadband absorption. The diagnostic feature is a **C-H stretch overtone at ~1730 nm** — the same Hydrocarbon Index (HI) band used by Kühn et al. (2004). Additional hydrocarbon features appear at **2310–2350 nm** and **2140–2180 nm** (aromatics). As asphalt ages, bitumen degrades and exposes aggregate minerals: overall reflectance **increases**, hydrocarbon features **weaken**, and iron oxide/silicate features from aggregate **emerge**. This spectral ageing trajectory makes old asphalt increasingly difficult to distinguish from bare soil.

### Brick and ceramic

Red clay brick shows a spectral signature that is a **superposition of Fe³⁺ crystal field transitions and residual clay mineral vibrations**. Strong absorption below 520 nm and features at **670 nm and 870 nm** mirror hematite exactly — iron oxides form during firing at 900–1100°C. Additionally, brick retains **Al-OH absorption at ~2200 nm** from incompletely dehydroxylated clay minerals, plus OH/water features at 1410 and 1900 nm. Ceramic/tile spectra depend heavily on composition and glaze. Kotthaus et al. (2014) noted that iron oxide features "cannot be used to reliably distinguish between ceramic and cement materials" due to the variable iron content in both.

---

## 4. Rubber, wood, textiles, and glass each occupy distinct spectral niches

### Rubber and tires

Vulcanised rubber is spectrally the most challenging waste material. Carbon black filler (**25–30% of tire composition**) absorbs radiation broadly via electronic transitions in conjugated carbon, producing extremely low, nearly featureless reflectance of **~2–5%** across the entire 400–2500 nm range. Weak hydrocarbon features at **~1730 nm** (C-H 1st overtone) and **~2300 nm** (C-H combination) are typically overwhelmed. Rubber/tire piles are commonly confused with **water, shadow, and fresh asphalt** in multispectral imagery. Discrimination from asphalt requires either spatial/texture analysis (circular tire shapes at sub-metre resolution) or the detection of silicate mineral features in aged asphalt that rubber lacks.

### Wood (fresh vs. weathered)

Wood's spectral signature derives from its **cellulose (~40–50%), hemicellulose (~20–30%), and lignin (~20–30%)** composition. Fresh wood shows moderate VIS reflectance (10–30%) with a yellow-brown hue from lignin chromophores, a modest NIR rise to 25–45% (cell wall scattering, but no red edge), and deep SWIR absorptions:

- **~1450 nm and ~1940 nm**: liquid water O-H bands (strong in fresh wood with 30–100% moisture)
- **~2100 nm**: cellulose O-H + C-O combination — key NPV indicator
- **~2270–2340 nm**: cellulose/hemicellulose C-H combination bands
- **~1200 nm**: cellulose C-H 2nd overtone

Weathered wood loses moisture (weakening 1450/1940 nm bands), grays in the VIS from lignin photodegradation, and retains cellulose features at 2100 and 2340 nm. **Critically, wood lacks the 1730 nm C-H absorption** that characterises plastics — this wavelength cleanly separates plastic from natural lignocellulosic debris (Garaba et al., 2021).

### Textiles

Textile spectral signatures depend on fibre chemistry. **Polyester** (PET-based) shares PET plastic's absorption bands at 1660 nm (aromatic C-H), 2130 nm (ester C=O), and 1730 nm (aliphatic C-H) — it is chemically identical to PET bottles and spectrally indistinguishable at the molecular level. **Nylon** (polyamide) has distinctive **N-H amide features** at ~1500 nm (1st overtone), ~2050 nm (amide combination), and ~2170 nm that are absent in polyester. **Cotton** (>90% cellulose) mirrors wood's cellulose features at 1200, 1450, 2100, and 2280 nm. **Wool** (α-keratin protein) shows amide N-H bands at ~1500, 2050, and 2170 nm similar to nylon, plus disulphide features unique to keratin. The **1500–2200 nm region** is most diagnostic for fibre-type discrimination; VIS signatures are dominated by dyes and are non-diagnostic.

### Glass

Glass is largely **transparent** in VIS-SWIR, producing only Fresnel surface reflections of **~4–8%** per surface (refractive index ~1.5). Soda-lime glass shows very weak Si-O-H features at **~1390 nm** and **~2200 nm**, but these are typically below detection thresholds. In the SWIR, glass appears **extremely dark** because photons transmit through rather than reflect back. Coloured glass adds metal oxide d-d electronic transitions: Fe²⁺/Cr³⁺ for green glass (absorption at ~450 and ~620 nm), Fe³⁺ for brown/amber glass (broad VIS absorption). Glass can be confused with **water** in SWIR imagery (both appear near-zero) and with specular surfaces when oriented to create glint.

---

## 5. Natural background materials define the baseline against which waste must be detected

### Green vegetation

The canonical vegetation signature features chlorophyll absorption troughs at **~450 nm** (blue) and **~670 nm** (red), a green reflectance peak at **~550 nm**, the steep **red edge** from 680–750 nm (reflectance jumps from ~5% to ~50%), and a broad NIR plateau at **750–1300 nm** driven by mesophyll cell wall scattering. Liquid water absorption at **970, 1200, 1450, and 1940 nm** modulates the SWIR. **NDVI = (NIR − Red)/(NIR + Red)** reaches **0.6–0.9** for healthy canopies. No waste material produces this NIR/Red contrast, making vegetation masking straightforward with any sensor.

### Dry/senescent vegetation (NPV)

As vegetation dries, chlorophyll degrades (eliminating the 670 nm absorption and red edge), water features at 1450 and 1940 nm **weaken dramatically**, and **cellulose/lignin features emerge**: absorption at **~2100 nm** (cellulose C-O + O-H combination), **~2300–2340 nm** (lignin C-H + C-C), and **~1730–1754 nm** (lignin C-H 1st overtone). NDVI drops to **0.1–0.3**. The Cellulose Absorption Index (CAI = 0.5(R₂₀₀₀ + R₂₂₀₀) − R₂₁₀₀) detects dry plant matter specifically. **Dry vegetation shares cellulose features with wood waste, cardboard, and paper** — one of the most problematic confusion pairs for satellite classification.

### Bare soil types

Soil spectra are governed by three primary chromophores — **iron oxides** (VIS absorption), **organic matter** (broad VIS-NIR darkening), and **clay minerals** (SWIR absorption) — plus moisture content:

- **Clay-rich soil**: Kaolinite shows a diagnostic doublet at ~2170/2200 nm (Al-OH); montmorillonite adds strong 1900 nm water absorption. The 2200 nm feature position differs from concrete's carbonate feature at 2340 nm.
- **Sandy soil**: Highest reflectance among soils (up to **40–60%** for dry quartz sand), nearly featureless spectrum. Easily confused with concrete and light construction debris.
- **Organic-rich soil**: Lowest reflectance (**~5–15%**), broad VIS absorption from humic compounds, weak 1730 nm organic C-H feature. Can be confused with dark waste (tires, asphalt).
- **Iron-rich/lateritic soil**: Strong Fe³⁺ features at **480, 535, 670, and 870 nm** identical to rust — the most problematic natural-vs-waste confusion pair.

### Water

Clear water reflects **3–7%** in the blue, dropping to **near-zero beyond ~750 nm** due to liquid water absorption. This extreme NIR/SWIR darkness is the defining characteristic. NDWI = (Green − NIR)/(Green + NIR) yields positive values for water, negative for land. Turbid water shows elevated VIS reflectance (especially 500–700 nm) from suspended sediment but maintains near-zero SWIR reflectance even at high turbidity — the **SWIR provides the most reliable water discrimination** in all conditions.

---

## 6. Satellite sensor bands determine what can and cannot be classified

### Band specifications of the four target sensors

**Sentinel-2 MSI (13 bands)**

| Band | Centre (nm) | Width (nm) | Resolution | Region |
|------|------------|------------|------------|--------|
| B1 | 443 | 21 | 60 m | Coastal aerosol |
| B2 | 490 | 66 | 10 m | Blue |
| B3 | 560 | 36 | 10 m | Green |
| B4 | 665 | 31 | 10 m | Red |
| B5 | 705 | 15 | 20 m | Red edge 1 |
| B6 | 740 | 15 | 20 m | Red edge 2 |
| B7 | 783 | 20 | 20 m | Red edge 3 |
| B8 | 842 | 106 | 10 m | NIR broad |
| B8A | 865 | 21 | 20 m | NIR narrow |
| B9 | 945 | 20 | 60 m | Water vapour |
| B11 | **1610** | 91 | 20 m | **SWIR-1** |
| B12 | **2190** | 175 | 20 m | **SWIR-2** |

B11 captures the region near the critical **1730 nm C-H absorption** (though centred 120 nm away) and B12 overlaps with carbonate/clay features near **2200 nm**. The broad bandwidths dilute narrow absorption features significantly.

**WorldView-3 (8 VNIR + 8 SWIR bands)**

| Band | Centre (nm) | Width (nm) | Resolution | Key material feature covered |
|------|------------|------------|------------|------|
| SWIR-1 | **1210** | 30 | 3.7 m | PE/PP 2nd overtone C-H |
| SWIR-2 | **1570** | 40 | 3.7 m | Transition region |
| SWIR-3 | **1660** | 40 | 3.7 m | **PET aromatic C-H 1st overtone** |
| SWIR-4 | **1730** | 40 | 3.7 m | **PE/PP aliphatic C-H 1st overtone** |
| SWIR-5 | **2165** | 40 | 3.7 m | PET C=O; cellulose |
| SWIR-6 | **2205** | 40 | 3.7 m | Al-OH clay minerals |
| SWIR-7 | **2260** | 50 | 3.7 m | Carbonate/clay transition |
| SWIR-8 | **2330** | 70 | 3.7 m | Carbonate C-O; C-H combination |

WorldView-3 is the **only sensor of the four that directly resolves the PET-vs-PE/PP split**: SWIR-3 at 1660 nm captures PET's aromatic C-H feature while SWIR-4 at 1730 nm captures PE/PP's aliphatic C-H feature. The **SWIR-3/SWIR-4 ratio** is the most powerful plastic discrimination metric available from any current multispectral satellite.

**Planet SuperDove (8 bands, 431–885 nm)** and **Pléiades Neo (6 bands, 400–880 nm)** both lack any SWIR capability. Their spectral range ends at ~885 nm, covering only VNIR. They offer high spatial resolution (3 m and 1.2 m respectively) but **fundamentally cannot classify waste material type based on spectral chemistry**.

### Material detectability matrix

| Material | SWIR required? | Sentinel-2 | SuperDove | WorldView-3 | Pléiades Neo |
|---|---|---|---|---|---|
| PE vs PP vs PET discrimination | **Essential** | Very limited | **No** | **Yes** | **No** |
| Plastic vs non-plastic (on land) | Strongly preferred | Partial | Poor | **Yes** | Poor |
| Concrete vs bare soil | SWIR preferred | Partial (B12) | **No** | **Yes** | **No** |
| Asphalt (hydrocarbon ID) | SWIR preferred | Partial (B11) | **No** | **Yes** | **No** |
| Rubber/tires vs asphalt | SWIR + spatial | Minimal | **No** | Difficult | **No** |
| Textile fibre type | **Essential** | No | **No** | Partial | **No** |
| Green vegetation | Not needed | Yes | Yes | Yes | Yes |
| Water bodies | Not needed | Yes | Yes | Yes | Yes |
| Bare bright metal | Not needed | Yes | Yes | Yes | Yes |
| Rusted metal vs red soil | SWIR helpful | Partial | Limited | **Yes** | Limited |

**Materials that CANNOT be distinguished without SWIR bands:** PE, PP, PET plastics (from each other or from non-plastic bright materials); concrete from sandy soil; asphalt from dark organic soil; synthetic textiles from other polymers; fresh from aged construction materials. This is the core thesis argument for multispectral (with SWIR) over RGB/VNIR-only approaches.

---

## 7. Commonly confused material pairs and their spectral discriminators

The following pairs represent the primary classification challenges in satellite-based waste detection. For each, the optimal discriminating spectral region and sensor requirements are specified.

### Plastics vs. wood → SWIR 1660–1730 nm

Plastics show the **1730 nm C-H absorption** (PE/PP) or **1660 nm aromatic C-H** (PET); wood shows **no absorption at 1730 nm** but has cellulose features at 2100 and 2340 nm. The presence/absence of the 1730 nm feature is the cleanest discriminator. **Requires at minimum Sentinel-2 B11 (1610 nm)** to partially capture this region; WorldView-3 SWIR-4 (1730 nm) provides direct measurement.

### Plastics vs. dry vegetation → SWIR 1700–2100 nm

Both show features in the 2300 nm region (C-H combination bands in plastics; cellulose/lignin in NPV). The key discriminator is the **2100 nm cellulose absorption** present in dry vegetation but absent in plastics, plus the **1730 nm hydrocarbon feature** present in plastics but weak/absent in NPV cellulose. WorldView-3 SWIR-4 and SWIR-5 resolve this. The Cellulose Absorption Index (CAI) applied to the 2000–2200 nm region separates NPV from hydrocarbon materials.

### Concrete vs. bare soil → SWIR 2200–2350 nm

Concrete shows strong **CO₃²⁻ absorption at ~2340 nm** from calcite cement; clay-rich soils show **Al-OH absorption at ~2200 nm** from kaolinite/montmorillonite. These features are **140 nm apart** and separable with WorldView-3 SWIR-6 (2205 nm) vs. SWIR-8 (2330 nm). Sentinel-2 B12 (2190 nm, width 175 nm) partially captures both but cannot resolve them independently. Sandy soil, which lacks clay features, is the most problematic confusion case — it requires spatial/contextual analysis or thermal IR data.

### Rusted metal vs. iron-rich soil → SWIR 2200 nm (clay indicator)

Both share identical Fe³⁺ crystal field features at **480, 535, 670, and 870 nm** in the VNIR. The discriminator lies in the SWIR: lateritic soils contain **clay minerals** producing Al-OH absorption at **~2200 nm**, whereas pure rust on metal surfaces **lacks** these clay signatures. Additionally, soil shows organic matter effects (broad VIS absorption) absent in metal. WorldView-3 SWIR-6 (2205 nm) can detect the clay feature; VNIR-only sensors **cannot resolve this pair**.

### Asphalt vs. rubber/tires → extremely difficult

Both are very dark (**<8% reflectance**) with weak hydrocarbon C-H features near 1730 and 2300 nm. Aged asphalt develops mineral features (~2200 nm silicates from exposed aggregate) absent in rubber, but fresh asphalt and rubber are spectrally nearly identical. **This pair is the most difficult to resolve spectrally** and typically requires sub-metre spatial resolution to exploit the distinctive circular texture of tire piles. Even hyperspectral data provides limited discrimination.

### Dark organic soil vs. asphalt → SWIR 1730 nm + brightness

Both are dark in VIS-NIR. Asphalt shows hydrocarbon absorption at **~1730 nm** absent in organic soil (whose 1730 nm feature is very weak). Soil has clay mineral features at ~2200 nm that fresh asphalt lacks. Sentinel-2 B11 provides partial detection; WorldView-3 SWIR-4 is more diagnostic.

### Dry vegetation vs. wood/cardboard waste → near-identical cellulose signatures

Both contain cellulose producing absorption at **~2100 nm and ~2340 nm**. At multispectral resolution, these materials are **spectrally indistinguishable**. Discrimination requires either hyperspectral analysis of subtle band position shifts, temporal monitoring (seasonal senescence patterns vs. persistent waste), or spatial/contextual analysis.

### Glass vs. water → both dark in SWIR

Both show very low SWIR reflectance (glass transmits; water absorbs). Discrimination relies on **VIS brightness differences** (glass may show specular reflections; water has characteristic blue reflectance peak) and spatial context. Neither material poses significant confusion in practice for waste dump detection, as glass fragments are typically sub-pixel.

---

## 8. Spectral indices for waste detection and background masking

### Waste-specific indices

**Floating Debris Index (FDI)** — Biermann et al. (2020): FDI = ρ_NIR − ρ′_NIR, where ρ′_NIR is the linearly interpolated baseline between Red Edge 2 and SWIR-1. Uses Sentinel-2 B6 (740 nm), B8 (842 nm), B11 (1610 nm). Highlights floating material on water surfaces. FDI range for plastics: **0.02–0.06**. Must be combined with NDVI to separate plastic from seaweed/algae (plastics: NDVI 0–0.2; seaweed: NDVI > 0.2).

**Plastic Index (PI)** — Themistocleous et al. (2020): PI = ρ_NIR / ρ_Red. Uses Sentinel-2 B8/B4. Simple ratio exploiting higher NIR/Red reflectance of floating plastics vs. water. Validated with 3×10 m targets in Cyprus.

**Adjusted Plastic Index (API)** — Damayanti et al. (2023): Modified PI integrated with NDVI for river-based illegal dump identification in Indonesia. Applied to Sentinel-2 with Random Forest classifier.

**Hydrocarbon Index (HI)** — Kühn et al. (2004): Band-depth index at ~1730 nm detecting hydrocarbon absorption. Applicable to all plastics, asphalt, and bitumen-bearing materials. **Requires SWIR data** — WorldView-3 SWIR-4 (1730 nm) is ideally positioned.

### Background masking indices

- **NDVI** = (NIR − Red)/(NIR + Red): Masks healthy vegetation (threshold > 0.3–0.4). Usable by all four sensors.
- **NDWI** = (Green − NIR)/(Green + NIR): Masks water bodies (positive values). Usable by all four sensors.
- **MNDWI** = (Green − SWIR)/(Green + SWIR): Improved water masking in urban areas. Requires Sentinel-2 B11 or WV-3 SWIR.
- **BSI** = ((Red + SWIR) − (NIR + Blue))/((Red + SWIR) + (NIR + Blue)): Bare soil detection. Requires SWIR.
- **NDBI** = (SWIR − NIR)/(SWIR + NIR): Built-up area detection. Requires SWIR.

### Dry vegetation and soil indices

- **CAI** = 0.5(R₂₀₀₀ + R₂₂₀₀) − R₂₁₀₀: Cellulose Absorption Index for dry vegetation/residue. Requires SWIR hyperspectral.
- **Iron Oxide Index** = Red/Blue (B4/B2): Detects iron oxides in rust, brick, and lateritic soil. Usable by all sensors.
- **Clay Index** = SWIR1/SWIR2: Detects Al-OH clay minerals. Requires Sentinel-2 B11/B12 or WV-3 SWIR.

### Recommended pre-classification workflow

The standard approach in waste detection studies follows a hierarchical masking sequence: (1) NDVI to mask dense vegetation, (2) NDWI/MNDWI to mask water, (3) cloud/shadow masking, (4) NDBI to identify built-up areas, then (5) spectral classification of remaining pixels using material-specific features and machine learning.

---

## 9. Recent literature on satellite-based waste and material classification (2020–2026)

**Orbital plastic detection** has advanced rapidly. Estrela et al. (2025) achieved the first **global-scale plastic detection from space** using NASA's EMIT imaging spectrometer (380–2500 nm, 60 m resolution), identifying HDPE and PVC across agricultural landscapes through matched filter algorithms targeting the 1200, 1710, and 2300 nm features. This represents proof-of-concept for the SWIR-based approach at orbital scale.

**Sentinel-2 waste studies** include Biermann et al. (2020) demonstrating FDI-based floating plastic detection, Damayanti et al. (2023) applying the Adjusted Plastic Index to river-based illegal dumps in Indonesia, and Magyar et al. (2023) using Random Forest classification with spectral indices for illegal dump hot-spot detection along the Tisza River. Page et al. (2022) combined Sentinel-1 SAR with Sentinel-2 optical data for tyre and plastic waste classification in Scotland.

**VHR and deep learning approaches** include Marrocco et al. (2024) applying ResNet with Feature Pyramid Networks for multi-scale waste detection, Torres & Fraternali (2023) releasing the AerialWaste dataset of **3,478+ annotated waste sites** from WorldView-3 imagery in Lombardy, Italy, and a Nature Communications study (2023) using deep CNNs to detect ~1,000 dumpsites across 28 cities worldwide, reducing investigation time by over **96.8%**.

**Sensor comparison work** by Tasseron et al. (2021) compared Sentinel-2 and WorldView-3 band placements against hyperspectral discriminant analysis weights, finding that WV-3 SWIR-3 (1660 nm) and SWIR-4 (1730 nm) overlap with the **highest-weighted discriminating wavelengths**. Schmidt et al. (2023) confirmed that VNIR-only sensors produced the lowest plastic classification accuracy among 22 evaluated platforms.

**Emerging missions** relevant to waste detection include **EMIT** (operational since 2022, 380–2500 nm hyperspectral), **EnMAP** (2022, 420–2450 nm hyperspectral, 30 m), and **PRISMA** (2019, 400–2500 nm hyperspectral, 30 m). The **PACE** ocean colour mission (2024) adds SWIR capability for marine plastic studies.

---

## 10. The SWIR gap is the decisive constraint for waste material classification

The spectral evidence compiled in this reference leads to one overarching conclusion: **material-level waste classification from satellite imagery is fundamentally a SWIR problem**. Every major diagnostic feature — the 1730 nm hydrocarbon C-H absorption in plastics, the 1660 nm aromatic C-H in PET, the 2340 nm carbonate in concrete, the 2200 nm Al-OH in clay minerals, the 2100 nm cellulose in dry vegetation — falls between 1600 and 2400 nm. VNIR-only sensors can detect waste sites as anomalous surfaces (through brightness, texture, NDVI depression, and spatial pattern analysis) but cannot determine whether a bright patch is plastic, concrete, sandy soil, or cardboard.

A practical multi-sensor strategy emerges from this analysis. **Sentinel-2** provides free, global, 5-day-revisit screening with partial SWIR capability through its two broad SWIR bands (B11, B12), suitable for temporal change detection and coarse material discrimination. **SuperDove or Pléiades Neo** provide high-resolution spatial delineation of waste site boundaries but no material chemistry. **WorldView-3** — the only current multispectral satellite with narrow SWIR bands directly targeting plastic and mineral diagnostic features — enables material classification of identified sites. Emerging hyperspectral missions (EMIT, EnMAP, PRISMA) represent the future of waste characterisation, offering continuous spectral coverage across the full VNIR-SWIR range needed to resolve the most difficult confusion pairs.

The materials that remain spectrally intractable even with full SWIR coverage — rubber vs. fresh asphalt, dry vegetation vs. cardboard, polyester textile vs. PET plastic — require either hyperspectral resolution, thermal IR data, sub-metre spatial analysis of morphological features, or multi-temporal context. These limits define the boundary between what spectral remote sensing can achieve alone and where ancillary data, deep learning, and field validation become essential.

---

## Appendix: Master spectral signature reference table

| Material | Albedo range | Key absorption bands (nm) | Primary mechanism | Best sensor bands | SWIR required? |
|---|---|---|---|---|---|
| PE | 0.3–0.8 (colour-dep.) | 1210, **1730**, 2310 | C-H overtones/combinations (sp³) | WV-3 SWIR-1, SWIR-4, SWIR-8 | **Yes** |
| PP | 0.3–0.8 (colour-dep.) | 1192, 1394, **1730** | C-H overtones including –CH₃ | WV-3 SWIR-1, SWIR-4 | **Yes** |
| PET | 0.2–0.7 (colour-dep.) | 1130, **1660**, 1908, 2130 | Aromatic C-H overtone; ester C=O | WV-3 SWIR-3, SWIR-5 | **Yes** |
| Fresh steel | 0.4–0.7 | None (featureless) | Free-electron (Drude) reflectance | Any VNIR (brightness) | No |
| Rusted metal | 0.1–0.3 | 480, 535, 670, **870** | Fe³⁺ crystal field transitions | S-2 B2–B8A; WV-3 VNIR | SWIR helpful |
| Aluminium | 0.85–0.92 | None (featureless) | Free-electron reflectance | Any (saturation risk) | No |
| Rubber/tires | 0.02–0.05 | Weak ~2300 | Carbon black broadband absorption | WV-3 SWIR-8 (weak) | SWIR helpful |
| Concrete | 0.25–0.50 | 1410, **1940**, 2340 | CO₃²⁻ vibration; H₂O; OH | WV-3 SWIR-8; S-2 B12 | **Yes** |
| Asphalt (fresh) | 0.03–0.08 | **1730**, 2310 | Hydrocarbon C-H vibration | WV-3 SWIR-4; S-2 B11 | **Yes** |
| Brick | 0.10–0.30 | 520, 670, **870**, 2200 | Fe³⁺ + Al-OH clay residual | S-2 B4–B8A; WV-3 SWIR-6 | SWIR preferred |
| Fresh wood | 0.15–0.40 | 1200, **1450**, **1940**, 2100, 2340 | Cellulose/lignin + water O-H | WV-3 SWIR-5/8; S-2 B11/B12 | **Yes** |
| Weathered wood | 0.10–0.25 | 2100, 2340 | Cellulose/lignin (water reduced) | WV-3 SWIR-5/8 | **Yes** |
| Cotton textile | Variable | 1200, 1450, **2100**, 2280 | Cellulose O-H and C-H | WV-3 SWIR-5/7 | **Yes** |
| Wool textile | Variable | **1500**, **2050**, 2170 | Protein N-H amide bonds | WV-3 SWIR-2/5 | **Yes** |
| Polyester textile | Variable | **1660**, 1730, 2130 | PET-identical polymer features | WV-3 SWIR-3/4/5 | **Yes** |
| Nylon textile | Variable | **1500**, **2050** | Polyamide N-H amide bonds | WV-3 SWIR-2/5 | **Yes** |
| Glass (clear) | 0.04–0.08 | 1390, 2200 (weak) | Si-O-H overtone; Fresnel reflection | All (very low signal) | No (featureless) |
| Green vegetation | 0.05–0.50 | **450**, **670**, 970, 1450, 1940 | Chlorophyll; H₂O absorption | All sensors (NDVI) | No |
| Dry vegetation | 0.10–0.35 | **2100**, 2340, 1730 | Cellulose; lignin | WV-3 SWIR-4/5/8; S-2 B12 | **Yes** |
| Clay-rich soil | 0.10–0.30 | 1400, 1900, **2200** | Al-OH; H₂O in clay interlayers | WV-3 SWIR-6; S-2 B12 | **Yes** |
| Sandy soil | 0.30–0.60 | ~None (featureless quartz) | Quartz transparent in VNIR-SWIR | BSI (requires SWIR) | Partial |
| Iron-rich soil | 0.10–0.25 | **480**, 535, 670, 870 | Fe³⁺ crystal field (same as rust) | S-2 B2–B8A | SWIR helpful |
| Clear water | 0.03–0.07 | >750 (strong) | Liquid H₂O molecular absorption | All sensors (NDWI) | No |
| Turbid water | 0.05–0.15 VIS | >750 (strong) | Sediment scattering + H₂O absorption | All sensors | No |