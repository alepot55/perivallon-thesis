const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.author = "PERIVALLON thesis";
pres.title = "Waste detection from VHR 30-50 cm satellite";

const FONT = "Arial";
const INK = "111111";
const BODY = "2E2E2E";
const MUTE = "6E6E6E";
const FAINT = "9C9C9C";
const CARD = "F5F5F5";
const CARDLINE = "E8E8E8";
const GAPFILL = "E6E6E6";
const GAPLINE = "D6D6D6";
const W = 13.33, ML = 0.7, MR = 12.63, CW = MR - ML; // content width

// ---------- helpers ----------
function footer(slide, right) {
  slide.addText("PERIVALLON thesis  ·  waste detection from VHR 30–50 cm satellite", {
    x: ML, y: 7.14, w: 8.6, h: 0.3, fontSize: 8.5, color: FAINT, fontFace: FONT, margin: 0, valign: "middle"
  });
  if (right) slide.addText(right, {
    x: 9.4, y: 7.14, w: MR - 9.4, h: 0.3, fontSize: 8.5, color: FAINT, fontFace: FONT, align: "right", margin: 0, valign: "middle"
  });
}

function verdictBadge(slide, label, tier) {
  const x = MR - 2.15, y = 0.6, w = 2.15, h = 0.5;
  let fill, line, col;
  if (tier === "served") { fill = INK; line = { color: INK, width: 1 }; col = "FFFFFF"; }
  else if (tier === "partial") { fill = "FFFFFF"; line = { color: INK, width: 1.25 }; col = INK; }
  else { fill = GAPFILL; line = { color: GAPLINE, width: 1 }; col = "222222"; }
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line, rectRadius: 0.06 });
  slide.addText(label, { x, y, w, h, fontSize: 13, bold: true, color: col, fontFace: FONT, align: "center", valign: "middle", charSpacing: 1.5, margin: 0 });
}

function statusPill(slide, rightEdge, yTop, status) {
  const map = {
    yes: { t: "YES", w: 0.66, fill: INK, col: "FFFFFF", line: null },
    no: { t: "NO", w: 0.62, fill: GAPFILL, col: "3A3A3A", line: { color: GAPLINE, width: 0.75 } },
    na: { t: "N/A", w: 0.66, fill: "F0F0F0", col: "8A8A8A", line: { color: "E2E2E2", width: 0.75 } },
    partial: { t: "PARTIAL", w: 1.0, fill: "FFFFFF", col: INK, line: { color: INK, width: 1 } },
  };
  const s = map[status]; if (!s) return;
  const x = rightEdge - s.w, h = 0.32;
  const opt = { x, y: yTop, w: s.w, h, fill: { color: s.fill }, rectRadius: 0.05 };
  if (s.line) opt.line = s.line;
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, opt);
  slide.addText(s.t, { x, y: yTop, w: s.w, h, fontSize: 9.5, bold: true, color: s.col, fontFace: FONT, align: "center", valign: "middle", charSpacing: 1, margin: 0 });
}

function card(slide, x, y, w, h, label, status, text, emphasis) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: emphasis ? "FFFFFF" : CARD },
    line: emphasis ? { color: INK, width: 1.25 } : { color: CARDLINE, width: 1 },
    rectRadius: 0.07
  });
  const pad = 0.27;
  if (status) statusPill(slide, x + w - 0.22, y + 0.17, status);
  slide.addText(label, {
    x: x + pad, y: y + 0.19, w: w - (status ? 1.4 : 0.5), h: 0.3,
    fontSize: 10.5, bold: true, color: emphasis ? INK : MUTE, fontFace: FONT, charSpacing: 1.4, margin: 0, valign: "middle"
  });
  slide.addText(text, {
    x: x + pad, y: y + 0.62, w: w - 2 * pad, h: h - 0.82,
    fontSize: emphasis ? 14 : 13.5, color: emphasis ? INK : BODY, fontFace: FONT,
    valign: "top", margin: 0, lineSpacingMultiple: 1.05
  });
}

