#!/usr/bin/env python3
"""Hook di guardia per la repo tesi.

--mode pre  : blocca Edit/Write sui file auto-generati (papers/INDEX.md,
              papers/index.json, Excel in papers/) — vanno rigenerati con gli script.
--mode post : dopo un Edit/Write su EXPERIMENTS_LOG.md ricorda la checklist
              collegata (guida studio, CLAIMS, Excel Drive, naming, turni GPU).
"""
import json
import sys

GENERATED = ("papers/INDEX.md", "papers/index.json")

REMINDER = (
    "EXPERIMENTS_LOG.md aggiornato - checklist collegata (regola di progetto): "
    "1) docs/00_context/guida_studio.md sez. 5 + changelog; "
    "2) docs/04_planning/CLAIMS.md se un claim cambia status; "
    "3) riga nell'Excel 'Binary Experiments Results' su Drive; "
    "4) id esperimento nel formato bGSD_bande_arch_pretrain_aug_sSEED; "
    "5) se il run e' finito, togliere la prenotazione dal foglio Turni GPU."
)


def main():
    mode = sys.argv[sys.argv.index("--mode") + 1] if "--mode" in sys.argv else "pre"
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    path = (data.get("tool_input") or {}).get("file_path") or ""

    if mode == "pre":
        auto_generated = any(path.endswith(g) for g in GENERATED) or (
            "/papers/" in path and path.endswith(".xlsx")
        )
        if auto_generated:
            print(
                "File auto-generato: non editare a mano. "
                "Rigenera con: cd papers && python3 scripts/build_index.py",
                file=sys.stderr,
            )
            sys.exit(2)
        sys.exit(0)

    if path.endswith("EXPERIMENTS_LOG.md"):
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": REMINDER,
            }
        }))
    sys.exit(0)


main()
