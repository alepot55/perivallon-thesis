

Documento di lavoro: feedback Thomas sulla SOTA, riorganizzato per slide e per tema trasversale. Tag: **[STRATEGICO]** cambia impostazione, **[CONTENUTO]** modifica materiale, **[FORMA]** stile/layout.

---

## Trasversali

### Narrativa generale

Thomas conferma la struttura ma vuole sia più esplicita. Sequenza approvata:

1. Cosa è il problema
2. Perché è un problema
3. Cosa esiste oggi
4. Cosa manca
5. Cosa propongo e perché

L'ordine attuale è quasi giusto, Thomas l'ha riordinato un po' a voce — da riflettere nei titoli e nella sequenza slide.

### Riposizionamento del problema

**[STRATEGICO]** Non è "rilevare rifiuti" stile Gibellini con +63% di scoperta. È **individuare siti e classificarli per rischio**, per dare ad ARPA priorità di intervento. La proposition di valore è intervento più efficiente, non solo "trovo più siti". Da riscrivere nella slide 2.

Sapere *cosa c'è* in un sito (materiali) abilita la priorità: amianto e rifiuti pericolosi richiedono intervento rapido, materiali inerti meno. È utilità operativa per la PA.

### Generalizzazione, non OOD

**[STRATEGICO]** Sostituire "OOD" con "generalizzazione" nei titoli e nel discorso. Concetto vero: la generalizzazione fa schifo nei lavori esistenti. Il termine OOD è gergo, "generalization gap" è messaggio.

### Smettere di cavalcare Gibellini

**[STRATEGICO]** Citarlo come punto di partenza, non come riferimento centrale. Ridurre peso visivo (il 92% F1 in caratteri grossi nella slide 3 è troppo).

### Acronimi e definizioni

**[FORMA]** Definire alla prima occorrenza, sistematicamente: EO, MS, MSI, HSI, GSD, FM, SAM. Per slide importanti splittate aggiungere paginazione "1/2" e "2/2" nei titoli.

### Italianizzazione selettiva

**[FORMA]** Termini tecnici inglesi consolidati (red edge, foundation model, fine-tuning) restano in inglese. Verbi e nomi che hanno equivalente italiano puro vanno in italiano. Decisione caso per caso.

### Visuali concreti

**[FORMA]** Più esempi visuali, meno solo testo e grafici di laboratorio. In particolare:

- Slide 5: usare l'immagine "bande colorate per materiale" che Thomas ha mandato
- Slide 7: aggiungere foto materiali reali accanto ai grafici spettrali
- Generale: preparare esempi visuali per "detection waste a 10 m" (screenshot tile S2)

---

## Slide per slide

### Slide 2 — Problema e domanda

**[STRATEGICO]** Riscrivere completamente. C'è confusione tra problema / obiettivo / metodo, vanno separati chiaramente anche se serve splittare in 2-3 slide. Non importa il numero ma la chiarezza.

Nuovo contenuto:

- **Problema**: classificare siti per rischio, non solo rilevarli. Priorità d'intervento per ARPA
- **Obiettivo**: sapere *cosa c'è* (materiali), non solo *che c'è qualcosa*. Materiali → rischio → priorità
- **Metodo (anticipato)**: usare informazione spettrale satellitare per discriminare materiali

**[CONTENUTO]** Riposizionare Gibellini. Una riga, non il blocco "92% F1 / +63% scoperta" con caratteri grossi. Diventa: "il rilevamento RGB ha raggiunto buone performance in-distribution (Gibellini 2025), il gap è nella *classificazione del materiale* e nella *generalizzazione*".

### Slide 3 — Today's paradigm

**[CONTENUTO]** Ridurre enfasi sul 92%. Spostare focus su cosa il paradigma *non* fa: niente materiale, generalizzazione debole.

**[CONTENUTO]** Anticipare qui il messaggio "la generalizzazione fa schifo" — passa meglio come narrativa.

### Slide 4 — Beyond RGB

**[STRATEGICO]** Splittare in due slide. I risultati erano nascosti.

- **4a**: alta risoluzione gratuita → Sentinel-2 con MARIDA, MADOS, Kruse, Tisza, Desa
- **4b**: altissima risoluzione commerciale → WV-3 con Aguilar/Uhrin, Frassy, Cilia, Saba

