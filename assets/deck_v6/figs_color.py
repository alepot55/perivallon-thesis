"""Colored, polished deck figures. Palette validated with the dataviz skill:
materials  asbestos #9B3D6F · concrete #2a78d6 · plastic #eb6834   (all PASS)
sensors    WV-3 #2a78d6 · PNeo #eb6834 · SuperDove #eda100 (+grey context)
sequential blue ramp #86b6ef → #3987e5 → #1c5cab (ordinal-safe steps)
No embedded titles (slide titles carry them)."""
import sys; from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import numpy as np
NL=chr(10)
ROOT=Path("/home/alepot55/Desktop/uni/Tesi"); SPECDIR=ROOT/"spectral"
OUT=ROOT/"assets"/"deck_v6"/"figs_color"; OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(SPECDIR))
INK="#1A1A1A"; MUT="#52514e"; GRID="#E8E8E8"; MG="#8A8A8A"
ASB="#9B3D6F"; CON="#2a78d6"; PLA="#eb6834"
WV3="#2a78d6"; PNEO="#eb6834"; SDV="#eda100"; CTX1="#999999"; CTX2="#666666"
SEQ=["#86b6ef","#3987e5","#1c5cab"]
plt.rcParams.update({"font.family":"sans-serif","font.sans-serif":["Arial","DejaVu Sans"],
 "font.size":12,"text.color":INK,"axes.labelcolor":INK,"xtick.color":INK,"ytick.color":INK,
 "axes.edgecolor":INK,"figure.facecolor":"white","savefig.facecolor":"white",
 "savefig.dpi":300,"savefig.bbox":"tight"})

from spectral_plots.data import load_spectrum
from spectral_plots import config
ZIP=SPECDIR/"data"/"ASCIIdata_splib07a.zip"

# 1 ── SWIR-8 bottleneck ──────────────────────────────────────────────
mats=[("Chrysotile (asbestos)","Asbestos-cement",ASB,"-",2.6),
      ("Concrete (road)","Concrete / C&D",CON,"--",2.2),
      ("HDPE (white opaque)","Plastic (HDPE)",PLA,":",2.6)]
fig,ax=plt.subplots(figsize=(9.6,4.7))
ends={}
for nm,lab,col,ls,lw in mats:
    fp,wt,_=config.SPECTRA[nm]; wl,r=load_spectrum(ZIP,fp,wt)
    wl=wl*1000.0 if np.nanmax(wl)<100 else wl
    m=~np.isnan(r)&(r>-1.0)&(wl>=2000)&(wl<=2500)
    ax.plot(wl[m],r[m],color=col,ls=ls,lw=lw,label=lab)
    ends[lab]=(wl[m][-1],r[m][-1],col)
for b in [2160,2200,2260,2330]:
    ax.axvspan(b-15,b+15,color=CON,alpha=0.07,zorder=0); ax.axvline(b,color=CON,lw=0.7,ls=":",alpha=0.5,zorder=1)
ax.axvspan(2300,2350,color=ASB,alpha=0.12,zorder=0)
ax.annotate("Mg-OH 2.30-2.33 um"+NL+"(asbestos diagnostic)",xy=(2328,0.665),xytext=(2075,0.50),
    fontsize=10,color=ASB,fontweight="bold",
    arrowprops=dict(arrowstyle="->",color=ASB,lw=1.3))
for lab,(x,y,col) in ends.items():
    ax.annotate(lab,xy=(x,y),xytext=(6,0),textcoords="offset points",fontsize=9.5,
                color=col,fontweight="bold",va="center")
ax.set_xlim(2000,2560); ax.set_xlabel("Wavelength (nm)"); ax.set_ylabel("Reflectance")
for sp in ("top","right"): ax.spines[sp].set_visible(False)
ax.grid(alpha=0.35,color=GRID)
ax.text(0.012,0.05,"shaded verticals = WV-3 SWIR band centres",transform=ax.transAxes,
        fontsize=8.5,style="italic",color=MUT)
fig.savefig(OUT/"swir8_bottleneck.png"); plt.close(fig)

