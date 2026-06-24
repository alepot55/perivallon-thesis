# spectral/ — USGS splib07a reference spectral signatures

Libreria spettrale di riferimento per il pilot amianto (e in generale per la separabilità spettrale plastica/legno/cemento/vegetazione). Costruita a partire dalla USGS Digital Spectral Library `splib07a`.

## Layout

```
spectral/
├── README.md
├── Spec_Grafici_Firme_Spettrali.md   ← specifica dei 9 grafici
├── data/
│   └── ASCIIdata_splib07a.zip        ← libreria USGS completa (input)
├── scripts/
│   └── generate.py                   ← rigenera tutto (figure + CSV + PDF)
├── spectral_plots/                   ← modulo Python (config, data, plotting)
├── csv/
│   ├── spectral_signatures_all_materials.csv   ← combined CSV (tutti i materiali × 2151 bande)
│   └── per_material/                            ← CSV singoli per materiale
└── figures/
    ├── spectral_plot_01_plastics.png            ← plastiche (HDPE/LDPE/PET)
    ├── spectral_plot_02_pet_pe_zoom.png         ← zoom PET vs PE
    ├── spectral_plot_03_construction.png        ← materiali da costruzione (cemento, asfalto, ...)
    ├── spectral_plot_04_wood.png                ← legno
    ├── spectral_plot_05_textiles.png            ← tessuti
    ├── spectral_plot_06_natural_backgrounds.png ← vegetazione / suolo / acqua
    ├── spectral_plot_07_plastic_vs_vegetation.png  ← coppia di confusione critica
    ├── spectral_plot_08_iron_oxides.png         ← ossidi di ferro
    ├── spectral_plot_09_biochemicals.png        ← biochimici
    └── spectral_signature_library.pdf           ← PDF unico di tutti i 9 plot
```

## Regenerate

```bash
cd spectral
python3 scripts/generate.py
```

Output: ripopola `figures/`, `csv/` e il PDF combinato a partire da `data/ASCIIdata_splib07a.zip`. Scarica anche la firma `rubber` da ECOSTRESS se la rete è disponibile.

## Note

- **Range USGS splib07a:** 0.20–2.97 µm (2151 bande), che copre VNIR + SWIR.
- **Feature diagnostica cemento-amianto:** Mg-OH bending a **2.31 µm** (Frassy 2014, Bassani 2007). Fuori range SuperDove (≤0.86 µm); dentro range WV3 SWIR. Vedi `spectral_plot_03_construction.png`.
- I CSV sono pronti da consumare in numpy/pandas: una riga per materiale, una colonna per banda + colonna di wavelength.
