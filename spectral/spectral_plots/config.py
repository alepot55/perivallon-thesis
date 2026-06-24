"""Declarative configuration — materials, sensor bands, colors, plot specs.

To add a new material : add an entry to SPECTRA
To add a new plot     : add an entry to PLOTS
To change colors      : edit COLORS
To change band defs   : edit S2_BANDS / SD_BANDS / WV3_BANDS
"""
from __future__ import annotations

# ─────────────────────────────────────────────────────────────────────────────
# USGS zip internals
# ─────────────────────────────────────────────────────────────────────────────
_B  = "ASCIIdata_splib07a"
_CA = f"{_B}/ChapterA_ArtificialMaterials"
_CM = f"{_B}/ChapterM_Minerals"
_CO = f"{_B}/ChapterO_OrganicCompounds"
_CV = f"{_B}/ChapterV_Vegetation"
_CL = f"{_B}/ChapterL_Liquids"
_CS = f"{_B}/ChapterS_SoilsAndMixtures"

WVL_ASD  = f"{_B}/splib07a_Wavelengths_ASD_0.35-2.5_microns_2151_ch.txt"
WVL_BECK = f"{_B}/splib07a_Wavelengths_BECK_Beckman_0.2-3.0_microns.txt"

# ─────────────────────────────────────────────────────────────────────────────
# Material spectra: key → (zip_path, wavelength_type, sample_id)
# ─────────────────────────────────────────────────────────────────────────────
SPECTRA: dict[str, tuple[str, str, str]] = {
    # Plastics
    "HDPE (white opaque)":  (f"{_CA}/splib07a_Plastic_HDPE_GDS384_Wht_Opaq_ASDFRa_AREF.txt",  "ASD", "GDS384"),
    "HDPE (black)":         (f"{_CA}/splib07a_Plastic_HDPE_GDS351_BlkSheet_ASDFRa_AREF.txt",   "ASD", "GDS351"),
    "LDPE (white)":         (f"{_CA}/splib07a_Plastic_LDPE_GDS404_WhTrnslu_ASDFRa_AREF.txt",   "ASD", "GDS404"),
    "PET (clear)":          (f"{_CA}/splib07a_Plastic_PETE_GDS380_Clear_ASDFRa_AREF.txt",       "ASD", "GDS380"),
    "PET (brown)":          (f"{_CA}/splib07a_Plastic_PETE_GDS379_TrnslBrn_ASDFRa_AREF.txt",    "ASD", "GDS379"),
    "Polystyrene (blue)":   (f"{_CA}/splib07a_Polystyrene_GDS345_BluInsul_ASDFRa_AREF.txt",    "ASD", "GDS345"),
    "ABS (black)":          (f"{_CA}/splib07a_Plastic_ABS_GDS341_BlackPipe_ASDFRa_AREF.txt",    "ASD", "GDS341"),
    # Textiles
    "Polyester (black)":    (f"{_CA}/splib07a_Polyester_Pile_GDS434_Blk_ASDFRa_AREF.txt",      "ASD", "GDS434"),
    "Nylon (olive drab)":   (f"{_CA}/splib07a_Nylon_Webbing_GDS428_OlvDrab_ASDFRa_AREF.txt",   "ASD", "GDS428"),
    "Cotton (white)":       (f"{_CA}/splib07a_Cotton_Fabric_GDS437_White_ASDFRa_AREF.txt",      "ASD", "GDS437"),
    # Construction
    "Concrete (road)":      (f"{_CA}/splib07a_Concrete_GDS375_Lt_Gry_Road_ASDFRa_AREF.txt",    "ASD", "GDS375"),
    "Brick (red)":          (f"{_CA}/splib07a_Brick_GDS349_Paving_Red_ASDFRa_AREF.txt",         "ASD", "GDS349"),
    "Asphalt (road)":       (f"{_CA}/splib07a_Asphalt_GDS376_Blck_Road_old_ASDFRa_AREF.txt",   "ASD", "GDS376"),
    "Asphalt tar (roof)":   (f"{_CA}/splib07a_Asphalt_Tar_GDS346_Blck_Roof_ASDFRa_AREF.txt",  "ASD", "GDS346"),
    # Wood
    "Cedar (fresh)":        (f"{_CA}/splib07a_Cedar_Shake_GDS357_Fresh_ASDFRa_AREF.txt",       "ASD", "GDS357"),
    "Cedar (weathered)":    (f"{_CA}/splib07a_Cedar_Shake_GDS361_HiWeather_ASDFRa_AREF.txt",   "ASD", "GDS361"),
    "Pine beam (new)":      (f"{_CA}/splib07a_Wood_Beam_GDS363_Nw_Pine_2X4_ASDFRa_AREF.txt",  "ASD", "GDS363"),
    # Minerals
    "Goethite (pure)":      (f"{_CM}/splib07a_Goethite_GDS134_ASDFRb_AREF.txt",                "ASD", "GDS134"),
    "Iron oxide (pigment)": (f"{_CA}/splib07a_Iron_oxide_#4820_GDS782_ASDFRa_AREF.txt",        "ASD", "GDS782"),
    "Kaolinite (pure)":     (f"{_CM}/splib07a_Kaolinite_CM3_BECKa_AREF.txt",                   "BECK","CM3"),
    "Chrysotile (asbestos)":(f"{_CM}/splib07a_Chrysotile_HS323.1B_ASDNGa_AREF.txt",            "ASD", "HS323.1B"),
    # Organic
    "Cellulose (pure)":     (f"{_CO}/splib07a_Cellulose_SA-C6288_ASDHRa_AREF.txt",             "ASD", "SA-C6288"),
    "Lignin (alkali)":      (f"{_CO}/splib07a_Lignin_alkali_SA-370959_ASDHRa_AREF.txt",        "ASD", "SA-370959"),
    # Vegetation
    "Green vegetation":     (f"{_CV}/splib07a_Aspen_Aspen-1_green-top_ASDFRa_AREF.txt",        "ASD", "Aspen-1"),
    "Dry grass (golden)":   (f"{_CV}/splib07a_Grass_Golden_Dry_GDS480_ASDFRa_AREF.txt",        "ASD", "GDS480"),
    "Dry NPV (D.spicata)":  (f"{_CV}/splib07a_D.spicata_DWV6-0511_dryNPV.a_ASDFRa_AREF.txt",  "ASD", "DWV6-0511"),
    "Green grass":          (f"{_CV}/splib07a_Cheatgrass_ANPC1_field_calib_ASDFRa_AREF.txt",   "ASD", "ANPC1"),
    # Water / soil
    "Water (turbid)":       (f"{_CL}/splib07a_Water+Montmor_SWy-2+0.50g-l_ASDFRa_AREF.txt",  "ASD", "SWy-2+0.50"),
    "Bare soil":            (f"{_CS}/splib07a_Stonewall_Playa_Dry_Mud_2001_ASDFRa_AREF.txt",   "ASD", "DryMud2001"),
}

