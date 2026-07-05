"""Deck v7 visual. Same corrected content, visual layouts: real paper figures
(Torres CC-BY, Alari politesi, Bonifazi CC-BY) + quality diagrams.
Output: assets/deck_v7/deck_v7.pptx (+ ~/Downloads/slide_v7.pptx)"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

ROOT = "/home/alepot55/Desktop/uni/Tesi"
FIG = os.path.join(ROOT, "assets/deck_v7/figs")
OUT = os.path.join(ROOT, "assets/deck_v7/deck_v7.pptx")
INK = RGBColor(0x1A,0x1A,0x1A); GREY = RGBColor(0x66,0x66,0x66)
HDR = RGBColor(0xDD,0xDD,0xDD); ALT = RGBColor(0xF5,0xF5,0xF5); WHITE = RGBColor(0xFF,0xFF,0xFF)
F = "Calibri"
prs = Presentation(); prs.slide_width = Inches(10); prs.slide_height = Inches(5.625)
BLANK = prs.slide_layouts[6]
def IN(v): return Inches(v)

def tf_fill(tf, items, wrap=True):
    tf.clear(); tf.word_wrap = wrap
    for k, it in enumerate(items):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(it.get("sa", 6)); p.line_spacing = it.get("ls", 1.12)
        r = p.add_run(); r.text = it["t"]
        r.font.name = F; r.font.size = Pt(it.get("sz", 14))
        r.font.bold = it.get("b", False); r.font.italic = it.get("i", False)
        r.font.color.rgb = it.get("c", INK)

def slide(): return prs.slides.add_slide(BLANK)
def title(s, text):
    tb = s.shapes.add_textbox(IN(0.45), IN(0.28), IN(9.10), IN(0.6))
    tf_fill(tb.text_frame, [{"t": text, "b": True, "sz": 22}])
def body(s, items, top=1.20, left=0.45, w=9.10, h=3.85, mid=True):
    tb = s.shapes.add_textbox(IN(left), IN(top), IN(w), IN(h))
    tf_fill(tb.text_frame, items)
    if mid: tb.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    return tb
def foot(s, text):
    tb = s.shapes.add_textbox(IN(0.45), IN(5.26), IN(9.10), IN(0.26))
    tf_fill(tb.text_frame, [{"t": text, "sz": 8, "c": GREY, "sa": 0}])
def img(s, path, left, top, w, h):
    from PIL import Image
    iw, ih = Image.open(path).size; ar = iw / ih
    W = IN(w); H = int(W / ar)
    if H > IN(h): H = IN(h); W = int(H * ar)
    s.shapes.add_picture(path, IN(left)+(IN(w)-W)//2, IN(top)+(IN(h)-H)//2, width=W, height=H)
def table(s, data, left=0.45, top=1.25, w=9.10, colw=None, fs=9.5, rh=0.46, hh=0.38, vc=False):
    nr=len(data); nc=len(data[0]); th=hh+(nr-1)*rh
    if vc: top = 1.15 + max(0,(3.95-th)/2.0)
    gt = s.shapes.add_table(nr,nc,IN(left),IN(top),IN(w),IN(th)).table
    if colw:
        for j,cw in enumerate(colw): gt.columns[j].width=IN(cw)
    gt.rows[0].height=IN(hh)
    for i in range(1,nr): gt.rows[i].height=IN(rh)
    for i,row in enumerate(data):
        for j,val in enumerate(row):
            c=gt.cell(i,j); c.text=str(val); c.vertical_anchor=MSO_ANCHOR.MIDDLE
            c.margin_left=IN(0.05); c.margin_right=IN(0.04); c.margin_top=IN(0.02); c.margin_bottom=IN(0.02)
            c.fill.solid(); c.fill.fore_color.rgb = HDR if i==0 else (ALT if i%2==0 else WHITE)
            for p in c.text_frame.paragraphs:
                p.line_spacing=1.0
                for r in p.runs:
                    r.font.name=F; r.font.size=Pt(fs+0.5 if i==0 else fs)
                    r.font.bold=(i==0); r.font.color.rgb=INK
    return gt

# 1 title
s=slide()
tb=s.shapes.add_textbox(IN(0.7),IN(1.7),IN(8.6),IN(1.4))
tf_fill(tb.text_frame,[{"t":"Classification of waste materials in very-high-resolution satellite imagery","b":True,"sz":30}])
tb2=s.shapes.add_textbox(IN(0.7),IN(3.15),IN(8.6),IN(0.5))
tf_fill(tb2.text_frame,[{"t":"State of the art and thesis proposal","sz":17,"i":True,"c":GREY}])
tb3=s.shapes.add_textbox(IN(0.7),IN(4.5),IN(8.6),IN(0.4))
tf_fill(tb3.text_frame,[{"t":"Alessandro Potenza  ·  M.Sc. Computer Science and Engineering, AI  ·  PERIVALLON","sz":12,"c":GREY}])

# 2 context (text + Torres examples)
s=slide(); title(s,"Context")
body(s,[
 {"t":"Illegal waste dumping is an environmental crime with direct public-health consequences. Agencies (ARPA) have limited inspection capacity, and priority depends on what is dumped: rubble, plastics and asbestos-cement imply very different hazards.","sz":12.5},
 {"t":"Detecting dump sites from images is mature. Recognising the material is not: the reference survey (50 works, 1987-2023, almost all RGB) marks it as an open problem.","sz":12.5},
 {"t":"One thesis in the group has addressed material classification directly (Alari 2024). This work starts from there.","sz":12.5},
], top=1.00, h=1.85, mid=False)
img(s, os.path.join(FIG,"torres_examples.png"), 0.7, 2.95, 8.6, 2.20)
foot(s,"Images: AerialWaste positive examples, Torres and Fraternali 2023 (CC BY 4.0)  ·  survey: Fraternali et al. 2024")

# 3 task (text + IO diagram)
s=slide(); title(s,"Task definition")
body(s,[
 {"t":"Task: multi-label classification of waste materials in satellite images, at image level.","b":True,"sz":12.5},
 {"t":"Input: VHR optical imagery, GSD 0.2 to 1.3 m (aerial RGB baseline; satellite VNIR arm, up to 8 bands). SWIR excluded: not in the planned acquisitions, and its 3.7 m GSD does not match the task. Sentinel-2 excluded: too coarse.","sz":12.5},
 {"t":"Technique: classification, not detection or segmentation. Annotations are image-level (Alari 2024: 11,477 multi-label); waste piles have no stable shape for boxes; no masks exist.","sz":12.5},
 {"t":"Research question: does VNIR input improve waste-material classification over RGB, and for which materials?","b":True,"sz":12.5},
], top=0.95, h=2.15, mid=False)
img(s, os.path.join(FIG,"task_io.png"), 0.85, 3.20, 8.3, 1.95)
foot(s,"Annotations: Alari 2024  ·  imagery: WorldView-3, Pléiades Neo (VNIR + pan)  ·  tile: Alari 2024")

# 4 materials (Alari strip + compact table)
s=slide(); title(s,"Materials: which are considered and why")
img(s, os.path.join(FIG,"alari_row1.png"), 0.85, 0.95, 8.3, 1.66)
table(s,[
 ["Material","Target","Spectral analysis","Reason"],
 ["Rubble, plastic, wood, tires","yes","yes","frequent and confusable in RGB"],
 ["Asbestos-cement","yes","yes, dedicated pilot","public regional ground truth (WFS)"],
 ["Vehicles, tanks, containers, scrap, bulky, big bags","yes","no","shape-based; RGB sufficient in literature"],
 ["Sludge, foundry waste","yes","no","few labels; visually ambiguous at this GSD"],
], left=0.45, top=2.72, w=9.10, colw=[3.4,0.95,1.85,2.9], fs=9, rh=0.44, hh=0.36)
foot(s,"13 categories, taxonomy and samples from Alari 2024 (politesi 10589/230633). Band ablation focuses on the ambiguous subset.")

# 5 search (short text + flow)
s=slide(); title(s,"Literature search: method and numbers")
body(s,[
 {"t":"Scripted queries on the Scopus API (waste detection in remote sensing; asbestos roof mapping), deduplication, manual screening with explicit criteria, snowballing from the Fraternali 2024 survey and the Alari 2024 references.","sz":12.5},
], top=1.05, h=1.0, mid=False)
img(s, os.path.join(FIG,"search_flow.png"), 0.55, 2.15, 8.9, 2.55)
foot(s,"Search artifacts: papers/literature_search (queries, raw and deduplicated records)  ·  library: papers/notes")

# 6 related site-level (table)
s=slide(); title(s,"Related work: site-level waste detection")
table(s,[
 ["Work (year)","Input / GSD","Task","Method","Result"],
 ["Gibellini 2025","aerial RGB, 20 cm","classification","Swin-T, RSP pretraining","F1 92.0; cross-region -5.1"],
 ["Disaitek 2024","Pléiades Neo, 30 cm","detection","operational service","~95% on sites >2 m2 (vendor)"],
 ["CascadeDumpNet 2024","Pléiades, 50 cm","object detection","two-stage CNN + AutoML","mAP 84.6, cross-city transfer"],
 ["Sun 2023","VHR RGB, 0.3-1 m","object detection","BCA-Net (Faster R-CNN)","~2,500 dumpsites, 28 cities"],
 ["CWLD 2024","GF-2 + GE, 0.5-0.8 m","segmentation","DeepLabV3+ variant","F1 88.9, construction waste"],
 ["AerialWaste, Torres 2023","aerial RGB, 20-50 cm","dataset + cls.","ResNet-FPN baseline","F1 80.7; 22 material tags"],
], colw=[2.05,1.85,1.45,1.95,1.80], fs=9, vc=True)
foot(s,"All RGB. They answer where a site is, not what it contains. Disaitek is a vendor figure.")

# 7 related material-level (table + Bonifazi example)
s=slide(); title(s,"Related work: material-level classification")
table(s,[
 ["Work (year)","Input / GSD","Task","Result"],
 ["Alari 2024 (PoliMi)","satellite RGB","multi-label cls.","wF1 69.2 (5 cat.), 59.4 (10 cat.)"],
 ["Saba 2026","WV-3 VNIR, 1.24 m","pixel cls.","asbestos, Macro-F1 97.6"],
 ["Bonifazi 2026","WV-3 VNIR+SWIR","pixel cls.","asbestos roofs, removal tracking"],
 ["Abbasi 2024","aerial RGB","OBIA cls.","asbestos, OA ~96 (shape + time)"],
 ["Cilia 2015","airborne HSI, 3 m","pixel cls.","asbestos, PA 89 / UA 86"],
], left=0.45, top=1.30, w=6.35, colw=[1.75,1.60,1.30,1.70], fs=8.5, rh=0.44, hh=0.36)
img(s, os.path.join(FIG,"bonifazi_example.png"), 7.0, 1.15, 2.55, 3.55)
body(s,[{"t":"One multi-material predecessor (Alari). The rest is asbestos only. Right: building-level asbestos classification on WorldView-3 (Bonifazi 2026).","sz":10.5,"c":GREY}],
     top=4.05, left=0.45, w=6.35, h=1.0, mid=False)
foot(s,"Saba and Abbasi: paywalled or preprint  ·  image: Bonifazi et al. 2026, Geomatics (CC BY 4.0)")

# 8 rgb limits + vnir signatures
s=slide(); title(s,"Where RGB falls short, and what VNIR adds")
body(s,[
 {"t":"Different materials share the same colour at 0.3-1.3 m: plastic sheets, asbestos-cement and concrete all appear grey.","sz":12},
 {"t":"In the group predecessor, moving from 5 to 10 material categories costs 9.8 F1 points (69.2 to 59.4). Finer material distinctions are the hard part.","sz":12},
 {"t":"Red Edge and NIR separate vegetation, bare soil and weathered surfaces; in Saba 2026 they drive asbestos discrimination.","sz":12},
 {"t":"Whether this helps waste materials, and which ones, has not been measured. It is the object of this thesis.","sz":12},
], top=1.15, left=0.45, w=3.85, h=3.90)
img(s, os.path.join(FIG,"vnir_signatures.png"), 4.45, 1.20, 5.15, 3.85)
foot(s,"Reflectance: USGS splib07a (Kokaly et al. 2017), 400-1050 nm. Band centres: Maxar, Airbus.")

# 9 imagery (bands chart + two lines)
s=slide(); title(s,"Available imagery")
img(s, os.path.join(FIG,"bands_chart.png"), 0.55, 1.05, 8.9, 2.85)
body(s,[
 {"t":"Panchromatic: 0.31 m (WorldView-3), 0.30 m (Pléiades Neo). Access: commercial, or free quota via ESA proposal.","sz":12},
 {"t":"This is the band budget of the study: no SWIR, no Sentinel-2. RGB baseline runs on AerialWaste (20-50 cm).","sz":12},
], top=4.05, h=1.05, mid=False)
foot(s,"Band ranges: Maxar WorldView-3, Airbus Pléiades Neo data sheets")

# 10 gaps
s=slide(); title(s,"What is missing in the literature")
body(s,[
 {"t":"1.  Multi-material classification has one direct precedent, with ample margin: wF1 59-69 (Alari 2024)."},
 {"t":"2.  No work measures the added value of VNIR bands over RGB for waste materials at very high resolution."},
 {"t":"3.  Results are reported as aggregate scores; per-material behaviour is not analysed."},
 {"t":"4.  Generalisation across regions is rarely evaluated. At site level it costs 5 F1 points (Gibellini 2025)."},
 {"t":"5.  Asbestos is studied on roofs, in isolation, and never inside a waste-material taxonomy."},
])
foot(s,"Each gap maps to one element of the proposal on the next slide.")

# 11 proposal approach (short text + pipeline)
s=slide(); title(s,"Proposed work: approach")
body(s,[
 {"t":"Multi-label image classification, continuing the group line (Gibellini 2025, Alari 2024). Same taxonomy, input extended from RGB to VNIR.","b":True,"sz":12},
 {"t":"Band ablation with everything else fixed: same architecture, same splits, only the input changes. Asbestos pilot first: public labels, one material, clear VNIR evidence.","sz":12},
], top=0.95, h=1.35, mid=False)
img(s, os.path.join(FIG,"pipeline.png"), 0.55, 2.35, 8.9, 2.60)
foot(s,"Backbone: Swin-T with remote-sensing pretraining (group baseline); extra bands enter via the input layer.")

# 12 evaluation (text + grid)
s=slide(); title(s,"Proposed work: evaluation")
body(s,[
 {"t":"Per-material F1 alongside weighted and macro averages: aggregates hide exactly the classes this thesis targets.","sz":12},
 {"t":"Delta versus the RGB baseline for each band configuration, with confidence intervals over repeated runs.","sz":12},
 {"t":"Generalisation: train and test on disjoint geographic areas, besides the standard split.","sz":12},
 {"t":"Reference points: wF1 69.2 / 59.4 (Alari 2024); Macro-F1 97.6 (Saba 2026, per-pixel) as upper reference for the pilot, not directly comparable.","sz":12},
 {"t":"If VNIR does not help a material, that is a documented negative result with practical value for sensor choice.","sz":12},
], top=1.15, left=0.45, w=4.7, h=3.9)
img(s, os.path.join(FIG,"eval_grid.png"), 5.35, 1.55, 4.25, 2.9)
foot(s,"Metrics: per-class F1, macro-F1, weighted F1, confusion matrices. Splits frozen before testing.")

# 13 references
s=slide(); title(s,"References")
body(s,[
 {"t":"Alari 2024. Fighting environmental crime with deep learning: classifying waste materials from illegal landfills in satellite imagery. M.Sc. thesis, PoliMi, 10589/230633.","sz":11},
 {"t":"Fraternali et al. 2024. Solid waste detection, monitoring and mapping in remote sensing images: a survey. arXiv:2402.09066.","sz":11},
 {"t":"Gibellini et al. 2025. A deep learning pipeline for solid waste detection in remote sensing images. Waste Management Bulletin.","sz":11},
 {"t":"Torres, Fraternali 2023. AerialWaste: a dataset for illegal landfill discovery in aerial images. Scientific Data.","sz":11},
 {"t":"Zhang, Ma 2024. CascadeDumpNet. Remote Sensing of Environment.  ·  Sun et al. 2023. Nature Communications 14.  ·  CWLD 2024. Scientific Data.","sz":11},
 {"t":"Saba et al. 2026. J. Hazardous Materials.  ·  Bonifazi et al. 2026. Geomatics.  ·  Abbasi et al. 2024. RSASE.  ·  Cilia et al. 2015. ISPRS IJGI.","sz":11},
 {"t":"Kokaly et al. 2017. USGS Spectral Library v7 (splib07a). USGS Data Series 1035.  ·  Disaitek 2024, vendor report (Airbus).","sz":11},
])
foot(s,"Full annotated library: 47 papers, papers/INDEX.md")

# page numbers bottom-left
for pos,sl in enumerate(prs.slides,1):
    if pos==1: continue
    tb=sl.shapes.add_textbox(IN(0.10),IN(5.26),IN(0.45),IN(0.28))
    tf=tb.text_frame; tf.word_wrap=False
    p=tf.paragraphs[0]; p.alignment=PP_ALIGN.LEFT
    r=p.add_run(); r.text=str(pos)
    r.font.name=F; r.font.size=Pt(9); r.font.color.rgb=GREY

prs.save(OUT)
import shutil; shutil.copy(OUT, os.path.expanduser("~/Downloads/slide_v7.pptx"))
print("saved", OUT, len(prs.slides.__iter__.__self__._sldIdLst), "slides")
