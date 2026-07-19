#!/usr/bin/env bash
# Setup accesso SSH a eagle (container multispectralwaste) — idempotente, sicuro da rilanciare.
# Uso: bash docs/00_context/setup_eagle_ssh.sh   (su ogni PC da cui vuoi lavorare)
# Riferimento: server_eagle_howto.md §Setup passo-passo
set -euo pipefail

EMAIL="ap.alessandro.potenza@gmail.com"
KEY="$HOME/.ssh/id_ed25519"

mkdir -p "$HOME/.ssh" && chmod 700 "$HOME/.ssh"

# 1. Chiave: genera solo se manca (non tocca chiavi esistenti)
if [ ! -f "$KEY" ]; then
    ssh-keygen -t ed25519 -C "$EMAIL" -f "$KEY"
    echo ">> Nuova chiave generata."
else
    echo ">> Chiave già presente, non tocco nulla."
fi

# 2. Blocco eagle in ~/.ssh/config: aggiungi solo se manca
if ! grep -qs "multispectralwaste.eagle" "$HOME/.ssh/config"; then
    cat >> "$HOME/.ssh/config" <<'EOF'

Host multispectralwaste.eagle
    Hostname multispectralwaste.eagle.rslab.cc
    User dev
    Port 2212
    IdentityFile ~/.ssh/id_ed25519
EOF
    echo ">> Blocco eagle aggiunto a ~/.ssh/config."
else
    echo ">> Blocco eagle già in ~/.ssh/config."
fi
chmod 600 "$HOME/.ssh/config"

echo
echo "== Chiave pubblica di QUESTO PC =="
cat "$KEY.pub"
echo
echo "Se questa chiave non è ancora abilitata sul server:"
echo "  - primo PC: incollala a Thomas in chat"
echo "  - PC successivi: da un PC già abilitato (VPN accesa):"
echo "      ssh multispectralwaste.eagle \"echo '<incolla qui la riga ssh-ed25519>' >> ~/.ssh/authorized_keys\""
echo
echo "Poi, con VPN PoliMi attiva (portale DEIB gp-deib-saml.vpn.polimi.it):"
echo "  ssh multispectralwaste.eagle"
