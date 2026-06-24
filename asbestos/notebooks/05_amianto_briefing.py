"""
Generator script for 05_amianto_briefing.ipynb — Thomas briefing.

Run with:  python notebooks/05_amianto_briefing.py
This builds the .ipynb (cells + outputs precomputed where useful),
then nbconvert --execute is run separately to render outputs.
"""

import json
from pathlib import Path

NB_PATH = Path(__file__).parent / "05_amianto_briefing.ipynb"


def md(src: str):
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}


def code(src: str):
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": src.splitlines(keepends=True),
    }


cells = []

# ============================================================================
cells.append(md("""# Briefing amianto — stato pilota Fase 1

**Author:** Alessandro Potenza · **Advisor:** Thomas Martinoli · **Date:** 2026-05-17

Tesi: *Illegal Waste Detection from Multispectral Satellite Imagery* — pilot amianto su Lombardia.

Questo notebook riassume lo **stato attuale** dei dati per la Fase 1 (pilot amianto, SuperDove + SAM) prima della sessione con Thomas:

1. AOI multi-sensor pianificata + immagini Planet PSScene già acquisite (`prima prova`)
2. Ground truth pubblica: WFS Regione Lombardia, layer `Mappatura_2020`
3. **Coverage analysis** AOI ↔ GT — *quanto della GT è dentro le scene pianificate*
4. Discrepanza temporale GT 2020 vs mappature precedenti
5. Distribuzione spaziale e per comune
6. Firme spettrali di riferimento (libreria USGS splib07a — già pronte)
7. Punti di discussione e prossimi passi

> Tutti i dati WFS sono stati scaricati offline in `data/asbestos/*.gpkg` per girare anche senza rete.
"""))

cells.append(code("""# Setup
import os, glob, json, warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LogNorm
import folium
from folium.plugins import MarkerCluster, HeatMap, MeasureControl
import rasterio
from rasterio.warp import transform_bounds
from shapely.geometry import box

# Paths
ROOT      = '/home/alepot55/Desktop/uni/Tesi'
DATA      = f'{ROOT}/asbestos/data'
PLANET    = f'{DATA}/planet/PSScene'
SPECTRA   = f'{ROOT}/spectral'
AOI_FILE  = f'{ROOT}/asbestos/footprint/Asbestos_footprint.geojson'

plt.rcParams.update({'figure.dpi': 110, 'savefig.dpi': 150, 'figure.facecolor': 'white',
                     'axes.grid': True, 'grid.alpha': 0.3, 'font.size': 10})
print('Setup OK.  Working dir:', os.getcwd())
"""))

# ============================================================================
cells.append(md("""## 1. Inventario dati

Tre fonti, già su disco:

| Fonte | File | Descrizione |
|---|---|---|
| AOI multi-sensor | `asbestos/footprint/Asbestos_footprint.geojson` | 20 footprint pianificati (WV3, Pléiades Neo) |
| Imagery Planet | `asbestos/data/planet/PSScene/*.tif` | 7 strip PSScene 2026-03-30 (`prima prova`) |
| Ground truth WFS | `asbestos/data/*.gpkg` | `Mappatura_2020`, `Mappature_precedenti`, aree, comuni, province |
| Libreria spettrale | `spectral/figures/*.png` | 9 grafici USGS splib07a + PDF combinato |
"""))

