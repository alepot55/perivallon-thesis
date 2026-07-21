# EXPERIMENTS_LOG — registro esperimenti

> Un esperimento = una entry, appesa in cima alla sezione **Log** (ordine cronologico inverso). ID progressivo `EXP-NNN`. Compilato da Ale o da Claude (`/experiment`). Ogni entry che supporta/uccide un claim aggiorna anche `CLAIMS.md`. Niente numeri senza fonte riproducibile (path del run su eagle o del notebook).

## Template

```markdown
### EXP-NNN — <titolo breve> (YYYY-MM-DD)
- **Domanda**: cosa volevo sapere
- **Setup**: modello / pesi / dati (+ split, seed) / risoluzione / config (path Hydra o comando)
- **Dove**: path risultati su eagle (/data/... ) o notebook
- **Risultati**: metriche chiave (tabella se >2 numeri)
- **Conclusione** (1 riga, tag: HIGH/MEDIUM/UNCERTAIN)
- **Claims toccati**: C-N ↑/↓ (vedi CLAIMS.md)
- **Next**: cosa apre/chiude
```

## Coda esperimenti pianificati (dal piano 7 punti — da rivedere post-call Enrico)

| Priorità | Esperimento | Fase | Dipendenze |
|---|---|---|---|
| 1 | Sanity run: riproduzione baseline gruppo su satellite-only ~1.2k (modello indicato da Enrico) | Base | accesso eagle + GitLab |
| 2 | Baseline a 30 cm: numeri di riferimento propri (F1/P/R, seed ≥3 se budget lo consente) | Base | EXP precedente |
| 3 | Griglia risoluzioni: 30 → ~70 → 120 cm (stesso modello, stesso split) | Base | 2 |
| 4 | +WorldView (~2k img): impatto dimensione dataset | Base | disponibilità immagini |
| 5 | CAM sulla baseline: estrazione mappe + prima eval qualitativa strutturata | Semina C | 2 |
| 6 | Eval quantitativa localizzazione su test-set poligoni (se/quando esiste) | Innovazione | gating question |
| 7 | Method v1: CAM → pseudo-mask → refinement | Innovazione | 6 |
| 8 | Consistency cross-GSD sulla localizzazione | Innovazione | 3 + 6 |
| 9 | FM comparison (DOFA / Scale-MAE / pesi in-house se arrivano) a 1.2 m | Bonus | 3 |

## Log

### EXP-001 — Sanity run binario PNEO, 0.3m vs 1.2m (2026-07-21)
- **Domanda**: la pipeline dati end-to-end (split Thomas → ritaglio dai mosaici → training) funziona? Primo segnale sull'effetto risoluzione.
- **Setup**: ResNet-50 ImageNet (torchvision), 3 bande RGB dalle 6 PNEO, tile 224px, AdamW lr 1e-4 wd 0.05, batch 32, 5 epoche, no seed control. Split `SatRaw/PNEO/Thomas/{0.3m,1.2m}/binary` (train 963, val 120 dopo scarto di 57+15 tile fuori dai 5 mosaici Lombardia). Normalizzazione per-tile max (provvisoria). GPU 1 eagle, slot prenotato.
- **Dove**: `eagle:~/experiments/sanity_binary_pneo.py` + `sanity_03.log` / `sanity_12.log`
- **Risultati**:

| Risoluzione | best val F1 (5 ep) |
|---|---|
| 0.3m (pansharpened) | **0.7294** |
| 1.2m (MS nativo) | **0.6875** |

- **Conclusione**: pipeline funzionante, il modello impara (loss 0.66→0.10); primo indizio del gap di risoluzione (~4 pp F1), NON confrontabile con Gibellini 92.02 (modello, dati, epoche, protocollo diversi). Tag: UNCERTAIN (sanity, no seed, val 120 img).
- **Claims toccati**: nessuno (sanity). Prepara il terreno per C sulla griglia risoluzioni.
- **Next**: (a) chiedere a Enrico perché ~6% delle tile cade fuori dai 5 mosaici processed e quale sia la normalizzazione/ordine bande ufficiale; (b) EXP-002 = baseline vera (Swin-T+RSP, protocollo Gibellini, più epoche, seed); (c) integrare le 6 bande.
