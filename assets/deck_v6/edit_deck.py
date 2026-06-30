"""Edit ultime_slide.pptx in place: keep the good originals + their embedded
paper images, apply the WV-3 + Pléiades Neo pivot, add slides in the SAME
minimal B/W standard style. Output: assets/deck_v6/deck_bw.pptx (+ ~/Downloads)."""
import os, copy
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

SRC=os.path.expanduser("~/Downloads/ultime_slide.pptx")
OUT=os.path.expanduser("/home/alepot55/Desktop/uni/Tesi/assets/deck_v6/deck_bw.pptx")
BW=os.path.expanduser("/home/alepot55/Desktop/uni/Tesi/assets/deck_v6/figs_bw")
INK=RGBColor(0x1A,0x1A,0x1A); GREY=RGBColor(0x66,0x66,0x66)
HDR=RGBColor(0xDD,0xDD,0xDD); ALT=RGBColor(0xF5,0xF5,0xF5); WHITE=RGBColor(0xFF,0xFF,0xFF)
F="Calibri"
prs=Presentation(SRC)
S=list(prs.slides)
EMU=914400
def IN(v): return Inches(v)

# ---- low-level helpers -----------------------------------------------------
def fill_tf(tf, specs, wrap=True):
    """specs: list of dicts {t, b(old), i(talic), sz, c(olor)}."""
    tf.clear(); tf.word_wrap=wrap
    for k,sp in enumerate(specs):
        p=tf.paragraphs[0] if k==0 else tf.add_paragraph()
        p.alignment=PP_ALIGN.LEFT; p.space_after=Pt(sp.get("sa",4)); p.line_spacing=sp.get("ls",1.05)
        r=p.add_run(); r.text=sp["t"]
        r.font.name=F; r.font.size=Pt(sp.get("sz",14)); r.font.bold=sp.get("b",False)
        r.font.italic=sp.get("i",False); r.font.color.rgb=sp.get("c",INK)

def boxes(slide):
    """return (title_tb, body_tbs[], footer_tb) by first-run size heuristics."""
    title=foot=None; body=[]
    for sh in slide.shapes:
        if not (getattr(sh,"has_text_frame",False) and sh.has_text_frame): continue
        sz=None; 
        for p in sh.text_frame.paragraphs:
            for r in p.runs:
                sz=r.font.size.pt if r.font.size else None; break
            if sz is not None: break
        if sz and sz>=20: title=sh
        elif sz and sz<=9: foot=sh
        else: body.append(sh)
    return title, body, foot

def set_title(slide, text):
    t,_,_=boxes(slide)
    if t: fill_tf(t.text_frame,[{"t":text,"b":True,"sz":23,"c":INK}])

def set_footer(slide, text):
    _,_,f=boxes(slide)
    if f: fill_tf(f.text_frame,[{"t":text,"sz":8,"c":GREY}])

def set_body(slide, specs, idx=0):
    _,b,_=boxes(slide)
    if b and idx<len(b): fill_tf(b[idx].text_frame,specs)

def del_shape(sh): sh._element.getparent().remove(sh._element)

def reencode_all_pictures():
    """PIL-normalize every embedded PNG so LibreOffice renders all slides."""
    import io
    from PIL import Image
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    for sl in prs.slides:
        for sh in list(sl.shapes):
            if sh.shape_type==MSO_SHAPE_TYPE.PICTURE:
                try:
                    im=Image.open(io.BytesIO(sh.image.blob))
                    buf=io.BytesIO(); im.save(buf,"PNG"); buf.seek(0)
                    L,T,W,H=sh.left,sh.top,sh.width,sh.height
                    del_shape(sh); sl.shapes.add_picture(buf,L,T,W,H)
                except Exception as e:
                    print("  reencode skip:",e)

def add_slide():
    s=prs.slides.add_slide(prs.slide_layouts[10])  # BLANK
    # strip any leftover placeholders
    for ph in list(s.placeholders):
        try: del_shape(ph)
        except: pass
    return s

def n_title(s,text):
    tb=s.shapes.add_textbox(IN(0.45),IN(0.34),IN(9.10),IN(0.68))
    fill_tf(tb.text_frame,[{"t":text,"b":True,"sz":23,"c":INK}]); return tb
