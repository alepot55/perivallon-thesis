# -*- coding: utf-8 -*-
"""Discorso per deck v7 (27 slide). HTML -> PDF via wkhtmltopdf."""
import subprocess, os
HERE=os.path.dirname(os.path.abspath(__file__))
OUT_HTML=os.path.join(HERE,"_discorso_v7.html")
OUT_PDF=os.path.join(HERE,"discorso_v7.pdf")

S=[
(1,"Titolo",
 "Buongiorno. Presento lo stato dell'arte e la proposta di tesi: classificazione dei materiali di rifiuto in immagini satellitari ad altissima risoluzione, dentro PERIVALLON.",
 "Dire subito 'rifiuti illegali / discariche abusive'.",
 "Parto dal contesto, in breve."),
(2,"Context",
 "Lo smaltimento illegale è un crimine ambientale con conseguenze sanitarie. Le agenzie come ARPA hanno capacità di ispezione limitata, e la priorità dipende da cosa è stato sversato: macerie, plastiche e cemento-amianto sono pericoli molto diversi. Rilevare i siti è ormai maturo; riconoscere il materiale no: la survey di riferimento conta 50 lavori dal 1987 al 2023, quasi tutti RGB, e indica l'identificazione del materiale come problema aperto. Nel gruppo una tesi ha già affrontato il tema, quella di Alari: questo lavoro parte da lì. Le immagini sono esempi positivi di AerialWaste.",
 "Survey: 50 lavori, quasi tutti RGB. Alari = predecessore nel gruppo.",
 "Quindi, in una slide, il task."),
(3,"Task definition",
 "Il task: classificazione multi-label dei materiali di rifiuto, a livello di immagine. Input: immagini ottiche ad altissima risoluzione, da 0,2 a 1,3 metri; RGB aereo per la baseline, VNIR satellitare per il braccio multispettrale, fino a 8 bande. Lo SWIR è escluso: non è nelle acquisizioni previste, e comunque a 3,7 metri non è compatibile col task. Sentinel-2 escluso: troppo grossolano. Perché classificazione e non detection o segmentazione? Le annotazioni disponibili sono a livello di immagine, oltre 11.400 multi-label; i cumuli non hanno forma stabile per le box, e non esistono maschere. La domanda di ricerca: il VNIR migliora la classificazione rispetto all'RGB, e per quali materiali?",
 "Tecnica = classificazione, giustificata dalle annotazioni. GSD 0,2-1,3 m. No SWIR, no S-2.",
 "Lo schema, visivamente."),
(4,"Task scheme",
 "Visivamente: una immagine entra, esce l'insieme dei materiali presenti. Qui un tile reale con rottami: il modello deve dire scrap e bulky items, e non dire macerie o pneumatici. Lo stesso schema gira con input RGB o VNIR: cambia solo il primo layer della rete. È questa la leva sperimentale della tesi.",
 "Multi-label: più materiali insieme nella stessa immagine, non uno solo.",
 "Su quali materiali, di preciso?"),
(5,"The material taxonomy",
 "Questa è la tassonomia, con esempi reali dalla tesi di Alari: macerie, ingombranti, legno, rottami, plastica, veicoli, pneumatici, big bags, container chiusi, materiale ignoto. Il set completo di annotazioni conta 13 categorie: si aggiungono scorie di fonderia, fanghi e cisterne come classi separate. Si vede a occhio il punto: alcune classi si riconoscono dalla forma, altre sono cumuli grigi o marroni difficili da distinguere.",
 "10 mostrate + 3 (fonderia, fanghi, cisterne) = 13 totali.",
 "Per ognuna, dentro o fuori, e perché."),
(6,"Materials: in/out",
 "La decisione materiale per materiale. Tutti e 13 restano target di classificazione, per continuità col dataset del gruppo. L'analisi spettrale RGB-contro-VNIR si concentra dove il colore è ambiguo e le etichette bastano: macerie, plastica, legno, pneumatici. Il cemento-amianto ha un pilot dedicato perché ha ground truth pubblico regionale. Veicoli, cisterne, container, rottami, ingombranti e big bags si riconoscono dalla forma: per la letteratura l'RGB basta. Fanghi e scorie di fonderia restano nel set ma fuori dall'analisi spettrale: poche etichette e classi visivamente ambigue a questa risoluzione.",
 "Criteri espliciti: ambiguità in RGB, disponibilità di etichette, rilevanza di pericolo.",
 "Cosa dice la letteratura su ciascun materiale."),
(7,"Per-material coverage",
 "Questa tabella risponde alla domanda: la letteratura sui materiali è davvero così povera? Materiale per materiale: sull'amianto quattro lavori dedicati, ma sempre tetti, mai dentro una tassonomia di rifiuti. Cisterne, veicoli e container hanno detection matura, sono oggetti a forma fissa. Rottami solo a distanza ravvicinata con infrarosso. Macerie: segmentazione di discariche da costruzione e fotogrammetria da drone. Per plastica, legno, pneumatici, ingombranti e big bags: nessun lavoro dedicato alla scala del task, esistono solo come classi in AerialWaste e Alari. Fanghi e fonderia: niente.",
 "La risposta a Thomas: non è vuota, è sottile in modo documentabile, materiale per materiale.",
 "Come ho costruito questa bibliografia."),
(8,"Literature search",
 "La ricerca è stata fatta con query scriptate sulle API di Scopus, due insiemi: rilevamento rifiuti in remote sensing, e mappatura tetti in amianto. Dopo la deduplica: 699 record unici, 622 waste e 77 asbestos. Screening manuale con criteri espliciti: pertinenza al task, risoluzione compatibile, recency e citazioni, peer review; più snowballing dalla survey di Fraternali e dai riferimenti della tesi di Alari. Il risultato è una libreria curata di 47 paper con note strutturate. In queste slide ne cito 24. Tutti gli artefatti sono nel repository.",
 "699 → 47 → 24 citati. Se chiedono dell'AI: query scriptate, screening manuale, strumenti AI solo per organizzare le note.",
 "Cosa ho tenuto e cosa ho escluso, con che criterio."),
(9,"Kept vs excluded",
 "I gruppi esclusi, con esempi e ragioni. Sentinel-2 e marine debris: 10-20 metri, pixel troppo misti, dominio diverso. Iperspettrale spaziale come EnMAP ed EMIT: evidenza sul materiale ottima, ma 30-60 metri. SWIR ad alta risoluzione, i lavori di Aguilar e Zhou: lo SWIR non è nelle nostre acquisizioni e ha GSD 3,7 metri. Laboratorio e nastri di selezione: non è osservazione della Terra. Foundation model EO: pre-addestrati a 10-30 metri, il trasferimento a sub-metrico non è dimostrato. Tenuto: lavori su rifiuti terrestri o materiali da tetto a GSD compatibile, più la libreria spettrale di riferimento. Gli esclusi restano in libreria come contesto, annotati.",
 "Ogni esclusione ha un motivo tecnico, non è una dimenticanza. Bonifazi usa anche SWIR: citato correttamente, lo scope nostro è VNIR.",
 "Cosa dice la letteratura tenuta: prima i siti."),
(10,"Site-level table",
 "Il rilevamento dei siti, in una tabella. Gibellini, la baseline del gruppo: F1 92 su AerialWaste, meno 5,1 punti cross-region. L'ensemble su AerialWaste, preprint: 92,4 binario. Disaitek, servizio operativo su Pléiades Neo, dato del vendor. CascadeDumpNet, object detection su Pléiades a 50 centimetri, mAP 84,6 con trasferimento tra città. Sun, 2.500 discariche in 28 città. CWLD, segmentazione su rifiuti da costruzione. E AerialWaste stesso, il dataset. Tutti RGB: rispondono a dove è un sito, non a cosa contiene.",
 "Colonna Task pronta per la domanda 'che task è': classification / object detection / segmentation per riga.",
 "I tre lavori chiave uno per uno: dataset, baseline, predecessore."),
(11,"AerialWaste deep-dive",
 "AerialWaste in dettaglio, perché è la base di tutto. 10.434 località dai registri ARPA Lombardia, 487 comuni; tre sorgenti: ortofoto AGEA a 20 centimetri, WorldView-3 a 30, Google Earth a 50. Etichette binarie sito/non-sito per la detection, più 22 tag di materiale annotati da esperti: tipo di oggetto visibile e modalità di stoccaggio. I tag coprono circa il 72% dei positivi, ma il dataset è stato pubblicato per la detection: i tag sono metadati, non un benchmark. È la base di etichette su cui costruiscono sia Gibellini sia Alari.",
 "22 tag = metadati, non benchmark: per questo serve il lavoro di Alari e questa tesi.",
 "La baseline architetturale del gruppo."),
(12,"Gibellini deep-dive",
 "Gibellini 2025: classificazione binaria waste/no-waste su AerialWaste, Swin-T con pretraining remote sensing, fine-tuning in due fasi. F1 92,02 in dominio. In generalizzazione cross-region perde 5,1 punti in media: Grecia 85,4, Serbia 83,8, Romania 91,5. Le saliency map confermano che il modello guarda i cumuli. Ma l'output è solo presenza: nessuna informazione sul materiale. Questa architettura e questa ricetta di training sono il punto di partenza della proposta.",
 "92,02 in dominio, -5,1 fuori. Architettura = punto di partenza nostro.",
 "E il predecessore diretto sul materiale."),
(13,"Alari deep-dive",
 "La tesi di Alari, il predecessore diretto. Primo lavoro nel gruppo a impostare il riconoscimento del materiale come classificazione multi-label. Dataset: 11.477 annotazioni su 13 categorie, 3.190 immagini positive e 7.190 negative, costruite su AerialWaste e sui registri ARPA. Modelli: ResNet-50 e Swin con FPN, tre design di testa di classificazione, binary cross-entropy pesata per lo sbilanciamento, confronto tra pretraining. Risultati: weighted F1 69,21 su cinque categorie, 59,42 su dieci. Passare da 5 a 10 costa 9,8 punti. L'input è solo RGB: la dimensione spettrale è intatta, ed è l'apertura che questa tesi prende.",
 "69,21 / 59,42; da 5 a 10 categorie = -9,8 punti. Input solo RGB = la nostra apertura.",
 "Quanto rende, materiale per materiale."),
(14,"Alari: risultati per materiale",
 "Il grafico mostra l'F1 per classe del modello a 10 categorie. La media pesata, 59,4, nasconde la spaccatura: le classi definite da forma o estensione stanno vicino a 70 — macerie, ingombranti, container; quelle definite dall'aspetto del materiale scendono sotto 45 — plastica 44, legno 37, big bags 35, pneumatici 19. La tesi stessa attribuisce i punteggi bassi a poche annotazioni, alta varianza intra-classe e somiglianza tra classi in RGB. Tre dei quattro target dell'analisi spettrale stanno nella metà bassa della classifica; l'eccezione sono le macerie, visibili per estensione. Questo è il quadro che l'ablazione di bande deve muovere.",
 "In alto 72,5 / 70,7 / 67,8; in basso plastica 44,1, legno 37,0, big bags 34,6, pneumatici 18,6.",
 "Il quadro material-level completo."),
(15,"Material-level table",
 "Il material-level in tabella. Alari, l'unico multi-materiale. Poi quasi solo amianto: Saba su WorldView-3 solo VNIR, Macro-F1 97,6 ma per-pixel; Bonifazi, monitoraggio multi-temporale con VNIR e SWIR; Abbasi da aereo RGB con la dimensione temporale, OA circa 96; Cilia nel 2015 da iperspettrale aereo. Saba e Abbasi sono paywalled o preprint, li riporto come tali. Nessun lavoro misura RGB contro VNIR sui materiali di rifiuto: questo è il punto.",
 "Un predecessore multi-materiale + un materiale studiato in isolamento. Saba 97,6 = per-pixel, non confrontabile.",
 "L'amianto merita una slide dedicata: è il nostro pilot."),
(16,"Asbestos deep-dive",
 "La linea amianto in dettaglio. Saba: 32 classificatori confrontati su WorldView-3 solo VNIR, Red Edge e NIR portano la discriminazione. Bonifazi: workflow multi-temporale, decisioni a livello di edificio, traccia le rimozioni dei tetti tra acquisizioni; l'immagine è sua. Abbasi: aereo RGB più tempo, forma e tempo possono sostituire lo spettro a GSD fine. Cilia: iperspettrale aereo, più un indice di degrado dal rapporto rosso/NIR. E uno studio su drone mostra che l'ardesia si riconosce in parte già dalla forma. Perché conta qui: ground truth pubblico, il registro lombardo con 10.903 tetti, più evidenza VNIR chiara. È il pilot naturale.",
 "Red Edge + NIR = le bande che contano (Saba). GT pubblico Lombardia = 10.903 tetti.",
 "E il degrado stesso si vede nel VNIR."),
(17,"Asbestos weathering in VNIR",
 "Cilia ha misurato tetti in cemento-amianto di età ed esposizione diverse, a terra e dal sensore aereo MIVIS, nella finestra 0,48-0,82 micrometri: puro VNIR. I tetti più vecchi sono più scuri su tutto il visibile; la vegetazione che colonizza la superficie aggiunge un assorbimento di clorofilla verso 680 nanometri; l'esposizione a nord amplifica entrambi gli effetti. Da queste feature il paper costruisce un indice di deterioramento e ordina le priorità di rimozione; gli effetti di età ed esposizione sono statisticamente significativi. Per noi: le feature discriminanti stanno nella finestra VNIR dei sensori previsti; anche lo stato di degrado, non solo la presenza, è alla portata del pilot.",
 "Assorbimento clorofilla ~680 nm = proxy del degrado. ANOVA: età e esposizione p<0,001.",
 "Perché l'RGB non basta, e cosa aggiunge il VNIR."),
(18,"RGB limits, VNIR",
 "Il nodo tecnico. Materiali diversi hanno lo stesso colore a queste risoluzioni: teli di plastica, cemento-amianto e cemento appaiono grigi. Nel predecessore, passare da 5 a 10 categorie costa 9,8 punti: sono le distinzioni fini la parte difficile. Red Edge e NIR separano vegetazione, suolo nudo e superfici degradate; in Saba guidano la discriminazione dell'amianto. Se questo aiuti i materiali di rifiuto, e quali, non è stato misurato: è l'oggetto della tesi. Il grafico mostra firme di riflettanza reali nella finestra 400-1050 nanometri, con i centri banda dei due sensori.",
 "Curve limitate al VNIR (400-1050), coerenti con lo scope. Non addentrarsi nella fisica.",
 "Quante bande extra servono? C'è un numero."),
(19,"How many extra bands",
 "Evidenza in condizioni controllate: Vitek 2025, iperspettrale di laboratorio su dieci materiali da costruzione e demolizione. Solo RGB: accuratezza 0,87. RGB più due bande scelte bene: 0,96. L'intero spettro di 768 bande non aggiunge quasi nulla. E le due bande ottimali cadono a 650-750 e 850-1000 nanometri: dove stanno Red Edge e NIR di WorldView-3 e Pléiades Neo. È uno studio di laboratorio e lo dico chiaramente: delimita quanto lo spettro può dare; se si trasferisce al satellite è ciò che la tesi misura.",
 "0,87 → 0,96 con 2 bande; ottimo a 650-750 + 850-1000 nm. Dire sempre 'laboratorio'.",
 "Con che dati, in concreto."),
(20,"Available imagery",
 "Una sola slide sui sensori. WorldView-3: 8 bande VNIR a 1,24 metri, pancromatico a 31 centimetri. Pléiades Neo: 6 bande a 1,2 metri, pan a 30. Rispetto a RGB più NIR, WorldView-3 aggiunge Coastal, Yellow, Red Edge e un secondo NIR; Pléiades Neo aggiunge Deep Blue e Red Edge. Accesso commerciale o quota gratuita via proposta ESA. Questo è il budget di bande dello studio: niente SWIR, niente Sentinel-2. La baseline RGB gira su AerialWaste.",
 "Riassunto in 1 slide, subito dopo i limiti RGB, come chiesto.",
 "Ricapitolo tutto lo stato dell'arte in una tabella."),
(21,"SOTA at a glance",
 "Dieci righe riassumono ogni linea di lavoro in scope: la survey che dichiara il gap, il dataset, le baseline di sito, il predecessore multi-label, la detection di oggetti, la linea amianto. La colonna che conta è l'ultima: informazione sul materiale. Quasi tutte le righe dicono nessuna, o un solo materiale. L'evidenza material-level si riduce a: un predecessore multi-label e un materiale studiato in isolamento.",
 "Slide di sintesi: leggerla per colonna (Material info), non per riga.",
 "Da qui, cosa manca."),
(22,"Gaps",
 "Cinque mancanze. Uno: la classificazione multi-materiale ha un solo precedente diretto, con margine ampio, 59-69 di weighted F1. Due: nessuno misura il valore aggiunto delle bande VNIR rispetto all'RGB per i materiali di rifiuto ad altissima risoluzione. Tre: i risultati sono aggregati, il comportamento per materiale non viene analizzato. Quattro: la generalizzazione tra regioni è raramente valutata, e già a livello di sito costa 5 punti. Cinque: l'amianto è studiato sui tetti, isolato, mai dentro una tassonomia di rifiuti.",
 "Ogni gap mappa su un elemento della proposta: dirlo esplicitamente.",
 "Da qui la proposta."),
(23,"Proposal: approach",
 "La tecnica è classificazione multi-label di immagini, in continuità con Gibellini e Alari: stessa tassonomia, input esteso da RGB a VNIR. Backbone Swin-T con pretraining remote sensing, la baseline del gruppo; le bande extra entrano estendendo il layer di input della rete pre-addestrata. Ablazione con tutto il resto fisso: stessa architettura, stessi split, cambia solo l'input. RGB, poi RGB più NIR, poi VNIR completo. Il diagramma mostra il flusso: sorgenti dati, backbone, ablazione, output.",
 "Tecnica dichiarata + perché. Una sola variabile sperimentale: le bande di input.",
 "Il primo passo concreto."),
(24,"Asbestos pilot",
 "Il primo passo è il pilot amianto, quattro fasi. Uno: estrarre i poligoni dei tetti dal registro WFS lombardo, 10.903 tetti mappati, e accoppiarli con le immagini disponibili. Due: costruire input RGB e VNIR appaiati per gli stessi tetti, con negativi dalle footprint regionali. Tre: addestrare lo stesso classificatore sui due input e confrontare F1, precision e recall su aree tenute fuori. Quattro: punto di decisione: il delta VNIR misurato su un materiale singolo e ben etichettato dice se l'estensione multi-label completa vale il costo di acquisizione. Perché l'amianto per primo: etichette pubbliche accurate, un solo materiale, evidenza VNIR in letteratura, e valore regolatorio diretto.",
 "Pilot = de-risking della pipeline prima di comprare acquisizioni. Fase 4 = decision gate.",
 "E come misuro, in generale."),
(25,"Evaluation",
 "F1 per materiale, oltre alle medie pesata e macro: gli aggregati nascondono proprio le classi che ci interessano. Delta rispetto alla baseline RGB per ogni configurazione di bande, con intervalli di confidenza su run ripetute. Protocollo di generalizzazione: train e test su aree geografiche disgiunte, oltre allo split standard. Punti di riferimento: 69,2 e 59,4 di Alari per il multi-label; il 97,6 di Saba per il pilot, ma è per-pixel, non direttamente confrontabile. E l'esito è utile in ogni caso: se il VNIR non aiuta un materiale, è un risultato negativo documentato, con valore pratico per la scelta del sensore. La griglia mostra il disegno: per ogni materiale, il delta rispetto alla baseline RGB.",
 "Per-class F1 obbligatorio. Split congelati prima del test. Negativo = comunque risultato.",
 "Chiudo con i riferimenti."),
(26,"References 1/2",
 "Questi i riferimenti principali: la tesi di Alari, la survey di Fraternali, la pipeline di Gibellini, il dataset AerialWaste, e la linea amianto.",
 "Alari è il riferimento che Thomas si aspetta di vedere: c'è, ed è centrale.",
 "E la seconda pagina."),
(27,"References 2/2",
 "E i lavori su oggetti, close range e la libreria spettrale USGS. In tutto 24 lavori citati, inclusa l'evidenza di laboratorio sulle bande dalla libreria di 47; il resto è tenuto come contesto vagliato. Grazie, e sono pronto per le domande.",
 "24 citati / 47 in libreria / 699 record iniziali: la catena dei numeri regge.",
 "— Domande."),
]