# 2 ── band -> material map (ordinal blue ramp) ───────────────────────
rows=["Asbestos"+NL+"(Mg-OH)","Plastics"+NL+"(C-H)","Concrete/C&D"+NL+"(carbonate)","Slag/rust"+NL+"(Fe-oxide)","AC weathering"+NL+"(moss/lichen)"]
cols=["RGB","Red"+NL+"Edge","NIR","SWIR"+NL+"1.2um","SWIR"+NL+"1.73um","SWIR"+NL+"2.2um","SWIR"+NL+"2.33um"]
M=np.array([[0,0,0,0,0,1,2],[0,0,0,2,2,1,1],[0,0,0,0,0,2,2],[0,1,2,0,0,0,0],[0,2,1,0,0,0,0]])
fig,ax=plt.subplots(figsize=(9.6,4.8))
cmap={0:"#F2F2F2",1:SEQ[0],2:SEQ[2]}; nr,nc=5,7
for i in range(nr):
    for j in range(nc):
        v=M[i,j]; ax.add_patch(Rectangle((j,nr-1-i),1,1,fc=cmap[v],ec="white",lw=2.5))
        if v==2: ax.text(j+0.5,nr-1-i+0.5,"strong",ha="center",va="center",color="white",fontsize=8,fontweight="bold")
        elif v==1: ax.text(j+0.5,nr-1-i+0.5,"weak",ha="center",va="center",color="#0d366b",fontsize=8)
ax.axvline(3,color=INK,lw=1.8,ls="--")
ax.text(1.5,nr+0.28,"Pleiades Neo (VNIR-only)",ha="center",fontsize=10.5,fontweight="bold",color=PNEO)
ax.text(5,nr+0.28,"WorldView-3 adds SWIR",ha="center",fontsize=10.5,fontweight="bold",color=WV3)
ax.set_xlim(0,nc); ax.set_ylim(0,nr+0.85)
ax.set_xticks(np.arange(nc)+0.5); ax.set_xticklabels(cols,fontsize=9)
ax.set_yticks(np.arange(nr)+0.5); ax.set_yticklabels(rows[::-1],fontsize=9.5)
ax.tick_params(length=0)
for sp in ax.spines.values(): sp.set_visible(False)
fig.savefig(OUT/"band_material_map.png",bbox_inches="tight"); plt.close(fig)

# 3 ── sensor radar (thesis pair emphasised) ──────────────────────────
sensors=[("WorldView-3",[1/1.24,np.log10(16),1/3.0],WV3,"-",2.8,"^",0.10),
         ("Pleiades Neo",[1/1.2,np.log10(6),1/2.0],PNEO,"-",2.8,"o",0.10),
         ("SuperDove",[1/3.0,np.log10(8),1/0.5],SDV,"-",1.6,"s",0.0),
         ("Sentinel-2",[1/10.0,np.log10(13),1/5.0],CTX1,"--",1.4,"D",0.0),
         ("EnMAP",[1/30.0,np.log10(228),1/27.0],CTX2,":",1.6,"v",0.0)]
vals=np.array([x[1] for x in sensors],float); norm=vals/vals.max(axis=0)
N=3; ang=np.linspace(0,2*np.pi,N,endpoint=False).tolist(); ang+=ang[:1]
fig=plt.figure(figsize=(7.0,6.2)); ax=plt.subplot(111,polar=True)
ax.set_theta_offset(np.pi/2); ax.set_theta_direction(-1)
ax.set_xticks(ang[:-1]); ax.set_xticklabels(["Spatial"+NL+"(1/GSD)","Spectral"+NL+"bands","Revisit"+NL+"(1/days)"],fontsize=11.5,fontweight="bold")
ax.set_ylim(0,1.05); ax.set_yticklabels([]); ax.grid(color="#E3E3E3")
ax.spines["polar"].set_color("#CCCCCC")
for (name,_,col,ls,lw,mk,fa),nv in zip(sensors,norm):
    d=nv.tolist()+[nv.tolist()[0]]
    ax.plot(ang,d,color=col,ls=ls,lw=lw,marker=mk,ms=7,label=name)
    if fa: ax.fill(ang,d,color=col,alpha=fa)
