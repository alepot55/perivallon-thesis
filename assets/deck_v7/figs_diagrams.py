"""Deck v7 diagrams, quality pass v2."""
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.image as mpimg

OUT = Path(__file__).resolve().parent / "figs"
INK="#1A1A1A"; MUT="#666666"; BLU="#1A1A1A"; ORA="#1A1A1A"; BG="white"; BG2="white"
plt.rcParams.update({"font.family":"sans-serif","font.sans-serif":["Arial","DejaVu Sans"],
 "text.color":INK,"figure.facecolor":"white","savefig.facecolor":"white",
 "savefig.dpi":300,"savefig.bbox":"tight"})

def rbox(ax,x,y,w,h,fc="white",ec=INK,lw=1.4,r=1.6):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0,rounding_size={r}",
                 fc=fc,ec=ec,lw=lw,mutation_aspect=1))
def arr(ax,x0,y0,x1,y1,color=INK,lw=1.6):
    ax.add_patch(FancyArrowPatch((x0,y0),(x1,y1),arrowstyle="-|>",mutation_scale=14,
                 lw=lw,color=color,shrinkA=2,shrinkB=2))
def canvas(w,h):
    fig,ax=plt.subplots(figsize=(w,h))
    ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis("off")
    return fig,ax

# 1. task_io
fig,ax=canvas(9.6,3.0)
tile=mpimg.imread(OUT/"tile_scrap.png")
th,tw=tile.shape[0],tile.shape[1]
bw,bh=18,74
ar_canvas=(bw*9.6)/(bh*3.0); ar_tile=tw/th
if ar_tile>ar_canvas: w2,h2=bw,bh*ar_canvas/ar_tile
else: w2,h2=bw*ar_tile/ar_canvas,bh
x0,y0=3+(bw-w2)/2,16+(bh-h2)/2
ax.imshow(tile,extent=(x0,x0+w2,y0,y0+h2),aspect="auto",zorder=3)
ax.plot([x0,x0+w2,x0+w2,x0,x0],[y0,y0,y0+h2,y0+h2,y0],color=INK,lw=1.2,zorder=4)
ax.text(12,7,"input tile, RGB / VNIR",ha="center",fontsize=10,color=MUT)
arr(ax,23,53,33,53)
rbox(ax,33,32,26,42,fc="white",ec=INK,lw=1.3)
ax.text(46,60,"CNN / Transformer",ha="center",fontsize=11.5,fontweight="bold",color=INK)
ax.text(46,44,"Swin-T, RS pretraining",ha="center",fontsize=9.6,color=MUT)
arr(ax,61,53,71,53)
rbox(ax,71,10,26,82,fc="white",ec=INK,lw=1.3)
ax.text(84,84,"materials present",ha="center",fontsize=10.5,fontweight="bold")
for i,(lab,on) in enumerate([("scrap",True),("bulky items",True),("rubble",False),("tires",False),("asbestos-cement",False)]):
    y=70-i*12.5
    ax.text(75.4,y,"☑" if on else "☐",fontsize=12,color=(INK if on else "#B5B5B5"),va="center")
    ax.text(80,y,lab,fontsize=10.5,va="center",color=(INK if on else MUT))
fig.savefig(OUT/"task_io.png"); plt.close(fig)

# 2. search_flow
fig,ax=canvas(9.6,2.5)
steps=[("Scopus API","2 scripted\nquery sets","",BG),
       ("699","unique records","622 waste\n77 asbestos",BG),
       ("screening","task fit, GSD,\nrecency, review","",BG),
       ("47","annotated library","notes and\nteam Excel",BG),
       ("24","cited here","",BG2)]
n=len(steps); w=17.2; gap=(100-n*w)/(n+1)
for i,(big,small,tiny,fc) in enumerate(steps):
    x=gap+i*(w+gap)
    rbox(ax,x,12,w,74,fc="white",ec=INK,lw=1.3)
    if big.isdigit():
        ax.text(x+w/2,64,big,ha="center",fontsize=20,fontweight="bold",color=INK)
        ax.text(x+w/2,42,small,ha="center",fontsize=8.8,color=INK)
        if tiny: ax.text(x+w/2,24,tiny,ha="center",fontsize=7.8,color=MUT)
    else:
        ax.text(x+w/2,62,big,ha="center",fontsize=11.5,fontweight="bold",color=INK)
        ax.text(x+w/2,38,small,ha="center",fontsize=8.6,color=MUT)
    if i<n-1: arr(ax,x+w+0.6,49,x+w+gap-0.6,49)
fig.savefig(OUT/"search_flow.png"); plt.close(fig)

# 3. bands_chart
WV3=[("Coastal",400,450,"#3b6bb5"),("Blue",450,510,"#2a78d6"),("Green",510,580,"#2e9e4f"),
     ("Yellow",585,625,"#e3b505"),("Red",630,690,"#d64545"),("Red Edge",705,745,"#a83254"),
     ("NIR1",770,895,"#8a8a8a")]
NIR2=(860,1040,"#5c5c5c")
PNEO=[("Deep Blue",400,450,"#3b6bb5"),("Blue",450,520,"#2a78d6"),("Green",530,590,"#2e9e4f"),
      ("Red",620,690,"#d64545"),("Red Edge",700,750,"#a83254"),("NIR",770,880,"#8a8a8a")]
