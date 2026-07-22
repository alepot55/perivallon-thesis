# Scaletta call con Enrico (proposta: giovedì 24/7)

Preparata 2026-07-22. Obiettivo della call: uscirne con (1) conferma che stiamo usando i dati giusti, (2) le risposte che decidono l'angolo di innovazione, (3) accesso GitLab e regole del gruppo. Durata stimata 30-45 min.

## Apertura (2 min) — cosa è già fatto

Da dire in breve, senza dilungarsi:

- Accesso al server operativo da entrambi i PC, ambiente configurato, GPU testate.
- Fatta una ricognizione di `/data` e `/archive`: trovati gli split 0.3m/1.2m in `SatRaw/PNEO/Thomas/`, le bbox in `aw36_od_bin_sat_only.json`, i mosaici processed.
- Girati i primi training di prova sugli split (sanity ResNet + baseline Swin-T+RSP con protocollo Gibellini): la pipeline dati funziona, numeri preliminari in mano.

## Domande, in ordine di priorità

### Blocco A — dati (le risposte decidono tutto)

1. **Le 2827 bbox sulle 286 positive satellite-only**: chi le ha fatte, sono complete e affidabili? Si possono usare come test-set di localizzazione? ← LA domanda: decide l'angolo dei +2 punti.
2. **Gli split `Thomas/0.3m` e `1.2m`**: sono la configurazione ufficiale? Esistono già run del gruppo con numeri su questi split (per confronto)?
3. **~6% delle tile** (57 train + 15 val) cade fuori dai 5 mosaici in `processed/PNEO_LOMBARDIA_2023_ALL_30cm_16bit_THOMAS`: esistono altre strip processed, o quelle tile vanno scartate?
4. **Bande e preprocessing**: ordine esatto delle 6 bande PNEO nei mosaici? Gli esperimenti del gruppo usano RGB o tutte le bande? Come è fatto il pansharpening a 0.3m?
5. **Negative sampling**: come sono state scelte le negative del train?

### Blocco B — esperimenti e codice

6. Il livello **~0.7m** manca: lo generiamo degradando da 0.3m? Con che resampling?
7. **Pesi SSL** `SSL_pretrained_models/exported_last_{100,500}_ep.pt` (ResNet-50 RGB): che training è, e che rapporto ha col "FM in-house" annunciato? Ha senso usarli come pretraining nel confronto?
8. **Repo GitLab**: assegnazione, dove committare, e dove salvare risultati/checkpoint su `/data` (cartella progetto).
9. Le **~800 WorldView** attese: sono le 481 già presenti in `sat_only` più altre, o nuove? Tempi?

### Blocco C — allineamento (se resta tempo)

10. Cosa considerate già "fatto" nel gruppo su CAM/weakly-supervised localization (pipeline Gibellini, Mazzola)? Dove finisce il fatto e inizia il nuovo?
11. Cosa sarebbe utile per il gruppo come contributo di tesi? (allineamento per il pitch di settembre)

## Decisioni da portare a casa

- [ ] Bbox utilizzabili come test-set localizzazione: sì / no / in parte
- [ ] Split ufficiali confermati: sì / no (se no: quali)
- [ ] Come generare il livello 0.7m
- [ ] Dove mettere codice (GitLab) e risultati (/data/...)
- [ ] Prossimo checkpoint con Enrico/Thomas

## Materiale di supporto (se serve mostrare)

- Numeri preliminari: `docs/04_planning/EXPERIMENTS_LOG.md` (EXP-001, EXP-002)
- Ricognizione dati: `docs/02_research/2026-07-21_eda_dati_eagle.md`
- Verdetto novelty: `docs/02_research/wsol_mini_sota.md` (delta vs Mazzola)

Promemoria di registro: non dire "OOD" (dire "generalizzazione"); i numeri preliminari presentarli come sanity check, non come risultati.