QA=[
("Che task è, per ogni lavoro citato?","Colonna Task nelle tabelle: Gibellini e Alari classificazione (image-level); Sun e CascadeDumpNet object detection; CWLD e i lavori UAV segmentazione; Saba, Bonifazi e Cilia classificazione per-pixel; cisterne/veicoli/container object detection. U-Net e encoder-decoder = segmentazione."),
("Come hai cercato gli articoli? Con l'AI?","Query scriptate sulle API di Scopus (due insiemi: waste remote sensing, asbestos roofs), 699 record unici dopo deduplica, screening manuale con criteri espliciti, snowballing dalla survey e dalla tesi di Alari. Strumenti AI usati per organizzare note e sintesi, non per selezionare le fonti. Tutti gli artefatti della ricerca sono nel repository."),
("Perché niente SWIR?","Non è nelle acquisizioni previste e ha GSD 3,7 metri, incompatibile col task sub-metrico. Bonifazi lo usa su WorldView-3, lo riporto correttamente, ma è fuori dal nostro scope."),
("Perché niente foundation model?","Sono pre-addestrati a 10-30 metri su Sentinel-2/HLS; il trasferimento a sub-metrico non è dimostrato e non serve al disegno sperimentale. La baseline del gruppo (Swin-T con pretraining remote sensing) è più solida e confrontabile."),
("Ti aspetti il 97,6 di Saba sul pilot?","No: quello è per-pixel su tetti, il nostro è image-level multi-label. È un riferimento superiore, non un target confrontabile."),
("La letteratura multi-materiale è davvero così povera?","La slide 7 risponde materiale per materiale: amianto ha 4 lavori (solo tetti), gli oggetti a forma fissa hanno detection matura, ma plastica, legno, pneumatici, ingombranti, big bags, fanghi e fonderia non hanno nessun lavoro dedicato alla scala del task. Il precedente multi-materiale è uno: Alari."),
("Perché classificazione e non segmentazione?","Le annotazioni disponibili sono image-level (11.477 multi-label di Alari); i cumuli non hanno forma stabile per le box; non esistono maschere per questi dataset. Creare maschere ex novo non è nel budget della tesi."),
("Come entrano le bande extra nella rete?","Estendendo il primo layer convoluzionale della rete pre-addestrata: i pesi RGB restano, i canali nuovi si inizializzano dalla media o da zero. Tutto il resto dell'architettura è identico, così il confronto è pulito."),
("Che dati usi esattamente?","Baseline RGB: AerialWaste con le annotazioni di Alari. Braccio multispettrale: acquisizioni WorldView-3 (8 bande VNIR, 1,24 m) e Pléiades Neo (6 bande, 1,2 m). Pilot: registro amianto lombardo, 10.903 tetti, WFS pubblico."),
]

TIPS=[
"27 slide, ~20-22 minuti. Presentazione in italiano, termini tecnici in inglese.",
"Flusso: contesto → task (definizione + schema) → materiali (tassonomia, in/out, copertura) → ricerca (metodo, esclusi) → siti (tabella + 3 deep-dive) → materiali (per-classe, tabella, amianto, weathering) → limiti RGB + evidenza bande + dati → sintesi → gap → proposta (approccio, pilot, valutazione) → riferimenti.",
"Le slide di analisi (11-14, 16-17, 19) sono il cuore: i lavori chiave letti a fondo, con i numeri per classe e per banda.",
"Slide 21 (sintesi) e le tabelle: passarci veloci, non rileggerle riga per riga.",
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
parts.append("<h1>Discorso — deck v7 (27 slide)</h1>")
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
os.remove(OUT_HTML)
print("PDF:",OUT_PDF, os.path.getsize(OUT_PDF))
