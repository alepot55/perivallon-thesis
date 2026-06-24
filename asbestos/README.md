# asbestos/ — Pilot Fase 1: amianto Lombardia

Sub-task della tesi: rilevamento tetti in cemento-amianto su Lombardia con imagery satellitare commerciale (PNEO, WorldView-3) e Planet SuperDove, ground truth pubblica WFS Regione Lombardia.

**Riferimento:** Mazzola (2024), `reference/Mazzola_2024_Thesis.pdf` — tesi precedente sulla stessa AOI.

## Layout

```
asbestos/
├── README.md
├── data/                          ← ground truth + imagery
│   ├── mappatura_2020.gpkg              10,903 tetti amianto (anno 2020, ufficiale)
│   ├── mappature_precedenti.gpkg        50,131 tetti (storico pre-2020)
│   ├── aree_mappature_2020.gpkg         10 macro-zone censite
│   ├── aree_mappature.gpkg              15 macro-zone storiche
│   ├── tutti_i_comuni.gpkg              1506 comuni Lombardia (anagrafica ISTAT)
│   ├── province.gpkg                    12 province
│   └── planet/PSScene/                  7 strip Planet 2026-03-30 (prima prova)
├── footprint/
│   └── Asbestos_footprint.geojson       20 footprint AOI multi-sensore (PNEO + WV3)
├── notebooks/
│   ├── 05_amianto_briefing.ipynb        Briefing per advisor (eseguito, con output)
│   └── 05_amianto_briefing.py           Generatore .ipynb (riproducibile)
├── qgis/
│   └── mazzola.qgz                      Progetto QGIS con tutti i layer
└── reference/
    └── Mazzola_2024_Thesis.pdf          Tesi precedente sulla AOI
```

## Origine dei dati

Tutti i `.gpkg` sono stati scaricati offline dal WFS pubblico Regione Lombardia.

- Endpoint: `https://www.cartografia.regione.lombardia.it/...` (WFS / REST)
- Layer: `Mappatura_2020`, `Mappature_precedenti`, `Aree_Mappature_2020`, `Aree_Mappature`
- CRS: EPSG:32632 (UTM 32N)

## Notebook

Aprire `notebooks/05_amianto_briefing.ipynb` per la cover analytics completa (coverage AOI↔GT, discrepanza temporale, distribuzione per provincia, preview imagery Planet). Tutte le path sono assolute (`ROOT = /home/alepot55/Desktop/uni/Tesi`) e si risolvono automaticamente nella nuova struttura.

Dipendenze: geopandas, rasterio, folium, matplotlib, shapely, PIL — incluse nell'env di `../waste/`.

## Numeri chiave (snapshot 2026-05-17)

- GT Mappatura_2020: **10,903 tetti**, area mediana 226 m² (~25 px SuperDove)
- Coverage AOI ↔ GT: **1,126 tetti dentro AOI (10.3%)**
- Footprint con più GT: `PNEO_LOMBARDIA3_20230416_ALL_RAW` (600 tetti)
- Overlap Planet prima-prova ↔ GT: **0** (fuori area mappata → pipeline test only)

## Next steps

1. Re-acquisire Planet PSScene/SuperDove sull'overlap PNEO_LOMBARDIA2+3
2. Estrarre firme USGS chrysotile e confrontare con `../spectral/`
3. Pipeline `(poligono_GT × tile_imagery) → mean/median/std per banda` con maschera UDM2
4. SAM intra-class vs inter-class, distribuzione Bhattacharyya
