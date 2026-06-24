# Deep Learning Multispettrale per il Rilevamento di Rifiuti Illegali

Fondamenti tecnici e stato dell'arte

*Documento interno di studio — Marzo 2026*

## Indice

## 1. Come funziona il telerilevamento

Il telerilevamento (remote sensing) consiste nel raccogliere
informazioni su un oggetto o un'area senza contatto fisico diretto. Nel
nostro caso, un sensore montato su un satellite misura la luce riflessa
dalla superficie terrestre. Questo capitolo parte dalle basi fisiche per
costruire l'intuizione necessaria a capire perché il multispettrale è
utile.

### 1.1 Luce, spettro elettromagnetico e riflettanza

La luce del sole è radiazione elettromagnetica. Quando colpisce una
superficie, una parte viene assorbita, una parte riflessa, e una parte
trasmessa. Il rapporto tra luce riflessa e luce incidente si chiama
riflettanza, e varia in funzione della lunghezza d'onda. Questa
variazione è il segnale fondamentale che sfrutta il telerilevamento.

Lo spettro elettromagnetico si divide in regioni. Quelle rilevanti per
noi sono: **visibile** (400--700 nm, quello che vede l'occhio umano),
**infrarosso vicino (NIR)** (700--1000 nm), e **infrarosso a onde corte
(SWIR)** (1000--2500 nm). Un'immagine RGB standard cattura solo tre
bande strette dentro il visibile (rosso, verde, blu). Un sensore
multispettrale cattura 4--16 bande, estendendosi nel NIR e nel SWIR. Un
sensore iperspettrale cattura centinaia di bande strettissime.

L'idea chiave è semplice: materiali diversi assorbono e riflettono la
luce in modo diverso a diverse lunghezze d'onda. Se misuri la
riflettanza a più lunghezze d'onda, puoi distinguere materiali che a
occhio nudo (RGB) appaiono identici.

### 1.2 Firma spettrale: l'impronta digitale dei materiali

La **firma spettrale** di un materiale è la curva che descrive la sua
riflettanza in funzione della lunghezza d'onda. È come un'impronta
digitale: diversi materiali producono curve diverse. Vediamo tre esempi
classici che appaiono nella slide 9 della presentazione PERIVALLON:

-   **Vegetazione verde:** alta riflettanza nel NIR (\~700--900 nm),
    causata dalla struttura interna delle foglie che riflette la
    radiazione infrarossa. Nel visibile, la clorofilla assorbe rosso e
    blu, riflettendo il verde --- ecco perché le piante sono verdi. Il
    "red edge", il brusco aumento di riflettanza tra rosso e NIR (\~700
    nm), è uno dei segnali più diagnostici in remote sensing.

-   **Suolo:** riflettanza che cresce gradualmente dal visibile al SWIR,
    senza picchi netti. La forma esatta dipende da umidità, composizione
    minerale e contenuto organico.

-   **Acqua:** riflettanza molto bassa ovunque, quasi zero oltre il NIR.
    L'acqua assorbe quasi tutta la radiazione infrarossa. Questo la
    rende facilissima da discriminare nel NIR.

Queste tre firme sono molto diverse tra loro, e basterebbe una singola
banda NIR per separarle. Ma il problema diventa interessante quando i
materiali da distinguere sono più simili tra loro --- come diversi tipi
di rifiuti.

### 1.3 Perché l'RGB non basta per i rifiuti

Con tre bande RGB (rosso, verde, blu, tutte tra 400 e 700 nm) vedi
forma, colore e texture. Queste feature bastano per detection binaria:
"c'è un mucchio di roba anomala in questo campo?" --- ed è esattamente
quello che fa la pipeline di Gibellini et al. con 92% F1. Ma per la
classificazione dei materiali, l'RGB è strutturalmente limitato.

Considera due pile di rifiuti: una di plastica e una di legno secco. Nel
visibile possono avere colori simili (marrone chiaro, grigio). Ma nel
SWIR succede qualcosa di diverso:

-   **Plastica (PE, PP, PET):** mostra assorbimenti diagnostici a \~1215
    nm, \~1730 nm e \~2312 nm, causati dai legami C--H nei polimeri.
    Questi assorbimenti sono come "vallate" nella curva di riflettanza,
    assenti nei materiali non plastici. Diversi tipi di plastica
    (polietilene, polipropilene, PET) hanno picchi di assorbimento
    leggermente diversi, il che li rende separabili tra loro nel SWIR.

-   **Legno:** la cellulosa ha feature di assorbimento attorno a 1730 nm
    e 2100 nm. La firma assomiglia a quella della vegetazione secca, il
    che ha senso --- il legno è vegetazione morta. Nel NIR (\~1100 nm)
    mostra riflettanza medio-alta.

-   **Metallo:** riflettanza alta e piatta dallo spettro visibile al
    SWIR, senza feature di assorbimento significative. Non ha "vallate"
    perché la riflessione è di tipo speculare, non dipendente dalla
    composizione molecolare. Si discrimina per brightness e texture, non
    per firma spettrale.

-   **Pneumatici/gomma:** contengono carbon black, che assorbe
    fortemente in tutto lo spettro. La riflettanza è molto bassa
    ovunque, con deboli feature di assorbimento da idrocarburi. Gomma
    nera e plastica nera restano difficili da separare anche nel SWIR.

-   **Tessili:** poliestere (sintetico) mostra un calo a \~1650 nm,
    mentre cotone e fibre naturali hanno assorbimenti a 1400--1600 nm.
    Questa distinzione sintetico/naturale è impossibile nell'RGB.

-   **Macerie/inerti:** i minerali argillosi mostrano un assorbimento a
    \~2200 nm. La firma è composita e dipende dal mix di materiali
    (cemento, mattoni, terra).

+-----------------------------------------------------------------------+
| **Il punto chiave**                                                   |
|                                                                       |
| Le feature di assorbimento diagnostiche per i materiali rifiuto       |
| cadono quasi tutte oltre i 700 nm (NIR e SWIR). Con sole 3 bande RGB  |
| non le vedi. Aggiungere anche solo una banda NIR migliora             |
| significativamente la classificazione; aggiungere bande SWIR la       |
| trasforma.                                                            |
+-----------------------------------------------------------------------+

### 1.4 Le evidenze quantitative

Non è solo teoria. La letteratura recente fornisce numeri concreti sul
valore aggiunto del multispettrale:

-   **Krauz et al. (2025):** su rifiuti da costruzione e demolizione,
    aggiungere la sola banda a 800 nm (NIR) all'RGB ha prodotto
    accuratezze comparabili all'uso di tutte le 768 bande iperspettrali.
    Risultato sorprendente: poche bande ben scelte valgono quanto
    centinaia.

-   **SatMAE (NeurIPS 2022):** +7% su benchmark supervisionati e +14% su
    transfer learning aggiungendo bande multispettrali Sentinel-2
    rispetto al solo RGB. Il guadagno è più evidente nel transfer
    learning, dove il modello deve generalizzare.

-   **Uhrin et al. (2025):** precisione 0.92--0.95 nel mappare
    aggregazioni di plastica (80--150 m²) usando le 8 bande SWIR di
    WorldView-3, con correlazione lab-to-satellite di r = 0.95. Le firme
    misurate in laboratorio matchano quelle misurate da 600 km di
    altezza.

-   **Magyar et al. (2023):** \~96% di accuratezza nella detection di
    discariche illegali con Sentinel-2 multispettrale + Random Forest.
    Il NIR è risultata la banda più discriminante.

-   **SpectralWaste (IROS 2024):** la fusione RGB + dati spettrali
    (anche ridotti a 3 bande via PCA) supera costantemente entrambe le
    modalità singole. La fusione vince sempre.

## 2. I satelliti che userai

Questa sezione spiega cosa significa operativamente lavorare con dati
satellitari. Non è come scaricare un dataset da Zenodo --- ci sono
trade-off reali tra risoluzione spaziale, risoluzione spettrale,
copertura temporale, e costo.

### 2.1 Risoluzione spaziale: cosa significa in pratica

La **Ground Sample Distance (GSD)** è la dimensione del lato di un pixel
a terra. Se il GSD è 10 m, ogni pixel rappresenta un'area di 10×10 m =
100 m². Una discarica illegale tipica ha un'estensione di 50--200 m².
Vedi il problema: a 10 m di GSD, la discarica è contenuta in 1--2 pixel.
A 3 m di GSD, occupa 6--22 pixel. A 30 cm di GSD, occupa 550--2200
pixel.

Questo trade-off è cruciale per la tesi:

-   **Detection** (trovare le discariche): richiede GSD fine, idealmente
    ≤50 cm, per risolvere le texture dei rifiuti e distinguerli dal
    contesto. Gibellini et al. usano 20 cm GSD.

-   **Classificazione materiali** (capire di cosa sono fatti): richiede
    molte bande spettrali, ma il GSD può essere più grossolano --- se la
    discarica è già localizzata e sufficientemente grande, anche 3--10 m
    possono bastare per l'analisi spettrale del pixel medio.

Nessun satellite attuale offre contemporaneamente GSD submeter e molte
bande spettrali. Quindi la pipeline pratica è a due livelli: prima
rilevi con VHR RGB, poi classifichi i materiali con dati multispettrali
a risoluzione più bassa.

### 2.2 Le quattro piattaforme rilevanti

Sentinel-2 (Copernicus) --- il cavallo da lavoro

Gratuito, 13 bande, rivisita ogni 5 giorni. È il punto di partenza più
pratico. Le bande sono distribuite su tre gruppi di risoluzione:

-   **10 m:** B2 (Blue, 490 nm), B3 (Green, 560 nm), B4 (Red, 665 nm),
    B8 (NIR, 842 nm). Queste quattro bande sono la tua baseline RGB+NIR.

-   **20 m Red Edge:** B5 (705 nm), B6 (740 nm), B7 (783 nm), B8A (865
    nm). Il "Red Edge" è la regione tra rosso e NIR dove la riflettanza
    della vegetazione aumenta bruscamente. Queste bande catturano la
    transizione con alta risoluzione spettrale.

-   **20 m SWIR:** B11 (1610 nm), B12 (2190 nm). Le bande critiche per i
    materiali. B11 cattura gli assorbimenti C--H della plastica (\~1730
    nm è vicino). B12 cattura i minerali argillosi (\~2200 nm). Ma a 20
    m di GSD, ogni pixel copre 400 m² --- molte discariche occupano meno
    di un pixel.

Il dato Sentinel-2 viene distribuito come **Level-2A**: surface
reflectance, cioè la riflettanza già corretta per gli effetti
atmosferici. Formato GeoTIFF. Accesso tramite Copernicus Data Space o
Google Earth Engine.

+-----------------------------------------------------------------------+
| **Implicazione per la tesi**                                          |
|                                                                       |
| Sentinel-2 ti dà gratis 13 bande con SWIR, ma a 10--20 m. Per la      |
| detection di discariche piccole è inutile. Per l'analisi spettrale di |
| discariche già note e sufficientemente grandi, è un punto di partenza |
| solido.                                                               |
+-----------------------------------------------------------------------+

Planet SuperDove (PlanetScope) --- il compromesso

130+ satelliti, 8 bande VNIR a 3 m, copertura giornaliera. **Non ha
SWIR**. Le 8 bande sono: Coastal Blue (443 nm), Blue (490 nm), Green I
(531 nm), Green (565 nm), Yellow (610 nm), Red (665 nm), Red Edge (705
nm), NIR (865 nm). Progettate per interoperabilità con Sentinel-2.

Il vantaggio rispetto a Sentinel-2 è il GSD: a 3 m, una discarica di 100
m² occupa \~11 pixel invece di 1. Il Red Edge e il NIR permettono di
separare vegetazione da non-vegetazione con alta affidabilità. Accesso
gratuito tramite il programma Education & Research (hai già fatto
richiesta).

WorldView-3 (Maxar) --- l'unico con SWIR ad alta risoluzione

L'unico satellite commerciale operativo con bande SWIR a risoluzione
utile: **8 bande VNIR a 1.24 m + 8 bande SWIR a 3.7 m + pancromatico a
31 cm**. Le 8 bande SWIR coprono 1184--2373 nm con 165 combinazioni
uniche. Guo & Li (2020) hanno creato un indice specifico per la plastica
(NDPI) usando proprio queste bande. Costo: elevato, accesso tramite ESA
Third Party Missions o acquisto commerciale.

+-----------------------------------------------------------------------+
| **Perché è unico**                                                    |
|                                                                       |
| WorldView-3 è l'unico satellite che può sia vedere le discariche (31  |
| cm pan) sia identificare i materiali tramite SWIR (3.7 m). Se il      |
| gruppo PoliMi ha accesso a dati WV3, la tesi ha un vantaggio enorme.  |
| Le tile WV3 in AerialWaste sono RGB --- ma le acquisizioni originali  |
| includono 8 bande VNIR. Chiedi a Thomas.                              |
+-----------------------------------------------------------------------+