# ─────────────────────────────────────────────────────────────────────────────
# Colors — high contrast, colorblind-aware
# ─────────────────────────────────────────────────────────────────────────────
COLORS: dict[str, str] = {
    "HDPE_w": "#2166AC", "HDPE_b": "#4393C3", "LDPE": "#92C5DE",
    "PET_c":  "#D6604D", "PET_b":  "#F4A582",
    "PS":     "#8856A7", "ABS":    "#7A7A7A",
    "polyester": "#555555", "nylon": "#8C6D31", "cotton": "#2171B5",
    "concrete": "#969696", "brick": "#CB181D", "asphalt": "#525252", "tar": "#252525",
    "cedar_f": "#238B45", "cedar_w": "#A65628", "pine": "#E6AB02",
    "veg": "#1B7837", "dgrass": "#D4A017", "soil": "#8C510A", "water": "#2171B5",
    "feo": "#E31A1C", "goethite": "#FF7F00", "brick2": "#B2182B",
    "cellulose": "#1B7837", "lignin": "#543005",
}

# ─────────────────────────────────────────────────────────────────────────────
# Sensor band definitions: (label, center_nm, fwhm_nm)
# ─────────────────────────────────────────────────────────────────────────────
S2_BANDS = [
    ("B1",443,21),("B2",490,66),("B3",560,36),("B4",665,31),
    ("B5",705,15),("B6",740,15),("B7",783,20),("B8A",865,21),("B9",945,20),
    ("B11",1610,91),("B12",2190,175),
]

SD_BANDS = [
    ("CB",443,20),("B",490,50),("GI",531,36),("G",565,36),
    ("Y",610,20),("R",665,31),("RE",705,15),("NIR",865,40),
]
SD_SWIR_GAP_NM = 885

WV3_BANDS = [
    ("S1",1210,30),("S2",1570,40),("S3",1660,40),("S4",1730,40),
    ("S5",2165,40),("S6",2205,40),("S7",2260,50),("S8",2330,70),
]

SENSOR_COLORS = {"S2": "#3F7FBF", "SD": "#3D8B37", "WV3": "#D4721A"}
SENSOR_LABELS = {"S2": "Sentinel-2", "SD": "SuperDove", "WV3": "WV3 SWIR"}