function listCard(slide, x, y, w, h, header, sub, items, emphasis) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: emphasis ? "FFFFFF" : CARD },
    line: emphasis ? { color: INK, width: 1.25 } : { color: CARDLINE, width: 1 },
    rectRadius: 0.07
  });
  const pad = 0.34;
  slide.addText(header, { x: x + pad, y: y + 0.28, w: w - 2 * pad, h: 0.4, fontSize: 15, bold: true, color: INK, fontFace: FONT, charSpacing: 1, margin: 0, valign: "middle" });
  if (sub) slide.addText(sub, { x: x + pad, y: y + 0.7, w: w - 2 * pad, h: 0.3, fontSize: 11.5, color: MUTE, fontFace: FONT, margin: 0, valign: "middle" });
  const runs = items.map((it, i) => ({ text: it, options: { bullet: { indent: 16 }, breakLine: true, paraSpaceAfter: 7, color: emphasis ? INK : BODY } }));
  slide.addText(runs, { x: x + pad, y: y + (sub ? 1.08 : 0.78), w: w - 2 * pad, h: h - (sub ? 1.3 : 1.0), fontSize: 14.5, fontFace: FONT, valign: "top" });
}

function header(slide, num, name, type, badge) {
  slide.addText(num, { x: ML, y: 0.5, w: 1.15, h: 0.95, fontSize: 46, bold: true, color: "CFCFCF", fontFace: FONT, margin: 0, valign: "middle" });
  slide.addText(name, { x: 1.92, y: 0.55, w: 8.0, h: 0.6, fontSize: 26, bold: true, color: INK, fontFace: FONT, margin: 0, valign: "middle" });
  slide.addText(type, { x: 1.94, y: 1.16, w: 8.0, h: 0.3, fontSize: 12, color: MUTE, fontFace: FONT, margin: 0, valign: "middle", charSpacing: 0.5 });
  verdictBadge(slide, badge.label, badge.tier);
}

// 2x2 card grid geometry
const COLW = (CW - 0.32) / 2;        // 5.755
const COL1 = ML, COL2 = ML + COLW + 0.32;
const ROW1 = 1.95, ROWH = 2.15, ROW2 = ROW1 + ROWH + 0.3; // 4.40

function classSlide(d) {
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  header(s, d.num, d.name, d.type, d.badge);
  const c = d.cards;
  card(s, COL1, ROW1, COLW, ROWH, c[0].label, c[0].status, c[0].text, false);
  card(s, COL2, ROW1, COLW, ROWH, c[1].label, c[1].status, c[1].text, false);
  card(s, COL1, ROW2, COLW, ROWH, c[2].label, c[2].status, c[2].text, false);
  card(s, COL2, ROW2, COLW, ROWH, c[3].label, c[3].status, c[3].text, true);
  s.addText("Sources  ·  " + d.sources, { x: ML, y: 6.72, w: CW, h: 0.3, fontSize: 9, color: MUTE, fontFace: FONT, margin: 0, valign: "middle" });
  footer(s, "Class " + parseInt(d.num, 10) + " / 13");
}

// ---------- Slide 1: title ----------
(function () {
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  s.addText("PERIVALLON THESIS  ·  2026-06", { x: ML, y: 0.75, w: 8, h: 0.35, fontSize: 12, color: MUTE, fontFace: FONT, charSpacing: 2.5, margin: 0 });
  s.addText("Detecting waste materials from\n30–50 cm satellite imagery", { x: ML, y: 1.7, w: 11.4, h: 1.9, fontSize: 42, bold: true, color: INK, fontFace: FONT, margin: 0, lineSpacingMultiple: 1.02 });
  s.addText("What the literature delivers for our 13 target classes, by satellite and by drone.", { x: ML, y: 3.75, w: 10.5, h: 0.5, fontSize: 18, color: BODY, fontFace: FONT, margin: 0 });
  s.addText("Input = VHR 30–50 cm broadband VNIR (no SWIR)  ·  resolution-first", { x: ML, y: 4.35, w: 10, h: 0.4, fontSize: 13, color: MUTE, fontFace: FONT, margin: 0 });

  // 13-square status motif
  const served = [1, 3, 5, 6, 8, 11, 12], partial = [4, 9, 13], gap = [2, 7, 10];
  const sq = 0.44, g = 0.13, y0 = 5.45, x0 = ML;
  for (let i = 1; i <= 13; i++) {
    const x = x0 + (i - 1) * (sq + g);
    let opt = { x, y: y0, w: sq, h: sq, rectRadius: 0.04 };
    if (served.includes(i)) { opt.fill = { color: INK }; }
    else if (partial.includes(i)) { opt.fill = { color: "FFFFFF" }; opt.line = { color: INK, width: 1.25 }; }
    else { opt.fill = { color: GAPFILL }; opt.line = { color: GAPLINE, width: 1 }; }
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, opt);
    s.addText(String(i), { x, y: y0 + sq + 0.04, w: sq, h: 0.22, fontSize: 8, color: FAINT, fontFace: FONT, align: "center", margin: 0 });
  }
  s.addText("7 served   ·   3 partial (presence yes, material needs SWIR)   ·   3 gap", { x: ML, y: 6.4, w: 11, h: 0.3, fontSize: 11, color: MUTE, fontFace: FONT, margin: 0 });
  footer(s, "Overview");
})();

