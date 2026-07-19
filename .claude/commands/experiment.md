---
description: Registra un esperimento nel log e aggiorna il claims ledger
argument-hint: [descrizione: cosa hai lanciato/ottenuto, path risultati]
---

Esperimento da registrare: $ARGUMENTS

1. Apri `docs/04_planning/EXPERIMENTS_LOG.md` e appendi una entry **in cima alla sezione Log** usando il template in testa al file: ID progressivo `EXP-NNN` (guarda l'ultimo usato), data, domanda, setup completo (modello/pesi/dati/split/seed/risoluzione/config o comando), path dei risultati (eagle `/data/...` o notebook), metriche, conclusione in una riga con tag HIGH/MEDIUM/UNCERTAIN, claims toccati, next.
2. **Niente numeri inventati**: se manca un valore, chiedi ad Ale o metti `TODO`. Ogni metrica deve puntare a una fonte riproducibile.
3. Aggiorna `docs/04_planning/CLAIMS.md`: se l'esperimento supporta/indebolisce un claim, cambia lo status (OPEN → SUPPORTED/REFUTED/WEAKENED) e collega l'EXP-ID nella colonna Evidenza. I claim REFUTED non si cancellano.
4. Se l'esito cambia lo stato del progetto (baseline raggiunta, gate superato/fallito, decisione implicata), aggiorna anche `STATO.md` e — se tocca il piano — segnala il delta ad Ale.
5. Se l'esperimento chiude una voce della coda pianificata, spuntala/aggiornala nella tabella "Coda esperimenti".
