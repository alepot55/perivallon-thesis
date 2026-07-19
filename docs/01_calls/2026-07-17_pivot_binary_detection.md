# Call Thomas — 2026-07-17 (pivot: binary detection satellite-only)

Enrico assente: il deep-dive tecnico su esperimenti e codice slitta alla call della settimana del 20/7 (mar/mer, con lui). Fonte: trascrizione STT del 2026-07-17 h10:31, ~25 min.

Nomi verificati post-call: **Enrico Targhini** ✓ (enrico.targhini@polimi.it), **Alari** ✓ (tesi 2024 material classification, politesi 10589/230633). "Asha"/~Mohamed Jabbari… (short change detection) resta da confermare.

---

## Verdetto generale

La SOTA sui materiali non ha mostrato premesse abbastanza solide: portare a casa il lavoro su quella strada era **rischioso**. In più il dataset interno è **solo satellitare e piccolo** (~1.200 immagini): rifare il discorso di Alari (material classification) non sta in piedi ora. Quindi si parte **più cauti**: **binary landfill detection** (detection, non classificazione) su immagini satellitari multispettrali, esplorando modelli, combinazioni, pretraining e soprattutto il comportamento **al variare della risoluzione**. Il filone materiali non muore — "ci sarà in programma", quando e come TBD.

## Cambio di rotta

| Prima | Dopo (questa call) |
|---|---|
| RQ: valore aggiunto MS vs RGB per **material classification** | **Binary detection** di landfill, satellite-only |
| Asse sperimentale: band ablation (RGB→VNIR→+SWIR) | Asse sperimentale: **risoluzione** (30 cm → ~70 cm → 1.2 m) |
| Riferimento: pipeline materiali stile Alari 2024 | Riferimento: **binary di Fede (Federico Gibellini)** |
| Guida tecnica: Thomas | Thomas + **Enrico Targhini** (sale ufficialmente a bordo per la parte AI: è lui che ha in mano il codice) |

Nota di contesto: Thomas stesso sul filone waste è sempre stato coinvolto "di striscio" — per il codice la guida è Enrico (in gruppo da 2 anni, codice sotto mano).

## Piano sperimentale

- **Task**: binary detection su satellite-only, multispettrale. Capire se ci sono modelli più adatti, combinazioni, pretraining.
- **Risoluzioni**:
  - **30 cm** (pansharpened) — punto di partenza;
  - **1.20 m nativo** (WorldView / Pléiades senza pansharpening) — a questa risoluzione i **foundation model** pretrained diventano utilizzabili;
  - esperimenti intermedi: accorpamento/dimezzamento → **~70 cm**.
- **FM in-house in preparazione**: il gruppo sta costruendo un foundation model su tutte le immagini interne → arriveranno **pesi ad hoc** per quelle risoluzioni/bande.
- **PlanetScope 3 m**: improbabile che si testi — per come è annotato il dataset e per il tipo di waste cercato (non mega costruzioni/cantieri) difficilmente esce qualcosa.
- Carta bianca a Ale sul migliorare i modelli, dentro un set di esperimenti base definiti dal team ("ti diremo gli esperimenti base […] e poi la tua vena artistica da AI engineer").

### Perché l'asse risoluzione