# ─────────────────────────────────────────────────────────────────────────────
# Plot specifications — each dict fully describes one figure
#
#   curves      : list of (material_key, color_key, legend_label)
#   annotations : list of (wavelength_nm, label_text, "top"|"bottom")
#   xrange      : (xmin, xmax)  — default (350, 2500)
#   figsize     : (w, h)        — default (14, 7.5)
#   lw          : line width    — default 1.6
#   note        : optional text note at top of plot
# ─────────────────────────────────────────────────────────────────────────────
CITATION = "Data: USGS splib07a (Kokaly et al., 2017)"

PLOTS: list[dict] = [
    # 1 — Plastics
    {
        "filename": "spectral_plot_01_plastics.png",
        "title": "Spectral Reflectance of Common Packaging Plastics",
        "curves": [
            ("HDPE (white opaque)", "HDPE_w", "HDPE white opaque"),
            ("LDPE (white)",        "LDPE",   "LDPE white translucent"),
            ("PET (clear)",         "PET_c",  "PET clear"),
            ("PET (brown)",         "PET_b",  "PET translucent brown"),
            ("Polystyrene (blue)",  "PS",     "Polystyrene blue"),
            ("ABS (black)",         "ABS",    "ABS black"),
            ("HDPE (black)",        "HDPE_b", "HDPE black"),
        ],
        "annotations": [
            (1660, "PET aromatic C-H", "bottom"),
            (1730, "PE aliphatic C-H", "top"),
            (2310, "C-H combination",  "bottom"),
        ],
        "note": "PP omitted — spectrally similar to HDPE; PE/PP requires hyperspectral",
    },
    # 2 — PET vs PE zoom
    {
        "filename": "spectral_plot_02_pet_pe_zoom.png",
        "title": "PET vs PE Discrimination — SWIR (1500–1900 nm)",
        "xrange": (1500, 1900),
        "figsize": (14, 7.5),
        "lw": 2.0,
        "curves": [
            ("HDPE (white opaque)", "HDPE_w", "HDPE white opaque"),
            ("LDPE (white)",        "LDPE",   "LDPE white translucent"),
            ("PET (clear)",         "PET_c",  "PET clear"),
        ],
        "annotations": [
            (1660, "PET aromatic C-H", "bottom"),
            (1730, "PE aliphatic C-H", "top"),
        ],
    },
    # 3 — Construction
    {
        "filename": "spectral_plot_03_construction.png",
        "title": "Spectral Reflectance of Construction Materials",
        "curves": [
            ("Concrete (road)",    "concrete", "Concrete, light grey road"),
            ("Brick (red)",        "brick",    "Brick, paving red"),
            ("Asphalt (road)",     "asphalt",  "Asphalt, black road"),
            ("Asphalt tar (roof)", "tar",      "Asphalt tar, black roof"),
        ],
        "annotations": [
            ( 870, "Fe³⁺ (brick)",  "top"),
            (1730, "Hydrocarbon",   "top"),
            (1940, "H₂O (concrete)","bottom"),
            (2340, "CO₃²⁻",        "bottom"),
        ],
    },
    # 4 — Wood
    {
        "filename": "spectral_plot_04_wood.png",
        "title": "Spectral Reflectance of Wood (Fresh vs Weathered)",
        "curves": [
            ("Cedar (fresh)",     "cedar_f", "Cedar shake, fresh"),
            ("Cedar (weathered)", "cedar_w", "Cedar shake, heavily weathered"),
            ("Pine beam (new)",   "pine",    "Pine beam, new"),
        ],
        "annotations": [
            (1450, "H₂O",             "bottom"),
            (1940, "H₂O",             "bottom"),
            (2100, "Cellulose",        "top"),
            (2340, "Lignin/cellulose", "bottom"),
        ],
    },
    # 5 — Textiles
    {
        "filename": "spectral_plot_05_textiles.png",
        "title": "Spectral Reflectance of Textile Fibers",
        "curves": [
            ("Polyester (black)",  "polyester", "Polyester pile, black"),
            ("Nylon (olive drab)", "nylon",     "Nylon webbing, olive drab"),
            ("Cotton (white)",     "cotton",    "Cotton fabric, white"),
        ],
        "annotations": [
            (1500, "N-H (nylon)",               "top"),
            (1660, "Aromatic C-H (polyester)",   "bottom"),
            (2050, "Amide (nylon)",              "top"),
            (2100, "Cellulose (cotton)",          "bottom"),
        ],
    },
    # 6 — Natural backgrounds
    {
        "filename": "spectral_plot_06_natural_backgrounds.png",
        "title": "Spectral Reflectance of Natural Background Materials",
        "curves": [
            ("Green vegetation",  "veg",    "Green vegetation (aspen)"),
            ("Dry grass (golden)","dgrass",  "Dry grass, golden"),
            ("Bare soil",         "soil",   "Bare soil (dry playa)"),
            ("Water (turbid)",    "water",  "Water, slightly turbid"),
        ],
        "annotations": [
            ( 670, "Chl absorption", "bottom"),
            ( 870, "NIR plateau",    "top"),
            (1450, "H₂O",           "bottom"),
            (1940, "H₂O",           "bottom"),
        ],
    },
    # 7 — Plastic vs dry vegetation
    {
        "filename": "spectral_plot_07_plastic_vs_vegetation.png",
        "title": "Plastic vs Dry Vegetation: SWIR Discrimination",
        "curves": [
            ("HDPE (white opaque)", "HDPE_w",    "HDPE white opaque"),
            ("Dry grass (golden)",  "dgrass",     "Dry grass, golden"),
            ("Cellulose (pure)",    "cellulose",  "Cellulose, pure"),
        ],
        "annotations": [
            (1730, "Plastic only — C-H",     "top"),
            (2100, "Cellulose only — C-O-C", "top"),
        ],
    },
    # 8 — Iron oxides
    {
        "filename": "spectral_plot_08_iron_oxides.png",
        "title": "Iron Oxide Features: Rust vs Soil Minerals",
        "curves": [
            ("Iron oxide (pigment)", "feo",      "Iron oxide pigment"),
            ("Goethite (pure)",      "goethite",  "Goethite, pure"),
            ("Brick (red)",          "brick2",    "Brick, paving red"),
        ],
        "annotations": [
            ( 480, "Fe³⁺ CT",                "bottom"),
            ( 670, "Fe³⁺ CF",                "top"),
            ( 870, "Fe³⁺ NIR",               "top"),
            (2200, "Al-OH (absent in rust)",  "bottom"),
        ],
    },
    # 9 — Biochemicals
    {
        "filename": "spectral_plot_09_biochemicals.png",
        "title": "Spectral Signatures of Plant Biochemical Components",
        "lw": 1.8,
        "curves": [
            ("Cellulose (pure)", "cellulose", "Cellulose, pure"),
            ("Lignin (alkali)",  "lignin",    "Lignin, alkali"),
        ],
        "annotations": [
            (1200, "O-H / C-H",       "top"),
            (1450, "H₂O / O-H",       "bottom"),
            (1730, "C-H 1st overtone", "top"),
            (2100, "C-O-C",           "top"),
            (2340, "Lignin",          "bottom"),
        ],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Combined CSV column definitions: (csv_column_name, material_key)
# ─────────────────────────────────────────────────────────────────────────────
CSV_COLUMNS: list[tuple[str, str]] = [
    ("HDPE_white_GDS384",       "HDPE (white opaque)"),
    ("HDPE_black_GDS351",       "HDPE (black)"),
    ("LDPE_white_GDS404",       "LDPE (white)"),
    ("PET_clear_GDS380",        "PET (clear)"),
    ("PET_brown_GDS379",        "PET (brown)"),
    ("Polystyrene_blue_GDS345", "Polystyrene (blue)"),
    ("ABS_black_GDS341",        "ABS (black)"),
    ("Polyester_black_GDS434",  "Polyester (black)"),
    ("Nylon_olive_GDS428",      "Nylon (olive drab)"),
    ("Cotton_white_GDS437",     "Cotton (white)"),
    ("Concrete_grey_GDS375",    "Concrete (road)"),
    ("Brick_red_GDS349",        "Brick (red)"),
    ("Asphalt_black_GDS376",    "Asphalt (road)"),
    ("Asphalt_tar_GDS346",      "Asphalt tar (roof)"),
    ("Cedar_fresh_GDS357",      "Cedar (fresh)"),
    ("Cedar_weathered_GDS361",  "Cedar (weathered)"),
    ("Pine_beam_GDS363",        "Pine beam (new)"),
    ("GreenVeg_aspen",          "Green vegetation"),
    ("DryGrass_golden_GDS480",  "Dry grass (golden)"),
    ("DryNPV_Dspicata",         "Dry NPV (D.spicata)"),
    ("BareSoil_playa",          "Bare soil"),
    ("Water_turbid",            "Water (turbid)"),
    ("IronOxide_GDS782",        "Iron oxide (pigment)"),
    ("Goethite_GDS134",         "Goethite (pure)"),
    ("Cellulose_SAC6288",       "Cellulose (pure)"),
    ("Lignin_SA370959",         "Lignin (alkali)"),
]
