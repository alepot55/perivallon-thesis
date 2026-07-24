---
description: Stato del server eagle in un colpo — VPN, GPU, tmux, dischi
argument-hint: [opzionale: gpu | tmux | disk]
---

Controlla lo stato del server eagle e riporta uno schema compatto. Argomento opzionale per limitare il check: $ARGUMENTS

1. **VPN**: `ssh -o ConnectTimeout=5 multispectralwaste.eagle true` — se fallisce, prova `bash docs/00_context/vpn_eagle.sh status` e, se la VPN è giù, `bash docs/00_context/vpn_eagle.sh up` (se serve login SPID, avvisa Ale e fermati).
2. **Stato server**, un solo comando ssh:
   `ssh multispectralwaste.eagle 'nvidia-smi --query-gpu=index,utilization.gpu,memory.used,memory.total --format=csv,noheader; echo ---; tmux ls 2>/dev/null || echo no-tmux; echo ---; df -h /data /scratch | tail -n +2'`
3. Riporta in forma schematica: GPU (libera/occupata, da chi se deducibile), tmux nostri attivi (nomi e da quanto), spazio disco.
4. **Regola turni**: se una nostra run risulta finita (tmux morto o GPU libera), ricorda di togliere la prenotazione dal foglio Turni GPU; se stiamo per lanciare, ricorda di verificare la prenotazione prima.
