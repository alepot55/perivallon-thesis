# -*- coding: utf-8 -*-
"""Discorso per deck v7 (13 slide). HTML -> PDF via wkhtmltopdf."""
import subprocess, os
OUT_HTML="/home/alepot55/.claude/jobs/49614db0/tmp/discorso_v7.html"
OUT_PDF="/home/alepot55/Desktop/uni/Tesi/assets/deck_v7/discorso_v7.pdf"

S=[
(1,"Titolo",
 "Buongiorno. Presento lo stato dell'arte e la proposta di tesi: classificazione dei materiali di rifiuto in immagini satellitari ad altissima risoluzione, dentro PERIVALLON.",
 "Dire subito 'rifiuti illegali / discariche abusive'.",
 "Parto dal contesto, in breve."),
(2,"Context",
 "Lo smaltimento illegale è un crimine ambientale con conseguenze sanitarie. Le agenzie come ARPA hanno capacità di ispezione limitata, e la priorità dipende da cosa è stato sversato: macerie, plastiche e cemento-amianto sono pericoli molto diversi. Rilevare i siti è ormai maturo; riconoscere il materiale no: la survey di riferimento conta 50 lavori dal 1987 al 2023, quasi tutti RGB, e indica l'identificazione del materiale come problema aperto. Nel gruppo una tesi ha già affrontato il tema, quella di Alari: questo lavoro parte da lì.",
 "Survey: 50 lavori, quasi tutti RGB. Alari = predecessore nel gruppo.",
 "Quindi, in una slide, il task."),
(3,"Task definition",
 "Il task: classificazione multi-label dei materiali di rifiuto, a livello di immagine. Input: immagini ottiche ad altissima risoluzione, da 0,2 a 1,3 metri; RGB aereo per la baseline, VNIR satellitare per il braccio multispettrale. Lo SWIR è escluso: non è nelle acquisizioni previste, e comunque a 3,7 metri non è compatibile col task. Sentinel-2 escluso: troppo grossolano. Perché classificazione e non detection o segmentazione? Le annotazioni disponibili sono a livello di immagine, oltre 11.400 multi-label; i cumuli non hanno forma stabile per le box, e non esistono maschere. La domanda di ricerca: il VNIR multispettrale migliora la classificazione rispetto all'RGB, e per quali materiali?",
 "Tecnica = classificazione, giustificata dalle annotazioni. GSD 0,2-1,3 m. No SWIR, no S-2.",
 "Su quali materiali, di preciso?"),
(4,"Materials",
 "I 13 materiali della tassonomia di Alari, uno per uno. Tutti restano target di classificazione, per continuità col dataset del gruppo. L'analisi spettrale RGB-contro-VNIR si concentra sul sottoinsieme ambiguo: macerie, plastica, legno, pneumatici, e cemento-amianto come pilot dedicato perché ha ground truth pubblico regionale. Veicoli, cisterne e container si riconoscono dalla forma, l'RGB basta secondo la letteratura. Fanghi e scorie di fonderia restano nel set ma fuori dall'analisi spettrale: poche etichette e classi visivamente ambigue a questa risoluzione.",
 "Tutti e 13 target; ablazione su 5 ambigui; amianto = pilot con GT pubblico.",
 "Come ho costruito la bibliografia."),
(5,"Literature search",
 "La ricerca è stata fatta con query scriptate sulle API di Scopus, due insiemi di query: rilevamento rifiuti in remote sensing, e mappatura tetti in amianto. Dopo la deduplica: 699 record unici, 622 waste e 77 asbestos. Screening per pertinenza al task, risoluzione compatibile, recency e citazioni, peer review; più snowballing dalla survey di Fraternali e dai riferimenti della tesi di Alari. Il risultato è una libreria curata di 47 paper con note strutturate, sincronizzata con l'Excel del team. In queste slide ne cito 13.",
 "699 → 47 → 13 citati. Se chiedono dell'AI: le query sono scriptate, lo screening è manuale, gli strumenti AI li ho usati per organizzare le note.",
 "Cosa dice questa letteratura: prima i siti."),
(6,"Related work: site-level",
 "Il rilevamento dei siti. Gibellini, la baseline del gruppo: F1 92 su AerialWaste, ma meno 5,1 punti cross-region. Disaitek, servizio operativo su Pléiades Neo, dato del vendor. CascadeDumpNet, object detection su Pléiades a 50 centimetri, mAP 84,6 con trasferimento tra città. Sun, 2.500 discariche in 28 città. CWLD, segmentazione su rifiuti da costruzione. AerialWaste, il dataset, con 22 tag di materiale. Tutti RGB: rispondono a dove è un sito, non a cosa contiene.",
 "Colonna Task pronta per la domanda 'che task è': classification / object detection / segmentation per riga.",
 "E sul materiale?"),
(7,"Related work: material-level",
 "Sul materiale la letteratura è più sottile, ma non vuota. Il predecessore diretto è la tesi di Alari nel gruppo: multi-label su 13 categorie, weighted F1 69,2 su 5 categorie e 59,4 su 10. Il resto è quasi tutto amianto: Saba su WorldView-3 solo VNIR arriva a Macro-F1 97,6 per-pixel; Bonifazi fa monitoraggio multi-temporale; Abbasi lavora da aereo RGB con la dimensione temporale; Cilia nel 2015 da iperspettrale aereo. Saba e Abbasi sono paywalled o preprint, li riporto come tali.",
 "Alari 69,2/59,4 = margine ampio. Amianto: forte evidenza VNIR (Saba 97,6 per-pixel).",
 "Perché l'RGB non basta, e cosa aggiunge il VNIR."),
(8,"RGB limits, VNIR",
 "Materiali diversi hanno lo stesso colore a queste risoluzioni: teli di plastica, cemento-amianto e cemento appaiono grigi. Nel predecessore, passare da 5 a 10 categorie costa quasi 10 punti di F1: sono le distinzioni fini la parte difficile. Red Edge e NIR separano vegetazione, suolo nudo e superfici degradate; in Saba guidano la discriminazione dell'amianto. Se questo aiuti i materiali di rifiuto, e quali, non è stato misurato: è l'oggetto della tesi. Il grafico mostra le firme reali nella finestra 400-1050 nanometri, con le bande dei due sensori.",
 "Curve limitate al VNIR (400-1050), coerenti con lo scope. Non addentrarsi nella fisica.",
 "Con che dati, in concreto."),
(9,"Available imagery",
 "Una sola slide sui sensori. WorldView-3: 8 bande VNIR a 1,24 metri, pancromatico a 31 centimetri. Pléiades Neo: 6 bande a 1,2 metri, pan a 30. Rispetto a RGB più NIR, WorldView-3 aggiunge Coastal, Yellow, Red Edge e un secondo NIR; Pléiades Neo aggiunge Deep Blue e Red Edge. Questo è il budget di bande dello studio: niente SWIR, niente Sentinel-2.",
 "Riassunto in 1 slide, subito dopo i limiti RGB, come chiesto.",
 "Cosa manca quindi in letteratura."),
(10,"Gaps",
 "Cinque mancanze. Uno: la classificazione multi-materiale ha un solo precedente diretto, con margine ampio. Due: nessuno misura il valore aggiunto delle bande VNIR rispetto all'RGB per i materiali di rifiuto ad altissima risoluzione. Tre: i risultati sono aggregati, il comportamento per materiale non viene analizzato. Quattro: la generalizzazione tra regioni è raramente valutata, e già a livello di sito costa 5 punti. Cinque: l'amianto è studiato sui tetti, isolato, mai dentro una tassonomia di rifiuti.",
 "Ogni gap mappa su un elemento della proposta: dirlo esplicitamente.",
 "Da qui la proposta."),
(11,"Proposal: approach",
 "La tecnica è classificazione multi-label di immagini, in continuità con Gibellini e Alari. Backbone Swin-T con pretraining remote sensing, la baseline del gruppo; le bande VNIR extra entrano estendendo il layer di input della rete pre-addestrata. Dati: AerialWaste con le annotazioni di Alari come baseline RGB; acquisizioni WorldView-3 e Pléiades Neo per il braccio multispettrale; il registro amianto della Lombardia, 10.903 tetti, come ground truth per un pilot controllato. Ablazione: RGB, poi RGB più NIR, poi VNIR completo, stessa architettura e stessi split. Il pilot amianto va per primo: etichette pubbliche, un solo materiale, evidenza VNIR chiara in letteratura.",
 "Tecnica dichiarata + perché. Pilot amianto = de-risking della pipeline.",
 "E come misuro."),
(12,"Proposal: evaluation",
 "F1 per materiale, oltre alle medie pesata e macro: gli aggregati nascondono proprio le classi che ci interessano. Delta rispetto alla baseline RGB per ogni configurazione di bande, con intervalli di confidenza su run ripetute. Protocollo di generalizzazione: train e test su aree geografiche disgiunte, oltre allo split standard. Punti di riferimento: 69,2 e 59,4 di Alari per il multi-label; il 97,6 di Saba per il pilot, ma è per-pixel, non direttamente confrontabile. E l'esito è utile in ogni caso: se il VNIR non aiuta un materiale, è un risultato negativo documentato, con valore pratico per la scelta del sensore.",
 "Per-class F1 obbligatorio. Split congelati prima del test. Negativo = comunque risultato.",
 "Chiudo con i riferimenti."),
(13,"References",
 "Questi i lavori citati, tredici, dalla libreria di 47. I riferimenti principali: la tesi di Alari, la survey di Fraternali, la pipeline di Gibellini e il dataset AerialWaste. Grazie, e sono pronto per le domande.",
 "Alari è il riferimento che Thomas si aspetta di vedere: c'è, ed è centrale.",
 "— Domande."),
]