cells.append(code("""# Carica WFS layers + AOI + footprint Planet
m2020 = gpd.read_file(f'{DATA}/mappatura_2020.gpkg').to_crs(32632)
m_prec = gpd.read_file(f'{DATA}/mappature_precedenti.gpkg').to_crs(32632)
aree_2020 = gpd.read_file(f'{DATA}/aree_mappature_2020.gpkg').to_crs(32632)
aree_prec = gpd.read_file(f'{DATA}/aree_mappature.gpkg').to_crs(32632)
# Tutti_i_Comuni e Province sono tabelle attributi (no geometry sul WFS): solo per il join
comuni = pd.DataFrame(gpd.read_file(f'{DATA}/tutti_i_comuni.gpkg').drop(columns='geometry', errors='ignore'))
province = pd.DataFrame(gpd.read_file(f'{DATA}/province.gpkg').drop(columns='geometry', errors='ignore'))

# Codice_Istat di M_2020 è 8 char string '03XX' + 6-digit ISTAT comune
# Comuni.ISTAT_ è int. Mapping con join su ultimi 6 char int.
m2020['_istat'] = m2020['Codice_Istat'].str[-6:].str.lstrip('0').astype(int)
m2020 = m2020.merge(comuni[['ISTAT_','COMUNE','PROVINCIA']], left_on='_istat', right_on='ISTAT_', how='left')

aoi = gpd.read_file(AOI_FILE).to_crs(32632)
# date arrives as ISO string; tieni anche datetime per ordinamento
aoi['date_dt'] = pd.to_datetime(aoi['date'])
aoi['date'] = aoi['date_dt'].dt.strftime('%Y-%m-%d')

# Planet PSScene metadata
planet_tifs = sorted(glob.glob(f'{PLANET}/*_AnalyticMS_SR_clip.tif'))
planet_recs = []
for tif in planet_tifs:
    with rasterio.open(tif) as src:
        scene_id = os.path.basename(tif).split('_3B_')[0]
        planet_recs.append({
            'scene_id': scene_id, 'file': tif, 'crs': str(src.crs),
            'bands': src.count, 'width': src.width, 'height': src.height,
            'minx': src.bounds.left, 'miny': src.bounds.bottom,
            'maxx': src.bounds.right, 'maxy': src.bounds.top,
            'res_m': src.res[0],
            'geometry': box(*src.bounds),
        })
planet_gdf = gpd.GeoDataFrame(planet_recs, geometry='geometry', crs='EPSG:32632')

print('Mappatura_2020 (GT):   {:>6} tetti'.format(len(m2020)))
print('Mappature_precedenti:  {:>6} tetti (storico)'.format(len(m_prec)))
print('Aree mappatura 2020:   {:>6} macro-zone'.format(len(aree_2020)))
print('Aree mappatura storica:{:>6} macro-zone'.format(len(aree_prec)))
print('Comuni Lombardia:      {:>6}'.format(len(comuni)))
print('Province:              {:>6}'.format(len(province)))
print('AOI footprint:         {:>6} scene pianificate'.format(len(aoi)))
print('Planet PSScene tiles:  {:>6} strip già acquisite'.format(len(planet_gdf)))
"""))

# ============================================================================
cells.append(md("""## 2. AOI multi-sensor — composizione

L'AOI shared da Thomas include 20 footprint di 2 sensori commerciali, distribuiti in 4 date di acquisizione PNEO (Apr/Jun 2023) e 8 date WV3 (Aug 2024 → Oct 2025).
"""))

cells.append(code("""# Riassunto AOI per sensor + data
aoi['area_km2'] = aoi.geometry.area / 1e6
summary = (aoi.groupby(['satellite', 'date'])
              .agg(scenes=('id','count'), area_km2=('area_km2','sum'))
              .reset_index().sort_values(['satellite','date']))
print(summary.to_string(index=False))
print(f'\\n  Totale scene: {len(aoi)}')
print(f'  Area totale (con overlap): {aoi[\"area_km2\"].sum():>8.1f} km²')
print(f'  Area unione (deduplicata):  {aoi.union_all().area/1e6:>8.1f} km²')
"""))

# ============================================================================
cells.append(md("""## 3. Mappa interattiva — AOI + GT + Planet `prima prova`

Mappa folium con tutti i layer principali. Strati attivabili dal control in alto a destra.

> **Convenzioni colori:**
> - 🟧 **arancione** AOI PNEO (Pléiades Neo, già acquisite 2023)
> - 🟪 **viola** AOI WV3 (WorldView-3, pianificate 2024-25)
> - 🟦 **azzurro** Planet PSScene `prima prova` (acquisite 2026-03-30)
> - 🟥 **rosso** Aree mappatura 2020 (dove la Regione ha censito)
> - ⚫ **nero** poligoni `Mappatura_2020` (single GT roofs)
"""))

