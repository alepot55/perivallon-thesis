# Tesi — PERIVALLON

Master's Thesis at Politecnico di Milano, part of PERIVALLON Horizon Europe (Grant 101073952).

**Current direction (pivot 2026-07-17):** binary illegal-landfill detection on satellite-only multispectral imagery, with resolution (GSD 30 cm → 1.2 m) as the main experimental axis. Previous direction (material classification, asbestos pilot, spectral signatures) is on hold and kept as knowledge base.

**Author:** Alessandro Potenza · **Advisor:** Prof. Piero Fraternali · **Supervisors:** Thomas Martinoli, Enrico Targhini

## Orientation

| Entry point | What |
|---|---|
| `STATO.md` | Current state, TODOs, decision log — **start here** |
| `CLAUDE.md` | Agent guide (protocol, conventions, commands) |
| `docs/INDEX.md` | Reading map of all thesis docs |
| `docs/01_calls/` | Supervisor call notes, dated — latest wins |
| `docs/04_planning/` | Operating plan, experiments log, claims ledger |

## Layout

```
Tesi/
├── STATO.md       Working memory (state, TODOs, decisions)
├── docs/          Thesis knowledge base (context, calls, research, planning)
├── papers/        Bibliography system (kebab-case IDs, auto-generated indexes)
├── waste/         Code — baseline replication on AerialWaste v3 (Swin-T + RSP, F1 0.9519)
├── asbestos/      Code/data — asbestos pilot (on hold; Mazzola 2024 reference thesis)
├── spectral/      USGS splib07a spectral signatures (on hold, knowledge base)
└── assets/        Slide decks (deck_v7 latest)
```

Not tracked here: the LaTeX thesis (Overleaf), the group's experiment code (PoliMi GitLab, runs on the `eagle` server — see `docs/00_context/server_eagle_howto.md`), heavy checkpoints and imagery.

## Status

- [x] Baseline Swin-T + RSP replicated on AerialWaste v3 — val F1 **0.9519**
- [x] EuroSAT band ablation · backbone comparison (Swin-T / SSL4EO / DOFA) · multi-class extension
- [x] Materials SOTA loop (6 iterations) — related-work draft + verified bibliography (`docs/02_research/loop_prof_sota/`)
- [x] 2026-07-17 pivot: satellite-only binary detection, resolution axis
- [ ] Infra setup on eagle (VPN + SSH key pending)
- [ ] Satellite-only baseline reproduction (~1.2k imgs, models per Enrico)
- [ ] Resolution grid 30/70/120 cm
- [ ] Weakly-supervised localization track (goal: +2 punti — see `docs/04_planning/2026-07-19_piano_7_punti.md`)

## Key references

- Gibellini et al. (2025) — *Waste Management Bulletin*. Binary baseline pipeline (replicated in `waste/`).
- Torres & Fraternali (2023) — *Scientific Data* 10:63. AerialWaste dataset.
- Alari (2024) — politesi 10589/230633. Satellite material classification (group predecessor).
- Mazzola (2024) — politesi 10589/230433. Asbestos + Grad-CAM/WSL (`asbestos/reference/`).

Full bibliography: `papers/` (see its README for the ID system and scripts).
