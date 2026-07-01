# -*- coding: utf-8 -*-
import html, subprocess, os
OUT_HTML="/home/alepot55/.claude/jobs/49614db0/tmp/discorso.html"
OUT_PDF="/home/alepot55/Desktop/uni/Tesi/assets/deck_v6/discorso_presentazione.pdf"

# (num, titolo slide, discorso, da_ricordare, transizione)
S=[
(1,"Titolo — SOTA: waste material classification from MS satellite imagery",
 "Buongiorno. Sono Alessandro Potenza. Presento lo stato dell'arte per il mio lavoro di tesi: la classificazione del <b>materiale</b> dei rifiuti illegali (illegal waste) da immagini satellitari multispettrali. L'obiettivo di oggi non è proporre un esperimento, ma mostrare in modo rigoroso <b>cosa esiste in letteratura per questo specifico task</b>, con quelle caratteristiche — è da qui che nasce la domanda di ricerca.",
 "Dire chiaramente \"illegal waste\". È uno stato dell'arte del task, non dei miei dati.",
 "Partiamo dal problema."),
(2,"The problem: priority, not just presence",
 "Lo smaltimento illegale di rifiuti è un crimine ambientale e un problema di salute pubblica. Agenzie come ARPA non possono ispezionare tutto: devono <b>dare priorità</b>. Il punto chiave: le pipeline automatiche oggi trovano bene i siti — classificano la <i>presenza</i>, non <i>cosa</i> c'è. Da qui la domanda di ricerca, che tengo aperta: qual è il valore aggiunto del multispettrale, rispetto al solo RGB, per classificare il materiale del rifiuto?",
 "Research question aperta, non pre-risposta. \"classificare per rischio\", non solo \"rilevare\".",
 "Perché il materiale conta così tanto? Perché è lui a definire il rischio."),
(3,"Why material matters: risk = hazard × exposure × magnitude",
 "Il pericolo dipende dal materiale: macerie inerti, plastiche e cemento-amianto sono mondi diversi. È il materiale a portare il <b>pericolo</b> — il Catalogo Europeo dei Rifiuti (EWC) marca i codici pericolosi con l'asterisco: l'amianto è 17 06 05*. Il rischio prioritario è <b>pericolo × esposizione × magnitudine</b>. Quindi identificare il materiale — non solo localizzare il sito — è la variabile che conta davvero per la decisione operativa.",
 "EWC amianto = 17 06 05*. Rischio = hazard × exposure × magnitude.",
 "Vediamo come lavora oggi lo stato dell'arte."),
(4,"Today's paradigm: RGB deep learning detects sites, not materials",
 "Il paradigma attuale: tile RGB ad altissima risoluzione, backbone CNN o transformer, pretraining, fine-tuning in due step, output binario rifiuto / non-rifiuto. Funziona bene <i>nel contesto</i> su cui è addestrato — Gibellini 2025 arriva a F1 92%. Ma tre limiti spingono verso lo spettro: classifica la presenza, non il materiale; è legato al solo colore; e la <b>generalizzazione</b> crolla fuori contesto, meno 5% cross-region.",
 "Gibellini F1 92,0%. Cross-region −5,1%. Dire \"generalizzazione\", mai \"OOD\".",
 "Guardiamo i lavori principali di questa linea RGB."),
(5,"State of the art: RGB waste detection (tabella)",
 "Questi sono i lavori chiave sul rilevamento RGB. Gibellini, la baseline su AerialWaste, F1 92%. Il dataset AerialWaste di Torres: 22 categorie di materiale, ma solo RGB. Sun 2023: circa 2.500 discariche in 28 città, sensibilità 98%. CascadeDumpNet su Pléiades, mAP 84,6, e generalizza tra città. Disaitek, servizio operativo su Pléiades Neo, ~95% — ma è un dato vendor, non peer-reviewed. Il messaggio: sono <b>tutti RGB</b>, imparano forma e contesto; la composizione del materiale resta fuori portata.",
 "Tutte le righe = RGB. † = vendor/pre-print, dirlo. Non presentare i numeri † come certi.",
 "Perché l'RGB è cieco al materiale? Serve la fisica."),
(6,"A satellite pixel is a spectrum, not just a colour",
 "Un pixel satellitare non è un colore: è un <b>vettore di riflettanza</b>, la firma spettrale del materiale. RGB sono 3 bande larghe nel visibile — solo colore. Il multispettrale (MS) sono 4–15 bande scelte: WorldView-3 ne ha 8 nel VNIR più 8 nello SWIR, Pléiades Neo 6 VNIR. L'iperspettrale (HSI) sono centinaia di bande contigue. Questo vettore è l'input grezzo da cui qualsiasi classificatore ragiona.",
 "Definire EO/MS/HSI alla prima occorrenza. WV-3 = 8 VNIR + 8 SWIR; PNeo = 6 VNIR.",
 "E ogni materiale ha una sua firma."),
(7,"Every material has a spectral fingerprint",
 "Ogni materiale riflette la luce in modo diverso lungo le lunghezze d'onda: sono le <b>firme spettrali</b>. Le curve diagnosticano la chimica, non solo il colore. Gli indizi decisivi stanno nel NIR e soprattutto nello SWIR: il legame Mg-OH dell'amianto intorno a 2,3 µm, il C-H delle plastiche a 1,2 e 1,7 µm. Nessuno di questi è visibile in RGB. Questa è la base fisica di tutto ciò che segue.",
 "Amianto Mg-OH ~2,3 µm; plastiche C-H 1,2/1,7 µm. Fonte: USGS splib07a (Kokaly 2017).",
 "Quando manca lo spettro, l'RGB fallisce — e in due modi precisi."),
(8,"RGB fails in two distinct ways",
 "L'RGB fallisce in due modi. Primo, <b>iso-cromaticità</b>: materiali diversi con lo stesso colore — un telo di plastica HDPE, un tetto in cemento-amianto e una lastra di cemento chiaro sono quasi identici all'occhio. Secondo, il <b>mixing sub-pixel</b>: a 10–30 m un pixel raramente contiene un solo materiale, e la miscela di due può cadere sulla firma di un terzo. Entrambi invisibili senza informazione spettrale; solo le feature SWIR li tengono separati.",
 "Due modi: iso-cromaticità + mixing sub-pixel. Fonte: Tasseron 2021, Aguilar 2025.",
 "Dove diventa separabile ciascun materiale? Dipende dalla banda."),
(9,"Where each hazard becomes separable: feature → band",
 "Questa griglia mostra dove ciascun pericolo diventa separabile. Pléiades Neo arriva solo fino al NIR: prende bene la ruggine e il degrado dei tetti amianto (muschio/licheni nel red-edge), ma è cieca alla chimica. WorldView-3 aggiunge lo SWIR: è lì che amianto, plastiche e carbonati del cemento diventano distinguibili. È la traduzione operativa della slide precedente: la chimica sta nello SWIR.",
 "PNeo si ferma al NIR; WV-3 aggiunge SWIR. La chimica è nello SWIR.",
 "Vediamo ora le prove sperimentali, materiale per materiale — a partire dall'amianto."),
(10,"State of the art: asbestos discrimination (tabella)",
 "L'amianto è la prova più netta che MS e HSI recuperano l'identità del materiale. Shepherd 2025, iperspettrale EnMAP a 30 m: 86% di match sul campo. Cilia 2015, storico italiano, iperspettrale aereo MIVIS: PA 89% / UA 86%. Saba 2026, WorldView-3 solo VNIR: Macro-F1 97,6% — mostra che a volte bastano 8 bande VNIR. Bonifazi 2026, WV-3 16 bande, monitoraggio multi-temporale. Abbasi 2024, addirittura da aereo RGB senza SWIR, sfruttando forma e serie temporale, ~96%.",
 "Shepherd 86% campo; Cilia PA89/UA86; Saba 97,6% (†); i † sono paywalled/pre-print.",
 "E per le plastiche e i materiali urbani?"),
(11,"State of the art: plastics & urban materials (tabella)",
 "Qui la seconda linea. Aguilar 2021 è il riferimento canonico: ablazione VNIR / SWIR / tutto su WV-3 — 90,85 → 96,79 → 97,38, lo SWIR fa il salto. Aguilar 2025, macroplastiche con matched filter, precisione 92,5% e correlazione lab-immagine r 0,95. EMIT 2025, prima mappa globale orbitale di plastica. MARIDA, Sentinel-2 a 10 m, F1 0,79 ma soffre il mixing. CDW 2025: RGB 0,87 sale a 0,96 con sole 2 bande NIR. SpectralWaste: la fusione RGB+HSI batte entrambi. Il messaggio: l'identità viene dalla chimica NIR-SWIR, non dal colore.",
 "Aguilar 90,85→96,79→97,38. CDW: RGB 0,87 → +2 NIR 0,96.",
 "Fermiamoci su quel numero di Aguilar: è la prova più citata del valore aggiunto."),
(12,"Spectral added value, measured: Aguilar 2021",
 "Aguilar 2021 è l'ablazione di bande più citata su WorldView-3 per una classificazione tipo-rifiuto — plastica da serre, 14 milioni di pixel, OBIA più albero decisionale, cross-validation. L'accuratezza va da 90,85% con solo VNIR, a 96,79% con solo SWIR, a 97,38% con tutte le 16 bande. È la prova canonica che lo SWIR aggiunge potere discriminante sul materiale. È anche il template metodologico di riferimento.",
 "90,85 → 96,79 → 97,38 (VNIR → SWIR → tutto). Il salto è lo SWIR.",
 "Ma servono davvero tante bande? No."),
(13,"More bands ≠ more information, well-chosen few suffice",
 "Non conta quante bande, conta <b>quali</b>. Aguilar: da VNIR a tutto, il salto lo fa lo SWIR. CDW 2025, su rifiuti da costruzione in laboratorio: RGB a 0,87 sale a 0,96 con sole 2 bande NIR — alla pari con 768 bande iperspettrali. Zhou 2021: 8 bande SWIR strette separano i tipi di polimero. Quindi poche bande SWIR ben scelte recuperano gran parte del guadagno: è un'informazione importante per il costo e la fattibilità.",
 "\"Quali bande, non quante\". CDW: +2 NIR ≈ HSI 768 bande.",
 "Onestà scientifica: c'è però un limite fisico."),
(14,"Honest limit: resolution split between texture and chemistry",
 "Un limite da dichiarare: la risoluzione è divisa tra tessitura e chimica. Lo spettro è campionato grossolanamente — VNIR a 1,24 m, SWIR a 3,7 m, pixel da ~14 m². Il pancromatico dà tessitura fine a 0,3 m, ma da solo non dà materiale. Una piccola discarica si <i>vede</i> (tessitura) più facilmente di quanto si <i>identifichi</i> chimicamente. E c'è il collo di bottiglia SWIR-8: amianto 2,32, cemento 2,34, plastica 2,31 finiscono in un'unica banda WV-3. E attenzione: a volte lo SWIR non serve — Saba e Abbasi classificano l'amianto senza.",
 "SWIR 3,7 m, pixel ~14 m². Bottleneck SWIR-8. Volontariamente onesti: SWIR non sempre necessario.",
 "Passiamo ai sensori: qual è il compromesso?"),
(15,"The sensor trade-off: spatial × spectral × revisit",
 "Tre assi, un solo budget di fotoni: nessun satellite li massimizza tutti. WorldView-3: 1,24 m nel VNIR più 3,7 m nello SWIR, 16 bande — l'unica opzione VHR con SWIR. Pléiades Neo: 1,2 m, 6 bande VNIR, niente SWIR — il più nitido dei solo-VNIR. Sentinel-2 ed EnMAP: 10–30 m, spettro ricco ma troppo grossolano per il materiale a scala di sito. SuperDove: 3 m, 8 VNIR, gratis e quasi giornaliero, ma solo VNIR.",
 "Radar PRIMA dei singoli sensori (roadmap). GSD non si traduce.",
 "Zoomiamo sull'altissima risoluzione: è qui che si gioca lo SWIR."),
(16,"Very-high resolution: the SWIR divide",
 "All'altissima risoluzione c'è uno spartiacque, la presenza o meno dello SWIR. WorldView-3 è l'unica piattaforma sotto i 2 m che porta anche lo SWIR — dove sta la chimica. Pléiades Neo e SuperDove sono solo-VNIR: nitidi, ma ciechi alle assorbanze diagnostiche dello SWIR. È il compromesso su cui gira tutto lo stato dell'arte: dettaglio spaziale contro informazione spettrale (chimica). Nota: qui i sensori sono il <b>panorama</b> del task, non un dataset che possiedo.",
 "WV-3 = unico VHR + SWIR. Sensori = panorama, NON \"i miei dati\".",
 "E i dataset? Qui emerge un buco strutturale."),
(17,"State of the art: datasets & the data gap",
 "I dataset disponibili. AerialWaste di Torres: 22 categorie di materiale ma solo RGB, e le coordinate sono riservate. CWLD 2024: maschere di segmentazione per rifiuti da costruzione, ma solo Cina. MARIDA: benchmark a pixel a 15 classi, però marine — acqua, non terra, a 10 m. SpectralWaste: RGB più SWIR, ma su nastro trasportatore, non da satellite. Conclusione netta: <b>nessun dataset pubblico combina altissima risoluzione, rifiuti terrestri e etichette di materiale</b>. È il gap strutturale.",
 "Nessun dataset: VHR + rifiuti terrestri + label di materiale. È il gap.",
 "Passiamo al metodo: come si confrontano bande diverse in modo equo?"),
(18,"Foundation models for Earth Observation",
 "Dal 2024 c'è un'ondata di foundation model per l'osservazione della Terra — Prithvi, SpectralGPT, DOFA, AnySat. La maggior parte è pre-addestrata a 10–30 m su Sentinel-2 o HLS, quindi il trasferimento all'altissima risoluzione non è garantito. Due strade: modelli sensor-agnostic che accettano set di bande arbitrari, e adattatori parameter-efficient che congelano il backbone e aggiungono meno dell'1% di parametri. Domanda aperta: il pretraining a 10–30 m trasferisce al VHR?",
 "Pretraining 10–30 m → VHR non garantito. Definire FM.",
 "Vediamo i modelli principali."),
(19,"State of the art: foundation models (tabella)",
 "I foundation model rilevanti. DOFA, di Xiong 2024: una hypernetwork condizionata sulla lunghezza d'onda, gestisce fino a 202 bande, plug-in per nuovi sensori. AnySat, 11 sensori, stato dell'arte su 9 task. Prithvi-EO-2.0, ha lo SWIR nativo ma bande fisse. SoftCon, batte con inizializzazione casuale delle bande extra. DEFLECT, l'adattatore sotto l'1% di parametri, alla pari col fine-tuning completo. Il limite comune: pre-addestrati a 10–30 m, non testati su materiale al VHR.",
 "DOFA = wavelength-conditioned, fino a 202 bande. Limite: VHR + materiale non testati.",
 "DOFA merita una slide a sé: è il candidato per un confronto equo."),
(20,"DOFA: a band-agnostic backbone",
 "DOFA, Dynamic One-For-All. Una hypernetwork genera i pesi del patch-embedding a partire dalla lunghezza d'onda centrale di ogni banda. Un solo backbone ingerisce qualsiasi sensore — WV-3 a 16 bande, Pléiades Neo a 6, Sentinel-2 a 13, o iperspettrale — indicizzando per lunghezza d'onda. Questo rende <b>equo</b> un confronto RGB contro VNIR contro SWIR: stesso modello, cambia solo il set di bande. È il substrato naturale per un'ablazione controllata, e si abbina agli adattatori PEFT.",
 "DOFA rende equo il confronto RGB/VNIR/SWIR (stesso backbone, cambiano le bande).",
 "Un'ultima distinzione importante: oggetto contro materiale."),
(21,"State of the art: object vs material",
 "Il confine oggetto-materiale. Ramachandran 2024: serbatoi con precision 0,96, oltre 169 mila mappati — la classe \"serbatoi\" è matura. YOLOv7-OT, serbatoi al 90%. Ma i veicoli a fine vita e la composizione del rottame: Hybrid-YOLOv5 lavora su infrarosso ravvicinato, mAP 84%, e serve lo spettro o la vicinanza. UAV solid-waste: OA oltre 94%, ma cumulo generico, nessuna scomposizione per materiale. Il messaggio: gli oggetti a forma definita (serbatoi, veicoli) sono maturi; la <b>composizione del materiale</b> (rottame, scoria) richiede ancora lo spettro.",
 "Oggetti (forma) = maturi; materiale (scoria/rottame) = serve spettro.",
 "Tiriamo le fila: quali gap emergono dallo stato dell'arte?"),
(22,"Gaps the state of the art reveals",
 "I gap che lo stato dell'arte rivela. Uno: il tetto dell'RGB — ogni rilevatore operativo è solo RGB e impara forma e contesto, non il materiale. Due: nessun dataset combina VHR, rifiuti terrestri ed etichette di materiale. Tre: le prove di materiale sono adiacenti — serre, tetti amianto isolati — mai dentro una pipeline di rifiuti. Quattro: la generalizzazione è fragile e non misurata per il MS. Cinque: i foundation model non sono testati sul materiale al VHR. Sei: manca il legame materiale → classe di pericolo → rischio.",
 "6 gap. Sono la giustificazione della direzione di tesi.",
 "Un gap merita un approfondimento: la generalizzazione."),
(23,"Generalization: fragile and largely unmeasured for MS",
 "La generalizzazione è un punto cieco ricorrente. In-domain l'RGB è forte, ma cross-region perde il 5% (Gibellini) e cross-sensor porta banalmente solo perché è il minimo comune denominatore. Aggiungere bande dovrebbe restringere il gap cross-region — la fisica trasferisce meglio dell'apparenza — ma cross-sensor lo può allargare se le bande non sono armonizzate. Quasi tutti i lavori riportano solo l'in-domain: se le bande in più restringano o allarghino il gap è, di per sé, una domanda aperta.",
 "Cross-region −5,1%. MS restringe within-sensor, può allargare cross-sensor.",
 "Cosa indica, in sintesi, tutto questo stato dell'arte?"),
(24,"What the state of the art points to",
 "In sintesi, lo stato dell'arte lascia una domanda netta e senza risposta: quanto batte davvero il multispettrale l'RGB per il <b>materiale</b> del rifiuto, e dove smette di aiutare? La direzione naturale: un'ablazione di bande controllata — RGB, poi red-edge e NIR, poi VNIR completo, poi SWIR — su un backbone wavelength-agnostic come DOFA; con la generalizzazione come asse di prima classe; con piattaforme VHR ai due lati dello spartiacque SWIR, WorldView-3 e Pléiades Neo; e l'amianto come primo materiale, perché ha ground-truth pubblico e una firma SWIR da manuale. Il punto: è lo stato dell'arte a definire l'esperimento, indipendentemente dal dataset che avrò.",
 "Chiudere sul fatto che la SOTA definisce l'esperimento, non i dati in mano.",
 "— Grazie. Domande."),
]