Pléiades Neo (Airbus) --- il VHR con Red Edge

30 cm pancromatico, 1.2 m multispettrale, 6 bande (Deep Blue, Blue,
Green, Red, Red Edge, NIR). Niente SWIR. Il Red Edge è utile per la
vegetazione ma non discrimina plastica da legno. È essenzialmente un
upgrade di Pléiades per la detection, non per la material
classification.

### 2.3 Il dilemma iperspettrale vs multispettrale

I satelliti iperspettrali come **PRISMA** (ASI, 239 bande) e **EnMAP**
(DLR, 230+ bande) offrono discriminazione materiale eccezionale. Ma a
30--60 m di GSD: una discarica di 100 m² è un terzo di pixel.
Inutilizzabile per il nostro caso d'uso.

Il sweet spot per la tesi è il **multispettrale commerciale**: 8--16
bande a 1--10 m di GSD. Abbastanza bande per discriminare i materiali
principali, abbastanza risoluzione per risolvere le discariche.
WorldView-3 è l'ideale (SWIR + VHR), Sentinel-2 è il fallback gratuito.

### 2.4 Formati dati e concetti operativi

I dati satellitari multispettrali vengono distribuiti come **GeoTIFF**:
un file TIFF con metadati geospaziali embedded (coordinate, proiezione,
CRS). Un file GeoTIFF multibanda ha N layer, uno per banda. In Python lo
apri con rasterio e ottieni un array NumPy di shape (N_bands, height,
width).

