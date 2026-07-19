# Piano operativo — obiettivo ≥7 punti a dicembre 2026

> Redatto 2026-07-19, post call 17/7 (pivot binary detection + follow-up punteggio). Obiettivo dichiarato di Ale: **≥7 punti alla sessione di dicembre**. Riferimenti: `../01_calls/2026-07-17_pivot_binary_detection.md`, `../01_calls/2026-07-17_punteggio_strategia.md`.

---

## Premesse oneste

1. **[fatto]** Thomas: impostazione attuale ≈5 punti; i ~2 extra si sbloccano solo con **innovazione riconoscibile dalla commissione** (che è severa e variabile). I punti non si "decidono": si massimizza la probabilità.
2. **[fatto, da repo]** La pipeline Gibellini **include già Grad-CAM** (tile → classifier → Grad-CAM saliency → GIS; Fig. 2 del paper) e anche Sun 2023 (global dumpsites) mostra CAM. → "Aggiungo la localizzazione dalle label binarie" **non supera l'asticella da solo**: nel gruppo i CAM qualitativi sono routine. Il delta deve essere **metodo oltre vanilla CAM + valutazione quantitativa delle maschere**.
3. **[fatto, da repo]** Gibellini ha già fatto l'ablation GSD 20/30/50 cm (36 configurazioni, su aereo). → La griglia risoluzioni satellite 30→120 cm è **base necessaria ma non innovazione**: estende un esperimento esistente a un dominio nuovo.
4. **[inferenza]** Leva principale sotto il tuo controllo: **quando** arrivi al checkpoint di settembre. Se ci arrivi con l'innovazione già dimostrata (numeri in mano), il pitch a Thomas→prof è su risultati; se ci arrivi con la sola base, i +2 slittano fuori tempo massimo.

### ⚠️ Update 19/7 sera — novelty bar più alta

- **[fatto]** La tesi di **Mazzola** (politesi 10589/230433, corr. Gibellini) usa **già Grad-CAM + weakly supervised learning per la localizzazione** dei materiali su imagery MS satellitare (WV-3 + Pléiades Neo). → Nel gruppo il WSL-localization esiste già anche come tesi. Il delta per A/C va dichiarato esplicitamente: task **waste** (non asbestos) + **asse GSD** + **valutazione quantitativa** + metodo oltre vanilla CAM. Mazzola = prima lettura del mini-SOTA (PDF in `asbestos/reference/Mazzola_2024_Thesis.pdf`).
- **[fatto, deck v7]** Per i dataset del gruppo "**no segmentation masks exist**" (annotazioni image-level, Alari 2024: 11.477 multi-label). → La gating question sui poligoni è ancora più centrale: il test-set di localizzazione va **costruito** (Mappatura/ARPA o annotazione ad hoc).

## Strategia in una riga

Comprimere la base (luglio) → sprint sperimentale nelle 2 settimane di ferie (10–23/8) → settembre = iterazione + pitch dei +2 con risultati → ottobre–novembre scrittura. **L'innovazione non è un modulo dopo la base: emerge dagli stessi training della base** (stesse griglie di risoluzione, stessi modelli), quindi il costo marginale di seminarla subito è basso.

## Angolo di innovazione — raccomandazione

**North Star: "Weakly-supervised waste localization under GSD degradation"** — unisce la proposta di Thomas (WSOL da label image-level, buy-in già suo) con l'asse risoluzione che va fatto comunque.

| Opzione | Cos'è | Pro | Contro/rischio |
|---|---|---|---|
| **A. WSOL quantitativo** | Da label binarie a maschere **valutate con metriche** (non solo figure CAM) | Proposta di Thomas; utile in produzione (la pipeline ARPA usa già saliency→GIS); non richiede annotazione densa | Serve un **test-set con poligoni**; delta metodologico obbligatorio oltre Grad-CAM (e oltre Mazzola) |
| **B. Risoluzione×spettro** | Il MS compensa la risoluzione persa? (a 1.2 m le bande contano più che a 30 cm?) | Ricicla il lavoro materiali; narrativa IRIDE/ARPA | È già negli esperimenti base del gruppo → rischia di leggersi come riproduzione |
| **C = A×risoluzione** | La localizzazione weakly-supervised sopravvive alla degradazione di GSD? Metodo che la rende robusta | Novel plausibile (to our knowledge, **da verificare con mini-SOTA**); massima coerenza narrativa; contributo che emerge dagli esperimenti base | Somma i rischi di A + dipende dalla griglia base pronta in tempo |
| **D. FM/GSD-aware** | Scale-MAE/DOFA + primi test dei pesi FM in-house | Cavalca lavoro del gruppo | Tempi di altri → non pianificarci sopra, solo opportunistico |