// ---------- Slide 2: the rule ----------
(function () {
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  s.addText("The rule that decides feasibility", { x: ML, y: 0.6, w: 11, h: 0.6, fontSize: 30, bold: true, color: INK, fontFace: FONT, margin: 0 });
  s.addText("At 30–50 cm broadband VNIR, a class is feasible when its identity lives in shape and context, and weak when it lives in spectral chemistry.", { x: ML, y: 1.4, w: 11.6, h: 0.6, fontSize: 15, color: BODY, fontFace: FONT, margin: 0, lineSpacingMultiple: 1.05 });

  const y = 2.45, h = 3.45;
  listCard(s, COL1, y, COLW, h, "DETECTABLE", "object  ·  shape",
    ["Vehicles", "Tanks and cisterns", "Containers and skips", "Rubble heaps", "Bulky items", "Firewood", "Tires (piles)", "Big bags"], true);
  listCard(s, COL2, y, COLW, h, "WEAK AT BROADBAND VHR", "material  ·  spectral chemistry",
    ["Asbestos (mineral identity)", "Plastic polymer type", "Foundry slag", "Sludge composition", "Scrap metal composition"], false);

  s.addText("Confirmed independently by the Waste Management RS survey (2024) and the Gibellini (2025) review.", { x: ML, y: 6.05, w: CW, h: 0.3, fontSize: 11, color: MUTE, fontFace: FONT, margin: 0 });
  footer(s, "The decision rule");
})();

// ---------- Slide 3: prior work ----------
(function () {
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  s.addText("Who already detects this from satellite", { x: ML, y: 0.6, w: 11.6, h: 0.6, fontSize: 30, bold: true, color: INK, fontFace: FONT, margin: 0 });
  s.addText("Every system finds aggregate dumpsites or binary waste by shape. None resolves per-class material.", { x: ML, y: 1.36, w: 11.6, h: 0.35, fontSize: 14, color: MUTE, fontFace: FONT, margin: 0 });

  const head = ["Work (year)", "Platform / GSD", "Method", "Result"];
  const rows = [
    ["Gibellini 2025", "VHR <50 cm (WV-3, GE, AGEA)", "Swin-T + RSP, binary", "F1 92.0% / Acc 94.6%"],
    ["CascadeDumpNet 2024", "Pléiades 0.5 m", "CNN detection + AutoML", "84.6% mAP, transferable"],
    ["Sun 2023", "Gaofen / SuperView 0.3–1 m", "CNN + channel attention", "~1000 dumpsites, 15 countries"],
    ["AerialWaste 2023", "WV-3 0.3 m + GE 0.5 m", "ResNet-50 + FPN, binary", "AP 88.0% / 94.5% (0.2 m)"],
    ["Disaitek + Airbus 2024", "Pléiades Neo 30 cm", "AI semantic segmentation", "waste ≥2 m² at ~95% (operational)"],
  ];
  const headRow = head.map(t => ({ text: t, options: { fill: { color: INK }, color: "FFFFFF", bold: true, fontSize: 13, align: "left", valign: "middle" } }));
  const body = rows.map((r, i) => r.map((t, j) => ({ text: t, options: { fill: { color: i % 2 ? "FFFFFF" : "FAFAFA" }, color: j === 0 ? INK : BODY, bold: j === 0, fontSize: 12, valign: "middle" } })));
  s.addTable([headRow, ...body], {
    x: ML, y: 1.9, w: CW, colW: [2.65, 3.25, 3.0, 3.03],
    border: { pt: 0.75, color: "E6E6E6" }, rowH: 0.62, margin: [0.06, 0.12, 0.06, 0.12], fontFace: FONT, valign: "middle"
  });
  s.addText("Disaitek/Airbus is a vendor claim. It qualifies type at 30 cm: end-of-life vehicles, construction waste, tires, vegetal waste.", { x: ML, y: 6.55, w: CW, h: 0.3, fontSize: 11, color: MUTE, fontFace: FONT, margin: 0 });
  footer(s, "Prior work");
})();

