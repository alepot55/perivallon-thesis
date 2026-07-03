"""Iso-chromaticity panel in the ORIGINAL deck-figure style (panel A of
rgb_fails_two_panels, standalone) — original palette, boxes, annotations."""
import importlib.util, sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
ROOT=Path("/home/alepot55/Desktop/uni/Tesi")
sys.path.insert(0,str(ROOT/"spectral"))
spec=importlib.util.spec_from_file_location("mdp", ROOT/"spectral/scripts/make_deck_plots.py")
mdp=importlib.util.module_from_spec(spec)
# prevent main() execution on load: module only runs main under __main__ guard? check: it calls main() at bottom unguarded?
src=open(ROOT/"spectral/scripts/make_deck_plots.py").read()
if 'if __name__ == "__main__"' not in src:
    # guard missing: execute in controlled namespace without main()
    ns={"__name__":"mdp_ns"}
    exec(compile(src.replace("main()","# main()") if src.rstrip().endswith("main()") else src, "mdp","exec"), ns)
    C=ns["C"]; SPECTRA=ns["SPECTRA"]; _clean=ns["_clean"]
else:
    spec.loader.exec_module(mdp); C=mdp.C; SPECTRA=mdp.SPECTRA; _clean=mdp._clean
OUT=ROOT/"assets/deck_v6/figs_color"

fig,ax=plt.subplots(figsize=(8.2,5.2))
grid=np.arange(400,2501,5,dtype=float)
wl_c,r_c=_clean(*SPECTRA["Concrete (road)"])
wl_a,r_a=_clean(*SPECTRA["Chrysotile (asbestos)"])
conc=np.interp(grid,wl_c,r_c,left=np.nan,right=np.nan)
chry=np.interp(grid,wl_a,r_a,left=np.nan,right=np.nan)
ac=0.20*chry+0.80*conc
ax.plot(grid,conc,color=C["concrete"],lw=2.4,label="Concrete (no asbestos)")
ax.plot(grid,ac,color=C["asbestos"],lw=2.4,label="Asbestos-cement roof (modelled)")
ax.axvspan(400,700,alpha=0.18,color=C["vnir_box"],zorder=0)
ax.axvspan(1000,2500,alpha=0.18,color=C["swir_box"],zorder=0)
ax.text(550,0.65,"VIS:\nboth look grey\n(ΔR ≈ 0.11)",ha="center",va="top",fontsize=10,color="#5D7B9D",
        bbox=dict(boxstyle="round,pad=0.2",fc="white",ec="#CCCCCC",lw=0.5))
ax.text(1750,0.65,"SWIR:\nMg-OH dip @ 2.31 µm\nonly in AC roof",ha="center",va="top",fontsize=10,color="#8B5A2B",
        bbox=dict(boxstyle="round,pad=0.2",fc="white",ec="#CCCCCC",lw=0.5))
ax.axvline(2310,color=C["asbestos"],lw=0.8,ls=":",alpha=0.6)
ax.set_xlim(400,2500); ax.set_ylim(0,0.8)
ax.set_xlabel("Wavelength (nm)"); ax.set_ylabel("Reflectance")
ax.legend(loc="upper right",fontsize=10)
ax.xaxis.set_major_locator(mticker.MultipleLocator(500))
ax.text(0.995,-0.14,"USGS splib07a (Kokaly et al., 2017)",transform=ax.transAxes,
        ha="right",va="top",fontsize=9,style="italic",color="#888")
fig.savefig(OUT/"iso_chromaticity.png",dpi=300,bbox_inches="tight")
print("iso_chromaticity.png saved")
