# Call Thomas — 2026-07-17, follow-up (punteggio tesi e strategia)

Seconda call della giornata (h13:14, ~3 min): Thomas richiama dopo essersi informato sulla domanda emersa la mattina ("la tesi vale fino a 8 punti?"). Call principale: `2026-07-17_pivot_binary_detection.md`. Fonte: trascrizione STT.

---

## Il punto

- Tesi in modalità journal: **può arrivare a 8 punti**, ma il punteggio dipende dal **contenuto**, non da lunghezza/formato.
- Per come è impostata adesso — esperimenti su task nuova, ma di fatto ricostruzione/riproduzione dello stato dell'arte — è **più da 5**. La commissione è rigida e severa su cosa conta come ricerca.
- I **~2 punti extra** si sbloccano solo con **innovazione** vera. E innovare oggi è difficile e dipende anche dal task, non solo dall'effort: "trovi dieci cinesi che l'hanno già fatto meglio di te, o dichiarano di averlo fatto".

## Strategia concordata (due fasi)

1. **Base per dicembre** — priorità assoluta: impacchettare questa tesi così com'è impostata e portarla a casa nei tempi.
2. **Upgrade opzionale** — se piano ed esperimenti arrivano a buon punto **già a settembre**, valutare cosa aggiungere per sbloccare i punti extra. Conta più **efficienza/effort** che tempo assoluto (e il contratto di Ale scade proprio a fine settembre).

- **Posizione Ale**: ci punta. Media **28.7** → base d'ingresso **~105**. Disposto ad aumentare il carico ("chiusone" in arrivo).
- Thomas trasparente sul rischio, meglio dirlo ora che scoprirlo sotto data. La sua esperienza da studente-lavoratore: tesi applicativa (tool QGIS, algoritmo del CNR implementato, "ricerca zero"), niente punti da innovazione — entrato con ~104, uscito con 107.

## Candidato per l'innovazione (con le pinze)

- **Weakly-supervised localization**: niente annotazioni dense — solo label image-level (waste presente/assente) → il modello produce una **maschera/localizzazione**. "Magari si riesce a passare come innovazione."
- Sequenza: prima **baseline ed esperimenti base**, poi si valuta insieme (Thomas/Enrico) se e come inserirlo.
- A favore: la task è nuova (binary su satellite-only) → la SOTA va comunque ricostruita da capo, e posizionarsi potrebbe essere più facile che sul filone materiali.

## Prossimi passi

- Ale parte già dal weekend con i TODO della call del mattino (Docker, baseline Gibellini, indice) e aggiorna Thomas man mano; Thomas risponde quando può.
- Checkpoint punti extra: **~settembre**, a valle degli esperimenti base.

## Quote

> "Non è il discorso lunghezza, è il contenuto. Per come la stiamo impostando adesso è più da 5."

> "Innovare, ad oggi: trovi dieci cinesi che l'hanno già fatto meglio di te, o dichiarano di averlo fatto meglio di te. E ne so qualcosa."

> "Cerchiamo di impacchettare questa qua, in modo tale che te la porti a casa. Poi sbloccare i due punti può essere qualcosa in più — però metterei quella base."

> "Te lo voglio dire subito, perché almeno non è tempo perso e non arriva sotto data."