1. **IRIDE in arrivo**: best resolution **1 m** (tempi ignoti; ora in orbita c'è il 4 m). Se già a 1.2 m WorldView/Pléiades i risultati fanno schifo, "salutiamo IRIDE".
2. **Costi lato ARPA/agenzie**: trend verso dati meno risoluti — un 30 cm WorldView costa molto più di uno SkySat a 50 cm.

## Baseline: binary di Fede (Gibellini)

- Da segnare **"inciso su pietra"**: modelli usati, preprocessing, risultati → congelare in un doc/PDF che non si tocca più.
- È il riferimento **che il prof ha in testa**: obiettivo avvicinarsi a quei numeri.
- Caveat (confronto solo indicativo): immagini scalate a **20 cm**, modelli diversi, risoluzioni diverse. Non è detto che ci si arrivi.
- Esperimenti preliminari del team sul satellite-only: "qualcosa di interessante", ma su ~1.200 immagini.
- Da quali modelli si partirà esattamente → si decide con Enrico.

## Dataset

- Satellite-only: **~1.200 immagini**, → **~2.000** aggiungendo le WorldView. Contro le **~10.000 di AerialWaste**: siamo al ~10–20%.
- **Nuove annotazioni satellite-only in programma**; Ale verrà coinvolto → contributo al dataset spendibile in tesi.
- Policy annotazione (lezione appresa dal gruppo): non "annotare a man bassa" — annota → esperimenti → se migliora continua, se no si cambia qualcosa. Previsti esperimenti sull'impatto di aggiungere/togliere immagini.

## TODO Ale (weekend / breve termine)

1. **Guida Docker**: rileggerla e fare i passaggi (Thomas la rimanda se persa). Manca il **docker name** del container già creato → lo passa Thomas. *(Arrivato 17/7 pomeriggio: eagle / porta 2212 / `multispectralwaste` — vedi `../00_context/server_eagle_howto.md`.)*
2. **Binary di Fede**: studiare modelli, preprocessing, risultati → produrre il doc-baseline congelato (punto sopra).
3. **GitLab** (non GitHub): passare l'account a Enrico → aggiunta al branch, accesso ai codici.
4. **Scrivere a Enrico su Teams** (contatto girato da Thomas in call) per organizzare la call di settimana prossima.
5. Codice pubblico di Fede su GitHub: guardarlo **con parsimonia** — non è detto sia quello in produzione, sono girate troppe varianti. Utile per capire i passaggi di testimone, ma "sii pronto a dimenticartelo". Il codice vero lo indica Enrico.
6. Se avanza tempo: **indice di tesi** (il prof lo chiede sempre: scomporre pezzo per pezzo cosa dici e a cosa rispondi) + abbozzo di introduction.

## Formato tesi

- Storico: il prof voleva la **classica 80–90 pagine**. Gli ultimi due laureati hanno fatto la short in formato articolo → standard de facto recente. *(In call si era detto "~10 pagine"; **errata corrige di Thomas via messaggio: il formato article/journal è ≈30 pagine**, più Executive Summary ~6 pp — vedi STATO.md.)*
- **Contro-relatore**: possibile anche con la short (l'ultimo ce l'aveva: è arrivata una domanda scritta). Lo sceglie il prof/la commissione — Ale non deve attivarsi.
- **Decisione Ale (ok Thomas)**: scrivere **lunga con calma**, poi eventualmente condensare nella short — utile anche in ottica **pubblicazione**. Razionale Thomas: tagliare si è sempre in tempo, aggiungere sotto deadline è rischioso.
- **SOTA**: non investire ora su una SOTA materiali (rischio incoerenza: "hai fatto una SOTA sui materiali ma poi mi spieghi solo il binary"). Una base SOTA su **detection** va bene comunque — servirà anche per gli eventuali materiali dopo. Rifinitura dopo che gli esperimenti chiariscono il focus.
- Riferimenti formato (mandati da Thomas post-call): tesi di **Alari** (lunga, struttura da ricalcare); **Merlo** *Inter-annotator agreement* (politesi 10589/252150); **Mazzola** *Asbestos* (politesi 10589/230433, formato journal + executive summary). La short "Asha" (change detection) mai arrivata.
- Ale si informa su **modalità e cadenze di deposito tesi** PoliMi; guarda anche Thomas.

## Logistica

- **Call con Enrico**: mar/mer settimana del 20/7; sentirsi **lunedì 20/7** per fissare.
- **Agosto**: Thomas & co. via le prime due settimane (assenza "relativa": risposte con lag, mezz'ora di call si trova sempre). Ale conta di spingere forte da fine luglio — agosto più leggero sul lavoro.
- Contratto Ale: tempo determinato 6 mesi ("visiting"), scadenza **fine settembre**; ferie nelle due settimane centrali di agosto.

## Quote

> "Quella lì è un attimo la nostra baseline di riferimento. Dobbiamo avvicinarci a quei risultati."

> "Se l'un metro e venti di WorldView piuttosto che Pléiades fa schifo, salutiamo IRIDE."

> "Guardalo [il codice di Fede], ma sii pronto a dimenticartelo."

> "Ti diremo più o meno gli esperimenti base da fare per portare a casa dei risultati, e poi la tua vena artistica da AI engineering."

> "Tu raccogli i documenti e inizi a scriverla come se fosse lunga. Tanto ad accorciare si fa sempre in tempo."

## Punti aperti

1. ~~Docker name~~ → ✓ arrivato (eagle / 2212 / multispectralwaste).
2. **Modelli di partenza** (quelli di Fede o altro) → si decide con Enrico.
3. ~~Tesi di riferimento~~ → ✓ arrivate (Alari, Merlo, Mazzola). Resta l'eventuale short change detection ("Asha").
4. **Modalità/cadenza deposito tesi** → verifica Ale (+ Thomas). Formato chiarito (article ≈30 pp), restano le **date** di deposito per dicembre.
5. Nuova campagna di **annotazione**: quando e come → TBD, Ale coinvolto.
6. **Pesi FM in-house**: tempi di arrivo → TBD.
