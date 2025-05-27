# 11. Glossario Interattivo in Game

Sezione accessibile dal menu e durante la partita dove il giocatore può consultare i principali concetti di networking:

- **Rete**: Insieme di dispositivi (computer, router, server) collegati tra loro per scambiarsi dati.
- **Router**: Dispositivo che indirizza i pacchetti di dati tra reti diverse.
- **Interfaccia**: Punto di connessione fisica o logica su un router (nord, sud, est, ovest nel gioco).
- **Interfaccia logica (sub-interface)**: Interfaccia virtuale creata su un'interfaccia fisica, identificata dal numero VLAN.




## 8.2 Tutorial Step-by-Step (Modalità Offline)

Il tutorial guida il giocatore attraverso tutte le principali meccaniche del gioco, simulando localmente le azioni e fornendo feedback immediato. Ogni step è pensato per essere sia una guida testuale sia una sequenza interattiva integrata nella UI.

### Step 1: Inserimento nome giocatore
- All’avvio, il gioco chiede di inserire il proprio nome (max 10 caratteri).
- Il nome viene visualizzato in alto a sinistra sopra i token.

### Step 2: Claim di un router
- Il giocatore seleziona un router non claimato (grigio) e lo “claim-a” con un click sinistro.
- Il router diventa del colore del giocatore e il campo hostname viene impostato secondo la regola `nomegiocatore_hostname`.
- Feedback visivo: messaggio di conferma, cambio colore immediato.

### Step 3: Attivazione/disattivazione interfacce
- Il giocatore può cliccare sulle frecce (interfacce) del router claimato per attivarle (verde) o disattivarle (rosso).
- Ogni azione consuma un token.
- Se non ci sono token disponibili, viene mostrato un messaggio di errore.
- Feedback visivo: la freccia cambia colore in tempo reale.

### Step 4: Visualizzazione hostname e stato
- Passando il mouse sopra un router, viene sempre mostrato il box hostname aggiornato.
- Il box mostra sempre il valore più recente dal polling API (o '?' se non disponibile).

### Step 5: Gestione token e timer
- Il giocatore vede solo i propri token e il timer per la ricarica (+1 token ogni 10s).
- I token degli altri giocatori non sono mai visibili.

### Step 6: Link attivi e neighborship
- Attivando le interfacce di due router adiacenti, può comparire una linea tratteggiata verde tra di essi (neighborship attiva).
- Il tutorial spiega che la neighborship rappresenta una sessione di routing attiva tra i due router.

### Step 7: Condizione di vittoria
- Il tutorial mostra come la vittoria si ottiene quando almeno un router obiettivo ha nella sua tabella di routing tutte le rotte verso le loopback degli altri router obiettivo.
- Viene simulato il raggiungimento della condizione di vittoria e mostrato un messaggio di successo.

### Step 8: Glossario e aiuto
- Il glossario è sempre accessibile tramite pulsante in basso a destra.
- Il tutorial invita il giocatore a consultare i termini tecnici e le regole in qualsiasi momento.

---
