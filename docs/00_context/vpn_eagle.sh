#!/usr/bin/env bash
# VPN PoliMi (portale DEIB) per il server eagle — su/giu/stato senza pensarci.
# Uso: bash vpn_eagle.sh [up|down|status]
#
# Come funziona: al primo "up" serve il login SPID (finestra gp-saml-gui);
# il cookie di autenticazione che ne esce vale circa 30 giorni e viene salvato
# in /root/.vpn-eagle-cookie, quindi i successivi "up" si connettono da soli.
# openconnect gira come unita systemd transiente "vpn-eagle": sopravvive alla
# chiusura del terminale e con "down" ripulisce DNS e route correttamente.
set -euo pipefail
umask 077

PORTAL=gp-deib-saml.vpn.polimi.it
CK=/root/.vpn-eagle-cookie
CMD=${1:-up}

tun_up() { ip link show 2>/dev/null | grep -q ': tun'; }

start_unit() {
    sudo systemctl reset-failed vpn-eagle 2>/dev/null || true
    sudo systemd-run --unit=vpn-eagle --collect /bin/bash -c \
        '. /root/.vpn-eagle-cookie; echo "$COOKIE" | exec openconnect --protocol=gp --useragent="PAN GlobalProtect" --os=linux-64 --cookie-on-stdin --servercert "$FINGERPRINT" "$HOST"'
    for _ in $(seq 1 15); do sleep 2; tun_up && return 0; done
    return 1
}

case "$CMD" in
status)
    if tun_up; then echo "VPN su (unita: $(systemctl is-active vpn-eagle 2>/dev/null || echo esterna))"
    else echo "VPN giu"; fi
    ;;
down)
    sudo systemctl stop vpn-eagle 2>/dev/null || true
    echo "VPN spenta."
    ;;
up)
    if tun_up; then echo "VPN gia su."; exit 0; fi
    # 1) prova col cookie salvato (nessuna interazione)
    if sudo test -s "$CK" && start_unit; then echo "VPN su (cookie salvato)."; exit 0; fi
    sudo systemctl stop vpn-eagle 2>/dev/null || true
    # 2) cookie assente o scaduto: login SAML (qui serve lo SPID, una volta al mese)
    echo "Serve il login PoliMi: si apre la finestra..."
    TMP=$(mktemp)
    DISPLAY=${DISPLAY:-:0} gp-saml-gui -g -q "$PORTAL" > "$TMP"
    PRELOGIN=$(grep -oP '^COOKIE=\K.*' "$TMP")
    SAMLUSER=$(grep -oP '^USER=\K.*' "$TMP")
    rm -f "$TMP"
    [ -n "$PRELOGIN" ] || { echo "Login fallito."; exit 1; }
    # 3) converti il cookie monouso in cookie di sessione (~30 giorni) e salvalo
    AUTH=$(mktemp)
    echo "$PRELOGIN" | sudo openconnect --protocol=gp --useragent='PAN GlobalProtect' \
        --user="$SAMLUSER" --os=linux-64 --usergroup=gateway:prelogin-cookie \
        --passwd-on-stdin --authenticate "$PORTAL" > "$AUTH"
    sudo install -m 600 -o root -g root "$AUTH" "$CK"
    rm -f "$AUTH"
    start_unit && echo "VPN su (nuovo cookie salvato, valido ~30 giorni)." || { echo "Connessione fallita."; exit 1; }
    ;;
*)
    echo "Uso: $0 [up|down|status]"; exit 1;;
esac
