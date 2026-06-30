import sys
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
NL = chr(10)
ROOT = Path("/home/alepot55/Desktop/uni/Tesi"); SPECDIR = ROOT/"spectral"
OUT = ROOT/"assets"/"deck_v6"/"figs"; sys.path.insert(0, str(SPECDIR))
C = {"plastic":"#E07A3F","concrete":"#555555","asbestos":"#9B3D6F","teal":"#2E8B8B",
     "teal_dk":"#1F6F6F","teal_lt":"#A6CFCF","accent":"#E07A3F","ink":"#222222",
     "grey":"#888888","gold":"#C9A227","no":"#C0392B"}
plt.rcParams.update({"font.family":"sans-serif","font.sans-serif":["Helvetica","Arial","DejaVu Sans"],
    "font.size":12,"axes.titlesize":14,"axes.titleweight":"bold","figure.facecolor":"white",
    "savefig.facecolor":"white","savefig.dpi":300,"savefig.bbox":"tight"})
def rbox(ax,x,y,w,h,fc,ec,lw=1.4,rad=0.04,z=2):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=%s"%rad,
        fc=fc,ec=ec,lw=lw,zorder=z,mutation_aspect=1))
def arrow(ax,x0,y0,x1,y1,color=C["ink"],lw=2.0,ms=13):
    ax.add_patch(FancyArrowPatch((x0,y0),(x1,y1),arrowstyle="-|>",mutation_scale=ms,lw=lw,color=color,zorder=3))
def noax(ax): ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis("off")
def footer(fig,t): fig.text(0.995,0.012,t,ha="right",va="bottom",fontsize=8.5,style="italic",color="#8A8A8A")

# SWIR bottleneck
from spectral_plots.data import load_spectrum
from spectral_plots import config
ZIP = SPECDIR/"data"/"ASCIIdata_splib07a.zip"
fig,ax=plt.subplots(figsize=(11,5.2))
for nm,col,lab in [("Chrysotile (asbestos)",C["asbestos"],"Asbestos-cement (chrysotile)"),
                   ("Concrete (road)",C["concrete"],"Concrete / C&D"),
                   ("HDPE (white opaque)",C["plastic"],"Plastic (HDPE)")]:
    fp,wt,_=config.SPECTRA[nm]; wl,r=load_spectrum(ZIP,fp,wt)
    wl = wl*1000.0 if np.nanmax(wl)<100 else wl
    m=~np.isnan(r)&(r>-1.0)&(wl>=2000)&(wl<=2500); ax.plot(wl[m],r[m],color=col,lw=2.2,label=lab)
for b in [2160,2200,2260,2330]:
    ax.axvspan(b-18,b+18,color=C["teal"],alpha=0.10,zorder=0); ax.axvline(b,color=C["teal_dk"],lw=0.7,ls=":",zorder=1)
ax.axvspan(2300,2350,color=C["asbestos"],alpha=0.12,zorder=0)
ax.annotate("Mg-OH ~2.30-2.33 um"+NL+"(asbestos diagnostic)",xy=(2330,0.66),xytext=(2120,0.50),
    fontsize=9.5,color=C["asbestos"],fontweight="bold",arrowprops=dict(arrowstyle="->",color=C["asbestos"],lw=1.2))
ax.set_xlabel("Wavelength (nm)"); ax.set_ylabel("Reflectance"); ax.set_xlim(2000,2500)
ax.set_title("The SWIR-8 bottleneck: three hazards crowd into one WV-3 band",pad=10)
ax.legend(loc="lower left",frameon=True,fontsize=9.5)
ax.text(0.5,-0.20,"asbestos 2.32 . concrete 2.34 . plastic 2.31 - all inside WV-3 SWIR-7 (~2.33 um); discrimination leans on shoulders + VNIR shape",
    transform=ax.transAxes,ha="center",fontsize=9,color=C["ink"],bbox=dict(boxstyle="round,pad=0.35",fc="#FFF8F0",ec=C["accent"],lw=0.9))
