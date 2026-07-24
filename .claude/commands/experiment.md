---
description: Registra un esperimento nel log e aggiorna il claims ledger
argument-hint: [descrizione: cosa hai lanciato/ottenuto, path risultati]
---

Esperimento da registrare: $ARGUMENTS

1. **Id descrittivo obbligatorio** nel formato `bGSD_bande_arch_pretrain_aug_sSEED` (es. `b120_vnir_swint_rsp_aug1_s42`) — mai "esperimento 1,2,3". Pretraining: 1=ImageNet, 2=RSP, 3=SSL. Verifica che rispetti "una modifica alla volta" rispetto all'esperimento precedente; se cambia più di una cosa, segnalalo esplicitamente nella entry.
2. Apri `docs/04_planning/EXPERIMENTS_LOG.md` e appendi una entry **in cima alla sezione Log** usando il template in testa al file: id descrittivo (+ eventuale EXP-NNN legacy), data, domanda, setup completo (modello/pesi/dati/split/seed/risoluzione/config o comando), path dei risultati (eagle `/data/...` o notebook), metriche, conclusione in una riga con tag HIGH/MEDIUM/UNCERTAIN, claims toccati, next.
3. **Niente numeri inventati**: se manca un valore, chiedi ad Ale o metti `TODO`. Ogni metrica deve puntare a una fonte riproducibile.
4. Aggiorna `docs/04_planning/CLAIMS.md`: se l'esperimento supporta/indebolisce un claim, cambia lo status (OPEN → SUPPORTED/REFUTED/WEAKENED) e collega l'id nella colonna Evidenza. I claim REFUTED non si cancellano.
5. **Excel di gruppo**: aggiungi/aggiorna la riga corrispondente nell'Excel "Binary Experiments Results" su Drive (metriche + best threshold). Se non puoi farlo ora, mettilo come TODO esplicito in STATO.md.
6. **Guida studio**: aggiorna `docs/00_context/guida_studio.md` — sez. 5 (storia esperimenti) e changelog — così Ale può studiarselo (regola fissa).
7. **Turni GPU**: se il run è concluso, ricorda di togliere la prenotazione dal foglio Turni (prenotare solo il minimo, liberare subito).
8. Se l'esito cambia lo stato del progetto (baseline raggiunta, gate superato/fallito, decisione implicata), aggiorna anche `STATO.md` e — se tocca il piano — segnala il delta ad Ale.
