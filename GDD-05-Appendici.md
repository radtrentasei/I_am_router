# GDD-05-Appendici

## 1. Audio

### 1.1 Stile Audio
- **Chiptune** e effetti sonori (SFX)
- **Musica di sottofondo** in stile retro gaming
- Palette sonora coerente con l'estetica pixel-art del gioco

### 1.2 Effetti Sonori
- **Azioni chiave**: claim router, attivazione link, errore, successo
- **Feedback audio** per tutte le azioni di gioco (click, attivazione/disattivazione link)
- **Eventi di gioco**: attivazione di un link, errore, successo, raggiungimento obiettivi

### 1.3 Opzioni Audio
- **Volume regolabile** tramite menu opzioni
- **Controlli separati** per disattivare musica o effetti sonori
- **Compatibilità**: supporto per ambienti senza audio (driver dummy)

## 2. Glossario Interattivo

### 2.1 Termini Fondamentali

**Rete**: Insieme di dispositivi (computer, router, server) collegati tra loro per scambiarsi dati.

**Router**: Dispositivo che indirizza i pacchetti di dati tra reti diverse.

**Interfaccia**: Punto di connessione fisica o logica su un router (nord, sud, est, ovest nel gioco).

**Interfaccia logica (sub-interface)**: Interfaccia virtuale creata su un'interfaccia fisica, identificata dal numero VLAN.

**VLAN**: Virtual Local Area Network - tecnologia che permette di creare reti logiche separate su una stessa infrastruttura fisica.

**Neighborship**: Relazione di routing attiva tra due router adiacenti che si scambiano informazioni di routing.

**Tabella di routing**: Struttura dati che contiene le informazioni sui percorsi migliori per raggiungere le diverse reti.

**Loopback**: Interfaccia virtuale interna al router, utilizzata per identificazione e gestione.

**Claim**: Azione di prendere controllo di un router nel gioco, assegnandogli un hostname personalizzato.

**Token**: Risorsa di gioco che limita le azioni del giocatore, si ricarica automaticamente nel tempo.

**API RESTCONF**: Protocollo per la configurazione e gestione dei dispositivi di rete tramite interfacce REST.

**Group ID**: Identificativo del gruppo logico di router (corrisponde alla VRF del router reale).

**Local ID**: Identificativo del router specifico all'interno del suo gruppo.

### 2.2 Accessibilità
- **Sempre disponibile**: dal menu principale e durante la partita
- **Ricerca rapida**: possibilità di cercare termini specifici
- **Collegamenti**: termini correlati linkati tra loro
- **Esempi pratici**: ogni termine accompagnato da esempi d'uso nel gioco

## 3. Requisiti di Qualità del Codice

### 3.1 Documentazione
- **Codice abbondantemente commentato**: ogni funzione, classe, modulo e blocco logico deve essere documentato tramite commenti e docstring
- **Materiale didattico**: ogni concetto implementato, pattern o soluzione deve essere spiegato
- **Esempi d'uso**: aggiungere esempi nei commenti/docstring dove utile

### 3.2 Stile e Struttura
- **Soluzioni semplici**: preferire leggibilità e linearità rispetto alla complessità, salvo necessità tecniche documentate
- **Best practice Python**: seguire PEP8, utilizzare nomi chiari, separazione in moduli
- **Manutenibilità**: attenzione alla facilità di modifica e estensione del codice
- **Robustezza**: logica di estrazione hostname robusta rispetto a dati assenti o vuoti nelle risposte API

### 3.3 Architettura
- **Separazione delle responsabilità**: logica di gioco, rendering, configurazione, audio in moduli separati
- **Gestione errori**: errori gestiti sempre con fallback visivo, nessun crash blocking
- **Estensibilità**: codice progettato per facilitare l'aggiunta di nuove funzionalità

## 4. Scelte di Sviluppo Software

### 4.1 Tecnologie Utilizzate
- **Linguaggio principale**: Python 3
- **Libreria grafica**: pygame per la UI 2D e gestione eventi
- **Standard di codifica**: PEP8, con eccezioni per leggibilità didattica

### 4.2 Architettura del Progetto
```
main.py                 # Entrypoint e ciclo principale
config.py               # Configurazione centralizzata
api.py                  # Gestione RESTCONF e debug API
router_grid.py          # Logica griglia e router
ui.py                   # Rendering grafico e UI
events.py               # Gestione eventi
glossary.py             # Glossario e tutorial
audio.py                # Effetti sonori e musica
utils.py                # Funzioni di utilità
requirements.txt        # Dipendenze Python
```

### 4.3 Principi di Design Software
- **Separazione netta** tra logica di gioco (router_grid.py) e rendering/UI (ui.py)
- **Configurazione centralizzata** in config.py
- **Modularità**: ogni componente ha responsabilità specifiche e ben definite
- **API simulate/locali** per comunicazione con router virtuali

### 4.4 Logica di Stato e Sincronizzazione
- **Claim router**: basato sul parsing del campo description della loopback
- **Stato router**: 
  - Propri: colore player
  - Altri giocatori: arancione  
  - Liberi: grigio
- **Hostname**: aggiornato solo se description presente e non vuota, altrimenti '?'
- **Polling continuo**: aggiornamento stato router/interfacce/token in tempo reale
- **Nessuna gestione locale "stale"**: la UI riflette sempre lo stato reale lato backend

### 4.5 Gestione Interfacce e VLAN
- **Visibilità frecce**: solo se VLAN configurata (link logico esiste)
- **Colorazione frecce**:
  - Verde: interfaccia up
  - Rosso: interfaccia down  
  - Giallo: hover (indipendente da stato up/down)
- **Hover coerente**: posizione calcolata esattamente come nel rendering

### 4.6 UI e User Experience
- **Stile retro pixel-art**: palette pastello, nessun effetto moderno
- **Griglia adattiva**: in base alla dimensione selezionata
- **Feedback immediato**: per claim, errori, cambi stato interfaccia
- **Solo token locali**: visibili solo i propri token e timer
- **Hostname sempre visibile**: sotto ogni router con aggiornamento real-time

### 4.7 Gestione Errori e Robustezza
- **Errori sempre mostrati**: a schermo con messaggio rosso pixel-art
- **Logica hostname robusta**: gestisce dati assenti o vuoti
- **Nessun crash**: errori gestiti sempre con fallback visivo
- **API asincrone**: non bloccano mai l'interfaccia utente

### 4.8 Debug e Sviluppo
- **ID router**: visibili solo a terminale per debug
- **Chiamate API**: sempre stampate a terminale
- **Nessun riferimento**: a token o timer di altri giocatori nella UI
- **Documentazione sincronizzata**: tutte le regole di rendering e logica mantenute in sync con il GDD

---

*Ultimo aggiornamento: 2 Luglio 2025*