QA=[
("Che task è, per ogni lavoro citato?","Colonna Task nelle tabelle: Gibellini e Alari classificazione (image-level); Sun e CascadeDumpNet object detection; CWLD segmentazione; Saba, Bonifazi e Cilia classificazione per-pixel. U-Net e encoder-decoder = segmentazione."),
("Come hai cercato gli articoli? Con l'AI?","Query scriptate sulle API di Scopus (due insiemi: waste remote sensing, asbestos roofs), 699 record unici dopo deduplica, screening manuale con criteri espliciti, snowballing dalla survey e dalla tesi di Alari. Strumenti AI usati per organizzare note e sintesi, non per selezionare le fonti. Tutti gli artefatti della ricerca sono nel repository."),
("Perché niente SWIR?","Non è nelle acquisizioni previste e ha GSD 3,7 metri, incompatibile col task sub-metrico. Bonifazi lo usa su WorldView-3, lo riporto correttamente, ma è fuori dal nostro scope."),
("Perché niente foundation model?","Sono pre-addestrati a 10-30 metri su Sentinel-2/HLS; il trasferimento a sub-metrico non è dimostrato e non serve al disegno sperimentale. La baseline del gruppo (Swin-T con pretraining remote sensing) è più solida e confrontabile."),
("Ti aspetti il 97,6 di Saba sul pilot?","No: quello è per-pixel su tetti, il nostro è image-level multi-label. È un riferimento superiore, non un target confrontabile."),
("La letteratura multi-materiale è davvero così povera?","Sui rifiuti terrestri a VHR sì: il precedente diretto è la tesi di Alari nel gruppo. Esistono lavori su singoli materiali (amianto soprattutto) e su domini diversi (nastri di selezione, marino), che ho escluso con criteri espliciti."),
]

