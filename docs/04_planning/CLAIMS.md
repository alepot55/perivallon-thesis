# CLAIMS — ledger dei claim di tesi

> Ogni claim che la tesi vorrà difendere, con lo stato dell'evidenza. Regole: un claim è **SUPPORTED** solo se punta a ≥1 `EXP-NNN` riproducibile; **novelty claims sempre hedged** ("to our knowledge"); se un esperimento lo contraddice → status **REFUTED**, non si cancella (la storia serve). Il pitch di settembre a Thomas e i capitoli risultati si scrivono da questa tabella.

| ID | Claim | Status | Evidenza | Dove in tesi |
|---|---|---|---|---|
| C-1 | Un classificatore binario allo stato dell'arte (stile Gibellini) è riproducibile sul dataset satellite-only, con gap quantificato vs i numeri aerei (F1 92.02 @20 cm) | **SUPPORTED** | EXP-002/003 (pipeline nostra, test F1 0.68-0.69 @1.2m) + EXP-012/014 (pipeline gruppo, SwinT-RSP RGB 0.694±0.019 @120cm, 3 seed); gap vs 92.02 aereo quantificato | Cap. esperimenti/base |
| C-2 | La performance di binary detection degrada con il GSD in modo misurabile (curva 30→70→120 cm) | OPEN | — (→ EXP #3) | Cap. risultati, fig. chiave |
| C-3 | A 1.2 m (risoluzione IRIDE-like) la detection resta/non resta operativamente utilizzabile — soglia esplicita da definire con ARPA/Thomas | OPEN | — (→ EXP #3) | Discussione/impatto |
| C-4 | Il beneficio dell'informazione spettrale extra **dipende dal GSD** (interazione bande×GSD), non compensa la risoluzione persa | **SUPPORTED come interazione** (non come guadagno assoluto) | 3 seed per livello, pipeline gruppo: delta (6bande−RGB) = **−2.9 pp @120cm** (EXP-014) vs **+2.2 pp @30cm** (EXP-017) → swing ~5 pp; AUROC +1.5 e varianza dimezzata a favore del MS a 30 cm; a best-threshold i due sono pari (caveat calibrazione, da dichiarare). Coerente con EXP-004 nella nostra pipeline 16-bit (+1.9 @0.3m, piatto @1.2m) | Cap. risultati, fig. chiave |
| C-5 | La localizzazione weakly-supervised da label image-level è valutabile quantitativamente sul dominio satellite waste | **SUPPORTED** | Protocollo WSOL (PG, MaxBoxAcc@0.5, best IoU vs bbox `aw36_od_bin_sat_only`, 50 positivi test) operativo in ENTRAMBE le pipeline: EXP-005→010 (nostra) + EXP-016 (`eval_wsol.py` nel flusso gruppo) | Cap. metodo |
| C-6 | Un metodo oltre vanilla Grad-CAM (distillazione cross-GSD delle CAM) migliora la localizzazione a bassa risoluzione in modo misurabile | OPEN — **prima evidenza a favore** | EXP-018 (λ=1, seed 0, pipeline gruppo @120cm): mean best IoU 0.075→0.155 e MaxBoxAcc 0.02→0.08 con detection invariata (−1 pp); pointing game piatto (conteggi su 50 img). Insufficiente: serve sweep λ con selezione su val + multi-seed + ablation simmetrica (tutti in coda) | Contributo principale (+2 punti) |
| C-7 | *To our knowledge*, nessun lavoro (a) valuta quantitativamente WSOL per waste detection satellitare sotto degradazione di GSD, né (b) usa le CAM di un classificatore ad alto GSD come teacher spaziale per uno studente a basso GSD | **VERIFICATO 24/7** — regge, ma con delta stretto | `docs/02_research/2026-07-24_novelty_distillazione.md`: nessun match diretto; prior art più vicino **SSENet 2019** (consistenza CAM cross-scala simmetrica, augmentation non GSD reale) da citare esplicitamente; rischio aperto SPScaleNet 2024 (stesso dominio, articolo in cinese da recuperare). Frase hedged pronta nel doc | Related work / novelty statement |
| C-8 | Aggiungere le immagini WorldView (~1.2k→2k) migliora la baseline in modo misurabile (curva dataset-size) | OPEN | — (→ EXP #4) | Cap. dataset / contributo annotazione |

## Storico modifiche

- 2026-07-24 (notte, 3): C-6 prima evidenza a favore (EXP-018, distillazione cross-GSD: IoU raddoppiato con detection intatta) — ancora OPEN in attesa di sweep, seed e ablation.

- 2026-07-24 (notte, 2): C-4 riformulato dopo multi-seed 30 cm (EXP-017) — il claim difendibile è l'INTERAZIONE bande×GSD (swing ~5 pp), non il guadagno assoluto del MS; caveat calibrazione da dichiarare sempre.

- 2026-07-24 (notte): C-7 verificato con ricerca dedicata — novelty regge ma stretta; il contributo primario si sposta sulla MISURA (disaccoppiamento classificazione/localizzazione lungo il GSD), il metodo diventa applicativo. Ablation SSENet-style implementata come mitigazione.

- 2026-07-24 (notte): C-4 riformulato e supportato (interazione bande×GSD completa: EXP-004/014/015); C-5 → SUPPORTED (eval WSOL portata nella pipeline gruppo, EXP-016: PG 0.04→0.40 tra 120 e 30 cm).

- 2026-07-24 (sera): C-1 → SUPPORTED (EXP-002/003/012/014, due pipeline); C-4 → prima evidenza (negativa a 120 cm, EXP-004+EXP-014), resta OPEN in attesa del 30 cm.

- 2026-07-19: creato con C-1…C-8 seminati dal piano 7 punti (tutti OPEN, pre-call Enrico).