QA=[
("\"Ma esattamente che task è?\"","Classificazione del <b>materiale</b> del rifiuto da satellite, per stimare il rischio. Il rilevamento del sito lo consideriamo sostanzialmente risolto in RGB (Gibellini F1 92%); il contributo aperto è il materiale. Prepararla bene: è la domanda che è già arrivata (slide 5, 10, 12)."),
("\"Sentinel-2 ha lo SWIR: perché non basta?\"","Ha lo SWIR ma a 20 m. Su una discarica il pixel è troppo misto: la risoluzione <i>spaziale</i> non basta per identificare il materiale a scala di sito. Per questo serve il VHR — è la risoluzione, non la presenza dello SWIR, il problema di Sentinel-2."),
("\"Ma se non hai ancora i dati?\"","È uno stato dell'arte <b>del task</b>, indipendente dal dataset. I sensori (WV-3, Pléiades Neo) sono il panorama tecnologico, non dati che possiedo: servono a inquadrare lo spartiacque SWIR, non a dire \"userò questi\"."),
("\"Perché proprio DOFA?\"","Perché è wavelength-agnostic: lo stesso backbone accetta RGB, VNIR o SWIR indicizzando per lunghezza d'onda. Rende il confronto tra set di bande <b>equo</b> — cambia solo l'input, non il modello. Senza, sarebbe mele-vs-arance."),
("\"Perché partire dall'amianto?\"","Perché è il caso più pulito: ground-truth pubblico (mappature regionali), una firma SWIR da manuale (Mg-OH ~2,3 µm) e un codice di pericolo chiaro (17 06 05*). Fa da de-risking dell'intera pipeline."),
("\"I numeri con † sono affidabili?\"","No, li presento come <i>motivanti, non stabiliti</i>: Saba e Bonifazi sono paywalled/pre-print, Disaitek è vendor. I numeri solidi sono Gibellini, Aguilar 2021, Shepherd, Cilia, MARIDA."),
]