fig,ax=plt.subplots(figsize=(9.6,3.1))
def draw(y,bands,label_below):
    for lab,a,b,col in bands:
        ax.barh(y,b-a,left=a,height=0.46,color=col,edgecolor="white",lw=1.2)
        if b-a>=58:
            ax.text((a+b)/2,y,lab,ha="center",va="center",fontsize=7.8,color="white",fontweight="bold")
        else:
            yy=y-0.42 if label_below else y+0.42
            ax.annotate(lab,xy=((a+b)/2,y-0.23 if label_below else y+0.23),xytext=((a+b)/2,yy),
                        fontsize=7.4,color=col,ha="center",va=("top" if label_below else "bottom"),
                        arrowprops=dict(arrowstyle="-",color=col,lw=0.7))
draw(2.0,WV3,label_below=False)
a,b,col=NIR2
ax.barh(1.60,b-a,left=a,height=0.2,color=col,edgecolor="white",lw=0.8)
ax.text(b+12,1.60,"NIR2",fontsize=7.4,color=col,va="center")
draw(0.8,PNEO,label_below=True)
ax.text(386,2.0,"WorldView-3",ha="right",va="center",fontsize=10.5,fontweight="bold",color=INK)
ax.text(386,1.76,"8 bands, 1.24 m",ha="right",va="center",fontsize=8.6,color=MUT)
ax.text(386,0.86,"Pléiades Neo",ha="right",va="center",fontsize=10.5,fontweight="bold",color=INK)
ax.text(386,0.62,"6 bands, 1.2 m",ha="right",va="center",fontsize=8.6,color=MUT)
ax.axvspan(400,700,color="#000000",alpha=0.035)
ax.text(550,2.78,"visible (RGB)",ha="center",fontsize=9,color=MUT)
ax.text(880,2.78,"Red Edge + NIR",ha="center",fontsize=9,color=MUT)
ax.set_xlim(210,1135); ax.set_ylim(-0.15,3.05)
ax.set_yticks([]); ax.set_xlabel("Wavelength (nm)",fontsize=10)
ax.set_xticks([400,500,600,700,800,900,1000])
for sp in ("top","right","left"): ax.spines[sp].set_visible(False)
ax.tick_params(axis="x",labelsize=9)
fig.savefig(OUT/"bands_chart.png"); plt.close(fig)

# 4. pipeline
fig,ax=canvas(9.6,3.3)
srcs=[("AerialWaste + Alari labels","RGB baseline, 20-50 cm",BG),
      ("WorldView-3 / Pléiades Neo","VNIR arm, 1.2 m",BG),
      ("Lombardy WFS registry","asbestos pilot, 10,903 roofs",BG2)]
for i,(t,st,fc) in enumerate(srcs):
    y=71-i*27
    rbox(ax,2,y,29,22,fc="white",ec=INK,lw=1.3)
    ax.text(16.5,y+14,t,ha="center",fontsize=9.4,fontweight="bold")
    ax.text(16.5,y+6,st,ha="center",fontsize=8.4,color=MUT)
    arr(ax,31.5,y+11,38.5,52,lw=1.3)
rbox(ax,39,30,22,44,fc="white",ec=INK,lw=1.3)
ax.text(50,63,"Swin-T backbone",ha="center",fontsize=10.5,fontweight="bold")
ax.text(50,46,"input layer extended\nto extra bands",ha="center",fontsize=8.6,color=MUT)
arr(ax,61.5,52,66.5,52)
rbox(ax,66.5,30,14,44,fc="white",ec=INK,lw=1.3)
ax.text(73.5,64,"band ablation",ha="center",fontsize=9.4,fontweight="bold")
ax.text(73.5,44,"RGB\nRGB + NIR\nfull VNIR",ha="center",fontsize=8.6,color=MUT)
arr(ax,81,52,85.5,52)
rbox(ax,85.5,22,13,60,fc="white",ec=INK,lw=1.3)
ax.text(92,70,"per-material\nF1",ha="center",fontsize=8.4)
ax.text(92,51,"Δ vs RGB",ha="center",fontsize=8.4)
ax.text(92,33,"generalisation\nsplit",ha="center",fontsize=8.4)
fig.savefig(OUT/"pipeline.png"); plt.close(fig)

# 5. eval_grid
fig,ax=plt.subplots(figsize=(5.6,2.5))
rows=["RGB","RGB + NIR","full VNIR"]; cols=["standard split","cross-region split"]
for i in range(len(rows)):
    for j in range(len(cols)):
        base=(i==0)
        ax.add_patch(plt.Rectangle((j,2-i),1,1,fc="white",ec="#1A1A1A",lw=1.0))
        ax.text(j+0.5,2-i+0.5,"baseline F1" if base else "ΔF1 per material",
                ha="center",va="center",fontsize=9,color=(MUT if base else INK),
                fontweight=("normal" if base else "bold"))
for j,c in enumerate(cols): ax.text(j+0.5,3.18,c,ha="center",fontsize=9.6,fontweight="bold")
for i,r in enumerate(rows): ax.text(-0.08,2-i+0.5,r,ha="right",va="center",fontsize=9.6,fontweight="bold")
ax.set_xlim(-1.15,2.05); ax.set_ylim(-0.1,3.5); ax.axis("off")
fig.savefig(OUT/"eval_grid.png"); plt.close(fig)
print("diagrams v2 done")