Concetti che devi conoscere:

-   **CRS (Coordinate Reference System):** il sistema di coordinate
    geospaziali. Sentinel-2 usa EPSG:32632 (UTM zone 32N) per l'Italia.
    SuperDove usa EPSG:4326 (WGS84) o UTM. Quando sovrapponi dati da
    sensori diversi, devi riproiettarli nello stesso CRS.

-   **Surface Reflectance vs Top-of-Atmosphere:** i livelli di
    processing. TOA è il dato grezzo (include effetti atmosferici).
    Surface Reflectance (SR) è corretto per l'atmosfera. Usa sempre SR
    quando disponibile --- è il dato fisicamente significativo.

-   **Pansharpening:** tecnica per fondere la banda pancromatica (alta
    risoluzione, una banda) con le bande multispettrali (bassa
    risoluzione, molte bande) per ottenere un prodotto ad alta
    risoluzione con informazione spettrale. Metodi classici:
    Gram-Schmidt, wavelet. Metodi DL: PanNet, LambdaPNN.

-   **Co-registrazione:** allineare pixel-per-pixel immagini da sensori
    diversi acquisite in tempi diversi. Necessaria quando sovrapponi
    label AerialWaste (RGB VHR) con imagery Sentinel-2 o Planet
    (multispettrale, risoluzione diversa).