TIPS=[
"Ritmo: ~40–50 secondi a slide di testo, ~30 per le tabelle. Totale ~15 minuti, poi Q&A.",
"Flusso lineare: problema → perché RGB non basta → fisica → prove (amianto, plastiche) → limiti → sensori/dataset → metodo → gap → direzione. Non anticipare i gap nelle slide introduttive.",
"Sulle tabelle non leggere ogni cella: dì il messaggio della slide (la riga in fondo) e cita 2–3 lavori chiave.",
"Terminologia: \"illegal waste\", \"classificare per rischio\" (non \"rilevare\"), \"generalizzazione\" (non \"OOD\"), \"multiband/multispettrale\" (non \"cubo spettrale\"). GSD non si traduce. Definire EO/MS/HSI/VNIR/SWIR alla prima occorrenza.",
"Onestà come forza: dichiarare i limiti (SWIR a 3,7 m, SWIR non sempre necessario, numeri †). Il relatore lo apprezza.",
"Chiudere sempre sul punto: è lo stato dell'arte a definire l'esperimento, non il dataset in mano.",
]

def esc(t): return t  # content already HTML-safe (we intentionally use <b>/<i>)

css="""
@page { size: A4; margin: 1.6cm 1.7cm; }
* { font-family: Carlito, Calibri, 'DejaVu Sans', sans-serif; }
body { color:#1a1a1a; font-size:10.7pt; line-height:1.42; }
h1 { font-size:19pt; margin:0 0 2px 0; }
.sub { color:#666; font-size:10.5pt; margin:0 0 14px 0; }
h2 { font-size:12.5pt; margin:16px 0 6px 0; border-bottom:1.4px solid #1a1a1a; padding-bottom:3px; }
.slide { page-break-inside:avoid; margin:0 0 11px 0; padding:8px 10px; border:0.8px solid #d8d8d8; border-radius:4px; }
.snum { display:inline-block; min-width:22px; font-weight:bold; }
.stitle { font-weight:bold; font-size:11.3pt; }
.lab { font-weight:bold; font-size:8.6pt; letter-spacing:.4px; color:#888; text-transform:uppercase; margin-top:6px; }
.disc { margin:2px 0 0 0; }
.rem { margin:1px 0 0 0; color:#333; }
.tr { margin:1px 0 0 0; font-style:italic; color:#555; }
.qa { margin:5px 0; } .qa .q { font-weight:bold; }
ul { margin:4px 0 4px 18px; padding:0; } li { margin:2px 0; }
.small { color:#888; font-size:9pt; }
"""