**Raccomandazione: C come North Star, A come nucleo minimo garantito, B resta nella base (dov'è già), D bonus.**

Method seeds per A/C **[speculazione, da validare con mini-SOTA e con Enrico]**: CAM → pseudo-mask → refinement (seed-and-expand / self-training di un segmenter); consistency loss cross-GSD sulle mappe di localizzazione (stessa scena a 30/70/120 cm → stessa maschera); confronto CAM families (Grad-CAM/LayerCAM/attention di Swin) come ablation, non come contributo.

**Gating question (decide tutto): esiste — o si può costruire — un test-set di localizzazione?** Poligoni anche solo su 100–200 tile (da Mappatura/ARPA, o inseriti nel protocollo della nuova campagna di annotazione a costo quasi zero). Senza maschere di valutazione → niente claim quantitativo → niente innovazione difendibile. È la domanda #1 per Enrico.

## Timeline a ritroso

| Periodo | Obiettivo | Note |
|---|---|---|
| **entro dom 26/7** | Infra funzionante (Docker+GitLab), dataset visto coi miei occhi, call Enrico fatta, angolo scelto v0, primo sanity-training lanciato | |
| **27/7 – 9/8** | Riproduzione baseline su satellite-only (numeri di riferimento) + griglia risoluzioni v1 + prime CAM con eval abbozzata | Serale/weekend; Thomas via dall'1/8 |
| **10 – 23/8 (ferie = full-time)** | **Sprint**: griglia completa, WSOL v1 quantitativo (pseudo-mask + metrica), indice tesi + introduction draft | Le 2 settimane che valgono il piano |
| **24/8 – 15/9** | Iterazione metodo + ablations; feedback Thomas al rientro (~17/8) | Scrivere ogni esperimento nel capitolo appena chiuso |
| **~metà settembre** | **CHECKPOINT**: pitch +2 a Thomas con risultati → decisione col prof | Anticipato rispetto al "vediamo a settembre" |
| **fine settembre** | Fine contratto → più tempo; freeze scope innovazione | |
| **ottobre** | Esperimenti finali + scrittura completa (versione lunga) | |
| **inizio–metà novembre** | Deposito/upload tesi (**data esatta da verificare** — le scadenze le pubblica la biblioteca PoliMi) + eventuale short version (formato article ≈30 pp + executive summary ~6 pp) | |
| **dicembre** | Discussione | |

Regola trasversale: **scrittura in parallelo, mai alla fine** — ogni esperimento chiuso finisce subito nel capitolo. Log esperimenti (`EXPERIMENTS_LOG.md`) + claims ledger (`CLAIMS.md`) dal giorno 1: a settembre il pitch si fa da lì, a novembre la tesi pure.

## Questa settimana (19–26/7)

| Giorno | Azioni |
|---|---|
| **Dom 19** | Guida Docker: passaggi fattibili senza accesso (chiave SSH, config). Claude: doc-baseline Gibellini + domande call. |
| **Lun 20** | Msg Teams a Enrico (username GitLab + proporre mar/mer). Msg a Thomas: VPN + chiave SSH pubblica. Cercare scadenze deposito dicembre (sito biblioteca PoliMi). |
| **Mar/Mer 21–22** | **Call Enrico** (domande sotto) + pitch dell'angolo innovazione. |
| **Gio–Ven** | Setup completato, dati esplorati (EDA veloce: bande, distribuzioni, qualità annotazioni), primo training di sanity. |
| **Entro dom 26** | Baseline run partita + decisione angolo v1 (aggiornata con le risposte di Enrico). |

## Domande per la call con Enrico

**Dati (le risposte decidono l'angolo):**
1. **Esistono poligoni/maschere per un sottoinsieme?** (Mappatura, ARPA, annotazioni interne) Se no: la nuova campagna può includerli su un subset? ← gating per WSOL
2. Dataset satellite-only: formato, bande esatte disponibili (VNIR? come è fatto il pansharpening?), struttura annotazioni (tile-level binaria?), split esistenti, quando entrano le ~800 WorldView.
3. Come sono state scelte le negative? (bias di campionamento → influenza tutto)

**Esperimenti e codice:**
4. Esperimenti preliminari sulle ~1.200: cosa avete provato, cosa è il "qualcosa di interessante", numeri?
5. Da che modelli partiamo (Swin-T+RSP come Gibellini? altro?) e qual è il codice di produzione vs le varianti?
6. Lista esperimenti base che avete in mente → cosa considerate "portato a casa"?

**Risorse e processo:**
7. Compute: che GPU, quote, come si lancia (docker: eagle/2212/multispectralwaste ✓).
8. FM in-house: tempi realistici, posso essere il primo a valutarne i pesi?
9. Cosa sarebbe **utile per il gruppo** come contributo di tesi? (allineamento = supporto al pitch di settembre)
10. Cosa considerate già "fatto" nel gruppo su CAM/weakly-supervised localization (Gibellini pipeline, Mazzola)? Dove finisce il fatto e inizia il nuovo?

## Divisione del lavoro con Claude

1. **Doc-baseline Gibellini congelato** — numeri già verificati in repo (Swin-T+RSP, 20 cm, context 100 m, F1 92.02; factorial 36 config; generalizzazione 86.92 F1 medio; utility ARPA).
2. **Mini-SOTA WSOL/WSSS in remote sensing** con verifica web (parte da Mazzola) → valida o uccide il novelty claim di A/C **prima** della call.
3. **Indice tesi v0** — narrativa C con fallback base-only (formato article ≈30 pp + executive summary).
4. Bozza related work detection (riciclo del draft esistente `../02_research/loop_prof_sota/10_related_work_draft.md`, riorientato).
5. Log esperimenti + claims ledger: attivi in `EXPERIMENTS_LOG.md` / `CLAIMS.md` (questa cartella).

## Rischi principali

| Rischio | Mitigazione |
|---|---|
| Niente poligoni per valutare le maschere ("no segmentation masks exist" — deck v7) | Domanda #1 a Enrico; piano B: annotare in proprio ~100 tile di test (chiedere ok al gruppo); piano C: fallback su angolo B potenziato |
| Metodo WSOL non batte vanilla CAM | Il fallback è comunque una **valutazione quantitativa** mai fatta nel gruppo → contributo minore ma reale; la base resta intatta |
| "Dieci cinesi l'hanno già fatto" (o Mazzola in casa) | Mini-SOTA subito (questa settimana), non a settembre; delta vs Mazzola dichiarato esplicitamente |
| Tempo eroso dal lavoro | Le decisioni pesanti si prendono entro il 26/7; agosto è esecuzione secondo piano |
| Prof non compra i +2 | Pitch anticipato a metà settembre via Thomas, con numeri; se no, la base da 5 è già impacchettata (floor garantito) |
