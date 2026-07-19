---
description: Trasforma una trascrizione STT di call in doc secondo le convenzioni della repo
argument-hint: [path del file trascrizione, o testo incollato]
---

Trascrizione della call da processare: $ARGUMENTS

Produci il doc della call seguendo le convenzioni di `docs/01_calls/`:

1. **File**: `docs/01_calls/YYYY-MM-DD_<slug>.md` — data della call (dal filename della trascrizione o dal contesto), slug tematico corto (es. `pivot_binary_detection`, `punteggio_strategia`).
2. **Header**: partecipanti e assenti, durata approssimativa, fonte (trascrizione STT), e — se ci sono nomi propri non verificabili — flag `[STT, da confermare]`. Verifica i nomi contro `STATO.md` e la repo prima di flaggarli.
3. **Struttura tipo** (adatta al contenuto, non riempire sezioni vuote): Verdetto generale → tabella "Prima | Dopo" se c'è un cambio di rotta → sezioni tematiche → TODO (di Ale e degli altri) → Quote testuali rilevanti → Punti aperti numerati.
4. **Stile**: italiano, termini tecnici in inglese, scannable, fedele a ciò che è stato detto — le interpretazioni incerte vanno marcate come tali, non spacciate per contenuto della call.
5. **Dopo il doc, aggiorna nella stessa sessione**:
   - `STATO.md`: fatti nuovi/corretti, TODO, log decisioni (la call più recente vince su tutto);
   - se la call contraddice il piano in `docs/04_planning/`, segnala esplicitamente il conflitto ad Ale e proponi l'aggiornamento del piano (non applicarlo in silenzio);
   - se la call tocca esperimenti pianificati, aggiorna la coda in `EXPERIMENTS_LOG.md`.
6. La trascrizione grezza non si committa: il valore sta nel doc rivisto.
