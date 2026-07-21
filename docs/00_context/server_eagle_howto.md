# Server eagle — guida operativa completa

> Tutto ciò che serve per lavorare sull'infra del gruppo, in un posto solo. Fonti: guida ufficiale "[Docker] User guide" (Google Doc del gruppo) + messaggi Thomas 17–19/7/2026.

## I tuoi dati

| Cosa | Valore |
|---|---|
| Server | **eagle** |
| Environment (container) | **multispectralwaste** |
| Porta SSH | **2212** |
| Hostname | `multispectralwaste.eagle.rslab.cc` *(pattern `<ENV>.<SERVER>.rslab.cc` dalla guida — [inferenza] verifica al primo accesso, se non risolve chiedi a Thomas l'hostname esatto)* |
| User | `dev` (home: `/home/dev`) |
| GPU | 2 per server, **condivise** tra tutti gli utenti (nell'esempio della guida: 2× RTX PRO 6000 Blackwell — verifica con `check-gpu`) |
| Web (TensorBoard ecc.) | `https://multispectralwaste.eagle.rslab.cc` → mappato sulla **porta 6006** interna |

## Mental model (30 secondi)

```
tu (Roma) ──VPN PoliMi (DEIB)──> rete PoliMi ──SSH:2212──> eagle
                                                    └── container "multispectralwaste" (il TUO ambiente isolato, user dev)
                                                          ├── /home/dev      → codice (git), venv, config   [persistente]
                                                          ├── /data/<prog>   → dataset + risultati          [persistente, condiviso]
                                                          ├── /scratch       → storage veloce temporaneo    [cancellabile!]
                                                          └── /archive       → imagery/pesi comuni          [read-only]
                                                          GPU ×2 condivise (prenotazione su spreadsheet)
```

Ogni ricercatore ha un container isolato sul server: niente collisioni di dipendenze, ma **niente sudo** (le modifiche di sistema le fa il supervisore su richiesta). Il server **non è raggiungibile da Internet**: solo rete PoliMi o VPN. Accesso **solo con chiave SSH**. Se il container va ricreato, sopravvive solo ciò che sta nelle 4 cartelle sopra.

## Passaggi preliminari (bloccanti — falli SUBITO)

| # | Cosa | Dipende da | Lead time |
|---|---|---|---|
| 1 | **VPN PoliMi**: l'accesso va **abilitato dall'IT su richiesta del supervisore**. Se non l'hai mai richiesta → chiedi a Thomas di attivarla per il tuo account | Thomas → IT PoliMi | il più lungo, giorni |
| 2 | **Chiave SSH**: generala (sotto) e manda la **sola chiave pubblica** (`.pub`) a Thomas | tu → Thomas abilita | ore/giorni |
| 3 | Repo **GitLab**: username a Enrico → ti assegna/aggiunge alla repo del team group | Enrico | — |

Senza 1+2 non entri. Il resto è self-service.

## Setup passo-passo

### 1. VPN (una tantum, su ciascun PC)

Portale DEIB: **`gp-deib-saml.vpn.polimi.it`** ([guida ICT PoliMi](https://www.ict.polimi.it/configurazioni/vpn/)). Account già abilitato (conferma Thomas 19/7). Due autenticazioni in sequenza (portal + gateway) sono normali.

- **Windows / WSL**: da browser Windows apri `https://gp-deib-saml.vpn.polimi.it` → login PoliMi → scarica e installa il client GlobalProtect 64-bit → apri il client, portal `gp-deib-saml.vpn.polimi.it`, Connect. La VPN di Windows copre anche WSL.
- **Linux nativo**: (a) prova il portale da browser: dopo il login la pagina Palo Alto a volte offre il pacchetto Linux del client ufficiale; (b) altrimenti open-source: `sudo apt install openconnect gp-saml-gui` (su Ubuntu 24.04 è pacchettizzato; NON è su PyPI), poi **`gp-saml-gui --gateway gp-deib-saml.vpn.polimi.it`** — apre la finestra di login SAML PoliMi (funziona anche via SPID). **Attenzione**: NON attacca la VPN da sola — a login riuscito **stampa** il comando `echo <cookie> | sudo openconnect --protocol=gp ... --usergroup=gateway:prelogin-cookie ...` da incollare subito (cookie monouso, scade in fretta). Il flag `--gateway` è necessario: senza, openconnect consuma il cookie sul portal e poi si blocca su `prelogin-cookie: fgets (stdin)` quando il gateway ne chiede un secondo (verificato 19/7). La VPN resta su finché il terminale con openconnect è aperto (Ctrl+C per staccare) → ssh da un secondo terminale.
- Per capire se sei in WSL: `grep -qi microsoft /proc/version && echo WSL || echo nativo`.
- Se il login SAML risponde "non autorizzato" → account non abilitato al portale DEIB: solo in quel caso serve Thomas→IT.

### 2. Chiave SSH (una tantum)

```bash
ssh-keygen -t ed25519 -C "ap.alessandro.potenza@gmail.com"
# invio → percorso default ~/.ssh/id_ed25519 (+ passphrase a scelta)
cat ~/.ssh/id_ed25519.pub   # ← QUESTA la mandi a Thomas (mai la privata)
```

**✅ Fatto il 2026-07-19** sul PC "Jimmy" (`/home/alepot55/.ssh/id_ed25519`). Chiave pubblica (questa è pubblica, si può committare — la privata resta SOLO su Jimmy):

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGw92Gix74c2jZFqKQCVF5QR8hb0mst0d+mwneRFfEqz ap.alessandro.potenza@gmail.com
```

Fingerprint: `SHA256:XGA3NHeEcZGWY38+ITzi+SzXpDsmPCBOW9usGibPMKQ`

> ⚠️ Da un **altro PC** questa chiave non funziona: la privata sta solo su Jimmy → una chiave per macchina.
>
> **✅ Secondo PC "Jhonny"** (setup 2026-07-21, chiave preesistente riusata, blocco eagle aggiunto a `~/.ssh/config`). Pubblica da abilitare (self-service da Jimmy, o via Thomas):
> ```
> ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIH94OAEvOjEY+6v/t/BCJcGjUyS9cE2e2FH9KPPRc+Q1 alepot55@Jhonny
> ```
>
> **Setup multi-PC (script pronto)**: su ogni PC lancia `bash docs/00_context/setup_eagle_ssh.sh` — idempotente: genera la chiave solo se manca, aggiunge il blocco eagle a `~/.ssh/config`, stampa la `.pub`. Per abilitare la chiave di un PC nuovo **non serve Thomas**: da un PC già abilitato (VPN accesa) basta
> ```bash
> ssh multispectralwaste.eagle "echo '<riga ssh-ed25519 del PC nuovo>' >> ~/.ssh/authorized_keys"
> ```
> La VPN invece va configurata su **ciascun** PC (guida ICT, portale DEIB).

### 3. Config SSH (una tantum)

Aggiungi a `~/.ssh/config` sul tuo computer:

```
Host multispectralwaste.eagle
    Hostname multispectralwaste.eagle.rslab.cc
    User dev
    Port 2212
    IdentityFile ~/.ssh/id_ed25519
```

Poi, con VPN attiva:

```bash
ssh multispectralwaste.eagle
```

### 4. VS Code Remote (consigliato dalla guida)

1. Installa l'estensione **Remote Development**.
2. Bottone `><` in basso a sinistra → *Connect to Host…* → `multispectralwaste.eagle`.
3. Apri il workspace demo: `/home/dev/setup/demo.code-workspace` → *Open Workspace*.
4. La guida **raccomanda i workspace**: copia `demo.code-workspace` in `/home/dev`, modificalo per aprire insieme la repo git e la cartella progetto in `/data`.

### 5. Ambiente Python + test GPU (una tantum)

```bash
cd ~/setup
bash setup.sh          # crea il venv "base" + installa requirements.txt
venv base              # alias per attivare un venv (i venv vivono in ~/.virtualenvs, $ENVSDIR)
pip list               # verifica
```

Poi apri `setup/test.ipynb` in VS Code → *Select Kernel* → *Python Environments* → `base` (refresh se non appare; installa estensioni Python+Jupyter e `ipykernel` se richiesto) → Run all. Output atteso: PyTorch con CUDA available, 2 GPU visibili.

Regola venv: pacchetti **sempre dentro venv**, mai system-wide. Nuovo venv: `python -m venv $ENVSDIR/<NOME>`. Il default `base` va bene per tutto, salvo test di versioni nuove.

### 6. GitLab dal server (una tantum)

Il codice vive in `/home/dev` come repo git (assegnata da Enrico sotto il team group).

1. Genera una **seconda** chiave SSH *sul server* (stessa procedura del punto 2).
2. Aggiungi la pubblica al tuo profilo GitLab ([guida GitLab SSH](https://docs.gitlab.com/user/ssh/)).
3. In `~/.ssh/config` *sul server* indica la chiave per GitLab.

## Storage — dove va cosa (importante)

| Cartella | Uso | Regole |
|---|---|---|
| `/home/dev` | Codice (repo git), config, venv | **MAI dataset o risultati esperimenti** |
| `/data/<progetto>` | Dataset + risultati | Storage **permanente**; condiviso tra utenti → attenzione a dove salvi e soprattutto a cosa cancelli |
| `/scratch` | Dati temporanei per job high-performance (più veloce di /data) | Gli admin possono **cancellare in qualsiasi momento** cartelle inutilizzate → niente di importante qui |
| `/archive` | Imagery satellitare, dataset comuni, pesi pretrained | **Read-only**; per modificare → copia in `/data` (o `/scratch` per test usa-e-getta) |

Tutto ciò che sta fuori da queste 4 cartelle **si perde** se il container viene ricreato.

## Regole di training (non scritte a caso — GPU condivise)

1. **Prenota il timeslot GPU** prima di ogni training: spreadsheet [Turni GPU](https://docs.google.com/spreadsheets/d/1RMrwoT3tvJXWq3A9GytZkyKQFK1Qff2K4rtTPU4pkcI/edit?gid=2057489764#gid=2057489764), pagina del server giusto (eagle). Nessun limite formale di ore consecutive, ma prenota **solo il necessario**.
2. **Training = script Python, mai notebook**: a fine script GPU e RAM si liberano da sole; un notebook tiene occupata la GPU finché non spegni il kernel.
3. **Sempre dentro tmux** (preinstallato): lanci, ti stacchi, chiudi il laptop, il job continua.
4. Web tools (TensorBoard, FiftyOne): lanciali sulla **porta 6006** → li vedi su `https://multispectralwaste.eagle.rslab.cc`.

## Cheat sheet

| Azione | Comando |
|---|---|
| Connettersi | `ssh multispectralwaste.eagle` |
| Nuova sessione tmux | `tmux new -s train1` |
| Detach | `Ctrl+b`, poi `d` |
| Lista sessioni | `tmux ls` |
| Riattacca | `tmux a -t train1` |
| Attiva venv | `venv base` |
| Nuovo venv | `python -m venv $ENVSDIR/<nome>` |
| Monitor CPU/RAM | `htop` |
| Monitor GPU | `check-gpu` (alias di `watch nvidia-smi`) |
| Riferimento tmux | [tmuxcheatsheet.com](https://tmuxcheatsheet.com/) |

## Cose che può fare solo il supervisore (chiedi, non forzare)

- Attivazione VPN (via IT)
- Abilitazione della tua chiave SSH sull'environment
- Pacchetti apt / qualsiasi cosa richieda sudo (l'ambiente non va modificato)
- Assegnazione repo GitLab nel team group (Enrico)
- Spazio/cartella progetto in `/data` se non esiste già

## Primo giorno operativo — checklist

- [ ] VPN su e funzionante (`ssh multispectralwaste.eagle` risponde)
- [ ] `bash setup.sh` + `test.ipynb` → 2 GPU visibili
- [ ] Workspace VS Code personale creato
- [ ] Chiave GitLab dal server configurata, `git clone` della repo del team
- [ ] Giro in `/data` e `/archive`: trova il dataset satellite-only e i pesi pretrained, annota i path in `STATO.md`
- [ ] Prima prenotazione GPU di prova sul foglio Turni