for sp in ("top","right"): ax.spines[sp].set_visible(False)
ax.grid(alpha=0.22); footer(fig,"USGS splib07a (Kokaly et al., 2017) . WV-3 SWIR band centres: Maxar")
fig.savefig(OUT/"swir8_bottleneck.png"); plt.close(fig)

# band->material map
mats=["Asbestos"+NL+"(Mg-OH)","Plastics"+NL+"(C-H)","Concrete/C&D"+NL+"(carbonate)","Slag/rust"+NL+"(Fe-oxide)","AC weathering"+NL+"(moss/lichen)"]
feats=["RGB","Red"+NL+"Edge","NIR","SWIR"+NL+"1.2um","SWIR"+NL+"1.73um","SWIR"+NL+"2.2um","SWIR"+NL+"2.33um"]
M=np.array([[0,0,0,0,0,1,2],[0,0,0,2,2,1,1],[0,0,0,0,0,2,2],[0,1,2,0,0,0,0],[0,2,1,0,0,0,0]])
fig,ax=plt.subplots(figsize=(11,5.4)); cmap={0:"#F2F2F2",1:C["teal_lt"],2:C["teal"]}; nr,nc=5,7
for i in range(nr):
    for j in range(nc):
        v=M[i,j]; ax.add_patch(mpatches.Rectangle((j,nr-1-i),1,1,fc=cmap[v],ec="white",lw=2))
        if v==2: ax.text(j+0.5,nr-1-i+0.5,"*",ha="center",va="center",color="white",fontsize=16,fontweight="bold")
        elif v==1: ax.text(j+0.5,nr-1-i+0.5,"o",ha="center",va="center",color=C["teal_dk"],fontsize=12,fontweight="bold")
ax.axvline(3,color=C["accent"],lw=2.4,ls="--")
ax.text(1.5,nr+0.30,"Pleiades Neo (VNIR-only)",ha="center",color=C["accent"],fontsize=10.5,fontweight="bold")
ax.text(5,nr+0.30,"WorldView-3 adds SWIR",ha="center",color=C["teal_dk"],fontsize=10.5,fontweight="bold")
ax.set_xlim(0,nc); ax.set_ylim(0,nr+0.9); ax.set_xticks(np.arange(nc)+0.5); ax.set_xticklabels(feats,fontsize=9)
ax.set_yticks(np.arange(nr)+0.5); ax.set_yticklabels(mats[::-1],fontsize=9.5); ax.tick_params(length=0)
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_title("Where each hazard becomes separable: diagnostic feature to band",pad=26)
leg=[mpatches.Patch(fc=C["teal"],label="strong"),mpatches.Patch(fc=C["teal_lt"],label="weak"),mpatches.Patch(fc="#F2F2F2",label="none")]
ax.legend(handles=leg,loc="lower center",bbox_to_anchor=(0.5,1.02),ncol=3,frameon=False,fontsize=9.5)
fig.text(0.5,0.005,"Diagnostic features: USGS splib07a . Aguilar 2021/2025 . Cilia 2015",ha="center",fontsize=8.5,style="italic",color="#8A8A8A")
fig.savefig(OUT/"band_material_map.png",bbox_inches="tight"); plt.close(fig)

# risk chain
fig,ax=plt.subplots(figsize=(11,4.6)); noax(ax)
ax.text(50,93,"From pixels to an ARPA intervention priority",ha="center",fontsize=15,fontweight="bold",color=C["ink"])
steps=[("Image","WV-3 / PNeo"+NL+"tile",C["teal_lt"]),("Material","multiband"+NL+"to chemistry",C["teal"]),
       ("EWC hazard","asbestos"+NL+"17 06 05*",C["asbestos"]),("Risk","hazard x exposure"+NL+"x magnitude",C["accent"]),
       ("ARPA priority","ranked"+NL+"inspection list",C["gold"])]