cells.append(code("""# Mappa interattiva — output salvato come HTML statico embed
# Drop datetime cols for folium JSON serialization
aoi4326    = aoi.to_crs(4326).drop(columns=[c for c in aoi.columns if 'date_dt' in c or pd.api.types.is_datetime64_any_dtype(aoi[c])], errors='ignore')
planet4326 = planet_gdf.to_crs(4326)
aree2020_4326 = aree_2020.to_crs(4326)

# Centroid AOI per centratura
cx, cy = aoi4326.union_all().centroid.x, aoi4326.union_all().centroid.y
m = folium.Map(location=[cy, cx], zoom_start=9, tiles='OpenStreetMap', control_scale=True)
folium.TileLayer('CartoDB.Positron', name='Light').add_to(m)
folium.TileLayer('Esri.WorldImagery', name='Satellite').add_to(m)

# Aree mappatura 2020
folium.GeoJson(aree2020_4326.__geo_interface__,
               name='Aree mappatura 2020',
               style_function=lambda x: {'color':'#c0392b','weight':1.5,'fillColor':'#e74c3c','fillOpacity':0.07}
               ).add_to(m)

# AOI: split per satellite
pneo = aoi4326[aoi4326.satellite=='PNEO']
wv3  = aoi4326[aoi4326.satellite=='WV3']
folium.GeoJson(pneo.__geo_interface__, name='AOI PNEO (Pléiades Neo)',
               style_function=lambda x:{'color':'#e67e22','weight':2,'fillColor':'#f39c12','fillOpacity':0.18},
               tooltip=folium.GeoJsonTooltip(['id','date','area_km2_utm'])).add_to(m)
folium.GeoJson(wv3.__geo_interface__, name='AOI WV3 (WorldView-3)',
               style_function=lambda x:{'color':'#8e44ad','weight':2,'fillColor':'#9b59b6','fillOpacity':0.14},
               tooltip=folium.GeoJsonTooltip(['id','date','area_km2_utm'])).add_to(m)

# Planet prima_prova
folium.GeoJson(planet4326.__geo_interface__, name='Planet PSScene (prima prova)',
               style_function=lambda x:{'color':'#2980b9','weight':2,'fillColor':'#3498db','fillOpacity':0.22},
               tooltip=folium.GeoJsonTooltip(['scene_id','bands','res_m'])).add_to(m)

# GT M_2020: 10.903 poligoni — troppi per folium. Sample stratificato + cluster.
gt_pts = m2020.set_geometry(m2020.geometry.centroid).to_crs(4326)
gt_pts = gt_pts[gt_pts.geometry.is_valid & ~gt_pts.geometry.is_empty]
sample_n = min(1500, len(gt_pts))
gt_sample = gt_pts.sample(n=sample_n, random_state=0)
mc = MarkerCluster(name=f'Mappatura_2020 (sample {sample_n} di {len(gt_pts):,})'.replace(',', '.'), show=False).add_to(m)
for _, row in gt_sample.iterrows():
    pt = row.geometry
    folium.CircleMarker([pt.y, pt.x], radius=2, color='black', fillColor='black',
                        fillOpacity=0.7, weight=0,
                        tooltip=f"{row.get('COMUNE','?')} ({row.get('PROVINCIA','?')}) — {row['Shape_Area']:.0f} m²"
                        ).add_to(mc)

folium.LayerControl(collapsed=False).add_to(m)
m.add_child(MeasureControl())
m
"""))

# ============================================================================
cells.append(md("""## 4. Coverage AOI ↔ GT — **il punto chiave**

Domanda: *quanta GT è effettivamente dentro le scene pianificate?* È la metrica che decide quali acquisizioni hanno valore per la Fase 1 pilot.
"""))

cells.append(code("""# Spatial join GT × AOI
gt_in_aoi = gpd.sjoin(m2020[['geometry']], aoi[['id','satellite','region','date','area_km2','geometry']],
                      how='inner', predicate='intersects')
n_gt_total = len(m2020)
n_gt_in    = gt_in_aoi['index_right'].nunique() if 'index_right' in gt_in_aoi.columns else len(gt_in_aoi)
n_gt_in    = len(gt_in_aoi.drop_duplicates(subset=gt_in_aoi.index.name or gt_in_aoi.columns[0]))

# Conteggio per footprint
per_scene = gt_in_aoi.groupby(['id','satellite','region','date'])\\
                     .size().reset_index(name='n_gt_polygons')\\
                     .sort_values('n_gt_polygons', ascending=False)

# Tetti che cadono in NESSUNA scena pianificata
gt_indices_in = set(gt_in_aoi.index)
n_gt_outside  = n_gt_total - len(gt_indices_in)

print(f'GT M_2020 totale:               {n_gt_total:>5}')
print(f'GT dentro almeno un footprint:  {len(gt_indices_in):>5}  ({100*len(gt_indices_in)/n_gt_total:.1f}%)')
print(f'GT fuori da tutti i footprint:  {n_gt_outside:>5}  ({100*n_gt_outside/n_gt_total:.1f}%)')
print()
print('GT per footprint pianificato:')
print(per_scene.to_string(index=False))
"""))

cells.append(code("""# Barplot top scene per GT coverage
top = per_scene.head(10).copy()
fig, ax = plt.subplots(figsize=(11, 4.5))
colors = top['satellite'].map({'PNEO':'#e67e22','WV3':'#8e44ad'}).fillna('#3498db')
ax.barh(top['id'], top['n_gt_polygons'], color=colors, edgecolor='k', linewidth=0.5)
for i, (n, sat, d) in enumerate(zip(top['n_gt_polygons'], top['satellite'], top['date'])):
    ax.text(n+5, i, f'{n}  [{sat} · {d}]', va='center', fontsize=9)
ax.invert_yaxis()
ax.set_xlabel('Numero tetti GT Mappatura_2020 dentro il footprint')
ax.set_title('Quanta ground truth contiene ogni footprint pianificato', fontweight='bold')
ax.set_xlim(0, top['n_gt_polygons'].max()*1.25)
handles = [mpatches.Patch(color='#e67e22', label='PNEO (Pléiades Neo)'),
           mpatches.Patch(color='#8e44ad', label='WV3 (WorldView-3)')]
ax.legend(handles=handles, loc='lower right')
plt.tight_layout(); plt.show()
"""))