// ---------- Slides 4-16: 13 classes ----------
const classes = [
  {
    num: "01", name: "Rubble / C&D debris", type: "Object  ·  shape", badge: { label: "STRONG", tier: "served" },
    cards: [
      { label: "SATELLITE", status: "yes", text: "CWLD on GF-2 80 cm + Google Earth 50 cm, improved DeepLabV3+, F1 88.9% / IoU 82% (Beijing 2024). Yong DeepLabv3+ 1 m, F1 77.4%. Disaitek 30 cm." },
      { label: "DRONE", status: "yes", text: "FCN + structure-from-motion, IoU 0.9 on concrete, with volume estimation (Drones 2022)." },
      { label: "METHOD", status: null, text: "Semantic segmentation and object detection." },
      { label: "VERDICT", status: null, text: "Strong at 30–50 cm. Recognised as heap morphology." },
    ],
    sources: "CWLD 2024  ·  Yong (in Gibellini 2025)  ·  Cheng et al., Drones 2022",
  },
  {
    num: "02", name: "Foundry waste / slag", type: "Material  ·  spectrum", badge: { label: "GAP", tier: "gap" },
    cards: [
      { label: "SATELLITE", status: "no", text: "No dedicated detector. Present only as AerialWaste annotations (9 labels, the rarest class)." },
      { label: "DRONE", status: "no", text: "Composition studied only at close-range hyperspectral (EJRS 2015)." },
      { label: "METHOD", status: null, text: "None at VHR. Spectral phase-mapping in lab only." },
      { label: "VERDICT", status: null, text: "Gap. Spectral problem plus extreme data scarcity. Weakest class." },
    ],
    sources: "Torres & Fraternali 2023  ·  Iron/steel by-products, Eur. J. Remote Sensing 2015",
  },
  {
    num: "03", name: "Vehicles / end-of-life vehicles", type: "Object  ·  shape", badge: { label: "EXCELLENT", tier: "served" },
    cards: [
      { label: "SATELLITE", status: "yes", text: "Region-based detector + domain adaptation (+10%, RS 2020). Heavy-duty truck classification (2025). Disaitek qualifies ELV at 30 cm." },
      { label: "DRONE", status: "yes", text: "Standard UAV vehicle detection." },
      { label: "METHOD", status: null, text: "Object detection (region-based, YOLO-family)." },
      { label: "VERDICT", status: null, text: "Excellent at 30–50 cm. Generic vehicles mature; a scrapyard-ELV detector is a sub-gap." },
    ],
    sources: "Koga et al., RS 2020  ·  heavy-duty truck PMC 2025  ·  Disaitek/Airbus 2024",
  },
  {
    num: "04", name: "Scrap metal", type: "Object + material", badge: { label: "PARTIAL", tier: "partial" },
    cards: [
      { label: "SATELLITE", status: "partial", text: "Scrapyard scenes detectable (AerialWaste, 167 labels). Metal type is not." },
      { label: "DRONE", status: "no", text: "No remote detector. Composition needs close-range infrared (Hybrid-YOLOv5 ELV non-ferrous, 84.2% mAP, not remote sensing)." },
      { label: "METHOD", status: null, text: "Scene classification. Composition needs spectral / close-range." },
      { label: "VERDICT", status: null, text: "Scenes yes; metal composition is a gap." },
    ],
    sources: "Torres & Fraternali 2023  ·  Hybrid-YOLOv5, Scientific Reports 2025",
  },
  {
    num: "05", name: "Bulky items (ingombranti)", type: "Object  ·  shape", badge: { label: "GOOD", tier: "served" },
    cards: [
      { label: "SATELLITE", status: "yes", text: "AerialWaste, 286 labels (2nd most frequent class)." },
      { label: "DRONE", status: "partial", text: "Large-area UAV solid-waste segmentation (~450 km², >94% OA), but as a generic 'waste pile' class." },
      { label: "METHOD", status: null, text: "Scene classification and semantic segmentation." },
      { label: "VERDICT", status: null, text: "Good at 30–50 cm as an object. No per-type breakdown." },
    ],
    sources: "Torres & Fraternali 2023  ·  Liu et al., Applied Sciences 14:2084, 2024",
  },
  {
    num: "06", name: "Containers / skips", type: "Object  ·  shape", badge: { label: "STRONG", tier: "served" },
    cards: [
      { label: "SATELLITE", status: "yes", text: "CenterNet + Mask R-CNN ensemble classifies container size and status. Satellogic ~90% counting at 0.7 m. AerialWaste 167 labels." },
      { label: "DRONE", status: "na", text: "Not specifically needed." },
      { label: "METHOD", status: null, text: "Object detection and instance segmentation." },
      { label: "VERDICT", status: null, text: "Strong at 30–50 cm as an object." },
    ],
    sources: "Heavy-duty/container detection PMC  ·  Satellogic 2023  ·  Torres & Fraternali 2023",
  },
  {
    num: "07", name: "Sludge (fanghi)", type: "Material  ·  context", badge: { label: "GAP", tier: "gap" },
    cards: [
      { label: "SATELLITE", status: "no", text: "No dedicated detector. Only tailings-pond analogues (SSD on Gaofen-1, 90.2% acc). AerialWaste 19 labels." },
      { label: "DRONE", status: "no", text: "No detector." },
      { label: "METHOD", status: null, text: "Context and colour. Composition is spectral." },
      { label: "VERDICT", status: null, text: "Gap. Lagoons visible by context; composition not classifiable at broadband VHR." },
    ],
    sources: "Yang et al., RS 12:2626, 2020 (tailings analogue)  ·  Torres & Fraternali 2023",
  },
  {
    num: "08", name: "Wood and firewood", type: "Object  ·  shape", badge: { label: "GOOD", tier: "served" },
    cards: [
      { label: "SATELLITE", status: "yes", text: "AerialWaste, 173 labels (4th most frequent class)." },
      { label: "DRONE", status: "partial", text: "Woody-debris volume estimation is airborne." },
      { label: "METHOD", status: null, text: "Scene classification." },
      { label: "VERDICT", status: null, text: "Good at 30–50 cm. Stacked-pile morphology." },
    ],
    sources: "Torres & Fraternali 2023",
  },
  {
    num: "09", name: "Plastic", type: "Material  ·  spectrum", badge: { label: "PARTIAL", tier: "partial" },
    cards: [
      { label: "SATELLITE", status: "partial", text: "Morphological only at 30–50 cm (WV-3 anomaly; Pléiades + S-2 index). True spectral plastic only at Sentinel-2 10 m (out of scope)." },
      { label: "DRONE", status: "yes", text: "UAV-SWIR Attention-U-Net 96.8% acc / 91.1% F1 (2026). UAV-RGB + IoT 92% on rivers (2025)." },
      { label: "METHOD", status: null, text: "Index/anomaly at VHR. Deep segmentation on UAV-SWIR for polymer type." },
      { label: "VERDICT", status: null, text: "Presence and extent at VHR. Polymer identity needs SWIR, so drone-HSI." },
    ],
    sources: "UAV-SWIR U-Net RS 18:182, 2026  ·  UAV+IoT J.Haz.Mat.Adv. 2025",
  },
  {
    num: "10", name: "Big bags (FIBC)", type: "Object  ·  shape  ·  small", badge: { label: "NEAR-GAP", tier: "gap" },
    cards: [
      { label: "SATELLITE", status: "partial", text: "Marginal. Only AerialWaste (50 labels). A ~1 m³ bag is roughly 3×3 px at 30 cm." },
      { label: "DRONE", status: "no", text: "No dedicated detector." },
      { label: "METHOD", status: null, text: "None specific." },
      { label: "VERDICT", status: null, text: "Near-gap. An object, but at the resolution limit and data-scarce." },
    ],
    sources: "Torres & Fraternali 2023",
  },
  {
    num: "11", name: "Tanks / cisterns", type: "Object  ·  shape", badge: { label: "EXCELLENT", tier: "served" },
    cards: [
      { label: "SATELLITE", status: "yes", text: "YOLOv7-OT 90% acc / 95.9% prec (2024). Ramachandran et al. precision 0.962 / recall 0.968, >169k tanks (Nature Comm. 2024)." },
      { label: "DRONE", status: "na", text: "Not specifically needed." },
      { label: "METHOD", status: null, text: "Object detection (circular tank tops)." },
      { label: "VERDICT", status: null, text: "Excellent, and not a gap. Correction vs the first matrix." },
    ],
    sources: "YOLOv7-OT RS 16:4510, 2024  ·  Ramachandran et al., Nature Communications 2024",
  },
  {
    num: "12", name: "Tires", type: "Object + spectral", badge: { label: "GOOD", tier: "served" },
    cards: [
      { label: "SATELLITE", status: "yes", text: "TIRe model on QuickBird 0.6 m for piles (≥100–400 tires). Disaitek qualifies tires at 30 cm. AerialWaste 45 labels." },
      { label: "DRONE", status: "partial", text: "Partial coverage." },
      { label: "METHOD", status: null, text: "Reflectance / decision-tree plus object detection." },
      { label: "VERDICT", status: null, text: "Good for piles. Dark targets confuse with shadow and water." },
    ],
    sources: "TIRe model (CIWMB/NASA NTRS)  ·  Disaitek/Airbus 2024  ·  Torres & Fraternali 2023",
  },
  {
    num: "13", name: "Asbestos-cement roofing", type: "Material  ·  spectrum", badge: { label: "PARTIAL", tier: "partial" },
    cards: [
      { label: "SAT + SWIR", status: "yes", text: "Bonifazi 2026 WV-3 VNIR+SWIR, MLC building-level (Mantua, open Python). Saba WV-3 8-VNIR, Macro-F1 97.6%. EnMAP 30 m ACE 91.4% (out of scope)." },
      { label: "SAT / AERIAL, NO SWIR", status: "partial", text: "Abbasi 2024 Nearmap aerial, DenseNet+LSTM multi-temporal, OA 95.8–96.0%, AC 94% (at ≤25 cm aerial)." },
      { label: "DRONE", status: "yes", text: "Asbestos-slate drone-RGB DL training data (2023)." },
      { label: "VERDICT", status: null, text: "Corrugated shape detectable at 30–50 cm. Material confirmation needs SWIR (≥1.2 m WV-3) or very fine VHR plus temporal." },
    ],
    sources: "Bonifazi Geomatics 6:41, 2026  ·  Saba 2026  ·  Abbasi RSASE 2024  ·  Shepherd Sci.Rep. 2025",
  },
];
classes.forEach(classSlide);