leg=ax.legend(loc="upper right",bbox_to_anchor=(1.40,1.10),fontsize=9.5,frameon=True,edgecolor="#CCCCCC")
fig.text(0.5,0.015,"Outer ring = better. Spatial 1/GSD (log) - bands log10(N) - revisit 1/days (log). Thesis pair emphasised.",
    ha="center",fontsize=8.5,style="italic",color=MUT)
fig.savefig(OUT/"sensor_radar.png",bbox_inches="tight"); plt.close(fig)

# 4 ── Aguilar bars (ordinal magnitude ramp) ──────────────────────────
fig,ax=plt.subplots(figsize=(7.4,4.4))
vals=[90.85,96.79,97.38]; labs=["VNIR only"+NL+"(8 bands)","SWIR only"+NL+"(8 bands)","All features"+NL+"(16 bands)"]
bars=ax.bar(labs,vals,color=SEQ,edgecolor="white",lw=1.0,width=0.58)
for b,v,c in zip(bars,vals,["#0d366b","white","white"]):
    ax.text(b.get_x()+b.get_width()/2,v-0.55,"%.2f%%"%v,ha="center",va="top",fontsize=11.5,fontweight="bold",
            color=c)
ax.annotate("+5.94 pp (SWIR > VNIR)",xy=(0.95,96.5),xytext=(0.02,98.6),fontsize=9.5,color=INK,
    arrowprops=dict(arrowstyle="->",color=INK,lw=1.0))
ax.annotate("+0.59 pp (All > SWIR)",xy=(2.0,97.9),xytext=(1.62,99.3),fontsize=9.5,color=INK)
ax.set_ylim(85,100.6); ax.set_ylabel("Overall accuracy (%)")
for sp in ("top","right"): ax.spines[sp].set_visible(False)
ax.grid(axis="y",alpha=0.4,color=GRID)
fig.savefig(OUT/"aguilar_bars.png"); plt.close(fig)

# 5 ── bands plateau ──────────────────────────────────────────────────
fig,ax=plt.subplots(figsize=(8.6,4.2))
nb=[3,4,5,7,10,20,50,100,250,500,768]
oa=[85.0,92.0,95.0,95.5,95.8,96.0,96.0,96.0,96.0,96.1,96.2]
ax.semilogx(nb,oa,color=CON,lw=2.2,marker="o",ms=5,label="C&D waste, narrowband selection (Vitek 2025)")
ax.plot([8,8,16],[90.85,96.79,97.38],marker="s",ms=8,color=PLA,ls="none",label="WV-3 band ablation (Aguilar 2021)")
ax.annotate("VNIR only 90.85%",xy=(8,90.85),xytext=(12.5,89.8),fontsize=9,color=PLA,fontweight="bold")
ax.annotate("SWIR only 96.79%",xy=(8,96.79),xytext=(3.2,98.3),fontsize=9,color=PLA,fontweight="bold")
ax.annotate("All 16: 97.38%",xy=(16,97.38),xytext=(25,98.3),fontsize=9,color=PLA,fontweight="bold")
ax.annotate("plateau ~96% from ~5 well-chosen bands",xy=(50,96.0),xytext=(85,92.4),fontsize=9.5,
    color="#0d366b",fontweight="bold",arrowprops=dict(arrowstyle="->",color="#0d366b",lw=1.1))
ax.set_xlabel("Number of spectral bands (log scale)"); ax.set_ylabel("Overall accuracy (%)")
ax.set_ylim(84,100)
ax.legend(loc="lower right",frameon=True,fontsize=8.5,edgecolor="#CCCCCC")
for sp in ("top","right"): ax.spines[sp].set_visible(False)
ax.grid(alpha=0.4,color=GRID)
fig.savefig(OUT/"bands_plateau.png"); plt.close(fig)
print("color figs:",len(list(OUT.glob('*.png'))))

