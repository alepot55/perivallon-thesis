# Dossier per giovedì 23/7 — tutto quello che serve, in un doc solo

> Da studiare domattina (~35 min). Ordine: leggi i diagrammi, poi le tabelle, poi il Q&A.
> La scaletta operativa della call è in `call_enrico_brief.md` (stampala o tienila aperta).

## 1. La giornata

```mermaid
flowchart LR
    A["Mattina<br>studio dossier (~35 min)"] --> B["Tarda mattinata<br>punto veloce con Thomas<br>(5 min, racconto avanzamento)"]
    B --> C["Pomeriggio<br>CALL con Enrico<br>(scaletta: call_enrico_brief.md)"]
    C --> D["Sera<br>trascrizione a Claude (/call)<br>aggiornamento piano"]
```

## 2. La tesi in 60 secondi (l'elevator pitch)

Individuare discariche abusive da immagini satellitari ad altissima risoluzione, con due domande:
1. **Quanto regge la detection quando la risoluzione scende** da 0.3 m a 1.2 m? (rilevante per ARPA e per la costellazione IRIDE, che lavora attorno al metro)
2. **Si può localizzare il rifiuto dentro la tile usando solo label sì/no**, e misurare quanto la localizzazione degrada con la risoluzione? (questo è il contributo da +2 punti: to our knowledge, nessuno l'ha misurato)

Base = replica del protocollo Gibellini sul dataset satellite-only del gruppo. Innovazione = valutazione quantitativa della localizzazione weakly-supervised lungo l'asse risoluzione, con metodo oltre la vanilla Grad-CAM.

## 3. I numeri da sapere a memoria

| Cosa | Numero | Fonte |
|---|---|---|
| Gibellini best (aereo, 20 cm) | **F1 92.02** | Tab. 2 del paper |
| Gibellini cross-country | F1 86.92 medio | Tab. 3 |
| Dataset satellite-only | **1.775 img** (1.294 PNEO + 481 WV3) | aw36 sat_only |
| Positive con bbox | **286 img, 2.827 bbox, 15 categorie** | idem |
| Split Thomas (per risoluzione) | train 1.020 / val 135 / test 139 | SatRaw/PNEO/Thomas |
| Nostra baseline RGB (3 seed, EXP-003) | val **0.780±0.015** @0.3m / 0.732±0.008 @1.2m; **test 0.692±0.011 / 0.680±0.010** | EXPERIMENTS_LOG |
| 6 bande (EXP-004) | *v. sezione 7 (girate stanotte)* | idem |
| Timeline | sprint 10–23/8 → checkpoint +2 ~metà set → deposito 23/10–12/11 → **laurea 16/12** | STATO |

Attenzione al confronto trappola: il nostro 0.68-0.69 di test **non è paragonabile** al 92 di Gibellini — dataset ~10 volte più piccolo, satellite vs aereo, test su comuni mai visti, protocollo leggero. Se qualcuno lo accosta, dillo subito tu.

## 4. Cosa dire a Thomas (tarda mattinata, 5 minuti)

1. Server a posto da entrambi i PC, ambiente e GPU testati.
2. Ricognizione dati fatta: trovati gli split 0.3/1.2, le bbox, il suo README con bande e normalizzazione (usati).
3. Primi training girati (protocollo Gibellini, slot prenotati sul foglio): pipeline funziona, numeri preliminari con più seed.
4. Per la call col gruppo ho le domande pronte, soprattutto su bbox e consolidamento strip.
5. (Se lo chiede) prossimi passi: livello 0.7m, protocollo localizzazione, GitLab da Enrico.

## 5. La call con Enrico — le 5 domande che contano davvero e perché

La scaletta completa è in `call_enrico_brief.md`. Le 5 vitali, con cosa cambia in base alla risposta:

| # | Domanda | Se SÌ | Se NO |
|---|---|---|---|
| 1 | Le 2.827 bbox sono affidabili/complete? Usabili come test-set di localizzazione? | Angolo C confermato: si parte col protocollo WSOL | Piano B: annotare ~100 tile in proprio, o fallback su eval di vanilla CAM |
| 2 | Gli split Thomas 0.3/1.2 sono ufficiali? Avete già numeri su di essi? | I nostri numeri sono confrontabili coi loro | Chiedere gli split giusti e rilanciare (poco costo, script pronti) |
| 3 | Le strip in /scratch si possono consolidare in /data? | Copertura test al sicuro | Rischio: /scratch cancellabile → test set azzoppato |
| 4 | Input size / context: come gestite tile grandi a 0.3m? (il nostro 224 fisso comprime il GSD effettivo) | Adottiamo il loro protocollo | Proposta nostra: factorial GSD × input size come Gibellini |
| 5 | Repo GitLab + dove salvare risultati su /data? | Si lavora nel flusso del gruppo | Continuare in ~/experiments (temporaneo) |

Regola d'oro in call: **prima ascoltare come lavorano loro, poi proporre**. I nostri script sono usa-e-getta finché non vediamo il codice del gruppo.

## 6. Se ti chiedono X → rispondi Y

- **"Che task è?"** → Binary classification a livello di tile (waste sì/no), con localizzazione weakly-supervised come asse di studio: da label image-level a mappe/box, valutate con metriche quantitative. Non è object detection supervisionata: le bbox servono solo per VALUTARE.
- **"Perché 1.2 m se hai lo 0.3?"** → Perché la domanda operativa è cosa si perde al degradare della risoluzione: IRIDE e i sensori accessibili stanno intorno al metro; il pansharpened a 0.3 esiste solo per parte delle strip.
- **"Non l'ha già fatto Mazzola?"** → Mazzola fa IoU su asbestos e confronta 0.3-vs-1.2 pansharpened-vs-nativo (2 punti, confusi dal pansharpening). Noi: task waste, protocollo WSOL standard (MaxBoxAcc, pointing game), degradazione controllata multi-punto, metodo oltre vanilla CAM. I 4 delta sono scritti nel mini-SOTA.
- **"E il multispettrale?"** → Le 6 bande PNEO ci sono e le stiamo già usando (weight inflation sul patch embedding); primi numeri RGB vs 6 bande stanotte. È l'angolo B del piano, riciclato dentro la nuova task.
- **"SWIR?"** → Fuori scope: non è nelle acquisizioni disponibili, e il limite di Sentinel-2 è la risoluzione (10 m), non le bande. (Trappola classica: banda vs risoluzione.)
- **"Perché non un foundation model?"** → A 0.3 m non ci sono FM pretrained sensati (10-30 m di pretraining); a 1.2 m tornano discutibili e infatti sono nel piano come bonus, inclusi gli eventuali pesi in-house del gruppo.
- **"Quanto è grande il modello?"** → Swin-T, ~27M parametri, pesi RSP (Million-AID) come Gibellini.

## 7. Numeri finali della notte (aggiornati automaticamente)

*Sezione compilata da Claude entro l'alba: EXP-003 (multi-seed RGB) ed EXP-004 (6 bande, 3 seed). Se leggi questo testo, gli esperimenti non sono ancora stati integrati: guarda `EXPERIMENTS_LOG.md`.*

## 8. Glossario minimo (una riga l'uno)

- **GSD**: dimensione al suolo di un pixel (0.3 m = un pixel copre 30 cm).
- **Pansharpening**: fusione della banda pancromatica ad alta risoluzione con le bande colore a bassa: dà i "0.3 m" multispettrali.
- **WSOL**: localizzare oggetti avendo in training solo label a livello di immagine.
- **CAM / Grad-CAM**: mappa di calore di dove il classificatore "guarda"; base del WSOL.
- **MaxBoxAcc / pointing game**: metriche WSOL: la box derivata dalla CAM coincide col GT? il picco della CAM cade nel GT?
- **TL / FT**: le due fasi del protocollo Gibellini (prima solo testa, poi ultimo stage sbloccato).
- **Weight inflation**: adattare i kernel RGB pretrained a input con più bande, copiandoli e riscalandoli.
- **RSP**: pretraining su Million-AID (immagini aeree), alternativa a ImageNet.

## 9. Registro (ripasso di 20 secondi)

- Mai "OOD" → di' "generalizzazione" / "comuni non visti".
- Mai "rilevare rifiuti" per ARPA → "individuare siti e classificarli per rischio, per intervento efficiente".
- I nostri numeri = "primi run di sanity/baseline", mai "risultati".
- Flusso lineare: non tornare indietro su argomenti già chiusi.
- Per ogni lavoro citato sappi rispondere "che task è" (classification / detection / segmentation).

## 10. Per approfondire (se hai più tempo)

1. `docs/02_research/2026-07-21_eda_dati_eagle.md` — i dati veri sul server (10 min)
2. `docs/02_research/baseline_gibellini_frozen.md` — la baseline congelata (15 min)
3. `docs/02_research/wsol_mini_sota.md` — il verdetto novelty coi 4 delta (10 min)
4. `docs/04_planning/indice_tesi_v0.md` — la struttura della tesi (5 min)