**[CONTENUTO]** Mostrare meglio i risultati di entrambi i filoni (F1, mAP dove disponibili). Non solo "esiste questo lavoro".

### Slide 5 — Cubo spettrale

**[CONTENUTO]** Cambiare immagine principale. Il cubo con facce colorate "è sempre una fotografia", non corretta concettualmente. Usare l'immagine bande-colorate-per-materiale di Thomas.

**[CONTENUTO]** Aggiungere mini-grafico spettro di vegetazione o foglia, stile immagine Thomas. Aiuta a digerire il concetto di "vettore di riflettanza".

### Slide 6 — Spectral fingerprints

**[FORMA]** Grafico va bene così. Conservare.

### Slide 7 — RGB fails in two distinct ways

**[CONTENUTO]** Migliorare il grafico di destra. Thomas non specifica come — probabile che la fascia di mixing sia ancora confusa o l'annotazione C-H 1730 nm vada resa più chiara.

**[CONTENUTO]** Aggiungere immagini di materiali reali accanto ai grafici spettrali. Foto di plastica bianca / amianto / cemento per ancorare visivamente l'argomento iso-cromatico.

### Slide 8 — Where the diagnostic information lives

**[STRATEGICO]** Riordino con la slide sensori (attuale 12). Thomas suggerisce di rimettere la slide satelliti *prima* del discorso sulle bande diagnostiche, perché contestualizza. Da rivedere ordine generale 8-12.

**[CONTENUTO]** Risoluzione radiometrica: non aggiungerla, Thomas dice esplicitamente che non è utile.

**[CONTENUTO]** SWIR a 3 m è utile come messaggio. Anche se SuperDove non ce l'ha, il fatto che WV-3 abbia SWIR a 3 m (non 30 m come PRISMA) va passato. Significa che la combinazione SWIR + alta risoluzione esiste, è solo costosa.

### Slide 9 — Photon-budget triangle

**[FORMA]** Conservare.

### Slide 10 — Tabella regioni spettrali

**[FORMA]** Conservare.

### Slide 11 — But more bands is not always more information

**[FORMA]** Conservare. Il caveat onesto in arancione resta importante.

### Slide 12 — SuperDove sweet spot

**[STRATEGICO]** Rivedere il messaggio centrale. "SuperDove is the sweet spot" è troppo netto. Thomas chiarisce: SuperDove non è l'unico. WV-3 e Pléiades Neo restano opzioni serie. SuperDove è scelta giustificata da costo/accesso, non da superiorità intrinseca.

Riformulare titolo: "SuperDove: the chosen trade-off for this thesis" o "SuperDove: balancing access, resolution, spectral coverage".

**[STRATEGICO]** Orizzonte 30-50 cm. Thomas dice "30-50 cm andremo" — interpreto come futuro post-tesi (Pléiades Neo, WorldView a risoluzioni più alte). Accennare come orizzonte futuro, non come scope tesi. **Da confermare con Thomas**.

**[CONTENUTO]** Rivedere punti dei satelliti. Thomas dice di ricontrollare — probabile che alcune specifiche tecniche siano imprecise.

**[STRATEGICO]** Anticipare questa slide. Spostarla prima della tabella regioni spettrali (slide 10). Ordine corretto: sensori → dove vive l'informazione → SuperDove sceglie qui.

### Slide 13 — Foundation models for EO

**[FORMA]** Definire EO nel titolo come acronimo.

**[CONTENUTO]** Motivare perché i primi FM non vanno bene. Aggiungere colonna o nota: GSD pretraining mismatch con SuperDove 3 m (Prithvi a 30 m, SatMAE su fMoW, etc.). Senza questa motivazione la slide è una lista neutra.

**[CONTENUTO]** DOFA piace. Va enfatizzato di più. Thomas suggerisce slide dedicata.

### Slide 14 — DOFA dedicata (nuova)

**[STRATEGICO]** Espandere la slide DOFA:

- Cosa fa / cosa non fa
- Quali bande e sensori gestisce
- Come gestisce l'input: preprocessing prima del modello, almeno riscalatura
- **Domanda critica di Thomas**: DOFA non colma già il gap? Se DOFA gestisce input arbitrari di bande, la domanda "i FM pretrained a 10-30 m trasferiscono a 3 m?" è già risolta? Da chiarire onestamente

**[CONTENUTO]** Citare tecnica two-rami RGB+MS che si uniscono. Thomas dice "è interessante e può valere la pena". Inserire come riferimento architetturale alternativo a DOFA. **Da approfondire quale paper o esempio specifico**.