// ---------- Slide 17: all 13 at a glance ----------
(function () {
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  s.addText("All 13 classes at a glance", { x: ML, y: 0.55, w: 11, h: 0.6, fontSize: 30, bold: true, color: INK, fontFace: FONT, margin: 0 });
  s.addText("✓ served      ◐ partial / morphology-only      ✗ gap      – not needed", { x: ML, y: 1.3, w: 11.6, h: 0.32, fontSize: 12, color: MUTE, fontFace: FONT, margin: 0 });

  const G = { "✓": INK, "◐": "555555", "✗": "AEAEAE", "–": "C8C8C8" };
  const data = [
    ["1", "Rubble / C&D", "✓", "✓", "Heap morphology, strong"],
    ["2", "Foundry slag", "✗", "✗", "Gap, spectral and data-starved"],
    ["3", "Vehicles / ELV", "✓", "✓", "Object, excellent (ELV sub-gap)"],
    ["4", "Scrap metal", "◐", "✗", "Scenes yes; composition gap"],
    ["5", "Bulky items", "✓", "◐", "Object, good"],
    ["6", "Containers", "✓", "–", "Object, strong"],
    ["7", "Sludge", "✗", "✗", "Gap, context only"],
    ["8", "Wood / firewood", "✓", "◐", "Pile morphology, good"],
    ["9", "Plastic", "◐", "✓", "Presence at VHR; type needs SWIR"],
    ["10", "Big bags", "◐", "✗", "Near-gap, small and scarce"],
    ["11", "Tanks / cisterns", "✓", "–", "Object, excellent"],
    ["12", "Tires", "✓", "◐", "Piles, good (dark-target)"],
    ["13", "Asbestos", "✓", "✓", "Shape yes; material needs SWIR"],
  ];
  const head = ["#", "Class", "Sat", "Drone", "Verdict at 30–50 cm"].map(t => ({ text: t, options: { fill: { color: INK }, color: "FFFFFF", bold: true, fontSize: 12, valign: "middle", align: (t === "Sat" || t === "Drone") ? "center" : "left" } }));
  const body = data.map((r, i) => {
    const bg = i % 2 ? "FFFFFF" : "FAFAFA";
    return [
      { text: r[0], options: { fill: { color: bg }, color: MUTE, fontSize: 11.5, valign: "middle" } },
      { text: r[1], options: { fill: { color: bg }, color: INK, bold: true, fontSize: 11.5, valign: "middle" } },
      { text: r[2], options: { fill: { color: bg }, color: G[r[2]], bold: true, fontSize: 14, align: "center", valign: "middle" } },
      { text: r[3], options: { fill: { color: bg }, color: G[r[3]], bold: true, fontSize: 14, align: "center", valign: "middle" } },
      { text: r[4], options: { fill: { color: bg }, color: BODY, fontSize: 11.5, valign: "middle" } },
    ];
  });
  s.addTable([head, ...body], {
    x: ML, y: 1.75, w: CW, colW: [0.55, 3.0, 0.9, 0.95, 6.5],
    border: { pt: 0.75, color: "ECECEC" }, rowH: 0.355, margin: [0.04, 0.12, 0.04, 0.12], fontFace: FONT, valign: "middle"
  });
  footer(s, "Summary matrix");
})();