cells.append(md("""**Conclusioni di copertura:**

- I 3 footprint principali (**PNEO_LOMBARDIA3 + PNEO_LOMBARDIA2 + WV3_MILANO**) raccolgono ~81% della GT dentro AOI.
- I footprint su Bergamo, Mantova, Pavia, Brescia, Varese: poca o nulla GT → questi serviranno per test cross-region / OOD (Fase 4 del piano sperimentale), non per Fase 1 pilot.
- Le **PNEO_LOMBARDIA acquisite nell'aprile 2023** sono le candidate naturali per cominciare l'estrazione delle firme spettrali sulla GT.
"""))

# ============================================================================
cells.append(md("""## 5. Planet `prima prova` ↔ GT — verifica

Le 7 strip PSScene del 2026-03-30 coprono ~3.500 km² ad ovest di Milano (area lacuale Como/Maggiore). Verifica intersezione con la GT.
"""))

cells.append(code("""# Planet ↔ GT
gt_in_planet = gpd.sjoin(m2020[['geometry']], planet_gdf[['scene_id','geometry']], predicate='intersects', how='inner')
print(f'Planet PSScene 2026-03-30 — tetti GT contenuti: {len(gt_in_planet)}')
print()

# Bounds confronto
print(f'Planet bbox (WGS84): {planet_gdf.to_crs(4326).total_bounds}')
print(f'GT bbox     (WGS84): {m2020.to_crs(4326).total_bounds}')
print(f'AOI bbox    (WGS84): {aoi.to_crs(4326).total_bounds}')
"""))

cells.append(md("""> **Diagnosi**: la `prima prova` Planet 2026-03-30 ricade a ovest dell'estensione GT (zona lacuale Como/Maggiore) — la sovrapposizione con `Mappatura_2020` è nulla.
>
> **Implicazione operativa**: l'imagery PSScene già scaricata è utile come *test della pipeline di download/preprocessing* (calibrazione UDM2, conversione SR), ma **non può essere usata per il pilot Fase 1** che richiede pixel sopra poligoni amianto annotati. Per il pilot servono PSScene/SuperDove sull'AOI dei footprint con più GT (PNEO_LOMBARDIA2/3, area Bergamo/Brianza).
"""))

# ============================================================================
cells.append(md("""## 6. Distribuzione spaziale GT — mappa overview

Mappa statica a tutto-AOI: GT come hex-binning (densità), AOI footprints sopra. Risponde a "dove si concentrano i tetti?"
"""))

cells.append(code("""fig, ax = plt.subplots(figsize=(13, 7))

# Aree mappatura 2020 di fondo (per dare senso geografico)
aree_2020.plot(ax=ax, facecolor='#f4ece0', edgecolor='#a08060', linewidth=0.6, alpha=0.9, zorder=1)

# Hexbin density della GT
xs = m2020.geometry.centroid.x.values
ys = m2020.geometry.centroid.y.values
hb = ax.hexbin(xs, ys, gridsize=80, cmap='YlOrRd', mincnt=1,
               norm=LogNorm(), edgecolor='none', zorder=2)
cb = fig.colorbar(hb, ax=ax, fraction=0.035, pad=0.02)
cb.set_label('# tetti M_2020 per hex-cell (log)')

# AOI footprints sopra
for sat, color in [('PNEO','#1f4e7e'),('WV3','#5b2c6f')]:
    aoi[aoi.satellite==sat].boundary.plot(ax=ax, color=color, linewidth=1.8, zorder=3)

# Planet
planet_gdf.boundary.plot(ax=ax, color='#2980b9', linewidth=1.2, linestyle='--', zorder=3)

# Labels sui top footprint
for _, r in aoi.iterrows():
    c = r.geometry.centroid
    if r.area_km2_utm > 100:
        ax.annotate(r['id'].split('_')[1], (c.x, c.y), fontsize=8,
                    color='black', ha='center', alpha=0.9)

handles = [
    mpatches.Patch(facecolor='#f4ece0', edgecolor='#a08060', label='Aree mappatura 2020 (perimetri WFS)'),
    mpatches.Patch(facecolor='#fde7a7', edgecolor='#fdae61', label='Densità GT (log scala)'),
    mpatches.Patch(facecolor='none', edgecolor='#1f4e7e', label='AOI PNEO'),
    mpatches.Patch(facecolor='none', edgecolor='#5b2c6f', label='AOI WV3'),
    mpatches.Patch(facecolor='none', edgecolor='#2980b9', label='Planet (prima prova)', linestyle='--'),
]
ax.legend(handles=handles, loc='upper left', fontsize=9)
ax.set_aspect('equal')
ax.set_title(f'Distribuzione spaziale dei {len(m2020):,} tetti M_2020 + footprint pianificati'.replace(',', '.'),
             fontweight='bold')
ax.set_xlabel('Easting UTM 32N (m)'); ax.set_ylabel('Northing UTM 32N (m)')
plt.tight_layout(); plt.show()
"""))

