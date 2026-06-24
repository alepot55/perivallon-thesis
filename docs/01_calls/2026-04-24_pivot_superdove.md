

## Decisioni operative

### Calendario
- **Lunedì o martedì 28-29 aprile** → re-sync operativo con Thomas
- **Venerdì 30 aprile** (o data da confermare) → SOTA ufficiale al lab, da rivedere con Thomas prima di portarla a Fraternali
- **Settimana 5-9 maggio** → presentazione SOTA al prof

### Cambio di rotta strategico

| Prima della call | Dopo la call |
|---|---|
| Sentinel-2 come piattaforma primaria | **SuperDove** come piattaforma primaria |
| 13 bande, SWIR incluso | 8 bande, no SWIR, ma 3 m di GSD |
| Riferimento sperimentale: Gibellini | Riferimento sperimentale: **Mazzola** |
| Estensione MS di AerialWaste v3 | Possibile uso di **AerialWaste v4** (satellite-only) |
| Focus su SWIR per material chemistry | Focus su alta risoluzione + firme spettrali |

---

## Narrativa nuova

> **Lab → Satellite**

L'aggancio tra firme spettrali misurate (in laboratorio o da libreria) e la loro applicazione su imagery satellitare diventa il filo conduttore. Se l'esperimento firme funziona, si passa al deep learning sul satellite.

### Approfondire Uhrin

Il paper **Uhrin et al. 2025** (WV-3 SWIR per macroplastiche terrestri) diventa riferimento centrale, non più solo citazione.

### Il problema GSD

Thomas ha detto: *"tutto a 10 metri banda lo vogliono sfocato, se lo guardi in alta risoluzione perdiamo informazione"*. A 10 m si perde dettaglio rispetto all'ortofoto. Domanda aperta:

> *"Se ha senso SSL per immagini anche a 1 metro"*

Cioè: i pesi pretrained di SSL4EO-S12 sono su Sentinel-2 a 10 m. Funzionano su SuperDove a 3 m? E su ortofoto a 30 cm? Aperto come **next step o limitation esplicita**.

### AerialWaste v4

Thomas ipotizza una versione che:
- Separi imagery satellitare da ortofoto
- Tenga solo satellite, eliminando AGEA aeree e Google Earth
- Annotazione fatta direttamente su immagini satellitari
- Combini più risoluzioni stessa area (SuperDove + altro)

**Da verificare se è già pronta o da costruire.**

---

## Pre-esperimento firme spettrali su amianto

Esperimento pratico **prima** di passare al deep learning. Riferimento: tesi di **Mazzola** (gruppo PoliMi, seguita da Gibellini), che aveva ottenuto ottimi risultati in-distribution ma con problemi di generalizzazione fuori dal dominio di training.

### Strumenti
- **QGIS** (da scaricare e installare)
- Istruzioni PoliMi per **WebMap service** → Thomas le manda
- **Python con librerie geospatial** (rasterio, geopandas) per il resto

### Workflow

1. Caricare imagery **SuperDove** su QGIS
2. Caricare shapefile con poligoni di **tetti in amianto** già annotati
3. Per ciascun poligono: estrarre i valori dei pixel per ciascuna banda
4. Aggregare con statistica: **media, mediana, max, min** — provare quali funzionano meglio
5. Applicare **Spectral Angle Mapper (SAM)**: distanza angolare tra curve spettrali → metrica di similarità
6. Definire una **soglia** sopra cui due firme sono "simili" (da determinare sperimentalmente)
7. **Clustering**: i poligoni amianto cadono tutti nello stesso cluster? Un campo incolto erroneamente etichettato come tetto cade fuori?

### Output da verificare
- **Unsupervised** (clustering puro) è sufficiente?
- O serve **supervised** (classificatore sulle firme)?
- Le firme di materiali diversi sono **sufficientemente separate** per discriminazione?

### Decisione conseguente
> *"Se non riusciamo a discriminare il materiale dalla firma → cambiamo strategia."*

Se l'esperimento fallisce, non ha senso complicare con il DL: si rivede il piano.

### Espansione: multi-class multi-label
Una volta che il workflow funziona su una classe (amianto), sovrapporre nuovi layer di poligoni con altre classi, estrarre firme, confrontare.

---

## SOTA per Fraternali — contenuto

Slide ufficiali da preparare per la presentazione al prof. Diverso dalle slide tecniche viste finora.

### Argomenti
1. **Cosa fanno** — stato dell'arte corrente sulla detection
2. **Cosa manca** — gap tecnico
3. **Perché multispettrale + super-resolution?**
   - È solo questione di costo (commerciale)?
   - O non si riesce proprio (limiti fisici/tecnici)?
4. **Come gestire l'informazione** — strategie disponibili
5. **Cosa fare** — direzione proposta

### Stile richiesto
- **Semplice e chiaro**
- Immaginare di spiegare a una persona che **non sa nulla**
- **Nulla dato per scontato**
- **Grafici con colori** (es. plastica vs dry vegetation)

> **Importante:** è uno stile **diverso** dal minimale B/N usato finora. Questa è SOTA didattica per non specialisti, non slide tecniche per peer.

---

## Stack tecnico aggiornato

- **QGIS** per visualizzazione raster + vettori, estrazione firme
- **Python**: rasterio (TIFF), geopandas (shapefile), shapely
- Annotazioni in formato **TIFF, shapefile, GeoJSON**
- **SuperDove** via Planet E&R (già approvato)
- **VPN PoliMi** ancora da sbloccare (Thomas non l'ha esplicitato, da chiedere)

---

## Citazione di Thomas che riassume tutto

> *"Assicurarsi che ci siano tutti i dataset — senno prof incazza."*

Priorità immediata: censire e consolidare tutti i dataset rilevanti prima della presentazione al prof. Se manca qualcosa, Fraternali non gradisce.

---

## Punti aperti / da chiarire

1. **AerialWaste v4 esiste?** Verificare con Thomas o Torres.
2. **Tesi di Mazzola disponibile?** Da chiedere a Thomas — diventa il nuovo riferimento sperimentale.
3. **VPN PoliMi sbloccata?** Non esplicitato nella call.
4. **SOTA per il prof — venerdì 30 o lunedì 5?** 1 maggio è festa, da chiarire.
5. **Statistica firma e soglia SAM:** da determinare durante l'esperimento.
6. **Pesi modelli a 30 cm:** ha senso riusare SSL4EO-S12 su imagery a risoluzione molto più alta del pretraining?

---

## Implicazioni della rotta nuova

- Il SWIR esce dal piano sperimentale (SuperDove non ha SWIR), ma resta come framework teorico nel related work
- La narrativa "RGB → multispettrale via SWIR" si trasforma in "alta risoluzione + firme spettrali nelle bande VNIR"
- Krauz 2025 (poche bande ben scelte ≈ 768 bande HSI) diventa il paper di copertura principale per giustificare l'assenza di SWIR
- La tesi di Mazzola sostituisce la baseline Gibellini come punto di partenza sperimentale
- Tutto il lavoro su firme spettrali SWIR (sigillib07a, Garaba, plastiche aromatiche/alifatiche) si riposiziona come **knowledge base** per interpretare cosa SuperDove può e non può fare
- Le slide minimali fatte finora restano valide come deck tecnico interno; per il prof serve un deck SOTA didattico nuovo