## 3. Da 3 a N canali: il problema architetturale

Sai come funziona un modello di visione: il primo layer (conv2d o patch
embedding) accetta un tensore di input con 3 canali. I pesi pretrained
di quel layer hanno shape che dipende da 3. Se vuoi 8 o 13 canali, **non
puoi semplicemente cambiare in_channels** e usare gli stessi pesi. Ci
sono cinque strategie, ognuna con trade-off diversi.

### 3.1 Weight Inflation (replicazione dei pesi)

L'idea: prendi i pesi del primo layer pretrained su RGB (shape \[C_out,
3, k, k\]) e li "inflati" a \[C_out, N, k, k\]. Il metodo più semplice è
**replicare i pesi RGB e dividere per il numero di repliche**, così che
l'output del layer al primo forward pass sia simile a quello originale.

Concretamente, per un input a 6 canali: i canali 0-2 (che mappano su
RGB) ricevono i pesi originali divisi per 2, i canali 3-5 ricevono una
copia degli stessi pesi divisi per 2. L'idea è che il layer inizia con
feature utili (quelle RGB) e impara a usare i canali extra durante il
fine-tuning.

Variante: inizializzare i canali extra con la media dei pesi RGB. O
usare i pesi del canale RGB più simile spettralmente (es. i pesi del
canale Red per Red Edge).

-   **Pro:** semplicissimo da implementare, preserva le feature
    pretrained, nessuna modifica architetturale.

-   **Contro:** i canali extra partono con pesi poco informativi, il
    modello deve imparare cosa farne durante il fine-tuning. Se i canali
    extra portano informazione molto diversa (es. SWIR), i pesi
    replicati dall'RGB sono un punto di partenza scarso.

-   **Quando usarlo:** baseline di partenza. È quello che userai per
    estendere Swin-T (Gibellini) da 3 a N canali.

### 3.2 Random Initialization dei canali extra

Variante della precedente: i 3 canali RGB mantengono i pesi pretrained,
i canali extra vengono inizializzati random (Kaiming o Xavier). Corley
et al. (CVPR Workshop 2024) hanno mostrato che per i Vision Transformer
questo funziona sorprendentemente bene. La ragione: nei ViT, il patch
embedding è un singolo layer lineare che proietta tutti i canali in uno
spazio latente. Se il backbone è potente (DINOv2, MAE pretrained),
**anche un embedding layer inizializzato random converge velocemente**
perché il backbone sa già come processare le feature latenti.

Il paper SoftCon (2024) conferma: con DINOv2 come backbone, **random
init dell'input embedding + fine-tuning raggiunge state-of-the-art su 10
di 11 task EO**. Lo chiamano "both flexible and impressively effective".

-   **Pro:** nessun bias strutturale sui canali extra. Il modello è
    libero di imparare la rappresentazione ottimale.