def n_body(s,specs,top=1.25,w=9.10,h=None):
    tb=s.shapes.add_textbox(IN(0.45),IN(top),IN(w),IN(h or (5.0-top+1.0)))
    fill_tf(tb.text_frame,specs); return tb
def n_foot(s,text):
    tb=s.shapes.add_textbox(IN(0.45),IN(5.29),IN(9.10),IN(0.26))
    fill_tf(tb.text_frame,[{"t":text,"sz":8,"c":GREY}]); return tb
def n_img(s,path,left=5.30,top=1.25,w=4.40,h=3.85):
    from PIL import Image
    iw,ih=Image.open(path).size; ar=iw/ih
    W=IN(w); H=int(W/ar)
    if H>IN(h): H=IN(h); W=int(H*ar)
    s.shapes.add_picture(path,IN(left)+ (IN(w)-W)//2, IN(top)+(IN(h)-H)//2, width=W,height=H)

def style_table(tbl, headerbold=True, fs=10.5):
    nr=len(tbl.rows); nc=len(tbl.columns)
    for i in range(nr):
        for j in range(nc):
            c=tbl.cell(i,j); c.vertical_anchor=MSO_ANCHOR.MIDDLE
            c.margin_left=IN(0.07); c.margin_right=IN(0.05); c.margin_top=IN(0.02); c.margin_bottom=IN(0.02)
            c.fill.solid(); c.fill.fore_color.rgb = HDR if i==0 else (ALT if i%2==0 else WHITE)
            for p in c.text_frame.paragraphs:
                p.line_spacing=1.0
                for r in p.runs:
                    r.font.name=F; r.font.size=Pt(fs); r.font.color.rgb=INK
                    r.font.bold=(i==0 and headerbold)

def new_table(s, data, left=0.45, top=1.25, w=9.10, colw=None, fs=10.5):
    nr=len(data); nc=len(data[0])
    gt=s.shapes.add_table(nr,nc,IN(left),IN(top),IN(w),IN(0.42*nr)).table
    if colw:
        for j,cw in enumerate(colw): gt.columns[j].width=IN(cw)
    for i,row in enumerate(data):
        for j,val in enumerate(row): gt.cell(i,j).text=str(val)
    style_table(gt,fs=fs); return gt

# ════════ EDIT EXISTING SLIDES ════════
# S4 pixel-spectrum: drop SuperDove anchor
set_body(S[3],[
 {"t":"Each pixel is a vector of reflectance values, the material's spectral signature.","sz":14},
 {"t":"•  RGB,  3 broad visible bands (colour only).","sz":14},
 {"t":"•  Multispectral (MS),  4-15 chosen bands. WorldView-3 records 8 VNIR + 8 SWIR; Pleiades Neo records 6 VNIR.","sz":14},
 {"t":"•  Hyperspectral (HSI),  hundreds of contiguous narrow bands.","sz":14},
 {"t":"This vector is the raw input from which any classifier reasons.","sz":14},
])
# S9 sensor trade-off: foreground WV-3 + PNeo
set_body(S[8],[
 {"t":"Three axes, one photon budget. No satellite maximises all three.","sz":12},
 {"t":"•  WorldView-3:  1.24 m VNIR + 3.7 m SWIR, 16 bands - the chemistry sensor.","sz":12},
 {"t":"•  Pleiades Neo:  1.2 m, 6 VNIR, no SWIR - the VNIR-only cross-sensor.","sz":12},
 {"t":"•  Sentinel-2:  10 m, 13 bands, free - too coarse for material.","sz":12},
 {"t":"•  SuperDove:  3 m, 8 VNIR, free, near-daily - wide-area screening.","sz":12},
 {"t":"•  PRISMA / EnMAP:  30 m, 200+ bands - resolves chemistry but coarse.","sz":12},
])
# S12 chosen data: replace title + table
set_title(S[11],"The chosen data: WorldView-3 + Pleiades Neo")
for sh in list(S[11].shapes):
    if getattr(sh,"has_table",False): del_shape(sh)
new_table(S[11],[
 ["","WorldView-3","Pleiades Neo"],
 ["VNIR","8 bands @ 1.24 m","6 bands @ 1.2 m"],
 ["SWIR","8 bands @ 3.7 m","none"],
 ["Pan","~0.31 m","~0.30 m"],
 ["Unique bands","Yellow, NIR2","Deep Blue"],
 ["Role","full ladder incl. SWIR chemistry","VNIR-only cross-sensor axis"],
], left=0.45, top=1.15, w=6.6, colw=[1.5,2.55,2.55], fs=11)
set_body(S[11],[
 {"t":"Both sub-metre VHR; access feasible for free via ESA Third-Party Missions (~9-week proposal lead).","sz":13},
 {"t":"WorldView-3 is rare civilian SWIR at high resolution; Pleiades Neo tests how far VNIR-only gets.","sz":13},
])
set_footer(S[11],"Specs: Maxar WorldView-3 · Airbus Pleiades Neo · ESA TPM")
# S14 more-bands: flip the SuperDove-disadvantage takeaway
set_body(S[13],[
 {"t":"•  Aguilar 2021 (WV-3 plastic): VNIR 90.85 -> All 97.38; SWIR carries the jump.","sz":14},
 {"t":"•  Vitek 2025 (C&D waste): RGB + 2 narrowbands = HSI 768 bands.","sz":14},
 {"t":"•  Zhou 2021 (WV-3 plastic): 8 SWIR bands separate 3 polymer clusters.","sz":14},
 {"t":"What matters is which bands, not how many. SWIR is the most informative region - and WorldView-3 gives us SWIR; Pleiades Neo (VNIR-only) measures how far we get without it.","i":True,"sz":12,"c":GREY},
])
# S17 DOFA: add Pleiades Neo
set_body(S[16],[
 {"t":"Dynamic One-For-All (Xiong et al. 2024).","b":True,"sz":14},
 {"t":"•  A hypernetwork generates patch-embedding weights from each band's central wavelength.","sz":14},
 {"t":"•  One backbone handles WV-3 (16 b), Pleiades Neo (6 b), Sentinel-2 (13 b), or HSI.","sz":14},
 {"t":"•  So RGB vs VNIR vs SWIR becomes a fair comparison, not apples-to-oranges.","sz":14},
 {"t":"•  Natural fit for the band-ablation study; pairable with a DEFLECT adapter (<1% params).","sz":14},
 {"t":"To verify: does pretraining at 10-30 m close the gap to ~1.2 m VHR?","i":True,"sz":12,"c":GREY},
])
# S18 gaps: add PNeo benchmark + object-vs-material
set_body(S[17],[
 {"t":"•  Material-level labels are missing: no public VHR waste dataset annotates the material.","sz":14},
 {"t":"•  No peer-reviewed Pleiades-Neo material benchmark exists.","sz":14},
 {"t":"•  RGB pipelines conflate iso-colour, chemically distinct materials.","sz":14},
 {"t":"•  No pipeline goes from spectra to a regulatory hazard class (material -> EWC -> risk).","sz":14},
 {"t":"•  The object-vs-material split is unaddressed; generalizzazione (region/sensor/time) rarely shown.","sz":14},
 {"t":"The test that matters: how much does multiband beat RGB for material, and where does it stop?","b":True,"sz":13},
])
# S19 proposed direction: WV-3 SWIR pilot + 3-axis ablation
set_body(S[18],[
 {"t":"Phase 1 - asbestos spectral pilot (run first, in full)","b":True,"sz":13},
 {"t":"•  Public GT: Lombardy WFS Mappatura 2020 (10,903 roofs). Textbook SWIR diagnostic (Mg-OH ~2.3 um).","sz":12},
 {"t":"•  Self-pair on WV-3 + PNeo -> surface reflectance -> per-roof signatures.","sz":12},
 {"t":"•  Unsupervised clustering (no labels) -> decision gate: do AC clusters form only with SWIR?","sz":12},
 {"t":"•  Then map material -> EWC 17 06 05* -> risk tier -> ARPA priority.","sz":12},
 {"t":"Phase 2 - multispectral waste benchmark","b":True,"sz":13},
 {"t":"•  Co-register AerialWaste with the VHR archive; 3-axis ablation (R0-R3 x WV-3/PNeo x native/pansharp).","sz":12},
 {"t":"•  DOFA backbone; cross-region / cross-sensor / cross-time splits.","sz":12},
])
set_footer(S[18],"Pilot GT: Mappatura 2020 (Lombardia WFS) · Backbone: DOFA (Xiong 2024) · Baseline ref.: Gibellini 2025")

# S13 Aguilar: drop the SuperDove aside
set_body(S[12],[
 {"t":"Most-cited band ablation on WV-3 for waste-like classification (greenhouse plastic, n = 14.3 M pixels).","sz":14},
 {"t":"OBIA + Decision Tree, 10-fold CV. The thesis measures exactly this VNIR -> +SWIR gain on waste materials.","sz":14},
])
# S15 SuperDove -> REPURPOSE as Honest caveat (+ swir8 figure)
sd=S[14]
set_title(sd,"Honest caveat: resolution is split between texture and chemistry")
# resize body to left half, refill
_,bd,_=boxes(sd)
if bd:
    bd[0].left=IN(0.45); bd[0].top=IN(1.25); bd[0].width=IN(4.55); bd[0].height=IN(3.9)
    fill_tf(bd[0].text_frame,[
     {"t":"•  Spectra are sampled coarsely: VNIR ~1.24 m, SWIR ~3.7 m (~14 m2 pixels).","sz":13},
     {"t":"•  The pan band gives fine texture ~0.3 m, but no material info alone.","sz":13},
     {"t":"•  A small dump is easier to SEE (texture) than to chemically IDENTIFY (spectra).","sz":13},
     {"t":"•  SWIR-8 bottleneck: asbestos 2.32 + concrete 2.34 + plastic 2.31 crowd one band.","sz":13},
     {"t":"•  Honest: at 3.7 m + atmosphere, R3 may = R2 - itself a valid finding.","sz":13},
    ])
n_img(sd, os.path.join(BW,"swir8_bottleneck.png"), left=5.05, top=1.3, w=4.7, h=3.7)
set_footer(sd,"USGS splib07a (Kokaly et al., 2017) · WV-3 SWIR band centres (Maxar)")

# ════════ NEW SLIDES (appended; reordered below) ════════
# N1 Risk
n=add_slide(); n_title(n,"Not all waste is equal: risk = hazard x exposure x magnitude")
n_body(n,[
 {"t":"•  The danger is material-bound: inert rubble vs plastics vs asbestos-cement are worlds apart.","sz":14},
 {"t":"•  \"Material\" carries the hazard; the European Waste Catalogue (EWC) flags hazardous codes with *.","sz":14},
 {"t":"   Asbestos = 17 06 05* (mirror-hazardous).","sz":13,"c":GREY},
 {"t":"•  Priority risk = hazard (material) x exposure (who/what is nearby) x magnitude (how much).","sz":14},
 {"t":"•  Goal: turn imagery into an actionable ARPA priority list - computer vision as decision support.","sz":14},
])
n_foot(n,"EWC List of Waste (Dec. 2000/532/EC) · Indice di Degrado d.d.g. 13237/2008 · Fazzo et al. 2023")
# N2 Asbestos precedents
n=add_slide(); n_title(n,"Asbestos: direct precedents to benchmark against")
n_body(n,[
 {"t":"•  Saba 2026 (WV-3 VNIR, 8 bands): 32 classifiers; Fine-KNN Macro-F1 97.6% - strong VNIR-only upper bound. [paywalled]","sz":14},
 {"t":"•  Bonifazi 2026 (WV-3, 16 bands, Max-Likelihood): AC roofs F1 0.87 (P 0.81 / R 0.92); 25,319 buildings; multi-temporal.","sz":14},
 {"t":"•  Shepherd 2025 (EnMAP, 230 bands @ 30 m): ACE 91.4% OA / F1 91.2%; 86% field match - but urban mixed pixels mimic asbestos.","sz":14},
 {"t":"Together: VNIR can detect AC; SWIR + hyperspectral add robustness on clean / ambiguous roofs.","b":True,"sz":13},
])
n_foot(n,"Saba 2026 J. Hazard. Mater. · Bonifazi 2026 Geomatics 6(3):41 · Shepherd 2025 Sci. Rep.")
# N3 Band -> material (fig)
n=add_slide(); n_title(n,"Where each hazard becomes separable: feature -> band")
n_img(n, os.path.join(BW,"band_material_map.png"), left=0.6, top=1.15, w=8.8, h=3.95)
n_foot(n,"Pleiades Neo reaches up to NIR; WorldView-3 adds the SWIR chemistry · USGS splib07a · Aguilar · Cilia 2015")
# N4 3-axis experiment (fig)
n=add_slide(); n_title(n,"The experiment: a 3-axis band ablation")
n_img(n, os.path.join(BW,"ablation_cube.png"), left=0.5, top=1.15, w=9.0, h=3.95)
n_foot(n,"Per-pixel AND full-CNN: B-A = pure chemistry gain, D-C = total MS gain · loop_prof_sota/04_experimental_design.md")
# N5 Generalization (table)
n=add_slide(); n_title(n,"Generalization as a first-class axis (expected, to be measured)")
new_table(n,[
 ["","In-domain","Cross-region","Cross-sensor"],
 ["R0 RGB","baseline","-5.1% (Gibellini)","ports trivially"],
 ["R2 full VNIR","+ small","gap narrows","needs harmonization"],
 ["R3 +SWIR","+ chemistry","gap narrows most","widens unless SBAF"],
], left=0.7, top=1.45, w=8.0, colw=[1.9,2.0,2.05,2.05], fs=12)
n_body(n,[{"t":"Whether added bands narrow or widen the generalization gap is publishable either way - report ID-OOD dF1 per cell.","i":True,"sz":12,"c":GREY}], top=4.1)
n_foot(n,"Cross-region -5.1%: Gibellini 2025 · cross-sensor: GeoCrossBench - cell values EXPECTED")
# N6 Material -> risk tier
n=add_slide(); n_title(n,"From material to risk tier")
n_body(n,[
 {"t":"•  Map predicted material -> EWC hazard code -> Indice di Degrado / PRAL x exposure x magnitude -> ARPA priority tier.","sz":14},
 {"t":"•  Output = a ranked intervention list; every step transparent and auditable.","sz":14},
 {"t":"   Indice di Degrado (<=25 / 26-44 / >=45 -> action windows) is NOT in the public WFS","sz":13,"c":GREY},
 {"t":"   -> estimated remotely (SWIR Mg-OH depth + VNIR weathering) = a thesis contribution.","sz":13,"c":GREY},
 {"t":"•  Exposure grounded in Fazzo et al. (residential-proximity mesothelioma risk); magnitude from site area.","sz":14},
])
n_foot(n,"EWC 17 06 05* · Indice di Degrado d.d.g. 13237/2008 · Fazzo et al. 2023")
# N7 Asbestos pilot (fig)
n=add_slide(); n_title(n,"The asbestos pilot: the immediately-feasible demonstrator")
n_img(n, os.path.join(BW,"pilot_workflow.png"), left=0.5, top=1.15, w=9.0, h=3.95)
n_foot(n,"Public pixel-accurate labels + textbook SWIR diagnostic (Mg-OH 2.30-2.33 um) - de-risks the whole pipeline")
# N8 Novelty + checklist
n=add_slide(); n_title(n,"What is novel - and what to confirm with Thomas")
n_body(n,[
 {"t":"Genuinely novel","b":True,"sz":13},
 {"t":"•  First to MEASURE RGB vs VNIR vs SWIR added value for waste material at VHR.","sz":13},
 {"t":"•  First WorldView-3 vs Pleiades Neo head-to-head for this task.","sz":13},
 {"t":"•  First to connect spectra -> EWC hazard -> ARPA risk tier; confidence-aware.","sz":13},
 {"t":"To confirm with Thomas","b":True,"sz":13},
 {"t":"•  Trigger the ESA TPM proposal now (~9-wk lead)? AOI over Lombardia?","sz":13},
 {"t":"•  Risk-chain depth: full Indice di Degrado, or stop at material + EWC?","sz":13},
 {"t":"•  SuperDove kept as wide-area layer, or dropped? · Backbone DOFA + Swin-RSP? · AerialWaste coordinate bridge?","sz":13},
])
n_foot(n,"Open dependencies: loop_prof_sota/00_LOOP_LOG.md")

# Rebuild the 2 slides LibreOffice drops (fingerprint, sensor) as fresh slides
import io
from PIL import Image as _PILImage
from pptx.enum.shapes import MSO_SHAPE_TYPE as _MST
def _extract_pic(slide, outpath):
    for sh in slide.shapes:
        if sh.shape_type==_MST.PICTURE:
            _PILImage.open(io.BytesIO(sh.image.blob)).save(outpath)
            return sh.left, sh.top, sh.width, sh.height
    return None
_fp=os.path.join(BW,"_fingerprint.png"); _sn=os.path.join(BW,"_sensor.png")
_fpg=_extract_pic(S[5], _fp); _sng=_extract_pic(S[8], _sn)
# fresh fingerprint slide (title + image + footer)
nf=add_slide(); n_title(nf,"Every material has a spectral fingerprint")
if _fpg: nf.shapes.add_picture(_fp, _fpg[0], _fpg[1], width=_fpg[2], height=_fpg[3])
n_foot(nf,"USGS splib07a (Kokaly et al., 2017). Diagnostic features: Cilia 2015, Aguilar 2025.")
# fresh sensor slide (title + bullets-left + image-right + footer)
ns=add_slide(); n_title(ns,"The sensor trade-off: spatial x spectral x revisit")
n_body(ns,[
 {"t":"Three axes, one photon budget. No satellite maximises all three.","sz":12},
 {"t":"•  WorldView-3:  1.24 m VNIR + 3.7 m SWIR, 16 bands - the chemistry sensor.","sz":12},
 {"t":"•  Pleiades Neo:  1.2 m, 6 VNIR, no SWIR - the VNIR-only cross-sensor.","sz":12},
 {"t":"•  Sentinel-2:  10 m, 13 bands, free - too coarse for material.","sz":12},
 {"t":"•  SuperDove:  3 m, 8 VNIR, free, near-daily - wide-area screening.","sz":12},
 {"t":"•  PRISMA / EnMAP:  30 m, 200+ bands - resolves chemistry but coarse.","sz":12},
], top=1.20, w=4.55)
if _sng: ns.shapes.add_picture(_sn, _sng[0], _sng[1], width=_sng[2], height=_sng[3])
n_foot(ns,"Specs: Planet, ESA, Maxar, ASI, DLR (mission documents).")
# their appended 0-based indices:
_IDX_FP=len(list(prs.slides))-2; _IDX_SN=len(list(prs.slides))-1

reencode_all_pictures()

# ════════ REORDER ════════
sldIdLst=prs.slides._sldIdLst
ids=list(sldIdLst)
order=[0,1,19, 2,3,4,_IDX_FP,6,7,_IDX_SN,9,10,11,14,12,13,20,21,15,16,17,22,23,24,18,25,26]
assert len(order)==27 and all(0<=i<len(ids) for i in order), (len(ids),len(order))
desired=[ids[i] for i in order]
for sid in ids: sldIdLst.remove(sid)
for sid in desired: sldIdLst.append(sid)

# stamp page numbers on new slides (originals keep their auto field)
from pptx.enum.text import PP_ALIGN as _AL
for pos,sl in enumerate(prs.slides,1):
    hasnum=any(sh.is_placeholder and sh.placeholder_format.type is not None and "SLIDE_NUMBER" in str(sh.placeholder_format.type) for sh in sl.shapes)
    if not hasnum:
        tb=sl.shapes.add_textbox(IN(4.12),IN(5.21),IN(1.75),IN(0.30))
        tf=tb.text_frame; tf.word_wrap=False; r=tf.paragraphs[0].add_run(); r.text=str(pos)
        tf.paragraphs[0].alignment=_AL.CENTER
        r.font.name=F; r.font.size=Pt(9); r.font.color.rgb=GREY

prs.save(OUT)
import shutil; shutil.copy(OUT, os.path.expanduser("~/Downloads/ultime_slide_v2.pptx"))
print("saved", OUT, "·", len(list(prs.slides)), "slides")
