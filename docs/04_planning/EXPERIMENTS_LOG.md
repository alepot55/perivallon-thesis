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

*(vuoto — prima entry al primo run su eagle)*