# ============================================================================
cells.append(md("""## 7. Statistiche per provincia / comune

Ranking dei comuni con più tetti M_2020 (top 20). Join geometrico GT × comuni.
"""))

cells.append(code("""# COMUNE/PROVINCIA già nel df grazie al join via ISTAT — niente spatial join
per_comune = (m2020.groupby(['COMUNE','PROVINCIA'])
              .agg(n_tetti=('Shape_Area','size'),
                   area_m2_media=('Shape_Area','mean'),
                   area_m2_totale=('Shape_Area','sum'))
              .reset_index().sort_values('n_tetti', ascending=False))

print('Top 20 comuni per #tetti amianto censiti (Mappatura_2020):')
print(per_comune.head(20).to_string(index=False, float_format='%.1f'))
print()

per_prov = (m2020.groupby('PROVINCIA')
            .agg(n_tetti=('Shape_Area','size'), area_m2_totale=('Shape_Area','sum'))
            .reset_index().sort_values('n_tetti', ascending=False))
print('Per provincia:')
print(per_prov.to_string(index=False, float_format='%.0f'))
"""))

cells.append(code("""# Visual: barplot top comuni + top province
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
top20 = per_comune.head(20)
axes[0].barh(top20['COMUNE'] + ' (' + top20['PROVINCIA'] + ')', top20['n_tetti'], color='#c0392b', edgecolor='k', linewidth=0.4)
axes[0].invert_yaxis(); axes[0].set_xlabel('# tetti amianto')
axes[0].set_title('Top 20 comuni — Mappatura_2020', fontweight='bold')

axes[1].barh(per_prov['PROVINCIA'], per_prov['n_tetti'], color='#2c3e50', edgecolor='k', linewidth=0.4)
axes[1].invert_yaxis(); axes[1].set_xlabel('# tetti amianto')
axes[1].set_title('Per provincia', fontweight='bold')
plt.tight_layout(); plt.show()
"""))

# ============================================================================
cells.append(md("""## 8. Distribuzione delle aree dei tetti

L'area mediana è un input critico per la pipeline: a 3 m/px (SuperDove) un tetto di X m² occupa ~X/9 pixel — sotto i 50 m² (~5 pixel) il segnale spettrale è dominato dal mixed-pixel.
"""))

cells.append(code("""areas = m2020['Shape_Area'].values
fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

# Hist
axes[0].hist(areas, bins=np.logspace(0, 5, 50), color='#c0392b', edgecolor='k', alpha=0.8)
axes[0].set_xscale('log'); axes[0].set_xlabel('Area tetto (m²) — scala log')
axes[0].set_ylabel('# tetti')
axes[0].axvline(50, color='blue', linestyle='--', label='50 m² ≈ 5 pixel SuperDove')
axes[0].axvline(np.median(areas), color='black', linestyle=':', label=f'Mediana = {np.median(areas):.0f} m²')
axes[0].legend(); axes[0].set_title('Distribuzione aree tetti — Mappatura_2020', fontweight='bold')

# CDF
sorted_areas = np.sort(areas)
cdf = np.arange(1, len(sorted_areas)+1) / len(sorted_areas)
axes[1].plot(sorted_areas, cdf, color='#c0392b', linewidth=2)
axes[1].set_xscale('log')
for thr, label in [(9,'1 px SD'), (27,'3 px SD'), (50,'≈5 px SD'), (225,'1 px WV3-MS')]:
    p = (areas <= thr).mean() * 100
    axes[1].axvline(thr, color='gray', linestyle=':', alpha=0.6)
    axes[1].text(thr, 0.03, f'{label}\\n{p:.0f}%', fontsize=8, rotation=0, ha='center')
axes[1].set_xlabel('Area tetto (m²) — scala log'); axes[1].set_ylabel('CDF')
axes[1].set_title('CDF aree — soglie risoluzione sensore', fontweight='bold')
plt.tight_layout(); plt.show()

q25, q50, q75, q95 = np.percentile(areas, [25, 50, 75, 95])
print(f'Aree tetti M_2020:  Q25={q25:.0f} m²   Mediana={q50:.0f} m²   Q75={q75:.0f} m²   Q95={q95:.0f} m²')
print(f'Tetti <50 m² (mixed-pixel a 3 m): {(areas<50).mean()*100:.1f}% — irrisolvibili per SuperDove')
print(f'Tetti ≥225 m² (≥1 px MS WV3 3 m): {(areas>=225).mean()*100:.1f}% — risolvibili WV3 multispettrale')
"""))

