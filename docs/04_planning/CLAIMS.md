# CLAIMS — ledger dei claim di tesi

> Ogni claim che la tesi vorrà difendere, con lo stato dell'evidenza. Regole: un claim è **SUPPORTED** solo se punta a ≥1 `EXP-NNN` riproducibile; **novelty claims sempre hedged** ("to our knowledge"); se un esperimento lo contraddice → status **REFUTED**, non si cancella (la storia serve). Il pitch di settembre a Thomas e i capitoli risultati si scrivono da questa tabella.

| ID | Claim | Status | Evidenza | Dove in tesi |
|---|---|---|---|---|
| C-1 | Un classificatore binario allo stato dell'arte (stile Gibellini) è riproducibile sul dataset satellite-only, con gap quantificato vs i numeri aerei (F1 92.02 @20 cm) | **SUPPORTED** | EXP-002/003 (pipeline nostra, test F1 0.68-0.69 @1.2m) + EXP-012/014 (pipeline gruppo, SwinT-RSP RGB 0.694±0.019 @120cm, 3 seed); gap vs 92.02 aereo quantificato | Cap. esperimenti/base |
| C-2 | La performance di binary detection degrada con il GSD in modo misurabile (curva 30→70→120 cm) | OPEN | — (→ EXP #3) | Cap. risultati, fig. chiave |
| C-3 | A 1.2 m (risoluzione IRIDE-like) la detection resta/non resta operativamente utilizzabile — soglia esplicita da definire con ARPA/Thomas | OPEN | — (→ EXP #3) | Discussione/impatto |
| C-4 | L'informazione spettrale extra compensa parte della perdita di risoluzione spaziale (interazione bande×GSD) | OPEN — **evidenza negativa a 120 cm** | EXP-004 (nostra pipeline 16-bit: +1.9 pp @0.3m, piatto @1.2m) + EXP-014 (pipeline gruppo 8-bit @120cm: RGB 0.694 vs 6-bande 0.665, RGB sopra 3/3 seed) → a 120 cm lo spettro NON compensa; test decisivo = 30 cm nella pipeline gruppo | Cap. risultati |
| C-5 | La localizzazione weakly-supervised da label image-level è valutabile quantitativamente sul dominio satellite waste (test-set poligoni costruito) | OPEN — **gated**: serve test-set | — (→ EXP #6) | Cap. metodo |
| C-6 | Un metodo oltre vanilla Grad-CAM (pseudo-mask/refinement e/o consistency cross-GSD) migliora la localizzazione in modo misurabile | OPEN | — (→ EXP #7-8) | Contributo principale (+2 punti) |
| C-7 | *To our knowledge*, nessun lavoro valuta quantitativamente WSOL per waste detection satellitare sotto degradazione di GSD | OPEN — da verificare con mini-SOTA (attenti a: Mazzola 2024 in-group, WSSS remote sensing) | mini-SOTA WSOL | Related work / novelty statement |
| C-8 | Aggiungere le immagini WorldView (~1.2k→2k) migliora la baseline in modo misurabile (curva dataset-size) | OPEN | — (→ EXP #4) | Cap. dataset / contributo annotazione |

## Storico modifiche

- 2026-07-24 (sera): C-1 → SUPPORTED (EXP-002/003/012/014, due pipeline); C-4 → prima evidenza (negativa a 120 cm, EXP-004+EXP-014), resta OPEN in attesa del 30 cm.

- 2026-07-19: creato con C-1…C-8 seminati dal piano 7 punti (tutti OPEN, pre-call Enrico).
