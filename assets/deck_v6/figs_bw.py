"""Black & white, standard, clean figures matching the original deck register."""
import sys; from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Rectangle
import numpy as np
NL=chr(10)
ROOT=Path("/home/alepot55/Desktop/uni/Tesi"); SPECDIR=ROOT/"spectral"
OUT=ROOT/"assets"/"deck_v6"/"figs_bw"; OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(SPECDIR))
K="#1A1A1A"; DG="#444444"; MG="#888888"; LG="#CCCCCC"; XLG="#EEEEEE"; W="#FFFFFF"
plt.rcParams.update({"font.family":"sans-serif","font.sans-serif":["Arial","DejaVu Sans"],
 "font.size":12,"axes.titlesize":14,"axes.titleweight":"bold","axes.edgecolor":K,
 "text.color":K,"axes.labelcolor":K,"xtick.color":K,"ytick.color":K,
 "figure.facecolor":W,"savefig.facecolor":W,"savefig.dpi":300,"savefig.bbox":"tight"})
def foot(fig,t): fig.text(0.995,0.012,t,ha="right",va="bottom",fontsize=8.5,style="italic",color=MG)
def noax(ax): ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis("off")
def rbox(ax,x,y,w,h,fc=W,ec=K,lw=1.4):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=2))
def arr(ax,x0,y0,x1,y1,lw=1.6):
    ax.add_patch(FancyArrowPatch((x0,y0),(x1,y1),arrowstyle="-|>",mutation_scale=13,lw=lw,color=K,zorder=3))

# 1. SWIR bottleneck (B/N, linestyle-coded)
from spectral_plots.data import load_spectrum
from spectral_plots import config
ZIP=SPECDIR/"data"/"ASCIIdata_splib07a.zip"
styles=[("Chrysotile (asbestos)","Asbestos-cement",K,"-",2.4),
        ("Concrete (road)","Concrete / C&D",DG,"--",2.0),
        ("HDPE (white opaque)","Plastic (HDPE)",MG,":",2.4)]
fig,ax=plt.subplots(figsize=(9.6,4.7))
for nm,lab,col,ls,lw in styles:
    fp,wt,_=config.SPECTRA[nm]; wl,r=load_spectrum(ZIP,fp,wt)
    wl=wl*1000.0 if np.nanmax(wl)<100 else wl
    m=~np.isnan(r)&(r>-1.0)&(wl>=2000)&(wl<=2500)
    ax.plot(wl[m],r[m],color=col,ls=ls,lw=lw,label=lab)
for b in [2160,2200,2260,2330]:
    ax.axvspan(b-15,b+15,color=XLG,zorder=0); ax.axvline(b,color=LG,lw=0.7,ls=":",zorder=1)
ax.axvspan(2300,2350,facecolor="none",edgecolor=K,hatch="////",lw=0,zorder=1,alpha=0.5)
ax.annotate("Mg-OH ~2.30-2.33 um (asbestos)",xy=(2330,0.66),xytext=(2080,0.50),
    fontsize=9.5,color=K,fontweight="bold",arrowprops=dict(arrowstyle="->",color=K,lw=1.2))
ax.set_xlabel("Wavelength (nm)"); ax.set_ylabel("Reflectance"); ax.set_xlim(2000,2500)
ax.set_title("SWIR-8 bottleneck: three hazards crowd into one WV-3 band",pad=8)
ax.legend(loc="lower left",frameon=True,fontsize=9.5,edgecolor=LG)
for s in ("top","right"): ax.spines[s].set_visible(False)
ax.grid(alpha=0.25,color=LG)
ax.text(0.99,0.03,"USGS splib07a (Kokaly et al., 2017) · grey bands = WV-3 SWIR centres (Maxar)",transform=ax.transAxes,ha="right",va="bottom",fontsize=8,style="italic",color=MG)
fig.savefig(OUT/"swir8_bottleneck.png"); plt.close(fig)

# 2. 3-axis ablation cube (B/N)
fig,ax=plt.subplots(figsize=(9.6,4.6)); noax(ax)
rungs=["R0 RGB","R1 +RedEdge/NIR","R2 full VNIR","R3 +SWIR"]
fills=[XLG,LG,MG,K]; tcol=[K,K,W,W]; x0=6
for i,(rg,fc,tc) in enumerate(zip(rungs,fills,tcol)):
    rbox(ax,x0+i*22.5,62,20,13,fc=fc,ec=K)
    ax.text(x0+i*22.5+10,68.5,rg,ha="center",va="center",fontsize=10,fontweight="bold",color=tc)
    if i<3: arr(ax,x0+i*22.5+20,68.5,x0+(i+1)*22.5,68.5)
