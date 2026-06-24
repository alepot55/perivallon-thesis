# Call Thomas — 2026-05-22 (slide rework)

Note di lavoro strutturate. Tag: **[STRUTTURA]** ordine/sequenza, **[CONTENUTO]** cosa va dentro la slide, **[FORMA]** stile/layout, **[STRATEGICO]** cambio di impostazione, **[AZIONE]** cosa fare adesso.

Raw transcript: cancellato (rumore STT alto, tutto il valore estratto qui e in `~/.claude/projects/-home-alepot55-Desktop-uni-Tesi/memory/`).

---

## Verdetto generale

Le slide attuali non funzionano. Il problema non è estetico, è **strutturale + contenuto**:
- troppo dense / poco discorsive
- introducono concetti tecnici troppo presto
- immagini scelte male (dimostrano poco)
- mancano riferimenti chiari ai limiti del SOTA

**[FORMA] Regola d'oro Thomas:** *"meglio 50 slide pulite, fluide, una idea per slide, che 10 incasinate"*. Non aver paura di splittare.

---

## Per slide (numerazione attuale)

### Slide 2 — intro problema
- **[CONTENUTO]** I 3 punti evidenziati esplicitamente vanno resi **impliciti**. Toglierli a parole, lasciare che la struttura li suggerisca.
- **[STRATEGICO]** Non introdurre qui i gap tecnici (classificazione materiali, generalizzazione). Quelli vanno dopo, nella sezione gap-analysis.

### Slide 3 — riferimento iniziale
- **[CONTENUTO]** Togliere il riferimento esplicito a Gibellini. Lasciare come **partenza generica** dell'ambito, non come citation slide.
- **[CONTENUTO]** **Research question da riformulare:** *"Qual è il valore aggiunto della classificazione di materiali"*. Aperta, non pre-risposta. (Thomas: *"può essere tranquillamente 'contesto della ricerca' tanto dopo dici già i problemi"*).

### Slide 4 — stack di bande (cos'è un dato satellitare)
- **[CONTENUTO]** Resta come è: spiega cos'è un dato satellitare multispettrale (stack di bande, ogni pixel = vettore di riflettanze).

### Slide 4.1 — NUOVA (era la "slide 5")
- **[STRUTTURA]** Sposta qui la slide attuale con RGB / false-color IR / NDVI.
- **[CONTENUTO]** Messaggio: *"dal dato satellitare posso costruire visualizzazioni diverse della stessa scena per mettere in risalto cose diverse"*. RGB → false-color IR (vegetazione in rosso) → NDVI (indice).
- **[FORMA]** Usare scene **pulite** (solo vegetazione, solo suolo). NIENTE scene miste/brutte.

### Slide 5 (vera) — Survey lavori, low/medium resolution
- **[STRUTTURA]** Diventa **2 slide separate** invece di una sola:
  1. **Low/medium resolution (10–30 m)** — Sentinel-2 + Aharoni-Mack 2025 (asbestos VNIR+SWIR @30m, dataset hyperspectral).
  2. **Very high resolution** — WorldView-3 e simili (slide successiva, stesso template).
- **[CONTENUTO]** **Formato riga tabella**: `Titolo lavoro | Input (es. Sentinel-2 RGB) | Metodo (es. encoder-decoder) | Risultato (es. 90% F1)`.
- **[FORMA]** **Titolo autoesplicativo** (es. "Marine Debris") → niente colonna/riga "Task" separata.
- **[CONTENUTO]** **Immagini scelte male.** Per ogni lavoro citato, mettere screenshot che mostrano *cosa il SOTA becca e cosa manca a 10 m*. Esempio buono: due foto affiancate, una dove il modello prende la spazzatura, una dove la perde. Esempio cattivo: figure architetturali astratte, mappe perfette.
- **[CONTENUTO]** Includere il paper Sentinel-2 + SuperDove (marine debris + landfill, Asia) trovato con lo script: combinazione di sensori a bassa risoluzione, candidato per la slide low-res.

### Slide 11 — Sensor comparison (LiDAR / radar / triangle)
- **[STRUTTURA]** Riformulare come **grafico radar/triangolo** con 3 assi minimo: **risoluzione spaziale, revisit time, # bande spettrali**. Se non ci incasiniamo, 4+ assi (es. + costo).
- **[STRUTTURA]** Decidere se va **prima** dei sensori individuali (roadmap di lettura) o **dopo** (recap). Una delle due, consistente con il resto del flow. Default suggerito: **prima**, come mappa di orientamento per il lettore.

---

## Trasversale

### Direzione tematica
- **[STRATEGICO]** **Amianto è la porta di ingresso**, non sotto-tesi separata. Thomas: *"trattare un altro materiale chi se ne frega, diventa automatico"*. Le slide possono partire dall'asbestos senza sembrare off-topic — anzi è la base coerente.
- **[CONTENUTO]** Aharoni-Mack 2025 finisce nella slide low-res come anchor del filone asbestos.

### Spectral signatures (slide pedagogica)
- **[CONTENUTO]** Usare **riflettanze vere** da libreria (matplotlib + USGS splib07a o `spy`).
- **[FORMA]** Una scena = un materiale. Plot con singole firme spettrali per vegetazione, suolo, asfalto. Niente plot misti incomprensibili.

### Stile generale (vedi anche `feedback_slide_style.md`)
- **[FORMA]** B/N minimal per Thomas. Inglese. Bullet `bullet:true`, mai dashes.
- **[CONTENUTO]** Ogni slide che cita un lavoro → riferimento bibliografico (titolo + anno) almeno.

---

## Pilot amianto — feedback tecnico

- **[AZIONE]** Migrare working format `.gpkg → GeoJSON`. ML pipeline downstream è geojson/json-native. Geopandas legge entrambi identici.
- **[AZIONE]** Investigare metodi matematici di similarità tra firme spettrali. SAM è il default (spectral angle mapper).
- Thomas: *"usa Claude per il codice senza farti problemi — è la direzione, chi non lo fa si taglia fuori"*.

---

## Logistica

- **[AZIONE]** Visita ufficio PoliMi proposta da Thomas (vedere dati dal vivo). Edificio aperto ~07:30–19:30. Alessandro libero pre-08:00 / post-18:00. Da pianificare nelle prossime settimane.
- **Prossima sync**: martedì **2026-05-26 mattina** (fallback lunedì sera). Messaggino su Teams quando le slide sono pronte.

---

## Timeline

- **Target fittizio: ottobre 2026** (per avere buffer).
- **Realistico: dicembre 2026** (Alessandro: *"mi sto abituando all'idea di laurea a dicembre"*, accettato).
- Settembre 2026 **non è più il target attivo**.
