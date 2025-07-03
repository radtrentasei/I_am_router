# GDD-02-Gameplay

## 1. Meccaniche di Gioco

### 1.1 Descrizione Generale
- Il gioco è un gioco collaborativo che permette ai giocatori di interagire con una rete reale tramite un client su PC.
- I giocatori assumono il ruolo di amministratori di rete che devono configurare e gestire una rete di router per raggiungere obiettivi specifici.
- Fino a 4 giocatori, ognuno con il proprio client su PC, interagiscono contemporaneamente e indipendentemente con la stessa infrastruttura di rete reale.

### 1.2 Elementi di Gioco Fondamentali
- I router sono rappresentati graficamente su una griglia e mostrano le loro interfacce (nord, sud, est, ovest).
- Ogni giocatore può **claimare** un router, prendendone il controllo e configurandolo tramite il client.
- Ogni router ha un **hostname**. Il campo hostname è sempre nella forma `nomegiocatore_hostname`, dove `nomegiocatore` è il nome del giocatore che ha claimato il router e `hostname` è un identificativo del router (max 10 caratteri) chiesto al giocatore in fase di claim.
- All'avvio della partita, il gioco chiede al giocatore di inserire il proprio nomegiocatore (max 10 caratteri).

### 1.3 Meccaniche Tempo Reale
- Ogni client legge e scrive lo stato di gioco direttamente sui router tramite API.
- Il gioco è realtime: ogni giocatore può agire in qualsiasi momento, effettuando claim di router non ancora assegnati o abilitando/disabilitando le interfacce dei router di cui è proprietario.
- L'attivazione di un'interfaccia può portare due router reali a instaurare una sessione di routing chiamata neighborship; la UI mostra visivamente i link attivi tra router con neighborship attiva.

### 1.4 Livelli di Difficoltà
- **Facile**: Griglia 4x4
- **Medio**: Griglia 5x5
- **Difficile**: Griglia 6x6
- **Estremo**: Griglia 8x8 (con UI adattiva per leggibilità)
- **Custom**: Dimensione personalizzabile da 2x2 a 8x8

## 2. Sistema di Token e Azioni

### 2.1 Regole dei Token
- Ogni azione (claim router o abilitazione/disabilitazione interfaccia) consuma un token
- Ogni giocatore inizia con 4 token
- **Ogni 10 secondi viene ricaricato 1 token a ogni giocatore**
- Il numero massimo di token accumulabili è 4
- Se il giocatore ha già 4 token, il timer di ricarica si ferma fino a quando non viene consumato almeno un token

### 2.2 Limitazioni delle Azioni
- Solo una interfaccia abilitabile/disabilitabile per azione e solo su router propri
- Tastiera solo per inserire hostname e nome giocatore
- Tutte le altre interazioni avvengono tramite mouse
- Non sono previsti shortcut da tastiera per azioni di gioco

### 2.3 Regole di Claim
Un router può essere claimato **solo** se:
1. `claimed_by is None` (nessun giocatore lo ha già claimato)
2. `hostname == 'Router'` (il router è ancora nello stato iniziale)

Se una di queste condizioni non è soddisfatta, viene mostrato un messaggio di errore: "Claim possibile solo su router liberi (hostname 'Router')!".

## 3. Flusso di Gioco

### 3.1 Flusso Tipico del Giocatore
1. Inserisce il proprio nomegiocatore all'avvio della partita (max 10 caratteri)
2. Visualizza la griglia dei router e seleziona un router libero per effettuare il claim
3. Inserisce l'hostname del router (max 10 caratteri) quando richiesto
4. Gestisce le interfacce del router claimato (attiva/disattiva link, configura la rete)
5. Utilizza i token per compiere azioni con ricarica automatica ogni 10 secondi
6. Collabora con gli altri giocatori per raggiungere gli obiettivi di rete del livello
7. Consulta il glossario o il tutorial in qualsiasi momento per chiarimenti
8. Raggiunge la condizione di vittoria quando la tabella di routing è completa

### 3.2 Flusso UI del Giocatore
1. **Avvio**: Splashscreen pixel-art con pulsanti "Gioca", "Tutorial", "Glossario"
2. **Inserimento Nome**: Popup per inserire nome giocatore (max 10 caratteri)
3. **Schermata Principale**: Griglia router con token/timer visibili in alto a sinistra
4. **Interazione Router**: Hover per evidenziare, click per claimare router liberi
5. **Gestione Interfacce**: Click su frecce per attivare/disattivare interfacce
6. **Feedback Visivo**: Messaggi immediati per ogni azione (claim, errori, cambi stato)
7. **Accesso Strumenti**: Glossario e tutorial sempre accessibili
8. **Vittoria**: Messaggio/popup pixel-art quando raggiunta la condizione

## 4. Condizioni di Vittoria

### 4.1 Definizione di Router Obiettivo
I **router obiettivo** sono identificati dalle coppie (groupID, localID) specificate per il livello.

### 4.2 Indirizzamento delle Loopback
L'indirizzo IP della loopback per ogni router obiettivo segue la convenzione:
```
G.0.0.L
```
dove:
- **G** = groupID del router
- **L** = localID del router

### 4.3 Regola di Vittoria
La vittoria si ottiene quando, **in almeno uno dei router obiettivo**, nella sua tabella di routing sono presenti tutte le rotte verso le loopback degli altri router obiettivo del livello (inclusa la propria).

Il controllo della vittoria avviene periodicamente, sincronizzato con il polling delle API.

## 5. Modalità Tutorial Offline

### 5.1 Caratteristiche Generali
- **Simulazione locale**: Tutto lo stato di gioco è gestito localmente, senza chiamate API
- **Step guidati**: Tutorial passo-passo attraverso le principali azioni
- **Feedback immediato**: Ogni azione fornisce feedback visivo e testuale
- **Nessun consumo di token**: Nel tutorial non ci sono limiti di token o timer
- **Ripetibilità**: Il giocatore può ripetere ogni fase del tutorial

### 5.2 Tutorial Step-by-Step

#### Step 1: Inserimento Nome Giocatore
- All'avvio, il gioco chiede di inserire il proprio nome (max 10 caratteri)
- Il nome viene visualizzato in alto a sinistra sopra i token

#### Step 2: Claim di un Router
- Il giocatore seleziona un router non claimato (grigio) e lo "claim-a"
- Il router diventa del colore del giocatore con hostname `nomegiocatore_hostname`
- Feedback visivo: messaggio di conferma, cambio colore immediato

#### Step 3: Attivazione/Disattivazione Interfacce
- Click sulle frecce del router claimato per attivarle (verde) o disattivarle (rosso)
- Feedback visivo: la freccia cambia colore in tempo reale

#### Step 4: Visualizzazione Hostname e Stato
- Passando il mouse sopra un router, mostra il box hostname aggiornato
- Il box mostra il valore più recente (o '?' se non disponibile)

#### Step 5: Gestione Token e Timer
- Il giocatore vede solo i propri token e il timer per la ricarica
- Spiegazione del sistema di ricarica automatica

#### Step 6: Link Attivi e Neighborship
- Attivando interfacce di router adiacenti, può apparire una linea tratteggiata verde
- Spiegazione della neighborship come sessione di routing attiva

#### Step 7: Condizione di Vittoria
- Simulazione del raggiungimento della condizione di vittoria
- Spiegazione della tabella di routing e degli obiettivi

#### Step 8: Glossario e Aiuto
- Il glossario è sempre accessibile
- Invito a consultare i termini tecnici in qualsiasi momento

---
