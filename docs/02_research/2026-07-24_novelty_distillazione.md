# Novelty check — distillazione CAM cross-risoluzione per WSOL

Ricerca del 24/7 sera, dopo aver implementato il metodo. Scopo: sapere cosa esiste già prima di scrivere un claim di novità. Tutte le citazioni sotto sono verificate salvo dove marcato `[DA VERIFICARE]`.

## Il verdetto in tre righe

1. **Non risulta un lavoro che usi le CAM di un classificatore ad alto GSD come teacher spaziale per uno studente a basso GSD in WSOL.**
2. **Ma il delta metodologico è stretto**: gli ingredienti esistono separati (consistenza CAM cross-scala: SSENet/SEAM; teacher HR → student LR su mappe: Shin 2022, Qi 2021; HR→LR su satellite: Revankar 2024). Un revisore severo legge il nostro metodo come "SSENet reso asimmetrico e portato su GSD reali".
3. **Il contributo più solido non è il metodo, è la misura**: la classificazione resta quasi invariata mentre la localizzazione crolla (pointing game 0.40 → 0.06 tra 30 e 120 cm). Non risulta nessuno studio che disaccoppi le due cose lungo l'asse GSD in remote sensing.

## I lavori più vicini

| Lavoro | Venue | Cosa fa | Differenza dal nostro |
|---|---|---|---|
| **SSENet** — Wang et al. 2019 | arXiv:1909.03714 (nessun venue trovato) | Consistenza tra CAM della stessa immagine a scale diverse ("scale equivariant regularization") | **Prior art più vicino.** Rete siamese a pesi condivisi, consistenza **simmetrica** e auto-supervisata; il rescaling è augmentation su input HR; il modello finale gira in HR. Nessun teacher congelato, nessun modello LR deployabile, nessuna degradazione sensoriale reale |
| **SEAM** — Wang et al. 2020 | CVPR 2020 (Oral), 12275-12284 | Consistenza equivariante tra CAM sotto trasformazioni affini + PCM | Cross-augmentation, non cross-GSD; siamese simmetrica; PASCAL VOC |
| Shin et al. 2022 | ECCV 2022 | Attention map teacher HR → student LR (similarità coseno) | Face recognition; attention non class-specific; nessuna metrica di localizzazione; non weakly-supervised |
| **MSAD** — Qi et al. 2021 | CVPR 2021 | Teacher multi-scala HR → student LR, distillazione feature FPN | Detection **fully supervised** (bbox); distillazione su feature, non su CAM |
| CRKD-YOLO — Huang et al. 2025 | IEEE TIM 2025 | KD cross-risoluzione per detection RS a bassa risoluzione | RS ma detection supervisionata con bbox, feature-level. Autori `[DA VERIFICARE]` |
| Revankar et al. 2024 | arXiv:2411.00210 | Distilla modello satellitare HR → LR (MSE) | Distilla **logit**, non mappe spaziali; nessuna valutazione di localizzazione |
| KD-MSI — Lu et al. 2024 | arXiv:2403.05796 | CAM + KD per change detection weakly supervised in RS | Teacher e student alla **stessa** risoluzione; il KD raffina la CAM, non la trasferisce tra GSD |
| Choe et al. 2020 | CVPR 2020, 3133-3142 | Benchmark WSOL, MaxBoxAcc, critica del model selection | Metodologia da adottare (lo stiamo facendo), non concorrente |
| Torres & Fraternali 2023 | Scientific Data 10 | AerialWaste: classificatore binario + CAM per ispezione | CAM come explanation, mai ottimizzate; nessun asse GSD sistematico |
| SPScaleNet 2024 | Acta Geod. Cartogr. Sin. 53(6):1212 | Contrastive multi-livello con vincolo di scale contrast su CAM per **solid waste dump** | **Stesso dominio: rischio reale.** Contrastive multi-scala su un solo modello HR, senza teacher-student cross-GSD. Autori `[DA VERIFICARE]`, articolo in cinese, da recuperare |

## La frase di novelty (da usare così, hedged)

> To our knowledge, no prior work uses class activation maps produced by a high-GSD classifier as a spatial teacher for a low-GSD student in weakly supervised object localization. Existing CAM consistency methods (SSENet, SEAM) enforce symmetric self-supervision across rescaled views of the same high-resolution input, while cross-resolution distillation in remote sensing has so far operated on logits or on fully supervised detection features.

Regole d'uso: mai "first"; citare **SSENet esplicitamente nello stesso paragrafo** come lavoro più vicino (se non lo citiamo noi lo trova la commissione).

## Rischi e mitigazioni

| Rischio | Mitigazione | Stato |
|---|---|---|
| SSENet: se la consistenza simmetrica funziona uguale, il delta si assottiglia | **Ablation esplicita**: `--mode symmetric` (SSENet-style) vs `--mode distill` (teacher HR congelato) | ✅ **RISOLTO 24/7 (EXP-020)**: la simmetrica peggiora (mean IoU 0.046 vs 0.075 baseline), il teacher asimmetrico raddoppia (0.155). L'asimmetria è essenziale, con spiegazione meccanicistica: riscalare un input a 120 cm non crea dettaglio. Il delta rispetto a SSENet ora è **dimostrato**, non solo argomentato |
| SPScaleNet 2024: stesso dominio (waste dump) | Recuperare e leggere l'articolo prima di scrivere il claim | ⬜ aperto |
| Revankar 2024: se una versione aggiornata aggiunge mappe spaziali | Ricontrollare a ridosso della scrittura | ⬜ aperto |
| Pointing game senza il protocollo di Choe (model selection su held-out) | Selezionare il checkpoint su val, mai su test; dichiararlo | ⬜ da formalizzare |

## Conseguenza sul posizionamento della tesi

Il capitolo dei contributi si riordina così:
1. **Misura** (primario): protocollo WSOL su waste satellitare + il disaccoppiamento classificazione/localizzazione lungo il GSD. Difendibile da solo.
2. **Metodo** (secondario, applicativo): distillazione cross-GSD come uso dell'alta risoluzione come *privileged information* a training time per un modello che in deployment vede ~1 m (IRIDE). Va presentato come applicazione ragionata di un'idea nota a un asse nuovo, non come invenzione.
3. **Spettro** (terzo): interazione bande × GSD (EXP-004/014/015).

## Riferimenti verificati

1. Wang, Y., Zhang, J., Kan, M., Shan, S., Chen, X. *Self-supervised Scale Equivariant Network for Weakly Supervised Semantic Segmentation*. arXiv:1909.03714, 2019.
2. Wang, Y., Zhang, J., Kan, M., Shan, S., Chen, X. *Self-Supervised Equivariant Attention Mechanism for Weakly Supervised Semantic Segmentation*. CVPR 2020, 12275-12284.
3. Choe, J., Oh, S.J., Lee, S., Chun, S., Akata, Z., Shim, H. *Evaluating Weakly Supervised Object Localization Methods Right*. CVPR 2020, 3133-3142.
4. Shin, S., Lee, J., Lee, J., Yu, Y., Lee, K. *Teaching Where to Look: Attention Similarity Knowledge Distillation for Low Resolution Face Recognition*. ECCV 2022.
5. Qi, L., Kuen, J., Gu, J., Lin, Z., Wang, Y., Chen, Y., Li, Y., Jia, J. *Multi-Scale Aligned Distillation for Low-Resolution Detection*. CVPR 2021.
6. Torres, R.N., Fraternali, P. *AerialWaste dataset for landfill discovery in aerial and satellite images*. Scientific Data 10, 2023.