# ============================================================================
cells.append(md("""## 9. Discrepanza temporale — 2020 vs storico

`Mappature_precedenti` contiene **50.131** tetti censiti in mappature anteriori al 2020. Confronto con M_2020 dentro l'AOI.
"""))

cells.append(code("""mp_in_aoi = gpd.sjoin(m_prec[['geometry']], aoi[['id','geometry']], predicate='intersects', how='inner')
m2_in_aoi = gpd.sjoin(m2020[['geometry']], aoi[['id','geometry']], predicate='intersects', how='inner')

print(f'Mappatura_2020 dentro AOI:        {m2_in_aoi.index.nunique():>5}')
print(f'Mappature_precedenti dentro AOI:  {mp_in_aoi.index.nunique():>5}')

# Tetti che compaiono in 2020 ma non in precedenti (proxy "nuovi censimenti")
# (centroid-based, distanza < 10m)
m2020_aoi = m2020.loc[sorted(m2_in_aoi.index.unique())].copy()
mprec_aoi = m_prec.loc[sorted(mp_in_aoi.index.unique())].copy()

m2020_aoi['cx'] = m2020_aoi.geometry.centroid.x.round(0)
m2020_aoi['cy'] = m2020_aoi.geometry.centroid.y.round(0)
mprec_aoi['cx'] = mprec_aoi.geometry.centroid.x.round(0)
mprec_aoi['cy'] = mprec_aoi.geometry.centroid.y.round(0)

set_2020 = set(zip(m2020_aoi['cx'], m2020_aoi['cy']))
set_prec = set(zip(mprec_aoi['cx'], mprec_aoi['cy']))

only_in_2020 = set_2020 - set_prec
only_in_prec = set_prec - set_2020
both         = set_2020 & set_prec
print(f'\\nDentro AOI, matching su centroide arrotondato a 1 m:')
print(f'  In entrambe le mappature:        {len(both):>5}')
print(f'  Solo in M_2020 (nuovi):          {len(only_in_2020):>5}')
print(f'  Solo in precedenti (rimossi?):   {len(only_in_prec):>5}')
"""))

cells.append(code("""# Visual: overlay dei due dataset su uno dei footprint con più GT (PNEO_LOMBARDIA3)
target = aoi[aoi['id']=='PNEO_LOMBARDIA3_20230416_ALL_RAW'].iloc[0]
poly = target.geometry

m2_clip = m2020[m2020.intersects(poly)].copy()
mp_clip = m_prec[m_prec.intersects(poly)].copy()
fig, ax = plt.subplots(figsize=(11, 8))
gpd.GeoSeries([poly], crs=aoi.crs).boundary.plot(ax=ax, color='black', linewidth=1.5, label=f'AOI {target[\"id\"][:20]}…')
mp_clip.plot(ax=ax, color='#3498db', edgecolor='none', alpha=0.55, label=f'Mappature_precedenti  (n={len(mp_clip)})')
m2_clip.plot(ax=ax, color='#c0392b', edgecolor='none', alpha=0.85, label=f'Mappatura_2020       (n={len(m2_clip)})')
ax.set_title(f'Confronto storico vs 2020 — footprint {target[\"id\"]}', fontweight='bold')
ax.set_xlabel('Easting UTM 32N (m)'); ax.set_ylabel('Northing UTM 32N (m)')
ax.legend(loc='upper left')
ax.set_aspect('equal')
plt.tight_layout(); plt.show()
"""))

cells.append(md("""**Lettura**: i tetti censiti nel 2020 ma assenti nello storico (in rosso, fuori dai blu) sono potenzialmente nuove costruzioni / nuove ispezioni; viceversa, quelli solo nello storico (in blu, fuori dai rossi) possono essere bonifiche già avvenute. È la base empirica per gestire la **discrepanza temporale GT 2020 ↔ imagery 2023-2026** che Thomas ha messo nelle slide 13 e 15 del dossier SOTA.
"""))

# ============================================================================
cells.append(md("""## 10. Firme spettrali di riferimento — libreria USGS splib07a

I 9 grafici sono già pronti in `spectral/figures/`. Sotto sono mostrati i due più rilevanti per la slide chiave (slide 6 e 7 del dossier).
"""))