n=5; w=17.0; gap=(100-n*w)/(n+1)
for i,(t,s,cc) in enumerate(steps):
    x=gap+i*(w+gap); rbox(ax,x,42,w,26,"#FFFFFF",cc,lw=2.4,rad=0.06); rbox(ax,x,60,w,8,cc,cc,rad=0.06)
    ax.text(x+w/2,64,t,ha="center",va="center",fontsize=10,fontweight="bold",color="white")
    ax.text(x+w/2,51,s,ha="center",va="center",fontsize=9,color=C["ink"])
    if i<n-1: arrow(ax,x+w+0.5,55,x+w+gap-0.5,55,color=C["grey"],lw=2.0,ms=13)
ax.text(gap+w/2,36,"RGB detects the site"+NL+"(shape / context)",ha="center",fontsize=8.3,color=C["grey"])
ax.text(gap+2*(w+gap)+w/2,36,"multiband infers the material"+NL+"(SWIR chemistry)",ha="center",fontsize=8.3,color=C["grey"])
ax.text(50,18,"Indice di Degrado (d.d.g. 13237/2008) is NOT in the public WFS - estimated remotely (SWIR Mg-OH + VNIR weathering) = a thesis contribution",
    ha="center",fontsize=8.8,style="italic",color=C["grey"])
footer(fig,"EWC List of Waste 2000/532/EC . Indice di Degrado d.d.g. 13237/2008 . Fazzo et al. 2023")
fig.savefig(OUT/"risk_chain.png"); plt.close(fig)
print("3 figs fixed")

# pilot workflow (fixed: no overlapping side note)
fig,ax=plt.subplots(figsize=(11,5.2)); noax(ax)
ax.text(50,95,"Phase-1 asbestos pilot: the immediately-feasible demonstrator",ha="center",fontsize=15,fontweight="bold",color=C["ink"])
boxes=[(6,70,"WFS Mappatura_2020"+NL+"10,903 roofs (EPSG:32632)",C["teal_lt"]),
       (38,70,"Self-pair on WV-3 + PNeo"+NL+"to surface reflectance",C["teal_lt"]),
       (70,70,"Per-roof spectral"+NL+"signature",C["teal_lt"]),
       (6,42,"(A) Unsupervised"+NL+"clustering (no labels)",C["teal"]),
       (38,42,"DECISION GATE"+NL+"clusters form only"+NL+"with SWIR?",C["accent"]),
       (70,42,"(B) Supervised"+NL+"RGB / VNIR / VNIR+SWIR",C["teal"])]
W,H=26,18
for x,y,t,cc in boxes:
    if "GATE" in t: rbox(ax,x,y,W,H,"#FDEFE6",C["accent"],lw=2.6,rad=0.05)
    else: rbox(ax,x,y,W,H,"#FFFFFF",cc,lw=2.0,rad=0.05)
    ax.text(x+W/2,y+H/2,t,ha="center",va="center",fontsize=9.3,color=C["ink"],fontweight="bold" if "GATE" in t else "normal")
rbox(ax,32,14,46,12,"#FBF6E6",C["gold"],lw=2.2,rad=0.05)
ax.text(55,20,"EWC 17 06 05*  to  risk tier  to  ARPA priority",ha="center",va="center",fontsize=9.6,fontweight="bold",color=C["ink"])
arrow(ax,32,79,38,79,color=C["grey"]); arrow(ax,64,79,70,79,color=C["grey"])
arrow(ax,19,70,19,60,color=C["grey"]); arrow(ax,51,42,55,26,color=C["accent"])
ax.text(50,34,"Public, pixel-accurate labels . textbook SWIR diagnostic . de-risks the whole pipeline before AerialWaste coordinates arrive",
    ha="center",fontsize=8.6,color=C["grey"])
footer(fig,"GT: Lombardia WFS Mappatura_2020 . physics: chrysotile Mg-OH 2.30-2.33um (splib07a)")
fig.savefig(OUT/"pilot_workflow.png"); plt.close(fig)
print("pilot fixed")