ax.text(2,68.5,"A",ha="center",va="center",fontsize=13,fontweight="bold",bbox=dict(boxstyle="circle,pad=0.3",fc=W,ec=K))
ax.text(6,79,"Axis A — spectral content (R3 = WV-3 only; the headline test)",fontsize=9.5,color=DG)
rbox(ax,6,40,42,12); ax.text(27,46,"WorldView-3  (VNIR + SWIR)",ha="center",va="center",fontsize=10,fontweight="bold")
rbox(ax,54,40,42,12); ax.text(75,46,"Pleiades Neo  (VNIR-only)",ha="center",va="center",fontsize=10,fontweight="bold")
ax.text(2,46,"B",ha="center",va="center",fontsize=13,fontweight="bold",bbox=dict(boxstyle="circle,pad=0.3",fc=W,ec=K))
ax.text(6,55,"Axis B — sensor (same physical sites)",fontsize=9.5,color=DG)
rbox(ax,6,20,42,12,fc=XLG); ax.text(27,26,"native bands",ha="center",va="center",fontsize=10,fontweight="bold")
rbox(ax,54,20,42,12,fc=XLG); ax.text(75,26,"pansharpened",ha="center",va="center",fontsize=10,fontweight="bold")
ax.text(2,26,"C",ha="center",va="center",fontsize=13,fontweight="bold",bbox=dict(boxstyle="circle,pad=0.3",fc=W,ec=K))
ax.text(6,35,"Axis C — resolution control (\"SWIR helps\" must hold in native, not only after pan)",fontsize=9.5,color=DG)
ax.text(50,9,"Same DOFA backbone · Swin-RSP = RGB reference · per-pixel AND full-CNN  ->  B-A = pure chemistry gain, D-C = total MS gain",
    ha="center",fontsize=9,color=K,bbox=dict(boxstyle="round,pad=0.4",fc=W,ec=K,lw=0.9))
foot(fig,"Design: loop_prof_sota/04_experimental_design.md")
fig.savefig(OUT/"ablation_cube.png"); plt.close(fig)

# 3. band -> material (B/N greyscale grid)
mats=["Asbestos"+NL+"(Mg-OH)","Plastics"+NL+"(C-H)","Concrete/C&D"+NL+"(carbonate)","Slag/rust"+NL+"(Fe-oxide)","AC weathering"+NL+"(moss/lichen)"]
feats=["RGB","Red"+NL+"Edge","NIR","SWIR"+NL+"1.2um","SWIR"+NL+"1.73um","SWIR"+NL+"2.2um","SWIR"+NL+"2.33um"]
M=np.array([[0,0,0,0,0,1,2],[0,0,0,2,2,1,1],[0,0,0,0,0,2,2],[0,1,2,0,0,0,0],[0,2,1,0,0,0,0]])
fig,ax=plt.subplots(figsize=(9.6,4.8)); cmap={0:W,1:LG,2:DG}; nr,nc=5,7
for i in range(nr):
    for j in range(nc):
        v=M[i,j]; ax.add_patch(Rectangle((j,nr-1-i),1,1,fc=cmap[v],ec=K,lw=1.0))
        if v==2: ax.text(j+0.5,nr-1-i+0.5,"strong",ha="center",va="center",color=W,fontsize=7.5,fontweight="bold")
        elif v==1: ax.text(j+0.5,nr-1-i+0.5,"weak",ha="center",va="center",color=K,fontsize=7.5)
ax.axvline(3,color=K,lw=2.0,ls="--")
ax.text(1.5,nr+0.28,"Pleiades Neo (VNIR-only)",ha="center",fontsize=10,fontweight="bold",color=K)
ax.text(5,nr+0.28,"WorldView-3 adds SWIR",ha="center",fontsize=10,fontweight="bold",color=K)
ax.set_xlim(0,nc); ax.set_ylim(0,nr+0.85); ax.set_xticks(np.arange(nc)+0.5); ax.set_xticklabels(feats,fontsize=9)
ax.set_yticks(np.arange(nr)+0.5); ax.set_yticklabels(mats[::-1],fontsize=9); ax.tick_params(length=0)
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_title("Where each hazard becomes separable: diagnostic feature to band",pad=22)
foot(fig,"USGS splib07a · Aguilar 2021/2025 · Cilia 2015")
fig.savefig(OUT/"band_material_map.png",bbox_inches="tight"); plt.close(fig)

# 4. pilot workflow (B/N)
fig,ax=plt.subplots(figsize=(9.6,4.7)); noax(ax)
boxes=[(4,70,"WFS Mappatura_2020"+NL+"10,903 roofs (EPSG:32632)"),
       (37,70,"Self-pair on WV-3 + PNeo"+NL+"to surface reflectance"),
       (70,70,"Per-roof spectral"+NL+"signature"),
       (4,42,"(A) Unsupervised"+NL+"clustering (no labels)"),
       (37,42,"DECISION GATE:"+NL+"clusters form only"+NL+"with SWIR?"),
       (70,42,"(B) Supervised"+NL+"RGB / VNIR / VNIR+SWIR")]
Wd,Hd=27,18
for x,y,t in boxes:
    rbox(ax,x,y,Wd,Hd,fc=(XLG if "GATE" in t else W),ec=K,lw=(2.2 if "GATE" in t else 1.4))
    ax.text(x+Wd/2,y+Hd/2,t,ha="center",va="center",fontsize=9,color=K,fontweight=("bold" if "GATE" in t else "normal"))
rbox(ax,30,14,48,12,fc=W,ec=K,lw=1.8)
ax.text(54,20,"EWC 17 06 05*  ->  risk tier  ->  ARPA priority",ha="center",va="center",fontsize=9.5,fontweight="bold")
arr(ax,31,79,37,79); arr(ax,64,79,70,79); arr(ax,17.5,70,17.5,60); arr(ax,50.5,42,54,26)
ax.text(50,34,"Public pixel-accurate labels · textbook SWIR diagnostic · de-risks the pipeline before AerialWaste coordinates arrive",
    ha="center",fontsize=8.6,color=DG)
foot(fig,"GT: Lombardia WFS Mappatura_2020 · physics: chrysotile Mg-OH 2.30-2.33um (splib07a)")
fig.savefig(OUT/"pilot_workflow.png"); plt.close(fig)
print("BW figs:",len(list(OUT.glob('*.png'))))