// ---------- Slide 18: gaps + thesis space ----------
(function () {
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  s.addText("The gaps, and the thesis space", { x: ML, y: 0.55, w: 11.6, h: 0.6, fontSize: 30, bold: true, color: INK, fontFace: FONT, margin: 0 });

  const y = 1.45, h = 2.45;
  listCard(s, COL1, y, COLW, h, "NO DEDICATED VHR DETECTOR", "satellite or drone",
    ["Foundry slag (2)", "Sludge (7)", "Big bags (10)", "Scrap metal composition (4)"], false);
  listCard(s, COL2, y, COLW, h, "SERVED ONLY WITH SWIR", "presence yes, material conditional",
    ["Asbestos material (13): WV-3 ≥1.2 m + SWIR, EnMAP 30 m, or ≤25 cm aerial", "Plastic polymer type (9): presence at 30–50 cm, identity needs SWIR"], false);

  // dark callout for the thesis contribution space
  const cy = 4.18, ch = 1.55;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: ML, y: cy, w: CW, h: ch, fill: { color: INK }, line: { color: INK, width: 1 }, rectRadius: 0.07 });
  s.addText("THE EMPTY CELL", { x: ML + 0.4, y: cy + 0.22, w: CW - 0.8, h: 0.3, fontSize: 11, bold: true, color: "BFBFBF", fontFace: FONT, charSpacing: 2, margin: 0 });
  s.addText([
    { text: "The whole field is binary or aggregate. No public per-class 13-material detector exists at the VHR satellite operating point. ", options: { color: "E8E8E8" } },
    { text: "This empty cell is the thesis contribution space.", options: { color: "FFFFFF", bold: true } },
  ], { x: ML + 0.4, y: cy + 0.55, w: CW - 0.8, h: 0.9, fontSize: 16, fontFace: FONT, valign: "top", margin: 0, lineSpacingMultiple: 1.08 });

  s.addText("Correction vs the first matrix: tanks (11) are well-served, not a gap.", { x: ML, y: 6.05, w: CW, h: 0.3, fontSize: 11.5, color: MUTE, fontFace: FONT, margin: 0 });
  footer(s, "Gaps and contribution");
})();

pres.writeFile({ fileName: "vhr_13classes_deck.pptx" }).then(f => console.log("written", f));