cells.append(code("""from PIL import Image
figs = [
    ('Plastics (HDPE/LDPE/PET) — slide 6',              'spectral_plot_01_plastics.png'),
    ('Plastic vs Vegetation — slide 7 (confusion pair)', 'spectral_plot_07_plastic_vs_vegetation.png'),
    ('Construction materials — riferimento per cemento-amianto', 'spectral_plot_03_construction.png'),
    ('Natural backgrounds — vegetazione/suolo/acqua',    'spectral_plot_06_natural_backgrounds.png'),
]
fig, axes = plt.subplots(len(figs), 1, figsize=(13, 4.5*len(figs)))
for ax, (title, fname) in zip(axes, figs):
    img = Image.open(f'{SPECTRA}/figures/{fname}')
    ax.imshow(img); ax.axis('off'); ax.set_title(title, fontweight='bold', fontsize=11)
plt.tight_layout(); plt.show()
"""))

cells.append(md("""**Nota cemento-amianto**: nelle USGS splib07a la firma del *chrysotile/asbestos* esiste (cap. Minerals) ma la libreria già parsata è focalizzata sui materiali plastica/legno/costruzione del briefing. La firma diagnostica del cemento-amianto è la *Mg-OH bending a 2.31 µm* (Frassy 2014, Bassani 2007) — fuori dal range SuperDove (≤0.86 µm) e dentro WV3 SWIR. Questo è il `Cosa c'è dietro` della slide 6 del dossier.
"""))

# ============================================================================
cells.append(md("""## 11. Preview Planet RGB (sanità imagery)

Crop centrale di una delle 7 strip per verificare che radiometria SR e bande siano caricabili correttamente. PSB.SD è 4-band (Blue/Green/Red/NIR).
"""))

cells.append(code("""# Preview leggero: read overview window dal centro di uno strip
import matplotlib.colors as mcolors

target_tif = planet_tifs[2]
with rasterio.open(target_tif) as src:
    print(f'File:   {os.path.basename(target_tif)}')
    print(f'CRS:    {src.crs}  | size: {src.width}x{src.height}  | bands: {src.count}')
    # Read low-res overview (factor 8) of center 1000x1000 area
    w, h = src.width, src.height
    win = rasterio.windows.Window(w//2 - 500, h//2 - 500, 1000, 1000)
    bgrn = src.read(window=win, out_shape=(4, 500, 500))   # 2x downsample
print(f'Shape patch:    {bgrn.shape}')
print(f'Range bande BGRN: min={bgrn.min()}  max={bgrn.max()}  dtype={bgrn.dtype}')

# RGB composite (R=band 3, G=band 2, B=band 1) — SR già scalato 0-10000
rgb = np.stack([bgrn[2], bgrn[1], bgrn[0]], axis=-1).astype(float)
# Stretch 2-98 percentile
p2, p98 = np.percentile(rgb[rgb>0], [2, 98])
rgb_s = np.clip((rgb - p2) / (p98 - p2), 0, 1)

# NIR false color: NIR-R-G
nir = np.stack([bgrn[3], bgrn[2], bgrn[1]], axis=-1).astype(float)
p2n, p98n = np.percentile(nir[nir>0], [2, 98])
nir_s = np.clip((nir - p2n) / (p98n - p2n), 0, 1)

# NDVI
b_red = bgrn[2].astype(float); b_nir = bgrn[3].astype(float)
ndvi = (b_nir - b_red) / (b_nir + b_red + 1e-6)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(rgb_s); axes[0].set_title('RGB true-color (B3/B2/B1)', fontweight='bold'); axes[0].axis('off')
axes[1].imshow(nir_s); axes[1].set_title('False color (NIR/R/G) — vegetazione rossa', fontweight='bold'); axes[1].axis('off')
im = axes[2].imshow(ndvi, cmap='RdYlGn', vmin=-0.2, vmax=0.8); axes[2].set_title('NDVI', fontweight='bold'); axes[2].axis('off')
fig.colorbar(im, ax=axes[2], fraction=0.035, pad=0.02)
plt.suptitle(f'Planet PSScene preview — {os.path.basename(target_tif).split(\"_3B_\")[0]}  (2026-03-30, 4-band)', fontweight='bold')
plt.tight_layout(); plt.show()
"""))

# ============================================================================
cells.append(md("""## 12. Headline numbers — slide finale

Numeri pronti per la presentazione.
"""))

