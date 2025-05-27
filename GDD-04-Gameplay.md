# 4. Gameplay

- Il gioco è un gioco collaborativo che permette ai giocatori di interagire con una rete reale tramite un client su PC.
- I giocatori assumono il ruolo di amministratori di rete che devono configurare e gestire una rete di router per raggiungere obiettivi specifici.
- Fino a 4 giocatori, ognuno con il proprio client su PC, interagiscono contemporaneamente e indipendentemente con la stessa infrastruttura di rete reale.
- I router sono rappresentati graficamente su una griglia e mostrano le loro interfacce (nord, sud, est, ovest).
- Ogni giocatore può **claimare** un router, prendendone il controllo e configurandolo tramite il client.
- Ogni router ha un **hostname**. Il campo hostname è sempre nella forma `nomegiocatore_hostname`, dove `nomegiocatore` è il nome del giocatore che ha claimato il router e `hostname` è un identificativo  del router (max 10 caratteri) chiesto al giocatore in fase di claim.
- All’avvio della partita, il gioco chiede al giocatore di inserire il proprio nomegiocatore (max 10 caratteri).
- Quando un giocatore effettua il claim di un router, il campo hostname del router viene impostato nel formato:  
  **nomegiocatore_hostname**  
  Il campo hostname non può superare 10 caratteri.
- Ogni client legge e scrive lo stato di gioco direttamente sui router tramite API.
- Il gioco è realtime: ogni giocatore può agire in qualsiasi momento, effettuando claim di router non ancora assegnati o abilitando/disabilitando le interfacce dei router di cui è proprietario.
- Ogni azione (claim, abilitazione interfaccia) consuma un token; ogni giocatore inizia con 4 token e ne riceve 1 aggiuntivo **ogni 10 secondi** (timer visibile).
- L’attivazione di un’interfaccia può portare due router reali a instaurare una sessione di routing chiamata neighborship; la UI mostra visivamente i link attivi tra router con neighborship attiva.
- Livelli di difficoltà: Facile (4x4), Medio (5x5), Difficile (6x6), Custom (dimensioni scelte dall’utente).
- Modalità tutorial offline per simulazione locale.
- La struttura del gioco e la distribuzione dei token sono pensate per incoraggiare la collaborazione: la rete può essere completata solo se i giocatori dialogano e si coordinano, proprio come in una vera squadra di amministratori di rete.
- La condizione di vittoria viene raggiunta quando almeno uno dei router obiettivo ha la sua tabella di routing configurata correttamente per raggiungere tutte le loopback degli altri router obiettivo del livello.
- Il gioco include un glossario interattivo accessibile in-game per aiutare i giocatori a comprendere i termini tecnici e le meccaniche di gioco.

### 4.1 Flusso tipico del giocatore

1. Inserisce il proprio nomegiocatore all’avvio della partita (max 10 caratteri).
2. Visualizza la griglia dei router e seleziona un router libero per effettuare il claim.
3. Inserisce l’hostname del router (max 10 caratteri) quando richiesto.
4. Gestisce le interfacce del router claimato (attiva/disattiva link, configura la rete).
5. Utilizza i token per compiere azioni (claim, attivazione/disattivazione interfacce), con ricarica automatica ogni 10 secondi.
6. Collabora con gli altri giocatori per raggiungere gli obiettivi di rete del livello.
7. Consulta il glossario o il tutorial in qualsiasi momento per chiarimenti.
8. Raggiunge la condizione di vittoria quando la tabella di routing di almeno un router obiettivo è completa.

### 4.2 Modalità Tutorial Offline

Oltre alla modalità di gioco standard collegata alla rete reale, il gioco offre una **modalità tutorial offline**.  
Questa modalità permette al giocatore di imparare le basi del networking e le meccaniche di gioco senza interagire con dispositivi reali, simulando localmente il comportamento dei router e della rete.

#### Caratteristiche della modalità tutorial
- **Simulazione locale:** Tutto lo stato di gioco (router, link, tabelle di routing) è gestito in locale, senza chiamate API.
- **Step guidati:** Il tutorial guida il giocatore passo-passo attraverso le principali azioni: claim di un router, attivazione/disattivazione interfacce, visualizzazione delle tabelle di routing, raggiungimento della condizione di vittoria.
- **Feedback immediato:** Ogni azione fornisce feedback visivo e testuale per facilitare l’apprendimento.
- **Glossario interattivo:** Il glossario è sempre accessibile sia durante il tutorial che durante la partita, per aiutare i giocatori a comprendere i termini tecnici e le meccaniche di gioco.
- **Possibilità di ripetere gli step:** Il giocatore può ripetere ogni fase del tutorial.
- **Nessun consumo di token:** Nel tutorial non sono previsti limiti di token o timer.