# 6 ── evidence timeline: the field is moving 2023-2026 ────────────────
# (year, GSD m, input, label, material-level?, ox pt, oy pt, ha) — verified from papers/notes
W=[(2015,3.0,"HSI","Cilia (MIVIS)",True,0,-11,"center"),
   (2021,1.24,"MS","Aguilar (WV-3)",True,0,-11,"center"),
   (2022,10.0,"MS","MARIDA (S-2)",True,0,-11,"center"),
   (2023,0.30,"RGB","AerialWaste",False,-9,9,"right"),
   (2023,0.60,"RGB","Sun, 28 cities",False,-9,-9,"right"),
   (2024,0.50,"RGB","CascadeDumpNet",False,11,-3,"left"),
   (2024,0.70,"RGB","CWLD",False,11,-11,"left"),
   (2024,0.30,"RGB","Disaitek (PNeo)",False,11,6,"left"),
   (2024,0.15,"RGB","Abbasi, asbestos",True,0,11,"center"),
   (2025,30.0,"HSI","Shepherd (EnMAP)",True,11,0,"left"),
   (2025,60.0,"HSI","EMIT, plastics",True,11,0,"left"),
   (2025,3.7,"MS","Aguilar (WV-3 SWIR)",True,-9,-10,"right"),
   (2026,1.24,"MS","Saba (WV-3)",True,-2,11,"center"),
   (2026.25,1.35,"MS","Bonifazi (WV-3)",True,4,-12,"center")]
COLI={"RGB":"#999999","MS":WV3,"HSI":ASB}
fig,ax=plt.subplots(figsize=(9.8,4.9))
ax.axhspan(5,100,color="#F2F2F2",zorder=0)
ax.text(2015.0,40,"coarser than the task (>5 m GSD)",fontsize=8.5,style="italic",color=MUT)
ax.axvspan(2023.5,2026.6,color=WV3,alpha=0.045,zorder=0)
for yr,g,inp,lab,mat,ox,oy,ha in W:
    mk="^" if mat else "o"
    fc=COLI[inp] if mat else "white"
    ax.plot([yr],[g],marker=mk,ms=9,mec=COLI[inp],mfc=fc,mew=1.8,ls="none",zorder=3)
    va="bottom" if oy>0 else ("top" if oy<0 else "center")
    ax.annotate(lab,xy=(yr,g),xytext=(ox,oy),textcoords="offset points",
                fontsize=8.2,color=COLI[inp],ha=ha,va=va,fontweight="bold")
ax.set_yscale("log"); ax.set_ylim(100,0.08)
ax.set_yticks([0.1,0.3,1,3,10,30,60]); ax.set_yticklabels(["0.1","0.3","1","3","10","30","60"])
ax.set_xlim(2014.4,2027.4); ax.set_xticks([2015,2017,2019,2021,2023,2024,2025,2026])
ax.set_xlabel("Year"); ax.set_ylabel("GSD (m, log)  -  finer resolution up")
from matplotlib.lines import Line2D
leg=[Line2D([0],[0],marker="^",ls="none",mec=WV3,mfc=WV3,ms=9,label="material-level"),
     Line2D([0],[0],marker="o",ls="none",mec="#777777",mfc="white",ms=9,label="site-level"),
     Line2D([0],[0],marker="s",ls="none",mec="#999999",mfc="#999999",ms=8,label="RGB"),
     Line2D([0],[0],marker="s",ls="none",mec=WV3,mfc=WV3,ms=8,label="Multispectral"),
     Line2D([0],[0],marker="s",ls="none",mec=ASB,mfc=ASB,ms=8,label="Hyperspectral")]
ax.legend(handles=leg,loc="upper left",bbox_to_anchor=(0.005,0.99),frameon=True,fontsize=8.5,
          edgecolor="#CCCCCC",ncol=2)
for sp in ("top","right"): ax.spines[sp].set_visible(False)
ax.grid(alpha=0.3,color=GRID)
fig.savefig(OUT/"evidence_timeline.png"); plt.close(fig)
print("timeline v2 done")