-   **Contro:** richiede più dati o più epoche di fine-tuning perché
    deve imparare l'embedding da zero.

-   **Quando usarlo:** con backbone ViT pretrained (DINOv2, MAE). Non
    ideale per CNN dove il primo conv layer ha un ruolo più strutturale.

### 3.3 Band Grouping con Spectral Positional Encoding (SatMAE)

SatMAE (NeurIPS 2022) introduce un'idea elegante per Sentinel-2: le 13
bande hanno GSD diversi (10m, 20m, 60m), quindi non ha senso trattarle
come un unico cubo. La soluzione è **raggruppare le bande per
risoluzione e usare patch embedding separati per ogni gruppo**:

-   **Gruppo 1 (10 m):** B2, B3, B4, B8 --- 4 bande, patch size 8×8

-   **Gruppo 2 (20 m):** B5, B6, B7, B8A (Red Edge/NIR) --- 4 bande,
    patch size 4×4

-   **Gruppo 3 (20 m):** B11, B12 (SWIR) --- 2 bande, patch size 4×4

Ogni gruppo produce la propria sequenza di token, che vengono
concatenati e processati insieme dal Transformer encoder. Viene aggiunto
un spectral positional encoding per indicare al modello a quale gruppo
appartiene ciascun token.

Risultato: +7% su benchmark supervisionati, +14% su transfer learning
rispetto a RGB-only. Il guadagno nel transfer learning è particolarmente
importante perché dimostra che il modello impara rappresentazioni
multispettrali generalizzabili.

-   **Pro:** rispetta la geometria reale dei dati (risoluzioni diverse),
    miglior performance empirica.

-   **Contro:** architettura specifica per Sentinel-2, non drop-in
    replacement per modelli esistenti.

### 3.4 Wavelength-Conditioned Dynamic Networks (DOFA)

DOFA (Xiong et al., 2024) è la soluzione più elegante al problema.
Invece di fissare i pesi del patch embedding, usa una **hypernetwork**
che genera i pesi dinamicamente in base alle lunghezze d'onda centrali
dei canali in input.

Come funziona: dai al modello la lista delle lunghezze d'onda (es.
\[490, 560, 665, 842, 1610, 2190\] per 6 bande Sentinel-2).
L'hypernetwork prende queste lunghezze d'onda come input e genera i pesi
dell'embedding layer. In questo modo, un singolo modello può processare
input da qualsiasi sensore con qualsiasi numero di bande, senza
ritraining.

-   **Pro:** sensor-agnostico, un modello per tutti i sensori. Massima
    flessibilità. Integrato in TorchGeo.

-   **Contro:** complessità implementativa maggiore, l'hypernetwork
    aggiunge parametri.

-   **Quando usarlo:** se lavori con dati multi-sensore (es. train su
    Sentinel-2, test su SuperDove) o vuoi un modello che scala a sensori
    futuri.

### 3.5 Late Fusion (branch separate)

Approccio dual-stream: una branch processa RGB con pesi pretrained
intatti, una branch separata processa le bande extra (NIR, SWIR). Le
feature vengono fuse a un livello intermedio (concatenazione, somma,
attention) e passate al classificatore.

-   **Pro:** il branch RGB mantiene le feature pretrained senza alcuna
    modifica. I due branch possono essere pretrained indipendentemente.

-   **Contro:** più parametri, rischio di disallineamento tra le due
    rappresentazioni, più complesso da implementare e debuggare.

### 3.6 Quale strategia per la tesi

La raccomandazione pratica, data la baseline Gibellini (Swin-T) e le
risorse disponibili:

1.  **Baseline:** weight inflation su Swin-T. Coerente con il paper del
    gruppo, immediato da implementare. Questo è il tuo punto di
    partenza.

2.  **Confronto:** random init dei canali extra su un ViT (es. ViT-B/16
    pretrained DINOv2). Corley et al. mostrano che funziona meglio del
    previsto.

3.  **Avanzato:** DOFA o Prithvi-EO-2.0 se i risultati delle prime due
    strategie sono promettenti e vuoi un risultato da "frontiera" per la
    tesi.

## 4. Fine-tuning: strategie e preprocessing

### 4.1 Il two-step di Gibellini et al.

La pipeline PoliMi usa una strategia a due fasi che è diventata standard
nel remote sensing:

1.  **Fase 1 --- Head training:** backbone congelato, alleni solo il
    classification head. Questo permette al head di adattarsi alle
    feature del backbone senza corrompere i pesi pretrained. Poche
    epoche, learning rate alto.

2.  **Fase 2 --- Partial unfreezing:** sbloccchi l'ultimo stage del
    backbone (es. stage 4 di Swin-T) e alleni head + ultimo stage
    insieme. Learning rate più basso. Questo permette al backbone di
    adattare le feature high-level al dominio dei rifiuti senza
    distruggere quelle low-level (edge, texture).