parts=[]
parts.append("<html><head><meta charset='utf-8'><style>%s</style></head><body>"%css)
parts.append("<h1>PERIVALLON — Discorso di presentazione (SOTA)</h1>")
parts.append("<p class='sub'>Multispectral satellite imagery for illegal waste material classification — State of the art · 24 slide · per-slide talk, numeri, transizioni, Q&A · Alessandro Potenza</p>")

parts.append("<h2>Apertura & consegna</h2><ul>")
for t in TIPS: parts.append("<li>%s</li>"%t)
parts.append("</ul>")

parts.append("<h2>Discorso, slide per slide</h2>")
for num,tit,disc,rem,tr in S:
    parts.append("<div class='slide'>")
    parts.append("<div><span class='snum'>%d.</span> <span class='stitle'>%s</span></div>"%(num,esc(tit)))
    parts.append("<div class='lab'>Cosa dico</div><div class='disc'>%s</div>"%esc(disc))
    parts.append("<div class='lab'>Da ricordare</div><div class='rem'>%s</div>"%esc(rem))
    parts.append("<div class='lab'>Transizione</div><div class='tr'>%s</div>"%esc(tr))
    parts.append("</div>")

parts.append("<h2>Domande probabili (Q&A) e trappole</h2>")
for q,a in QA:
    parts.append("<div class='qa'><div class='q'>%s</div><div>%s</div></div>"%(esc(q),esc(a)))

parts.append("<p class='small'>Numeri verificati dai paper (papers/notes). † = paywalled/pre-print/vendor — presentare come motivanti, non stabiliti. Fonti chiave: Gibellini 2025, Aguilar 2021, Shepherd 2025, Cilia 2015, Kokaly 2017 (splib07a), Xiong 2024 (DOFA), Torres 2023 (AerialWaste).</p>")
parts.append("</body></html>")

open(OUT_HTML,"w",encoding="utf-8").write("".join(parts))
r=subprocess.run(["wkhtmltopdf","--quiet","--enable-local-file-access",OUT_HTML,OUT_PDF])
print("PDF:",OUT_PDF, "exists:", os.path.exists(OUT_PDF), "size:", os.path.getsize(OUT_PDF) if os.path.exists(OUT_PDF) else 0)