TIPS=[
"13 slide, ~12 minuti. Presentazione in italiano, termini tecnici in inglese.",
"Flusso: contesto → task → materiali → ricerca → letteratura (siti, materiali) → limiti RGB + dati → gap → proposta → valutazione.",
"Mai tornare indietro su un lavoro già discusso.",
"GSD non si traduce. 'Generalizzazione', non OOD.",
]

css="""
@page { size: A4; margin: 1.6cm 1.7cm; }
* { font-family: Carlito, Calibri, 'DejaVu Sans', sans-serif; }
body { color:#1a1a1a; font-size:10.7pt; line-height:1.42; }
h1 { font-size:18pt; margin:0 0 2px 0; }
.sub { color:#666; font-size:10.5pt; margin:0 0 12px 0; }
h2 { font-size:12.5pt; margin:14px 0 6px 0; border-bottom:1.4px solid #1a1a1a; padding-bottom:3px; }
.slide { page-break-inside:avoid; margin:0 0 10px 0; padding:8px 10px; border:0.8px solid #d8d8d8; border-radius:4px; }
.snum { display:inline-block; min-width:22px; font-weight:bold; }
.stitle { font-weight:bold; font-size:11.2pt; }
.lab { font-weight:bold; font-size:8.6pt; letter-spacing:.4px; color:#888; text-transform:uppercase; margin-top:6px; }
.qa { margin:5px 0; } .qa .q { font-weight:bold; }
ul { margin:4px 0 4px 18px; padding:0; } li { margin:2px 0; }
"""
parts=["<html><head><meta charset='utf-8'><style>%s</style></head><body>"%css]
parts.append("<h1>Discorso — deck v7 (13 slide)</h1>")
parts.append("<p class='sub'>Classification of waste materials in VHR satellite imagery · per-slide talk, punti chiave, transizioni, Q&A</p>")
parts.append("<h2>Consegna</h2><ul>")
for t in TIPS: parts.append("<li>%s</li>"%t)
parts.append("</ul><h2>Slide per slide</h2>")
for num,tit,disc,rem,tr in S:
    parts.append("<div class='slide'><div><span class='snum'>%d.</span> <span class='stitle'>%s</span></div>"%(num,tit))
    parts.append("<div class='lab'>Cosa dico</div><div>%s</div>"%disc)
    parts.append("<div class='lab'>Da ricordare</div><div>%s</div>"%rem)
    parts.append("<div class='lab'>Transizione</div><div><i>%s</i></div></div>"%tr)
parts.append("<h2>Q&A — domande attese</h2>")
for q,a in QA:
    parts.append("<div class='qa'><div class='q'>%s</div><div>%s</div></div>"%(q,a))
parts.append("</body></html>")
open(OUT_HTML,"w",encoding="utf-8").write("".join(parts))
subprocess.run(["wkhtmltopdf","--quiet",OUT_HTML,OUT_PDF])
print("PDF:",OUT_PDF, os.path.getsize(OUT_PDF))