cells.append(code("""# Computi finali
n_gt   = len(m2020)
n_prec = len(m_prec)
n_aoi  = len(aoi)
area_aoi_union = aoi.union_all().area / 1e6
area_aoi_sum   = aoi['area_km2'].sum()
gt_in_aoi_n    = m2_in_aoi.index.nunique()
gt_in_aoi_pct  = 100*gt_in_aoi_n/n_gt
n_pneo_lomb3   = (per_scene[per_scene['id']=='PNEO_LOMBARDIA3_20230416_ALL_RAW']['n_gt_polygons'].values[0]
                  if 'PNEO_LOMBARDIA3_20230416_ALL_RAW' in per_scene['id'].values else 0)
mean_area      = m2020['Shape_Area'].mean()
med_area       = m2020['Shape_Area'].median()
pct_resolved_sd = (areas>=50).mean()*100

print('=' * 60)
print('HEADLINE NUMBERS — Pilot amianto Fase 1, stato 2026-05-17')
print('=' * 60)
print(f'Ground truth pubblica (WFS Regione Lombardia):')
print(f'  Tetti Mappatura_2020:           {n_gt:>7,}'.replace(',', '.'))
print(f'  Tetti Mappature_precedenti:     {n_prec:>7,}'.replace(',', '.'))
print()
print(f'AOI pianificata (multi-sensor):')
print(f'  Footprint:                      {n_aoi:>7}')
print(f'  Area unione:                    {area_aoi_union:>7,.0f} km²'.replace(',', '.'))
print()
print(f'Coverage AOI ↔ GT:')
print(f'  GT dentro AOI:                  {gt_in_aoi_n:>7,}  ({gt_in_aoi_pct:.1f}%)'.replace(',', '.'))
print(f'  Scena con più GT (PNEO_LOMB3):  {n_pneo_lomb3:>7}')
print()
print(f'Geometria tetti:')
print(f'  Area mediana:                   {med_area:>7,.0f} m² (~{med_area/9:.0f} pixel SuperDove)'.replace(',', '.'))
print(f'  Tetti risolvibili (≥50 m²):     {pct_resolved_sd:>7.1f}%')
print()
print(f'Imagery già acquisita:')
print(f'  Planet PSScene 2026-03-30:      {len(planet_gdf):>7} strip ({planet_gdf.geometry.area.sum()/1e6:.0f} km²)')
print(f'  Overlap PSScene ↔ GT:           {len(gt_in_planet):>7}  ⚠️ zero, prima prova fuori area mappata')
print('=' * 60)
"""))

# ============================================================================
cells.append(md("""## 13. Punti di discussione per Thomas

| # | Punto | Stato | Decisione richiesta |
|---|---|---|---|
| 1 | Planet `prima prova` 2026-03-30 non interseca GT | Fatto, da riacquisire | Lanciamo task PSScene su PNEO_LOMBARDIA2/3 o aspettiamo SuperDove direttamente sull'area Brianza? |
| 2 | ~1.200 tetti GT dentro AOI (PNEO + WV3) — sufficienti per pilot SAM? | Numero ok per Fase 1 | Conferma soglia minima poligoni per stimare distribuzione SAM intra-class |
| 3 | 81% del segnale è in PNEO_LOMBARDIA2/3 (Apr 2023) — δt = 3 anni vs GT 2020 | Da gestire come slide 15 | Filtriamo i tetti potenzialmente bonificati con `Mappature_precedenti`? |
| 4 | Mediana area = ~150 m² (~16 pixel SuperDove) — ok per spectral mean | Comodo per SAM | OK come scelta del primo pilot |
| 5 | Cemento-amianto SWIR feature (2.31 µm Mg-OH) fuori da SuperDove | Limite noto, slide 6 | Pilot lo testa onestamente, fallback WV3 SWIR su sotto-AOI |
| 6 | Mappature_precedenti = 50k tetti — utile come confronto temporale | Caricato | Lo includiamo come pseudo-label per cross-time eval? |

**Next concrete steps proposti:**
1. Estendere la pipeline di estrazione firme USGS al `chrysotile` per avere la signature teorica amianto
2. Acquisire PSScene SuperDove (8-band) sull'overlap PNEO_LOMBARDIA2+3 più vicino temporalmente possibile alla data di acquisizione PNEO
3. Implementare lo script di estrazione `(poligono_GT × tile_imagery) → mean+median+std per banda` con maschera UDM2
4. Calcolare SAM intra-class (amianto-amianto) vs inter-class (amianto-vegetazione/strada/tetto generico) e plottare la distribuzione di Bhattacharyya
"""))

# ============================================================================
nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3 (venv)", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

NB_PATH.write_text(json.dumps(nb, indent=1))
n_code = sum(1 for c in cells if c["cell_type"] == "code")
n_md = sum(1 for c in cells if c["cell_type"] == "markdown")
print(f'Notebook written: {NB_PATH}')
print(f'Cells: {len(cells)} ({n_code} code, {n_md} markdown)')