Perché non full fine-tuning? Perché AerialWaste ha \~10K immagini ---
sufficienti per un head ma rischiose per fine-tunare un intero Swin-T da
28M parametri senza overfitting.

### 4.2 ImageNet vs Remote Sensing pretraining

Un dibattito aperto nella comunità RS: ha senso inizializzare con pesi
ImageNet (1000 classi di oggetti naturali) per un task su immagini
satellitari?

Corley et al. (2024) hanno mostrato che **ImageNet pretraining resta
sorprendentemente competitivo** se il preprocessing è fatto
correttamente: resize a 224×224, normalizzazione con media/std del
dataset RS (non di ImageNet), data augmentation geometrica (flip,
rotate). Molti paper che riportavano vantaggi del RS pretraining in
realtà confrontavano preprocessings diversi, non pretrainings diversi.

Tuttavia, per **bande non-RGB il discorso cambia**. ImageNet non ha NIR
o SWIR. I pesi del primo layer non hanno alcuna conoscenza di cosa
significhino queste bande. Per questo il RS pretraining (es. SSL4EO-S12,
Prithvi) è chiaramente superiore quando usi più di 3 canali.

### 4.3 Parameter-Efficient Fine-Tuning (PEFT)

Se le GPU PoliMi non sono infinite, puoi considerare approcci PEFT.
**DEFLECT (2025)** estende i patch embedding di un ViT con meno dell'1%
di parametri aggiuntivi, raggiungendo performance comparabili al full
fine-tuning. LoRA applicato a ViT per RS è un'altra opzione matura.

### 4.4 Preprocessing: i dettagli che contano

Errori comuni che possono costare 5--10 punti percentuali di
performance:

-   **Normalizzazione:** calcola media e std per banda sul tuo dataset,
    non usare valori di ImageNet. Ogni sensore ha un range di
    riflettanza diverso. Sentinel-2 L2A è tipicamente \[0, 10000\],
    SuperDove SR è \[0, 1\]. Normalizza per canale.

-   **Resize:** Corley et al. mostrano che ridimensionare a 224×224 (la
    dimensione di ImageNet) migliora il transfer learning anche per
    immagini RS. Ma attenzione: se stai analizzando firme spettrali, il
    resize può introdurre artefatti di interpolazione. Usa resize
    bilineare o nearest-neighbor a seconda del task.

-   **Data augmentation:** flip orizzontale e verticale, rotazioni di
    90°, sono standard per RS (le immagini satellitari non hanno "alto"
    e "basso"). Evita color jitter sui canali non-RGB --- altereresti la
    firma spettrale.

-   **Valori di riflettanza negativi o \>1:** possono comparire nei
    prodotti SR a causa di errori nella correzione atmosferica. Clippali
    a \[0, 1\] o \[0, 10000\] a seconda del formato.

## 5. Foundation models per Earth Observation

Dal 2023 il panorama dei foundation model RS è esploso. La logica è la
stessa di BERT/GPT nel NLP: alleni un modello enorme su dati non
annotati (self-supervised), poi lo fine-tuni su task specifici con pochi
dati annotati. La differenza rispetto a ImageNet pretraining è che
questi modelli sono allenati su **immagini satellitari multispettrali**,
quindi le feature che imparano sono rilevanti per il RS (tipo di
terreno, vegetazione, acqua, infrastrutture).

### 5.1 Prithvi-EO-2.0 (NASA/IBM)

Il modello più rilevante per la tesi. Caratteristiche chiave:

-   **Input nativo:** 6 bande HLS (Blue, Green, Red, Narrow NIR, SWIR1
    1610 nm, SWIR2 2190 nm). Include le bande SWIR che servono per i
    materiali.

-   **Architettura:** ViT con 600M parametri e 3D patch embeddings
    (spazio + tempo). Può processare serie temporali di immagini per
    change detection.

-   **Pretraining:** Masked Autoencoder (MAE) su 4.2 milioni di campioni
    HLS globali. Impara a ricostruire patch mascherate.

-   **Performance:** 75.6% media su GEO-Bench, superando 6 altri
    foundation models di 8 punti percentuali.

-   **Fine-tuning:** supportato via TerraTorch (IBM), con decoder head
    UPerNet per segmentazione e FCN per classificazione.

Il vantaggio operativo di Prithvi è il supporto nativo alle bande SWIR.
Se alleni su dati Sentinel-2 ritagliando le 6 bande HLS, puoi usare
Prithvi out-of-the-box. Pesi su HuggingFace:
*ibm-nasa-geospatial/Prithvi-EO-2.0-600M*.

