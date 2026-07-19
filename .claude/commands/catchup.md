---
description: Riallineati allo stato della tesi e proponi la prossima azione
---

Riallineamento a inizio sessione. In ordine:

1. Leggi `STATO.md` (root).
2. Leggi l'ultima call per data in `docs/01_calls/` (`ls` e prendi la data più recente nel filename). Se contraddice STATO.md, correggi subito STATO.md: vince la call.
3. Scorri `docs/04_planning/2026-07-19_piano_7_punti.md` (o piano più recente), `EXPERIMENTS_LOG.md` (coda + ultime entry) e `CLAIMS.md`.
4. `git log --oneline -10` per vedere cosa è successo dall'ultima sessione.

Poi rispondi, in italiano, scannable, senza preamboli:

- **Stato** in ≤5 righe (fase, dove siamo rispetto al piano)
- **Blockers/in attesa** (chi deve fare cosa)
- **Prossima azione concreta proposta** (una, con motivazione in una riga; alternative solo se la scelta è davvero ambigua)

Non riassumere l'intera storia del progetto: solo ciò che serve per agire adesso.