**[STRATEGICO]** DOFA è candidato per partire, se Thomas conferma. Posizionare come scelta operativa concreta, non solo riferimento.

### Slide 15 — vuota

Placeholder grafo concettuale RGB → MS → U. Per ora lasciare o riassorbire.

### Slide 16 — Gaps in the literature

**[STRATEGICO]** Verificare il primo gap dei dataset. Thomas dice "controllare bene". Il primo gap attuale è "No public terrestrial multispectral waste dataset with material-level labels". La nostra ricerca dataset ha confermato che è vero: DroneWaste è terrestre ma da drone, dataset MS satellitare con label materiale non esiste pubblicamente. Va detto più rigorosamente però.

**[CONTENUTO]** Spostare al primo posto il gap "material-level labels still missing". È il gap fondamentale che giustifica la tesi — è la parte importante.

### Slide 17 — Proposed direction

**[STRATEGICO]** Riformulare la fase 1. Thomas suggerisce approccio meno AI, più terra terra:

1. Estrarre firme spettrali da SuperDove su tetti (con e senza etichette amianto)
2. Provare a clusterizzare *senza* usare le label
3. Vedere se vengono gruppi naturali

Due esiti possibili:

- Cluster si formano e corrispondono a materiali distinti → segnale c'è
- Cluster non si formano o sono confusi → segnale non c'è in VNIR

Domanda chiave: posso usare queste firme? Hanno senso? O non dicono niente? Prima ancora di darle a un modello deep.

Cambio significativo rispetto al SAM con endmember da WaRM/USGS. Più conservativo e più adatto a "vedere cosa c'è" prima di committersi a una pipeline specifica.

**[CONTENUTO]** Verificare se ha senso comprare scene WV-3 SWIR a 3 m per una piccola AOI, come gold standard di confronto. Tenerla come opzione di validazione.

**[CONTENUTO]** Preparare esempi visuali per detection waste a 10 m (Sentinel-2). Il prof potrebbe chiedere "ma 10 m vede qualcosa? Mostrami".

---

## Punti di azione prioritari

1. Eseguire lo script Python di review sistematica che Thomas ha mandato (rinominare `.txt → .py`). Prima azione concreta della lista
2. Riscrivere slide 2 con nuova framing: classificazione per rischio, priorità intervento, non solo "trovare di più"
3. Splittare slide 4 in due slide (alta risoluzione gratuita / altissima risoluzione commerciale)
4. Aggiungere slide DOFA dedicata (cosa fa, cosa non fa, bande/sensori, gestione input, risposta al gap-question)
5. Sostituire immagine slide 5 con quella di Thomas
6. Riformulare fase 1 del pilot: clustering esplorativo su firme spettrali, non SAM con endmember predefiniti
7. Spostare slide satelliti (12) prima della tabella regioni spettrali (10)
8. Sostituire "OOD" con "generalizzazione" ovunque

---

## Da chiarire con Thomas al prossimo sync

Punti dove non sono sicuro dell'interpretazione:

- "Slide in più meglio DOFA" — vuole una slide solo per DOFA (oltre alla tabella FM) o vuole rimpiazzare la tabella?
- "Two-rami per RGB e MS che si uniscono" — sta parlando di un'architettura specifica con cross-attention fusion? Quale paper o esempio?
- "30-50 cm andremo" — orizzonte futuro post-tesi o scope già rilevante per fase 4?
- "Detection waste 10" — interpreto come Sentinel-2 a 10 m con richiesta esempi visuali. Confermare
- WV-3 SWIR 3 m: tenerla come opzione di validazione o accantonare?

---

## Quote rilevanti per riferimento futuro

> "Non è solo 63% in più, è intervento più efficiente"

> "La generalizzazione è una merda"

> "Cosa esiste e cosa fanno, gap cosa manca, e poi cosa vorrei fare, scelte"

> "Quel grafichino di Thomas con vegetazione e foglia, una cosa di quel genere"

> "Tiriamo fuori 'ste firme spettrali. Posso usarle? Ha senso? O non dicono niente? Prima di darle a un modello deep..."

> "I grafici sono laboratorio ma io voglio da satellite, quindi capire satellite cosa può dare"

> "Material-level labels still missing — parte importante, obiettivo, occhio"