### 5.2 SSL4EO-S12 (TU Munich/DLR)

Il punto di partenza più pratico se usi Sentinel-2. Fornisce pesi
pretrained per tutte le 13 bande S2, su architetture standard:

-   **MoCo-v2** su ResNet-50: contrastive learning, buon tradeoff
    performance/complessità

-   **DINO** su ViT-S: self-distillation, produce feature molto buone
    per downstream

-   **MAE** su ViT-B e ViT-L: masked autoencoder, il più performante ma
    anche il più pesante

Allenato su 251K location globali con 4 timestamp stagionali. Il
vantaggio è che usi architetture standard (ResNet, ViT) che conosci già,
ma con pesi che "sanno" cosa sono le 13 bande Sentinel-2. Non devi
cambiare architettura, solo cambiare i pesi iniziali. Licenza
Apache-2.0.

### 5.3 DOFA (TU Munich)

Descritto nella sezione 3.4 come strategia architetturale. Come
foundation model, è pre-allenato su 5 modalità EO (multispettrale, SAR,
altimetria, ecc). Il vantaggio: **un singolo set di pesi gestisce
qualsiasi sensore**. Lo carichi da TorchGeo e gli passi le lunghezze
d'onda del tuo sensore. Massima flessibilità, utile se lavori con più
sensori (es. train su S2, inference su SuperDove).

### 5.4 Come scegliere

  ------------------ ----------------------- ----------------------------
  **Scenario**       **Modello consigliato** **Perché**

  Sentinel-2 only,   SSL4EO-S12 (ResNet-50 o Pesi pronti per 13 bande,
  architettura       ViT)                    drop-in replacement
  standard                                   

  Sentinel-2 con     Prithvi-EO-2.0          Supporto nativo 6 bande HLS
  SWIR focus                                 incluso SWIR

  Multi-sensore      DOFA                    Sensor-agnostico, un modello
  (S2 + SuperDove)                           per tutti

  Baseline rapida,   Weight inflation + RSP  Coerente con Gibellini,
  Swin-T                                     minimo effort
  ------------------ ----------------------- ----------------------------

## 6. La pipeline PoliMi: Gibellini et al. (2025)

Questa sezione spiega il paper di riferimento scelta per scelta, così
che tu sappia esattamente cosa stai estendendo.

### 6.1 Il task

**Classificazione binaria di scene**: data un'immagine (tile) RGB ad
alta risoluzione, il modello risponde "waste" o "no-waste". Non
localizza i rifiuti nell'immagine (non è detection con bounding box),
non segmenta. È il task più semplice, ma è già operativamente utile:
scansioni una regione tile per tile e ottieni una mappa di "hot spots".

### 6.2 Il dataset: AerialWaste v3

\~11.700 tile da 3 sorgenti con GSD diversi:

-   **AGEA (\~20 cm):** ortofoto dell'agenzia agricola italiana.
    Copertura uniforme della Lombardia.

-   **WorldView-3 (\~30 cm):** acquisizioni commerciali VHR. Solo bande
    RGB estratte.

-   **Google Earth (\~50 cm):** immagini scaricate dall'archivio web.

Le annotazioni hanno tre livelli: binary (waste/no-waste, 3.478 positivi
su 10.434), multi-class (22 categorie di materiali: macerie, pneumatici,
veicoli, container, big bags, ecc.), e segmentation masks per un
sottoinsieme di 169 immagini. Il dataset è **RGB-only**. Estenderlo con
bande multispettrali è il contributo principale della tesi.

### 6.3 L'architettura: Swin-T + RSP

**Swin Transformer-Tiny (Swin-T)** è un Vision Transformer con attention
a finestra scorrevole. A differenza di ViT vanilla (che ha attention
globale O(n²)), Swin-T opera in finestre locali 7×7 con shift tra layer
successivi, riducendo la complessità a O(n). Ha 28M parametri,
dimensione feature \[96, 192, 384, 768\] nei 4 stage.

**Remote Sensing Pretraining (RSP)** sono pesi ottenuti allenando Swin-T
su dataset RS (es. MillionAID, NWPU-RESISC45) prima di fine-tunarlo su
AerialWaste. Il vantaggio: il modello arriva già con feature rilevanti
per immagini aeree (pattern agricoli, edifici, strade, texture naturali)
invece delle feature di ImageNet (gatti, auto, cibo).

### 6.4 Il GSD ottimale: 20 cm

Gibellini et al. testano diversi GSD e trovano che 20 cm/pixel con tile
da 100×100 m (500×500 pixel) è ottimale. Perché:

-   GSD troppo fine (\<10 cm): le tile sono troppo piccole per catturare
    il contesto. Vedi dettagli individuali (singoli sacchi, mattoni) ma
    perdi la "scena".