### 4.3 Flusso UI del giocatore

1. All’avvio, il giocatore visualizza lo splashscreen in stile pixel-art 16-bit (logo, titolo, pulsanti "Gioca", "Tutorial", "Glossario"; colori saturi, doppio bordo, outline testo).
2. Selezionando "Gioca", accede alla schermata di inserimento nome (popup pixel-art, doppio bordo, input testuale, palette pastello). Il nome viene visualizzato in alto a sinistra sopra i token, troncato con '...' se troppo lungo.
3. Dopo aver inserito il nome, accede alla schermata principale con la griglia dei router (sprite pixel-art, bordi doppi, ombre a gradini), i token e il timer visibili in alto a sinistra (solo quelli del giocatore locale, box pixel-art). Gli ID router non sono mai visibili in UI.
4. Passando il mouse sui router, questi vengono evidenziati con colore più chiaro (pixel-art, nessun glow/ombra soft). I router liberi sono grigi, quelli claimati dal giocatore sono nel colore player, quelli di altri giocatori sono arancioni. Il bordo giallo spesso 3px evidenzia i router obiettivo. Il box hostname (pixel-art, bordi doppi, testo centrato, outline nero) è sempre visibile sotto ogni router e mostra il valore aggiornato dal polling API (o '?' se non disponibile).
5. Cliccando su un router libero, appare un popup per l’inserimento dell’hostname (box pixel-art, doppio bordo, input testuale). Dopo la conferma, il router cambia colore e mostra il nuovo hostname. Se il router non è claimabile (già claimato o hostname diverso da 'Router'), viene mostrato un messaggio di errore in stile pixel-art.
6. Le interfacce (frecce pixel-art) dei router sono visibili solo se la VLAN è configurata e il router adiacente è presente. Passando il mouse su una freccia, questa si colora di giallo (hover pixel-art, sempre giallo, indipendentemente dallo stato up/down). Le frecce sono verdi se up, rosse se down.
7. Cliccando su una freccia/interfaccia, se il router è claimato dal giocatore, viene attivata/disattivata l’interfaccia (feedback immediato: freccia verde/rossa, token decrementato, messaggio pixel-art). Se non ci sono token disponibili, viene mostrato un messaggio di errore. Se il router non è claimato dal giocatore, viene mostrato un errore.
8. I link attivi tra router con neighborship sono visualizzati come linee tratteggiate verdi, senza sovrapporsi ai cerchi dei router.
9. Ogni azione (claim, attivazione interfaccia) mostra un messaggio di feedback in stile pixel-art (box colorato, testo outline, nessun effetto moderno). Gli errori sono sempre mostrati a schermo con messaggio rosso pixel-art.
10. Il glossario e il tutorial sono sempre accessibili tramite pulsanti in alto o popup pixel-art. Il tutorial è navigabile step-by-step tramite pulsanti Avanti/Indietro e permette di ripetere ogni step. Il testo del tutorial viene automaticamente spezzato su più righe (word wrap) e non esce mai dal box, risultando sempre leggibile e ordinato.
11. La condizione di vittoria viene segnalata con un messaggio/popup pixel-art quando raggiunta.
12. In tutta la UI non è mai presente una legenda: tutte le regole di colori e simboli sono documentate solo nel GDD.

---

## Condizione di Vittoria del Livello

La **condizione di vittoria di un livello** viene raggiunta quando, in almeno uno dei router obiettivo, la sua tabella di routing contiene le rotte verso le loopback di **tutti** i router obiettivo.

### Definizione di router obiettivo

I **router obiettivo** sono quelli identificati dalle coppie (groupID, localID) specificate per il livello.  
Esempio:  
- (1,1)  
- (4,1)

### Indirizzamento delle loopback

L'indirizzo IP della loopback per ogni router obiettivo segue la convenzione:
```
G.0.0.L
```
dove:
- **G** = groupID del router
- **L** = localID del router

Esempi:
- Router obiettivo (1,1): loopback 1.0.0.1
- Router obiettivo (4,1): loopback 4.0.0.1

### Regola di vittoria

La vittoria si ottiene quando, **in almeno uno dei router obiettivo**, nella sua tabella di routing sono presenti tutte le rotte verso le loopback degli altri router obiettivo del livello (inclusa la propria).  
In altre parole, la tabella deve contenere tutte le destinazioni del tipo G.0.0.L dove (G,L) sono le coppie dei router obiettivo.

### Nota
- Il controllo della vittoria avviene periodicamente (sincronizzato con il polling delle API).
- La verifica può essere visualizzata nella UI tramite un indicatore di progresso o stato.


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
