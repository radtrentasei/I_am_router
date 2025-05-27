## 4. Gameplay e Funzionalità Principali

- Il gioco è un gioco collaborativo che permette ai giocatori di interagire con una rete reale tramite un client su PC.
- I giocatori assumono il ruolo di amministratori di rete che devono configurare e gestire una rete di router per raggiungere obiettivi specifici.
- Fino a 4 giocatori, ognuno con il proprio client su PC, interagiscono contemporaneamente e indipendentemente con la stessa infrastruttura di rete reale.
- Ogni giocatore può **claimare** un router, prendendone il controllo e configurandolo tramite il client.
- I router sono rappresentati graficamente su una griglia e mostrano le loro interfacce (nord, sud, est, ovest).
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


### 4.1 Modalità Tutorial Offline

Oltre alla modalità di gioco standard collegata alla rete reale, il gioco offre una **modalità tutorial offline**.  
Questa modalità permette al giocatore di imparare le basi del networking e le meccaniche di gioco senza interagire con dispositivi reali, simulando localmente il comportamento dei router e della rete.

#### Caratteristiche della modalità tutorial
- **Simulazione locale:** Tutto lo stato di gioco (router, link, tabelle di routing) è gestito in locale, senza chiamate API.
- **Step guidati:** Il tutorial guida il giocatore passo-passo attraverso le principali azioni: claim di un router, attivazione/disattivazione interfacce, visualizzazione delle tabelle di routing, raggiungimento della condizione di vittoria.
- **Feedback immediato:** Ogni azione fornisce feedback visivo e testuale per facilitare l’apprendimento.
- **Glossario interattivo:** Il glossario è sempre accessibile sia durante il tutorial che durante la partita, per aiutare i giocatori a comprendere i termini tecnici e le meccaniche di gioco.
- **Possibilità di ripetere gli step:** Il giocatore può ripetere ogni fase del tutorial.
- **Nessun consumo di token:** Nel tutorial non sono previsti limiti di token o timer.

---