-   GSD troppo grossolano (\>50 cm): perdi i dettagli. Un mucchio di
    macerie a 1 m/pixel è un quadrato grigio indistinguibile da un
    parcheggio.

-   20 cm è il compromesso: abbastanza dettaglio per vedere le texture
    dei rifiuti, abbastanza contesto per capire la scena.

### 6.5 Risultati chiave

  ------------------------------- ------------------- -------------------
  **Configurazione**              **F1-Score**        **Accuracy**

  Swin-T + RSP (best)             92.02%              94.56%

  Swin-T + ImageNet               89.74%              93.12%

  ResNet-50 + RSP                 88.45%              92.68%

  Cross-region (generalizzazione) \~87% (-5%)         \~90%
  ------------------------------- ------------------- -------------------

Il delta RSP vs ImageNet (+2.3% F1) conferma il valore del RS
pretraining per immagini aeree, anche su RGB. Il calo di \~5% F1 su
regioni non viste è un risultato solido per un modello di detection
senza alcun dato dalla regione target.

Impatto operativo: il sistema aumenta del 63% il tasso di scoperta di
discariche e riduce del 12% il tempo di analisi rispetto all'ispezione
manuale.

### 6.6 Cosa estendi e perché

La tesi prende questa pipeline e risponde alla domanda: se aggiungiamo
bande multispettrali, la classificazione migliora? Concretamente:

1.  **Stesso task** (scene classification), ma con input a N canali
    invece di 3.

2.  **Stesso backbone** (Swin-T), con weight inflation per gestire i
    canali extra. Più confronti con ViT + random init e con foundation
    models.

3.  **Ablation study sistematica:** RGB (3 bande) → RGB+RE+NIR (6 bande)
    → full Sentinel-2 (13 bande). Misuri il delta e capisci quale
    configurazione di bande dà il miglior rapporto costo-beneficio.

4.  **Eventuale estensione a material classification:** se i risultati
    lo giustificano, passi da classificazione binaria (waste/no-waste) a
    classificazione multi-class (tipo di materiale). Questo richiede le
    annotazioni a 22 classi di AerialWaste.

+-----------------------------------------------------------------------+
| **Il gap critico che riempi**                                         |
|                                                                       |
| Nessun dataset pubblico combina bande multispettrali satellitari con  |
| annotazioni di materiali rifiuto terrestri. Creare anche solo un      |
| paired dataset (tile AerialWaste + patch Sentinel-2 co-registrate)    |
| sarebbe una contribuzione significativa e pubblicabile.               |
+-----------------------------------------------------------------------+

## 7. Lo stack software

Panoramica dei tool che userai quotidianamente, con indicazione di cosa
serve a cosa.

### 7.1 TorchGeo

Framework di Microsoft (v0.8+), costruito su PyTorch Lightning. È
l'equivalente di Torchvision per il remote sensing. Cosa offre: 110+
modelli pretrained per imagery multispettrale (incluso DOFA), sampler
geospaziali che campionano patch basandosi su coordinate e CRS (non su
indici), e data loader per 120+ dataset RS (EuroSAT, BigEarthNet,
SEN12MS). Il vantaggio chiave: **gestisce automaticamente la
riproiezione CRS** quando sovrapponi raster e vettori.

### 7.2 Rasterio

Interfaccia Python a GDAL per leggere/scrivere GeoTIFF. In pratica:
rasterio.open('image.tif') ti dà un oggetto con .read() che restituisce
un array NumPy (n_bands, h, w), .crs per il sistema di coordinate,
.transform per la matrice affine pixel→coordinate. Supporta windowed
reading per leggere solo una porzione di scene grandi (che possono
pesare gigabyte).

### 7.3 GeoPandas

Pandas + geometrie geospaziali. Lo usi per gestire annotazioni
poligonali (le mask di AerialWaste), fare spatial join ("quali tile
intersecano questa scena Sentinel-2?"), e overlay vettore-raster
("estrami le statistiche spettrali dentro questi poligoni").

### 7.4 QGIS

Desktop GIS gratuito. Lo usi per visualizzare le scene satellitari,
verificare la co-registrazione, creare false-color composite
interattive, e fare analisi esplorative con il plugin SCP
(Semi-Automatic Classification Plugin). Non scrivi codice in QGIS --- lo
usi come tool di ispezione visiva.

### 7.5 TerraTorch

Toolkit IBM per fine-tunare Prithvi-EO-2.0. Gestisce il caricamento dei
pesi, l'aggiunta del decoder head (UPerNet per segmentazione, FCN per
classificazione), e il training loop. Se decidi di usare Prithvi,
passerài da qui.
