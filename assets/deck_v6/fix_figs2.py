import sys; from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
NL=chr(10)
ROOT=Path("/home/alepot55/Desktop/uni/Tesi"); SPECDIR=ROOT/"spectral"
OUT=ROOT/"assets"/"deck_v6"/"figs"; sys.path.insert(0,str(SPECDIR))
C={"asbestos":"#9B3D6F","teal":"#2E8B8B","teal_dk":"#1F6F6F","accent":"#E07A3F",
   "ink":"#222222","grey":"#888888","gold":"#C9A227","vnir":"#D6EAF1","swir":"#F5E6D3"}
plt.rcParams.update({"font.family":"sans-serif","font.sans-serif":["Helvetica","Arial","DejaVu Sans"],
    "font.size":12,"axes.titlesize":14,"axes.titleweight":"bold","figure.facecolor":"white",
    "savefig.facecolor":"white","savefig.dpi":300,"savefig.bbox":"tight"})

from spectral_plots.data import load_spectrum
from spectral_plots import config
ZIP=SPECDIR/"data"/"ASCIIdata_splib07a.zip"

# ── where_info_lives (NEW: WV-3 reaches SWIR, PNeo stops at NIR) ──
fp,wt,_=config.SPECTRA["Chrysotile (asbestos)"]; wl,r=load_spectrum(ZIP,fp,wt)
wl = wl*1000.0 if np.nanmax(wl)<100 else wl
m=~np.isnan(r)&(r>-1.0)&(wl>=400)&(wl<=2500)
fig,ax=plt.subplots(figsize=(11,5.3))
ax.axvspan(400,1000,color=C["vnir"],alpha=0.5,zorder=0)
ax.axvspan(1000,2500,color=C["swir"],alpha=0.5,zorder=0)
ax.plot(wl[m],r[m],color=C["asbestos"],lw=2.3,label="Asbestos-cement (chrysotile)",zorder=4)
wv3_vnir=[425,480,545,605,660,725,833,950]
wv3_swir=[1210,1570,1660,1730,2160,2200,2260,2330]
pneo=[425,483,562,655,725,840]
ymax=np.nanmax(r[m])
for b in wv3_vnir+wv3_swir:
    ax.axvline(b,color=C["teal"],lw=1.0,ymax=0.93,zorder=2)
for b in pneo:
    ax.plot([b],[ymax*1.02],marker="v",color=C["accent"],ms=7,zorder=5)
ax.axvline(1000,color=C["accent"],lw=2.2,ls="--",zorder=3)
ax.annotate("Pléiades Neo stops here"+NL+"(VNIR-only, up to NIR)",xy=(1000,ymax*0.55),
    xytext=(1080,ymax*0.30),fontsize=9.5,color=C["accent"],fontweight="bold",
    arrowprops=dict(arrowstyle="->",color=C["accent"],lw=1.3))
ax.axvspan(2300,2350,color=C["asbestos"],alpha=0.18,zorder=1)
ax.annotate("Mg-OH ~2.3 µm — WV-3 SWIR reaches"+NL+"the asbestos chemistry",
    xy=(2330,r[m][np.argmin(np.abs(wl[m]-2330))]),xytext=(1500,ymax*0.18),
    fontsize=9.5,color=C["asbestos"],fontweight="bold",
    arrowprops=dict(arrowstyle="->",color=C["asbestos"],lw=1.3))
ax.text(700,ymax*1.12,"VNIR",fontsize=11,color=C["teal_dk"],fontweight="bold",ha="center")
ax.text(1750,ymax*1.12,"SWIR (chemistry)",fontsize=11,color=C["gold"],fontweight="bold",ha="center")
ax.text(0.012,0.96,"|  WV-3 bands (16)      ▼ Pléiades Neo bands (6)",transform=ax.transAxes,
    fontsize=9,color=C["ink"],va="top")
ax.set_xlim(400,2500); ax.set_ylim(0,ymax*1.20)
ax.set_xlabel("Wavelength (nm)"); ax.set_ylabel("Reflectance")
ax.set_title("Where the diagnostic information lives — and which sensor reaches it")
for s in ("top","right"): ax.spines[s].set_visible(False)
ax.grid(alpha=0.18)
fig.text(0.995,0.012,"USGS splib07a (Kokaly et al., 2017) · band centres: Maxar WV-3 · Airbus Pléiades Neo",
    ha="right",fontsize=8.5,style="italic",color="#8A8A8A")
fig.savefig(OUT/"where_info_lives.png"); plt.close(fig)

# ── sensor_radar (NEW: WV-3 + Pléiades Neo prominent) ──
sensors=[
 ("WorldView-3",   [1/1.24, np.log10(16), 1/3.0],  C["teal"],   "^"),
 ("Pléiades Neo",  [1/1.2,  np.log10(6),  1/2.0],  C["accent"], "o"),
 ("SuperDove",     [1/3.0,  np.log10(8),  1/0.5],  C["gold"],   "s"),
 ("Sentinel-2",    [1/10.0, np.log10(13), 1/5.0],  "#777777",   "D"),
 ("EnMAP",         [1/30.0, np.log10(228),1/27.0], C["asbestos"],"v"),
]
axes_lab=["Spatial\n(1/GSD)","Spectral\nbands","Revisit\n(1/days)"]
# normalize each axis to [0,1] by max
vals=np.array([s[1] for s in sensors],float)
norm=vals/vals.max(axis=0)
N=3; ang=np.linspace(0,2*np.pi,N,endpoint=False).tolist(); ang+=ang[:1]
fig=plt.figure(figsize=(8.2,7.4)); ax=plt.subplot(111,polar=True)
ax.set_theta_offset(np.pi/2); ax.set_theta_direction(-1)
ax.set_xticks(ang[:-1]); ax.set_xticklabels(axes_lab,fontsize=12,fontweight="bold")
ax.set_ylim(0,1.05); ax.set_yticklabels([]); ax.grid(color="#DDDDDD")
for (name,_,col,mk),nv in zip(sensors,norm):
    d=nv.tolist()+[nv.tolist()[0]]
    lw=2.6 if name in ("WorldView-3","Pléiades Neo") else 1.4
    al=0.16 if name in ("WorldView-3","Pléiades Neo") else 0.05
    ax.plot(ang,d,color=col,lw=lw,marker=mk,ms=7,label=name)
    ax.fill(ang,d,color=col,alpha=al)
ax.legend(loc="upper right",bbox_to_anchor=(1.32,1.12),fontsize=10,frameon=True)
ax.set_title("The sensor trade-off: spatial × spectral × revisit",pad=26,fontsize=14)
fig.text(0.5,0.02,"Outer ring = better. The thesis pair (WV-3, Pléiades Neo) emphasised. Specs: Maxar · Airbus · Planet · ESA · DLR.",
    ha="center",fontsize=8.8,style="italic",color="#8A8A8A")
fig.savefig(OUT/"sensor_radar.png",bbox_inches="tight"); plt.close(fig)
print("where_info_lives + sensor_radar rebuilt")
