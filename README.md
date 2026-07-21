# Tesi — PERIVALLON

Master's Thesis at Politecnico di Milano, part of PERIVALLON Horizon Europe (Grant 101073952).

**Current direction (pivot 2026-07-17):** binary illegal-landfill detection on satellite-only multispectral imagery, with resolution (GSD 30 cm → 1.2 m) as the main experimental axis. Previous direction (material classification, asbestos pilot, spectral signatures) is on hold and kept as knowledge base.

**Author:** Alessandro Potenza · **Advisor:** Prof. Piero Fraternali · **Supervisors:** Thomas Martinoli, Enrico Targhini

## 🧭 Orientation

| Entry point | What |
|---|---|
| 📌 `STATO.md` | Current state, la rotta, TODOs, decision log — **start here** |
| 🤖 `CLAUDE.md` | Agent guide (protocol, conventions, commands) |
| 🗺️ `docs/INDEX.md` | Reading map of all thesis docs |
| 📞 `docs/01_calls/` | Supervisor call notes, dated — latest wins |
| 🎯 `docs/04_planning/` | Piano 7 punti, experiments log, claims ledger |
| 📚 `docs/02_research/` | Research — baseline frozen, EDA server data, mini-SOTA |

## 🛰️ Remote workspace (server eagle)

Experiments run on the group's server, not here. This repo holds knowledge, plans and results.

```bash
bash docs/00_context/vpn_eagle.sh up      # PoliMi VPN (SPID login ~once a month)
ssh multispectralwaste.eagle              # enter the container (user dev)
tmux new -s lavoro                        # always tmux for long jobs
```

- Full guide (storage, GPU rules, setup): `docs/00_context/server_eagle_howto.md`
- What is on the server (datasets, weights, paths): `docs/02_research/2026-07-21_eda_dati_eagle.md`
- The group's experiment code lives on PoliMi GitLab (assigned by Enrico), cloned in `/home/dev` on the server — not in this repo. Results and conclusions come back here (`docs/04_planning/EXPERIMENTS_LOG.md` + `CLAIMS.md`).

## 📁 Layout

```
Tesi/
├── STATO.md       Working memory (state, TODOs, decisions) — START HERE
├── docs/          Thesis knowledge base (context, calls, research, planning)
├── papers/        Bibliography system (kebab-case IDs, auto-generated indexes)
├── waste/         Code — baseline replication on AerialWaste v3 (Swin-T + RSP, F1 0.9519)
├── asbestos/      Code/data — asbestos pilot (on hold; Mazzola 2024 reference thesis)
├── spectral/      USGS splib07a spectral signatures (on hold, knowledge base)
└── assets/        Slide decks (deck_v8 = canonical, presented 17/7)
```

Not tracked here: the LaTeX thesis (Overleaf), the group's experiment code (PoliMi GitLab), heavy checkpoints and imagery.

## ✅ Status

- [x] Baseline Swin-T + RSP replicated on AerialWaste v3 — val F1 **0.9519**
- [x] EuroSAT band ablation · backbone comparison (Swin-T / SSL4EO / DOFA) · multi-class extension
- [x] Materials SOTA loop (6 iterations) — related-work draft + verified bibliography (`docs/02_research/loop_prof_sota/`)
- [x] 2026-07-17 pivot: satellite-only binary detection, resolution axis
- [x] Infra on eagle: VPN managed + SSH from both PCs + venv/GPU verified (21/7)
- [x] Server data recon: dataset 0.3m/1.2m with ready splits, 2827 object bboxes on satellite positives (21/7)
- [ ] Call Enrico → satellite-only baseline reproduction (models per Enrico)
- [ ] Resolution grid 30/70/120 cm
- [ ] Weakly-supervised localization track (goal: +2 punti — see `docs/04_planning/2026-07-19_piano_7_punti.md`)

## 📖 Key references

- Gibellini et al. (2025) — *Waste Management Bulletin*. Binary baseline pipeline (replicated in `waste/`; frozen numbers in `docs/02_research/baseline_gibellini_frozen.md`).
- Torres & Fraternali (2023) — *Scientific Data* 10:63. AerialWaste dataset.
- Alari (2024) — politesi 10589/230633. Satellite material classification (group predecessor).
- Mazzola (2024) — politesi 10589/230433. Asbestos + Grad-CAM/WSL (`asbestos/reference/`).

Full bibliography: `papers/` (see its README for the ID system and scripts).
