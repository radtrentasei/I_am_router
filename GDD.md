# Game Design Document (GDD)  
## 1. Titolo: I am a Router

---

## 2. Visione Generale

"I am a Router" è un gioco educativo multiplayer che introduce i concetti fondamentali del networking attraverso il coinvolgimento diretto su una vera infrastruttura di rete. Il gioco è pensato per ragazzi tra i 12 e i 15 anni, studenti avanzati e professionisti IT, offrendo un'esperienza interattiva in cui le azioni dei giocatori hanno effetto reale sui dispositivi di rete. Il client comunica direttamente con i router tramite API, sfruttando parametri configurabili come la descrizione delle interfacce loopback per memorizzare e condividere lo stato di gioco tra tutti i partecipanti. È disponibile anche una modalità tutorial offline per simulare l’esperienza senza una rete reale.

**Il gioco è un’esperienza 2D, a schermo intero, con grafica in stile retro gaming/pixel-art e palette di colori pastello.**

Uno degli obiettivi centrali del gioco è favorire la collaborazione tra i giocatori, che dovranno coordinarsi e pianificare insieme le attivazioni di link e la configurazione della rete, replicando le dinamiche cooperative tipiche delle reti informatiche reali.

---

## 3. Target e Obiettivi

- Ragazzi tra i 12 e i 15 anni interessati a tecnologia e informatica
- Studenti avanzati di networking
- Professionisti del networking
- Piattaforma: PC
- Obiettivi:
  - Introdurre i principi base del networking
  - Dimostrare la programmabilità delle reti
  - Offrire un'esperienza educativa collegata a dispositivi reali
  - Favorire la collaborazione tra i giocatori, simulando le dinamiche reali di cooperazione e troubleshooting presenti nelle reti informatiche.

---

## 4. Gameplay e Funzionalità Principali

- All’avvio della partita, il gioco chiede al giocatore di inserire il proprio nome (max 10 caratteri).
- Quando un giocatore effettua il claim di un router, il campo hostname del router viene impostato nel formato:  
  **nomegiocatore_hostname**  
  Il campo hostname non può superare 10 caratteri.
- Fino a 4 giocatori, ognuno con il proprio client su PC, interagiscono contemporaneamente e indipendentemente con la stessa infrastruttura di rete reale.
- Ogni client legge e scrive lo stato di gioco direttamente sui router tramite API.
- Il gioco è realtime: ogni giocatore può agire in qualsiasi momento, effettuando claim di router non ancora assegnati o abilitando/disabilitando le interfacce dei router di cui è proprietario.
- Ogni azione consuma un token; ogni giocatore inizia con 4 token e ne riceve 1 aggiuntivo **ogni 10 secondi** (timer visibile).
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

## 5. Regole e Parametri

- Ogni azione (claim o abilitazione/disabilitazione interfaccia) consuma un token.
- Ogni giocatore inizia con 4 token.
- **Ogni 10 secondi viene ricaricato 1 token a ogni giocatore.**
- Solo una interfaccia abilitabile/disabilitabile per azione e solo su router propri.
- Mouse/tastiera solo per hostname.
- Stato sempre aggiornato dai dispositivi reali.
- Nome giocatore massimo 10 caratteri.
- Hostname massimo 10 caratteri (inclusi eventuali separatori e nomegiocatore).
- Tutte le interazioni di gioco avvengono tramite mouse: il giocatore può selezionare router, claimare, attivare/disattivare interfacce, aprire popup info, glossario e tutorial solo tramite click o tap.
- L'unico uso della tastiera è per l'inserimento del nome giocatore e dell'hostname quando richiesto (popup di input testuale).
- Non sono previsti shortcut da tastiera per azioni di gioco (claim, attiva interfaccia, info, glossario, tutorial, ecc.): tutte queste azioni sono accessibili solo tramite pulsanti o click nella UI.
- La UI mostra sempre pulsanti o icone cliccabili per ogni azione disponibile.

---

## 6. UI & Grafica

- **Gioco 2D, schermo intero, stile retro gaming pixel-art**
- **Palette colori:** Pastello (esempi: azzurro chiaro, rosa, lilla, verde menta, giallo pallido)
- UI adattiva, leggibile, centrata, senza overflow
- Visualizzazione dello stato in tempo reale tramite letture dai dispositivi
- Stato token, timer, azioni disponibili e stato dei router sempre visibili e aggiornati dinamicamente
- Visualizzazione grafica dei link attivi tra router con neighborship di routing attiva
- Hostname router sempre visibile
- ID router solo a terminale per debug
- Glossario accessibile dal menu e in-game
- **Un router di cui non è stato fatto il claim viene visualizzato di colore grigio nella UI.**

### 6.1 Dettaglio: Regole di disegno di un router nella UI

Ogni router nella UI viene rappresentato secondo queste regole grafiche:

- **Forma base:**
  - Cerchio pieno, dimensione adattiva in base alla griglia e alla risoluzione.
  - Colore:
    - Grigio (libero, non claimato; ovvero nessun giocatore ha ancora effettuato il claim sul router)
    - Blu (claimato da un giocatore, colore del giocatore)
    - Bordo giallo spesso 3 pixel se router obiettivo già claimato
- **Interfacce:**
  - Quattro frecce spesse (5px) orientate verso nord, sud, est, ovest, sempre visibili.
  - Le frecce sono disegnate **all'interno** del cerchio del router, puntando dal bordo verso il centro.
  - Colore frecce:
    - Verde (interfaccia up)
    - Rosso (interfaccia down)
    - Giallo (interfaccia non configurata)
  - Quando il mouse passa sopra una freccia, questa viene evidenziata in giallo.
  - Le frecce sono disegnate in modo da non sovrapporsi al cerchio del router.
- **Link attivi:**
  - Linee tratteggiate tra i router con neighborship attiva, colore verde.
  - Le linee sono disegnate in modo da non sovrapporsi al cerchio del router.
  - Le linee sono bidirezionali e mostrano lo stato attivo della connessione.
- **Router obiettivo:**
  - Se il router è un obiettivo del livello, il suo bordo è evidenziato in giallo spesso 3 pixel.
  - Il colore del bordo giallo non cambia in base al claim del router.
- **Stato del router:**
  - Se il router è claimato, il suo colore di sfondo è quello del giocatore che lo ha claimato.
  - Se il router non è claimato, il colore di sfondo è grigio.
- **Stato delle interfacce:**
  - Le frecce delle interfacce sono sempre visibili, ma il loro colore cambia in base allo stato:
    - Verde se l'interfaccia è attiva (up, cioè 'admin up' secondo lo stato appreso dalla chiamata API ricorrente)
    - Rosso se l'interfaccia è inattiva (down, cioè 'admin down' secondo lo stato appreso dalla chiamata API ricorrente)
- **Hostname:**
  - Box rettangolare adattivo sempre visibile sotto ogni router, con bordo bianco e sfondo scuro.
  - Testo hostname sempre centrato e mai troncato.
  - Il box mostra sempre il valore aggiornato dal polling API, oppure '?' se non disponibile, senza ritardi o desincronizzazioni.
- **Feedback visivo:**
  - Quando un router viene claimato, il colore del cerchio cambia immediatamente e viene mostrato un messaggio di conferma.
  - Quando un’interfaccia viene attivata/disattivata, il colore della freccia cambia in tempo reale.
- **Hover e click:**
  - Al passaggio del mouse su un router, il suo colore di sfondo diventa leggermente più chiaro per indicare che è selezionato.
  - Al click su un router:
    - Se il router non è claimato, viene avviata la procedura di claim.
    - Se il router è già claimato dal giocatore locale, il click non mostra più la finestra informativa (popup) ma non fa nulla (o in futuro potrà attivare altre azioni contestuali).
- **ID router:**
  - Gli ID (global_id, local_id, group_id) non sono visibili nella UI, ma vengono stampati a terminale per debug quando si seleziona il router.
- **Posizionamento:**
  - Il router è centrato nella cella della griglia, con padding per evitare sovrapposizioni.
- **Legenda:**
  - In basso nella UI è sempre presente una legenda che spiega i colori e i simboli.
  - La legenda mostra solo:
    - Grigio: router non claimato
    - Colore player: router claimato dal giocatore locale
  - Non sono più presenti riferimenti o colori relativi ad altri giocatori.

#### Aggiornamenti e miglioramenti UI (storico changelog integrato)

- La visualizzazione dell'hostname nella UI è sempre aggiornata in tempo reale grazie alla chiamata continua di update_from_api().
- Il box hostname sotto il router mostra sempre il valore aggiornato o '?' se non disponibile, senza ritardi o desincronizzazioni.
- La UI mostra solo il numero di token e il timer del giocatore locale. I token degli altri giocatori non sono mai visualizzati.
- Ogni giocatore vede e gestisce solo i propri token nella UI. I token degli altri giocatori non sono più visibili o mostrati.
- La barra superiore visualizza solo i token e il timer del giocatore corrente.
- Un router è considerato claimato dal giocatore locale solo se il campo description della sua interfaccia loopback è nel formato `nomegiocatore_hostnameRouterVirtuale` e il `nomegiocatore` coincide esattamente con quello inserito dal giocatore locale. Se il nomegiocatore nella description è diverso dal nome inserito dal giocatore locale, il router è considerato sempre non claimato (colore grigio nella UI, azioni non permesse).
- Il claim non è più gestito solo localmente, ma sincronizzato tramite la description della loopback letta via API.
- La colorazione e lo stato claim dei router sono determinati dal confronto tra il nomegiocatore locale e quello letto dalla description della loopback.
- Un router con description valorizzata ma nomegiocatore diverso da quello locale appare sempre come non claimato (grigio) e non può essere gestito dal giocatore locale.
- La logica di claim di un router si basa ora sul parsing del campo description della loopback: se il nomegiocatore letto coincide con quello locale, il router risulta claimato dal giocatore. Altrimenti, è sempre considerato libero per il client locale.
- La logica di estrazione hostname è robusta rispetto a dati assenti o vuoti nelle risposte API: il client imposta sempre l'hostname a '?' se l'interfaccia Loopback{group_id} non è presente o il campo description è vuoto.
- L'hostname viene aggiornato solo se il campo description è presente e non vuoto.
- Il nome del giocatore locale viene visualizzato nella UI sopra i token, in alto a sinistra, e viene troncato con '...' se troppo lungo per lo spazio disponibile.

---

## 7. Dettaglio: Sistema di ID dei Router

### Tipologie di ID
- **ID globale (global_id):**
  - Ogni router riceve un ID progressivo unico da 1 a N*N, assegnato riga per riga nella griglia.
  - Serve per identificare in modo univoco ogni router nella rete e per debug.
  - il global_id ha scarso valore pratico per il gioco.
- **ID locale (local_id):**
  - All’interno di ogni gruppo 2x2 di router, ogni router riceve un local_id da 1 a 4 secondo uno schema a scacchiera (1,2,3,4).
  - Utilizzato per la corrispondenza con la numerazione delle interfacce e per le chiamate API.
  - Il local_id rappresenta l'identificativo del router reale.
- **ID gruppo (group_id):**
  - Ogni gruppo 2x2 di router riceve un group_id progressivo.
  - Serve per identificare i router che fanno parte dello stesso gruppo logico (ad esempio per le chiamate API alle LoopbackX).
  - Il group_id rappresenta la vrf (Virtual Routing and Forwarding) del router reale.

### Regole di visualizzazione e utilizzo
- Gli ID (global_id, local_id, group_id) **non sono visibili nella UI** accanto ai router durante il gioco normale.
- Quando si clicca su un router, i suoi ID vengono stampati a terminale per scopi di debug e sviluppo.
- In modalità API, gli ID sono utilizzati per:
  - Costruire l’indirizzo IP/hostname per la chiamata RESTCONF (es: https://198.18.1.1X dove X è il local_id).
  - Identificare l’interfaccia LoopbackX (dove X è il group_id) per recuperare l’hostname dinamico tramite API.
- In modalità tutorial, gli ID sono usati solo internamente e non sono mai mostrati all’utente.

### Assegnazione degli ID (algoritmo)
- All’avvio della partita, dopo la creazione della griglia, viene eseguita l’assegnazione:
  - global_id: progressivo da 1 a N*N, riga per riga.
  - group_id: assegnato a blocchi 2x2 a scacchiera, non per riga. Ogni blocco 2x2 di router adiacenti condivide lo stesso group_id, che viene incrementato da sinistra a destra e dall'alto verso il basso.
  - local_id: da 1 a 4 all’interno di ogni blocco 2x2 secondo uno schema a scacchiera (1,2,3,4).

### Esempio pratico
- In una griglia 4x4:
  - global_id: 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16
  - group_id:
    1 1 2 2
    1 1 2 2
    3 3 4 4
    3 3 4 4
  - local_id: 1,2,3,4 in ogni blocco 2x2

- La funzione generate_ids in utils.py implementa questa logica.

### Debug e sviluppo
- Per facilitare il debug, ogni volta che si seleziona un router, i suoi ID vengono stampati a terminale.
- Questo aiuta a verificare la corretta corrispondenza tra UI, logica di gioco e chiamate API.

---

## 8. Motore API del Gioco
### Comportamento delle API
Il client del gioco interagisce con i router reali tramite API RESTCONF, utilizzando le seguenti regole e logiche:
### Comportamento delle API
- **Chiamate API periodiche:**  
  Le chiamate API verso i router reali NON vengono attivate dal passaggio del mouse, ma vengono effettuate periodicamente dal client sin dall'inizio della partita (es. ogni 3 secondi).
- **Memorizzazione locale:**  
  Tutte le informazioni rilevanti recuperate dalle API (hostname, stato delle interfacce, stato delle neighborship) vengono memorizzate localmente dal client.
- **Comportamento UI al passaggio del mouse:**  
  Quando il mouse passa sopra un router, viene visualizzato l’hostname che è già stato recuperato dal ciclo periodico di query API.  
  Non viene effettuata alcuna chiamata API al momento dell’interazione dell’utente.
- **Aggiornamento informazioni:**  
  Le informazioni mostrate in UI sono aggiornate periodicamente in base alla frequenza delle chiamate API di polling.  
  In caso di perdita temporanea di connessione o errore nelle API, le informazioni rimangono quelle dell’ultimo ciclo di polling riuscito.
- **API asincrone:**  
  Le chiamate API sono asincrone e non bloccano l'interfaccia utente.  
  Il client continua a funzionare normalmente anche se una chiamata API fallisce o impiega più tempo del previsto.

### Logica di recupero hostname
- **Obiettivo:**  
  Recuperare l'hostname configurato sul router reale per visualizzarlo nella UI.
- **Interfaccia Loopback:**
  - Ogni router ha un'interfaccia loopback configurata con un nome specifico: `LoopbackY`, dove `Y` è il `group_id` del router.
  - Questa interfaccia viene utilizzata per identificare il router e recuperare l'hostname.
### Chiamata API per hostname
- **Endpoint RESTCONF:**
  - URL: `https://198.18.1.1X/restconf/data/ietf-interfaces:interfaces` dove `X` è il `local_id` del router selezionato.
  - Autenticazione: Basic Auth (username: `cisco`, password: `C1sco12345`).
  - Content-Type: `application/yang-data+json`
- **Logica di ricerca hostname:**
  - Viene cercata l'interfaccia `LoopbackY` dove `Y` è il `group_id` del router.
  - Il campo `description` di questa interfaccia viene utilizzato come hostname da mostrare nella UI.
- **Esempio di chiamata:**
  - Per un router con `local_id=3` e `group_id=2`:
    - URL: `https://198.18.1.13/restconf/data/ietf-interfaces:interfaces`
    - Si cerca l'interfaccia `Loopback2` e si legge il campo `description`.
- **Fallback:**
  - Se la chiamata fallisce o l'interfaccia non è presente, viene mostrato un hostname di default (`?`) oppure l'ultimo valore di hostname disponibile.

Questa logica consente di visualizzare in tempo reale l'hostname configurato realmente sul router (in base all’ultimo polling riuscito), favorendo apprendimento e troubleshooting.

### Logica di settaggio hostname
- **Obiettivo:**  
  Permettere ai giocatori di impostare l'hostname del router reale tramite l'interfaccia loopback.
- **Interfaccia Loopback:**
  - Ogni router ha un'interfaccia loopback configurata con un nome specifico: `LoopbackY`, dove `Y` è il `group_id` del router.
  - Questa interfaccia viene utilizzata per identificare il router e impostare l'hostname.
### Chiamata API per impostare hostname
- **Endpoint RESTCONF:**
  - URL: `https://198.18.1.1X/restconf/data/ietf-interfaces:interfaces/interface=LoopbackY`
  - Autenticazione: Basic Auth (username: `cisco`, password: `C1sco12345`).
  - Content-Type: `application/yang-data+json`
  - metodo: 'PUT'
- **Payload:**
    - Il payload deve contenere il campo `description` con il nuovo hostname.
    - Esempio di payload:
        ```json
            {
            "interface": [
                {
                "name": "Loopback1",
                "type": "iana-if-type:softwareLoopback",
                "description": "nomegiocatore_hostname"
                }
            ]
            }
        ```
- **Esempio di chiamata:**
  - Per un router con `local_id=3` e `group_id=2`, per impostare l'hostname a `Alice_Router`:
    - URL: `https://198.18.1.13/restconf/data/ietf-interfaces:interfaces/interface=Loopback2`
- **Esecuzione:**
  - Quando un giocatore effettua il claim di un router, il client invia questa chiamata API per impostare l'hostname.
  - Se la chiamata ha successo, l'hostname viene aggiornato. Non avviene nessuna memorizzazione locale dell'hostname.

### 8.1 Ottenimento della tabella di routing di un router (modalità API)

Per ottenere la tabella di routing di un router reale, il client deve effettuare la seguente chiamata API RESTCONF:

```
restconf/data/ietf-routing:routing-state/routing-instance
```

Questa chiamata restituisce lo stato di routing, inclusa la tabella di routing attuale del router.

> **Nota:** In futuro verranno aggiunti esempi pratici di risposta dell’API e di parsing delle rotte rilevanti.

---

## 9. Dettaglio: Collegamento Fisico e Logico dei Router (VLAN e link tra router)

### Collegamento fisico
- Ogni router reale è fisicamente connesso alla rete tramite la sua interfaccia **GigabitEthernet1**.

### Collegamento logico tramite VLAN
- Tutti i link tra router (ovvero le interfacce nord, sud, est, ovest nel gioco) sono realizzati tramite **interfacce logiche VLAN** (sub-interface) sulla stessa GigabitEthernet1.
- **Ciascun link tra due router** all’interno di un gruppo 2x2 è rappresentato da una VLAN univoca.

  - **Regola generale**:  
    Il numero VLAN è creato concatenando **group_id** + **local_id_A** + **local_id_B**, dove A e B sono i due router collegati.  
    L’ordine non conta, il link è bidirezionale.
    **local_id_A** è sempre inferiore a  **local_id_B**

  - **Esempi**:  
    - _VLAN 312_ rappresenta il link nel gruppo 3 tra router 1 e router 2 (e viceversa, il link è bidirezionale).
    - _VLAN 434_ rappresenta nel gruppo 4 il link tra router 3 e router 4 (e viceversa).

#### Mappatura e gestione dei link
- Ogni interfaccia logica di collegamento (n/s/e/w nel gioco) corrisponde a una sub-interface configurata su GigabitEthernet1, con il numero VLAN che rappresenta univocamente il link tra i due router del gruppo.
- Il link è **bidirezionale** e il numero VLAN è lo stesso su entrambi i router coinvolti.
- Quando un link viene “attivato” o “disattivato” nel gioco, la relativa sub-interface (es: `GigabitEthernet1.312`) viene abilitata/disabilitata via API.
- La UI riflette lo stato up/down della VLAN (interfaccia logica/link) con le frecce verdi/rosse.
- L’identificativo VLAN può essere mostrato a scopo didattico nel glossario o in una schermata avanzata/debug.

**Stato neighborship di routing:**  
Se una neighborship di routing è attiva su un link, il campo `description` della relativa sub-interface sarà impostato a `UP`.  
Se il campo `description` della sub-interface è vuoto, significa che non esiste nessuna neighborship attiva su quel link.
Se tra due router esiste una neighborship attiva, la UI mostra una linea tratteggiata verde tra i due router, indicando che il link è attivo e funzionante.

#### Schema esempio

```
Gruppo 3 (group_id = 3):

Routers:
- Router 1 (local_id=1)
- Router 2 (local_id=2)
- Router 3 (local_id=3)
- Router 4 (local_id=4)

Link tra Router 1 e Router 2: VLAN 312 (GigabitEthernet1.312 su entrambi)
Link tra Router 3 e Router 4: VLAN 334 (GigabitEthernet1.334 su entrambi)
Link tra Router 2 e Router 3: VLAN 323 (GigabitEthernet1.323 su entrambi)
...
```


---

## 10. Integrazione con la Rete Reale e Mockup

- Tutto lo stato di gioco è scritto/letto sui dispositivi reali via API.
- Parametri come hostname, stato delle interfacce e neighborship sono aggiornati in tempo reale.
- Le API sono utilizzate per leggere lo stato attuale della rete e per scrivere le modifiche apportate dai giocatori.
- In modalità offline, lo stato è simulato localmente.


---

## 11. Prototipo e Mockup

- Prototipazione con Figma/Excalidraw per griglia, feedback, ecc.



---

## 12. Audio

- Chiptune, SFX
- Musica di sottofondo in stile retro gaming
- Effetti sonori per azioni chiave (claim, attivazione link, errore, successo)
- Feedback audio per azioni di gioco (es. click, attivazione/disattivazione link)
- Effetti sonori per eventi di gioco (es. attivazione di un link, errore, successo)
- Volume regolabile tramite menu opzioni
- Opzioni per disattivare la musica o gli effetti sonori

---


## 13. Requisiti di Stile e Qualità del Codice

- Codice abbondantemente commentato: ogni funzione, classe, modulo e blocco logico deve essere documentato tramite commenti e docstring, per facilitare la comprensione e l’apprendimento.
- Codice pensato come materiale didattico: ogni concetto implementato, pattern o soluzione deve essere spiegato.
- Soluzioni semplici, leggibili e lineari preferite a quelle complesse, salvo necessità tecniche documentate.
- Best practice Python (PEP8), nomi chiari, separazione in moduli, attenzione alla manutenibilità.
- Dove utile, aggiungere esempi d’uso nei commenti/docstring.
- Logica di estrazione hostname robusta rispetto a dati assenti o vuoti nelle risposte API.

---

## 14. Glossario Interattivo in Game

Sezione accessibile dal menu e durante la partita dove il giocatore può consultare i principali concetti di networking:

- **Rete**: Insieme di dispositivi (computer, router, server) collegati tra loro per scambiarsi dati.
- **Router**: Dispositivo che indirizza i pacchetti di dati tra reti diverse.
- **Interfaccia**: Punto di connessione fisica o logica su un router (nord, sud, est, ovest nel gioco).
- **Interfaccia logica (sub-interface)**: Interfaccia virtuale creata su un'interfaccia fisica, identificata dal numero VLAN.
- **VLAN**: Rete virtuale che identifica univocamente un link tra due router reali.
- **Link**: Collegamento tra due dispositivi di rete che permette il passaggio delle informazioni.
- **Neighborship**: Relazione di vicinato tra due router che hanno instaurato una sessione di routing attiva.
- **Disservizio**: Situazione in cui una parte della rete o un link smette di funzionare correttamente.
- **Pacchetto**: Unità di dati che viaggia nella rete.
- **Routing**: Processo con cui un router decide il percorso migliore per un pacchetto.
- **API**: Interfaccia di programmazione delle applicazioni che permette al client di interagire con i router.

---

## 15. Condizione di Vittoria del Livello

La **condizione di vittoria di un livello** viene raggiunta quando, in almeno uno dei router obiettivo, la sua tabella di routing contiene le rotte verso le loopback di **tutti** i router obiettivo.

### Definizione di router obiettivo

I **router obiettivo** sono quelli identificati dalle coppie (groupID, localID) specificate per il livello.  
Esempio:  
- (1,1)  
- (4,1)

### Indirizzamento delle loopback

L’indirizzo IP della loopback per ogni router obiettivo segue la convenzione:
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
In altre parole, la tabella deve contenere tutte le destinazioni del tipo G.0.0. L dove (G,L) sono le coppie dei router obiettivo.

### Nota
- Il controllo della vittoria avviene periodicamente (sincronizzato con il polling delle API).
- La verifica può essere visualizzata nella UI tramite un indicatore di progresso o stato.

---

## 16. Ottenimento della tabella di routing di un router (modalità API)

Per ottenere la tabella di routing di un router reale, il client deve effettuare la seguente chiamata API RESTCONF:

```
restconf/data/ietf-routing:routing-state/routing-instance
```

Questa chiamata restituisce lo stato di routing, inclusa la tabella di routing attuale del router.

> **Nota:** In futuro verranno aggiunti esempi pratici di risposta dell’API e di parsing delle rotte rilevanti.

---

**Nota Bene:**  
Mockup grafici consigliati per la presentazione ufficiale.

---

## Specifiche tecniche

- **Linguaggio:** Python 3.x
- **Libreria grafica:** Pygame (ultima versione stabile)
- **Struttura modulare:** Il codice deve essere suddiviso in moduli separati per logica di gioco, gestione API, rendering UI, gestione eventi, glossario/tutorial, e configurazione.
- **Compatibilità:** Il gioco deve funzionare su Windows, macOS e Linux senza modifiche sostanziali.
- **Gestione dipendenze:** Fornire un file `requirements.txt` con tutte le dipendenze necessarie (incluso Pygame e librerie per richieste HTTP come `requests`).
- **API RESTCONF:** Tutte le chiamate API devono essere indirizzate esclusivamente ai 4 router fisici reali, utilizzando la logica di VRF per virtualizzare la griglia NxN.
- **Debug API:** Ogni chiamata API (claim, interfaccia, hostname, stato) deve essere stampata a terminale in modo conciso: solo metodo, endpoint, status code e, in caso di errore, il messaggio di errore.
- **Interazione:** Tutte le azioni di gioco sono accessibili solo tramite mouse (eccetto input nome/hostname tramite tastiera).
- **Polling API:** Le chiamate API di polling verso i router reali devono essere eseguite periodicamente in loop asincrono, senza bloccare la UI.
- **Documentazione:** Tutto il codice deve essere abbondantemente commentato e documentato secondo le best practice Python (PEP8, docstring, esempi d’uso dove utile).
- **Mockup:** La UI deve essere fedele ai mockup grafici allegati o descritti nel GDD.
- **Glossario e tutorial:** Devono essere integrati e accessibili in-game tramite pulsanti o menu.
- **Debug terminale:** Oltre alle API, anche la selezione di router/interfacce deve stampare a terminale gli ID e lo stato per facilitare il debug.
- **Architettura:** Prevedere una chiara separazione tra logica di gioco, interfaccia utente e gestione delle API.

---

## Regole per Copilot e AI Assistant

1. **Rispetta il GDD:** Tutte le implementazioni e suggerimenti devono essere coerenti con le specifiche e le regole descritte nel GDD.
2. **Mouse-driven:** Tutte le azioni di gioco (claim, attivazione/disattivazione interfacce, info, glossario, tutorial) devono essere accessibili solo tramite mouse, eccetto l’inserimento di nome/hostname che avviene tramite tastiera.
3. **Debug API:** Ogni chiamata API (claim, interfaccia, hostname, stato) deve essere stampata a terminale in modo conciso: solo metodo, endpoint, status code e, in caso di errore, il messaggio di errore.
4. **API RESTCONF:** Tutte le chiamate API devono essere indirizzate solo ai 4 router fisici reali, utilizzando la logica di VRF per virtualizzare la griglia NxN.
5. **Polling asincrono:** Le chiamate API di polling verso i router reali devono essere eseguite periodicamente in loop asincrono, senza bloccare la UI.
6. **Modularità:** Il codice deve essere suddiviso in moduli separati per logica di gioco, gestione API, rendering UI, gestione eventi, glossario/tutorial, e configurazione.
7. **Compatibilità:** Il gioco deve funzionare su Windows, macOS e Linux senza modifiche sostanziali.
8. **Documentazione:** Tutto il codice deve essere abbondantemente commentato e documentato secondo le best practice Python (PEP8, docstring, esempi d’uso dove utile).
9. **UI fedele ai mockup:** La UI deve essere fedele ai mockup grafici allegati o descritti nel GDD.
10. **Glossario e tutorial:** Devono essere integrati e accessibili in-game tramite pulsanti o menu.
11. **Debug terminale:** Oltre alle API, anche la selezione di router/interfacce deve stampare a terminale gli ID e lo stato per facilitare il debug.
12. **No shortcut tastiera:** Non devono essere implementate shortcut da tastiera per azioni di gioco.
13. **Gestione errori:** In caso di errore API, la UI mostra l’ultimo stato valido e segnala l’errore all’utente.
14. **Requisiti tecnici:** Utilizzare Python 3.x, Pygame, e fornire un file requirements.txt aggiornato.
15. **Suggerimento struttura file:**
    - `main.py`: entrypoint, ciclo principale e inizializzazione.
    - `config.py`: parametri di configurazione e costanti.
    - `api.py`: gestione delle chiamate RESTCONF e debug API.
    - `router_grid.py`: logica della griglia, assegnazione ID, gestione router e interfacce.
    - `ui.py`: rendering grafico, gestione pulsanti, popup, feedback visivi.
    - `events.py`: gestione eventi mouse, input nome/hostname.
    - `glossary.py`: gestione glossario e tutorial interattivo.
    - `audio.py`: gestione effetti sonori e musica.
    - `utils.py`: funzioni di utilità generiche.
    - `requirements.txt`: dipendenze Python.
    - `README.md`: istruzioni di avvio e note tecniche.

---

### [26/05/2025] Click destro: inventario router

- Al click destro su un router nella griglia, la UI mostra un popup riassuntivo dell'inventario del router selezionato.
  - Il popup inventario mostra: hostname, stato claim (TUO/No/Altro), token disponibili, ID router, stato e VLAN di tutte le interfacce, stato neighborship di ogni link.
  - Il popup si chiude con un click sinistro fuori dal popup.
- Il click sinistro mantiene il comportamento attuale (claim/interfaccia).
- La logica è documentata in ui.py e events.py.

---

## [26/05/2025] Miglioramento logica hostname in polling API

- **Sezione 8: Motore API del Gioco**
  - Aggiornata la descrizione della logica di polling per l'hostname:
    - Ora il client imposta sempre l'hostname a '?' se l'interfaccia Loopback{group_id} non è presente o il campo description è vuoto.
    - L'hostname viene aggiornato solo se il campo description è presente e non vuoto.
    - Questo garantisce che la UI mostri sempre un valore coerente e mai stringhe vuote o valori obsoleti.

- **Sezione 6: UI & Grafica**
  - Chiarito che il box hostname sotto il router mostra sempre il valore aggiornato dal polling API, oppure '?' se non disponibile.
  - Aggiornata la descrizione della barra superiore: ora visualizza solo i token e il timer del giocatore corrente.

- **Sezione 13: Requisiti di Stile e Qualità del Codice**
  - Specificato che la logica di estrazione dell'hostname deve essere robusta rispetto a dati assenti o vuoti nelle risposte API.

- **Changelog**
  - [26/05/2025] Migliorata la robustezza della logica di visualizzazione hostname nella UI: ora viene sempre mostrato il valore corretto o un fallback sicuro ('?').

## [26/05/2025] Sincronizzazione hostname in tempo reale nella UI

- **Sezione 6: UI & Grafica**
  - La UI ora aggiorna e visualizza l'hostname di ogni router in tempo reale, sincronizzandolo ad ogni frame con lo stato più recente ottenuto dal polling API.
  - Il box hostname sotto il router mostra sempre il valore aggiornato o '?' se non disponibile, senza ritardi o desincronizzazioni.

- **Sezione 8: Motore API del Gioco**
  - Chiarito che la funzione di aggiornamento della UI richiama la logica di polling API ad ogni frame, garantendo la coerenza tra stato reale e visualizzazione.

- **Changelog**
  - [26/05/2025] La visualizzazione dell'hostname nella UI è ora sempre aggiornata in tempo reale grazie alla chiamata continua di update_from_api().

## [26/05/2025] Rimozione riferimenti ai token degli altri giocatori

- **Sezione 4: Gameplay e Funzionalità Principali**
  - Ogni giocatore vede e gestisce solo i propri token nella UI. I token degli altri giocatori non sono più visibili o mostrati.

- **Sezione 6: UI & Grafica**
  - La UI mostra solo il numero di token e il timer del giocatore locale. I token degli altri giocatori non sono mai visualizzati.
  - Aggiornata la descrizione della barra superiore: ora visualizza solo i token e il timer del giocatore corrente.

- **Mockup**
  - Aggiornati i mockup testuali per riflettere che solo i token del giocatore locale sono visibili.

- **Changelog**
  - [26/05/2025] Rimossi tutti i riferimenti e la visualizzazione dei token degli altri giocatori dalla UI e dal GDD. Ora ogni giocatore vede solo i propri token e timer.

## [26/05/2025] Claim router tramite parsing nomegiocatore nella description della loopback

- **Sezione 4: Gameplay e Funzionalità Principali**
  - Un router è considerato claimato dal giocatore locale solo se il campo description della sua interfaccia loopback è nel formato `nomegiocatore_hostnameRouterVirtuale` **e il `nomegiocatore` coincide esattamente con quello inserito dal giocatore locale**.
  - Se il nomegiocatore nella description è diverso dal nome inserito dal giocatore locale, il router è considerato sempre non claimato (colore grigio nella UI, azioni non permesse).
  - Il claim non è più gestito solo localmente, ma sincronizzato tramite la description della loopback letta via API.

- **Sezione 6: UI & Grafica**
  - La colorazione e lo stato claim dei router sono determinati dal confronto tra il nomegiocatore locale e quello letto dalla description della loopback.
  - Un router con description valorizzata ma nomegiocatore diverso da quello locale appare sempre come non claimato (grigio) e non può essere gestito dal giocatore locale.

- **Sezione 8: Motore API del Gioco**
  - La logica di claim di un router si basa ora sul parsing del campo description della loopback: se il nomegiocatore letto coincide con quello locale, il router risulta claimato dal giocatore. Altrimenti, è sempre considerato libero per il client locale.
  - Aggiornata la descrizione del formato della description: sempre `nomegiocatore_hostnameRouterVirtuale`.

- **Changelog**
  - [26/05/2025] Il claim dei router è ora determinato dal parsing del campo description della loopback, in formato `nomegiocatore_hostnameRouterVirtuale`, e sincronizzato tra tutti i client tramite API. Un router con nomegiocatore diverso da quello locale è sempre considerato non claimato dal client locale.

## [26/05/2025] Consolidamento regole claim, colore e sincronizzazione hostname

- **Claim router:** Un router è considerato claimato dal giocatore locale solo se il campo description della sua interfaccia loopback è nel formato `nomegiocatore_hostnameRouterVirtuale` **e il `nomegiocatore` coincide esattamente con quello inserito dal giocatore locale**. In tutti gli altri casi (description mancante, vuota, o nomegiocatore diverso), il router è considerato non claimato dal client locale.
- **Colore router:** Un router non claimato (cioè non claimato dal giocatore locale) viene sempre visualizzato di colore grigio (`config.GRAY`) nella UI, indipendentemente dal contenuto del campo hostname/description. Solo i router effettivamente claimati dal giocatore locale sono colorati con il colore del player.
- **Hostname:** L'hostname mostrato nella UI è sempre quello letto via polling API dal campo description della loopback, oppure '?' se non disponibile. La sincronizzazione è in tempo reale.
- **Token:** La UI mostra solo i token e il timer del giocatore locale. I token degli altri giocatori non sono mai visibili.
- **Nome giocatore:** Il nome del giocatore locale viene visualizzato nella UI sopra i token, in alto a sinistra, e viene troncato con '...' se troppo lungo per lo spazio disponibile.
- **Sincronizzazione:** Tutta la logica di claim, colore e hostname è sincronizzata tra client e router reali tramite API, senza stato locale persistente.
- **UI:** La logica di disegno dei router nella UI è:
    - Se `claimed_by` è None → colore grigio
    - Se `claimed_by` è 0 (player locale) → colore player 0
    - (Altri player non sono mai visualizzati in questa versione)

- **Legenda:**
  - In basso nella UI è sempre presente una legenda che spiega i colori e i simboli.
  - La legenda mostra solo:
    - Grigio: router non claimato
    - Colore player: router claimato dal giocatore locale
  - Non sono più presenti riferimenti o colori relativi ad altri giocatori.

- **Changelog**
  - [26/05/2025] Consolidate e chiarite tutte le regole di claim, colore, hostname e token nel GDD. La UI e la logica sono ora perfettamente allineate alle specifiche.
  - [26/05/2025] Il nome del giocatore locale viene ora visualizzato nella UI sopra i token, in alto a sinistra, e viene troncato con '...' se troppo lungo per lo spazio disponibile.

- **Schema ASCII di un router nella UI:**

  Esempio di rappresentazione di un router con le frecce delle interfacce e il box hostname:

  ```
      ↑
    ┌───┐
←  │  ●  │  →
    └───┘
      ↓
     [hostname]
  ```

  Dove:
  - Il cerchio pieno (●) rappresenta il router.
  - Le frecce (↑, ↓, ←, →) rappresentano le interfacce nord, sud, ovest, est.
  - Il box rettangolare sotto il router mostra l'hostname.
  - Il colore del cerchio indica lo stato claim (grigio = non claimato, colore player = claimato dal giocatore locale).
  - Le frecce sono colorate (verde = up, rosso = down, giallo = non configurata, giallo evidenziato all'hover).

  Esempio con tutte le frecce attive (up):

  ```
      ↑
    ┌───┐
←  │  ●  │  →
    └───┘
      ↓
     [Router1]
  ```

  Esempio con alcune interfacce down (rosse):

  ```
      ↑
    ┌───┐
X  │  ●  │  →
    └───┘
      ↓
     [Router2]
  ```
  (dove X indica una freccia rossa, cioè interfaccia down)

  Nota: la rappresentazione grafica reale è in pixel-art, ma lo schema ASCII aiuta a comprendere la disposizione degli elementi nella UI.

---

## 11.1 Mockup e schermate ASCII della UI

Di seguito alcuni esempi di schermate ASCII che illustrano la disposizione degli elementi principali della UI, lo stato dei router, la visualizzazione dei token, del timer, del nome giocatore e della legenda.

### Schermata principale: griglia router 4x4 (esempio semplificato)

```
╔════════════════════════════════════════════════════════════════════╗
║  Giocatore: Alice      Token: ●●●●   Timer: 08s                  ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                  ║
║      ↑           ↑           ↑           ↑                       ║
║    ┌───┐       ┌───┐       ┌───┐       ┌───┐                     ║
║ ← │ ● │ →   ← │ ● │ →   ← │ ● │ →   ← │ ● │ →                   ║
║    └───┘       └───┘       └───┘       └───┘                     ║
║      ↓           ↓           ↓           ↓                       ║
║   [R1]        [R2]        [R3]        [R4]                      ║
║                                                                  ║
║      ↑           ↑           ↑           ↑                       ║
║    ┌───┐       ┌───┐       ┌───┐       ┌───┐                     ║
║ ← │ ● │ →   ← │ ● │ →   ← │ ● │ →   ← │ ● │ →                   ║
║    └───┘       └───┘       └───┘       └───┘                     ║
║      ↓           ↓           ↓           ↓                       ║
║   [R5]        [R6]        [R7]        [R8]                      ║
║                                                                  ║
║      ↑           ↑           ↑           ↑                       ║
║    ┌───┐       ┌───┐       ┌───┐       ┌───┐                     ║
║ ← │ ● │ →   ← │ ● │ →   ← │ ● │ →   ← │ ● │ →                   ║
║    └───┘       └───┘       └───┘       └───┘                     ║
║      ↓           ↓           ↓           ↓                       ║
║   [R9]       [R10]       [R11]       [R12]                      ║
║                                                                  ║
║      ↑           ↑           ↑           ↑                       ║
║    ┌───┐       ┌───┐       ┌───┐       ┌───┐                     ║
║ ← │ ● │ →   ← │ ● │ →   ← │ ● │ →   ← │ ● │ →                   ║
║    └───┘       └───┘       └───┘       └───┘                     ║
║      ↓           ↓           ↓           ↓                       ║
║  [R13]      [R14]      [R15]      [R16]                         ║
║                                                                  ║
╚════════════════════════════════════════════════════════════════════╝
Legenda: ● grigio = router non claimato, ● blu = router claimato dal giocatore locale
         ↑/→/↓/← verdi = interfaccia up, rosse = interfaccia down, gialle = non configurata
         [Rx] = hostname del router (o '?' se non disponibile)

```

### Esempio di router claimato e interfacce up/down

```
      ↑
    ┌───┐
X  │ ● │  →
    └───┘
      ↓
   [Router2]
```
Dove:
- ● blu = router claimato dal giocatore locale
- X = freccia rossa (interfaccia ovest down)
- → = freccia verde (interfaccia est up)
- ↑, ↓ = altre interfacce (colore variabile)
- [Router2] = hostname letto via API

### Barra superiore con nome giocatore troncato

```
Giocatore: SuperLongNa...   Token: ●●●   Timer: 04s
```

### Legenda in basso

```
Legenda: ● grigio = router non claimato, ● blu = router claimato dal giocatore locale
         ↑/→/↓/← verdi = interfaccia up, rosse = interfaccia down, gialle = non configurata
         [Rx] = hostname del router (o '?' se non disponibile)
```

### Esempio di router con hostname mancante

```
      ↑
    ┌───┐
←  │ ● │  →
    └───┘
      ↓
     [?]
```

---

## 4. Gameplay e Funzionalità Principali

- All’avvio della partita, il gioco chiede al giocatore di inserire il proprio nome (max 10 caratteri).
- Quando un giocatore effettua il claim di un router, il campo hostname del router viene impostato nel formato:  
  **nomegiocatore_hostname**  
  Il campo hostname non può superare 10 caratteri.
- Fino a 4 giocatori, ognuno con il proprio client su PC, interagiscono contemporaneamente e indipendentemente con la stessa infrastruttura di rete reale.
- Ogni client legge e scrive lo stato di gioco direttamente sui router tramite API.
- Il gioco è realtime: ogni giocatore può agire in qualsiasi momento, effettuando claim di router non ancora assegnati o abilitando/disabilitando le interfacce dei router di cui è proprietario.
- Ogni azione consuma un token; ogni giocatore inizia con 4 token e ne riceve 1 aggiuntivo **ogni 10 secondi** (timer visibile).
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

## 5. Regole e Parametri

- Ogni azione (claim o abilitazione/disabilitazione interfaccia) consuma un token.
- Ogni giocatore inizia con 4 token.
- **Ogni 10 secondi viene ricaricato 1 token a ogni giocatore.**
- Solo una interfaccia abilitabile/disabilitabile per azione e solo su router propri.
- Mouse/tastiera solo per hostname.
- Stato sempre aggiornato dai dispositivi reali.
- Nome giocatore massimo 10 caratteri.
- Hostname massimo 10 caratteri (inclusi eventuali separatori e nomegiocatore).
- Tutte le interazioni di gioco avvengono tramite mouse: il giocatore può selezionare router, claimare, attivare/disattivare interfacce, aprire popup info, glossario e tutorial solo tramite click o tap.
- L'unico uso della tastiera è per l'inserimento del nome giocatore e dell'hostname quando richiesto (popup di input testuale).
- Non sono previsti shortcut da tastiera per azioni di gioco (claim, attiva interfaccia, info, glossario, tutorial, ecc.): tutte queste azioni sono accessibili solo tramite pulsanti o click nella UI.
- La UI mostra sempre pulsanti o icone cliccabili per ogni azione disponibile.

---

## 6. UI & Grafica

- **Gioco 2D, schermo intero, stile retro gaming pixel-art**
- **Palette colori:** Pastello (esempi: azzurro chiaro, rosa, lilla, verde menta, giallo pallido)
- UI adattiva, leggibile, centrata, senza overflow
- Visualizzazione dello stato in tempo reale tramite letture dai dispositivi
- Stato token, timer, azioni disponibili e stato dei router sempre visibili e aggiornati dinamicamente
- Visualizzazione grafica dei link attivi tra router con neighborship di routing attiva
- Hostname router sempre visibile
- ID router solo a terminale per debug
- Glossario accessibile dal menu e in-game
- **Un router di cui non è stato fatto il claim viene visualizzato di colore grigio nella UI.**

### 6.1 Dettaglio: Regole di disegno di un router nella UI

Ogni router nella UI viene rappresentato secondo queste regole grafiche:

- **Forma base:**
  - Cerchio pieno, dimensione adattiva in base alla griglia e alla risoluzione.
  - Colore:
    - Grigio (libero, non claimato; ovvero nessun giocatore ha ancora effettuato il claim sul router)
    - Blu (claimato da un giocatore, colore del giocatore)
    - Bordo giallo spesso 3 pixel se router obiettivo già claimato
- **Interfacce:**
  - Quattro frecce spesse (5px) orientate verso nord, sud, est, ovest, sempre visibili.
  - Le frecce sono disegnate **all'interno** del cerchio del router, puntando dal bordo verso il centro.
  - Colore frecce:
    - Verde (interfaccia up)
    - Rosso (interfaccia down)
    - Giallo (interfaccia non configurata)
  - Quando il mouse passa sopra una freccia, questa viene evidenziata in giallo.
  - Le frecce sono disegnate in modo da non sovrapporsi al cerchio del router.
- **Link attivi:**
  - Linee tratteggiate tra i router con neighborship attiva, colore verde.
  - Le linee sono disegnate in modo da non sovrapporsi al cerchio del router.
  - Le linee sono bidirezionali e mostrano lo stato attivo della connessione.
- **Router obiettivo:**
  - Se il router è un obiettivo del livello, il suo bordo è evidenziato in giallo spesso 3 pixel.
  - Il colore del bordo giallo non cambia in base al claim del router.
- **Stato del router:**
  - Se il router è claimato, il suo colore di sfondo è quello del giocatore che lo ha claimato.
  - Se il router non è claimato, il colore di sfondo è grigio.
- **Stato delle interfacce:**
  - Le frecce delle interfacce sono sempre visibili, ma il loro colore cambia in base allo stato:
    - Verde se l'interfaccia è attiva (up, cioè 'admin up' secondo lo stato appreso dalla chiamata API ricorrente)
    - Rosso se l'interfaccia è inattiva (down, cioè 'admin down' secondo lo stato appreso dalla chiamata API ricorrente)
- **Hostname:**
  - Box rettangolare adattivo sempre visibile sotto ogni router, con bordo bianco e sfondo scuro.
  - Testo hostname sempre centrato e mai troncato.
  - Il box mostra sempre il valore aggiornato dal polling API, oppure '?' se non disponibile, senza ritardi o desincronizzazioni.
- **Feedback visivo:**
  - Quando un router viene claimato, il colore del cerchio cambia immediatamente e viene mostrato un messaggio di conferma.
  - Quando un’interfaccia viene attivata/disattivata, il colore della freccia cambia in tempo reale.
- **Hover e click:**
  - Al passaggio del mouse su un router, il suo colore di sfondo diventa leggermente più chiaro per indicare che è selezionato.
  - Al click su un router:
    - Se il router non è claimato, viene avviata la procedura di claim.
    - Se il router è già claimato dal giocatore locale, il click non mostra più la finestra informativa (popup) ma non fa nulla (o in futuro potrà attivare altre azioni contestuali).
- **ID router:**
  - Gli ID (global_id, local_id, group_id) non sono visibili nella UI, ma vengono stampati a terminale per debug quando si seleziona il router.
- **Posizionamento:**
  - Il router è centrato nella cella della griglia, con padding per evitare sovrapposizioni.
- **Legenda:**
  - In basso nella UI è sempre presente una legenda che spiega i colori e i simboli.
  - La legenda mostra solo:
    - Grigio: router non claimato
    - Colore player: router claimato dal giocatore locale
  - Non sono più presenti riferimenti o colori relativi ad altri giocatori.

#### Aggiornamenti e miglioramenti UI (storico changelog integrato)

- La visualizzazione dell'hostname nella UI è sempre aggiornata in tempo reale grazie alla chiamata continua di update_from_api().
- Il box hostname sotto il router mostra sempre il valore aggiornato o '?' se non disponibile, senza ritardi o desincronizzazioni.
- La UI mostra solo il numero di token e il timer del giocatore locale. I token degli altri giocatori non sono mai visualizzati.
- Ogni giocatore vede e gestisce solo i propri token nella UI. I token degli altri giocatori non sono più visibili o mostrati.
- La barra superiore visualizza solo i token e il timer del giocatore corrente.
- Un router è considerato claimato dal giocatore locale solo se il campo description della sua interfaccia loopback è nel formato `nomegiocatore_hostnameRouterVirtuale` e il `nomegiocatore` coincide esattamente con quello inserito dal giocatore locale. Se il nomegiocatore nella description è diverso dal nome inserito dal giocatore locale, il router è considerato sempre non claimato (colore grigio nella UI, azioni non permesse).
- Il claim non è più gestito solo localmente, ma sincronizzato tramite la description della loopback letta via API.
- La colorazione e lo stato claim dei router sono determinati dal confronto tra il nomegiocatore locale e quello letto dalla description della loopback.
- Un router con description valorizzata ma nomegiocatore diverso da quello locale appare sempre come non claimato (grigio) e non può essere gestito dal giocatore locale.
- La logica di claim di un router si basa ora sul parsing del campo description della loopback: se il nomegiocatore letto coincide con quello locale, il router risulta claimato dal giocatore. Altrimenti, è sempre considerato libero per il client locale.
- La logica di estrazione hostname è robusta rispetto a dati assenti o vuoti nelle risposte API: il client imposta sempre l'hostname a '?' se l'interfaccia Loopback{group_id} non è presente o il campo description è vuoto.
- L'hostname viene aggiornato solo se il campo description è presente e non vuoto.
- Il nome del giocatore locale viene visualizzato nella UI sopra i token, in alto a sinistra, e viene troncato con '...' se troppo lungo per lo spazio disponibile.

---

## 7. Dettaglio: Sistema di ID dei Router

### Tipologie di ID
- **ID globale (global_id):**
  - Ogni router riceve un ID progressivo unico da 1 a N*N, assegnato riga per riga nella griglia.
  - Serve per identificare in modo univoco ogni router nella rete e per debug.
  - il global_id ha scarso valore pratico per il gioco.
- **ID locale (local_id):**
  - All’interno di ogni gruppo 2x2 di router, ogni router riceve un local_id da 1 a 4 secondo uno schema a scacchiera (1,2,3,4).
  - Utilizzato per la corrispondenza con la numerazione delle interfacce e per le chiamate API.
  - Il local_id rappresenta l'identificativo del router reale.
- **ID gruppo (group_id):**
  - Ogni gruppo 2x2 di router riceve un group_id progressivo.
  - Serve per identificare i router che fanno parte dello stesso gruppo logico (ad esempio per le chiamate API alle LoopbackX).
  - Il group_id rappresenta la vrf (Virtual Routing and Forwarding) del router reale.

### Regole di visualizzazione e utilizzo
- Gli ID (global_id, local_id, group_id) **non sono visibili nella UI** accanto ai router durante il gioco normale.
- Quando si clicca su un router, i suoi ID vengono stampati a terminale per scopi di debug e sviluppo.
- In modalità API, gli ID sono utilizzati per:
  - Costruire l’indirizzo IP/hostname per la chiamata RESTCONF (es: https://198.18.1.1X dove X è il local_id).
  - Identificare l’interfaccia LoopbackX (dove X è il group_id) per recuperare l’hostname dinamico tramite API.
- In modalità tutorial, gli ID sono usati solo internamente e non sono mai mostrati all’utente.

### Assegnazione degli ID (algoritmo)
- All’avvio della partita, dopo la creazione della griglia, viene eseguita l’assegnazione:
  - global_id: progressivo da 1 a N*N, riga per riga.
  - group_id: assegnato a blocchi 2x2 a scacchiera, non per riga. Ogni blocco 2x2 di router adiacenti condivide lo stesso group_id, che viene incrementato da sinistra a destra e dall'alto verso il basso.
  - local_id: da 1 a 4 all’interno di ogni blocco 2x2 secondo uno schema a scacchiera (1,2,3,4).

### Esempio pratico
- In una griglia 4x4:
  - global_id: 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16
  - group_id:
    1 1 2 2
    1 1 2 2
    3 3 4 4
    3 3 4 4
  - local_id: 1,2,3,4 in ogni blocco 2x2

- La funzione generate_ids in utils.py implementa questa logica.

### Debug e sviluppo
- Per facilitare il debug, ogni volta che si seleziona un router, i suoi ID vengono stampati a terminale.
- Questo aiuta a verificare la corretta corrispondenza tra UI, logica di gioco e chiamate API.

---

## 8. Motore API del Gioco
### Comportamento delle API
Il client del gioco interagisce con i router reali tramite API RESTCONF, utilizzando le seguenti regole e logiche:
### Comportamento delle API
- **Chiamate API periodiche:**  
  Le chiamate API verso i router reali NON vengono attivate dal passaggio del mouse, ma vengono effettuate periodicamente dal client sin dall'inizio della partita (es. ogni 3 secondi).
- **Memorizzazione locale:**  
  Tutte le informazioni rilevanti recuperate dalle API (hostname, stato delle interfacce, stato delle neighborship) vengono memorizzate localmente dal client.
- **Comportamento UI al passaggio del mouse:**  
  Quando il mouse passa sopra un router, viene visualizzato l’hostname che è già stato recuperato dal ciclo periodico di query API.  
  Non viene effettuata alcuna chiamata API al momento dell’interazione dell’utente.
- **Aggiornamento informazioni:**  
  Le informazioni mostrate in UI sono aggiornate periodicamente in base alla frequenza delle chiamate API di polling.  
  In caso di perdita temporanea di connessione o errore nelle API, le informazioni rimangono quelle dell’ultimo ciclo di polling riuscito.
- **API asincrone:**  
  Le chiamate API sono asincrone e non bloccano l'interfaccia utente.  
  Il client continua a funzionare normalmente anche se una chiamata API fallisce o impiega più tempo del previsto.

### Logica di recupero hostname
- **Obiettivo:**  
  Recuperare l'hostname configurato sul router reale per visualizzarlo nella UI.
- **Interfaccia Loopback:**
  - Ogni router ha un'interfaccia loopback configurata con un nome specifico: `LoopbackY`, dove `Y` è il `group_id` del router.
  - Questa interfaccia viene utilizzata per identificare il router e recuperare l'hostname.
### Chiamata API per hostname
- **Endpoint RESTCONF:**
  - URL: `https://198.18.1.1X/restconf/data/ietf-interfaces:interfaces` dove `X` è il `local_id` del router selezionato.
  - Autenticazione: Basic Auth (username: `cisco`, password: `C1sco12345`).
  - Content-Type: `application/yang-data+json`
- **Logica di ricerca hostname:**
  - Viene cercata l'interfaccia `LoopbackY` dove `Y` è il `group_id` del router.
  - Il campo `description` di questa interfaccia viene utilizzato come hostname da mostrare nella UI.
- **Esempio di chiamata:**
  - Per un router con `local_id=3` e `group_id=2`:
    - URL: `https://198.18.1.13/restconf/data/ietf-interfaces:interfaces`
    - Si cerca l'interfaccia `Loopback2` e si legge il campo `description`.
- **Fallback:**
  - Se la chiamata fallisce o l'interfaccia non è presente, viene mostrato un hostname di default (`?`) oppure l'ultimo valore di hostname disponibile.

Questa logica consente di visualizzare in tempo reale l'hostname configurato realmente sul router (in base all’ultimo polling riuscito), favorendo apprendimento e troubleshooting.

### Logica di settaggio hostname
- **Obiettivo:**  
  Permettere ai giocatori di impostare l'hostname del router reale tramite l'interfaccia loopback.
- **Interfaccia Loopback:**
  - Ogni router ha un'interfaccia loopback configurata con un nome specifico: `LoopbackY`, dove `Y` è il `group_id` del router.
  - Questa interfaccia viene utilizzata per identificare il router e impostare l'hostname.
### Chiamata API per impostare hostname
- **Endpoint RESTCONF:**
  - URL: `https://198.18.1.1X/restconf/data/ietf-interfaces:interfaces/interface=LoopbackY`
  - Autenticazione: Basic Auth (username: `cisco`, password: `C1sco12345`).
  - Content-Type: `application/yang-data+json`
  - metodo: 'PUT'
- **Payload:**
    - Il payload deve contenere il campo `description` con il nuovo hostname.
    - Esempio di payload:
        ```json
            {
            "interface": [
                {
                "name": "Loopback1",
                "type": "iana-if-type:softwareLoopback",
                "description": "nomegiocatore_hostname"
                }
            ]
            }
        ```
- **Esempio di chiamata:**
  - Per un router con `local_id=3` e `group_id=2`, per impostare l'hostname a `Alice_Router`:
    - URL: `https://198.18.1.13/restconf/data/ietf-interfaces:interfaces/interface=Loopback2`
- **Esecuzione:**
  - Quando un giocatore effettua il claim di un router, il client invia questa chiamata API per impostare l'hostname.
  - Se la chiamata ha successo, l'hostname viene aggiornato. Non avviene nessuna memorizzazione locale dell'hostname.

### 8.1 Ottenimento della tabella di routing di un router (modalità API)

Per ottenere la tabella di routing di un router reale, il client deve effettuare la seguente chiamata API RESTCONF:

```
restconf/data/ietf-routing:routing-state/routing-instance
```

Questa chiamata restituisce lo stato di routing, inclusa la tabella di routing attuale del router.

> **Nota:** In futuro verranno aggiunti esempi pratici di risposta dell’API e di parsing delle rotte rilevanti.

---

## 9. Dettaglio: Collegamento Fisico e Logico dei Router (VLAN e link tra router)

### Collegamento fisico
- Ogni router reale è fisicamente connesso alla rete tramite la sua interfaccia **GigabitEthernet1**.

### Collegamento logico tramite VLAN
- Tutti i link tra router (ovvero le interfacce nord, sud, est, ovest nel gioco) sono realizzati tramite **interfacce logiche VLAN** (sub-interface) sulla stessa GigabitEthernet1.
- **Ciascun link tra due router** all’interno di un gruppo 2x2 è rappresentato da una VLAN univoca.

  - **Regola generale**:  
    Il numero VLAN è creato concatenando **group_id** + **local_id_A** + **local_id_B**, dove A e B sono i due router collegati.  
    L’ordine non conta, il link è bidirezionale.
    **local_id_A** è sempre inferiore a  **local_id_B**

  - **Esempi**:  
    - _VLAN 312_ rappresenta il link nel gruppo 3 tra router 1 e router 2 (e viceversa, il link è bidirezionale).
    - _VLAN 434_ rappresenta nel gruppo 4 il link tra router 3 e router 4 (e viceversa).

#### Mappatura e gestione dei link
- Ogni interfaccia logica di collegamento (n/s/e/w nel gioco) corrisponde a una sub-interface configurata su GigabitEthernet1, con il numero VLAN che rappresenta univocamente il link tra i due router del gruppo.
- Il link è **bidirezionale** e il numero VLAN è lo stesso su entrambi i router coinvolti.
- Quando un link viene “attivato” o “disattivato” nel gioco, la relativa sub-interface (es: `GigabitEthernet1.312`) viene abilitata/disabilitata via API.
- La UI riflette lo stato up/down della VLAN (interfaccia logica/link) con le frecce verdi/rosse.
- L’identificativo VLAN può essere mostrato a scopo didattico nel glossario o in una schermata avanzata/debug.

**Stato neighborship di routing:**  
Se una neighborship di routing è attiva su un link, il campo `description` della relativa sub-interface sarà impostato a `UP`.  
Se il campo `description` della sub-interface è vuoto, significa che non esiste nessuna neighborship attiva su quel link.
Se tra due router esiste una neighborship attiva, la UI mostra una linea tratteggiata verde tra i due router, indicando che il link è attivo e funzionante.

#### Schema esempio

```
Gruppo 3 (group_id = 3):

Routers:
- Router 1 (local_id=1)
- Router 2 (local_id=2)
- Router 3 (local_id=3)
- Router 4 (local_id=4)

Link tra Router 1 e Router 2: VLAN 312 (GigabitEthernet1.312 su entrambi)
Link tra Router 3 e Router 4: VLAN 334 (GigabitEthernet1.334 su entrambi)
Link tra Router 2 e Router 3: VLAN 323 (GigabitEthernet1.323 su entrambi)
...
```


---

## 10. Integrazione con la Rete Reale e Mockup

- Tutto lo stato di gioco è scritto/letto sui dispositivi reali via API.
- Parametri come hostname, stato delle interfacce e neighborship sono aggiornati in tempo reale.
- Le API sono utilizzate per leggere lo stato attuale della rete e per scrivere le modifiche apportate dai giocatori.
- In modalità offline, lo stato è simulato localmente.


---

## 11. Prototipo e Mockup

- Prototipazione con Figma/Excalidraw per griglia, feedback, ecc.



---

## 12. Audio

- Chiptune, SFX
- Musica di sottofondo in stile retro gaming
- Effetti sonori per azioni chiave (claim, attivazione link, errore, successo)
- Feedback audio per azioni di gioco (es. click, attivazione/disattivazione link)
- Effetti sonori per eventi di gioco (es. attivazione di un link, errore, successo)
- Volume regolabile tramite menu opzioni
- Opzioni per disattivare la musica o gli effetti sonori

---


## 13. Requisiti di Stile e Qualità del Codice

- Codice abbondantemente commentato: ogni funzione, classe, modulo e blocco logico deve essere documentato tramite commenti e docstring, per facilitare la comprensione e l’apprendimento.
- Codice pensato come materiale didattico: ogni concetto implementato, pattern o soluzione deve essere spiegato.
- Soluzioni semplici, leggibili e lineari preferite a quelle complesse, salvo necessità tecniche documentate.
- Best practice Python (PEP8), nomi chiari, separazione in moduli, attenzione alla manutenibilità.
- Dove utile, aggiungere esempi d’uso nei commenti/docstring.
- Logica di estrazione hostname robusta rispetto a dati assenti o vuoti nelle risposte API.

---

## 14. Glossario Interattivo in Game

Sezione accessibile dal menu e durante la partita dove il giocatore può consultare i principali concetti di networking:

- **Rete**: Insieme di dispositivi (computer, router, server) collegati tra loro per scambiarsi dati.
- **Router**: Dispositivo che indirizza i pacchetti di dati tra reti diverse.
- **Interfaccia**: Punto di connessione fisica o logica su un router (nord, sud, est, ovest nel gioco).
- **Interfaccia logica (sub-interface)**: Interfaccia virtuale creata su un'interfaccia fisica, identificata dal numero VLAN.
- **VLAN**: Rete virtuale che identifica univocamente un link tra due router reali.
- **Link**: Collegamento tra due dispositivi di rete che permette il passaggio delle informazioni.
- **Neighborship**: Relazione di vicinato tra due router che hanno instaurato una sessione di routing attiva.
- **Disservizio**: Situazione in cui una parte della rete o un link smette di funzionare correttamente.
- **Pacchetto**: Unità di dati che viaggia nella rete.
- **Routing**: Processo con cui un router decide il percorso migliore per un pacchetto.
- **API**: Interfaccia di programmazione delle applicazioni che permette al client di interagire con i router.

---

## 15. Condizione di Vittoria del Livello

La **condizione di vittoria di un livello** viene raggiunta quando, in almeno uno dei router obiettivo, la sua tabella di routing contiene le rotte verso le loopback di **tutti** i router obiettivo.

### Definizione di router obiettivo

I **router obiettivo** sono quelli identificati dalle coppie (groupID, localID) specificate per il livello.  
Esempio:  
- (1,1)  
- (4,1)

### Indirizzamento delle loopback

L’indirizzo IP della loopback per ogni router obiettivo segue la convenzione:
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
In altre parole, la tabella deve contenere tutte le destinazioni del tipo G.0.0. L dove (G,L) sono le coppie dei router obiettivo.

### Nota
- Il controllo della vittoria avviene periodicamente (sincronizzato con il polling delle API).
- La verifica può essere visualizzata nella UI tramite un indicatore di progresso o stato.

---

## 16. Ottenimento della tabella di routing di un router (modalità API)

Per ottenere la tabella di routing di un router reale, il client deve effettuare la seguente chiamata API RESTCONF:

```
restconf/data/ietf-routing:routing-state/routing-instance
```

Questa chiamata restituisce lo stato di routing, inclusa la tabella di routing attuale del router.

> **Nota:** In futuro verranno aggiunti esempi pratici di risposta dell’API e di parsing delle rotte rilevanti.

---

**Nota Bene:**  
Mockup grafici consigliati per la presentazione ufficiale.

---

## Specifiche tecniche

- **Linguaggio:** Python 3.x
- **Libreria grafica:** Pygame (ultima versione stabile)
- **Struttura modulare:** Il codice deve essere suddiviso in moduli separati per logica di gioco, gestione API, rendering UI, gestione eventi, glossario/tutorial, e configurazione.
- **Compatibilità:** Il gioco deve funzionare su Windows, macOS e Linux senza modifiche sostanziali.
- **Gestione dipendenze:** Fornire un file `requirements.txt` con tutte le dipendenze necessarie (incluso Pygame e librerie per richieste HTTP come `requests`).
- **API RESTCONF:** Tutte le chiamate API devono essere indirizzate esclusivamente ai 4 router fisici reali, utilizzando la logica di VRF per virtualizzare la griglia NxN.
- **Debug API:** Ogni chiamata API (claim, interfaccia, hostname, stato) deve essere stampata a terminale in modo conciso: solo metodo, endpoint, status code e, in caso di errore, il messaggio di errore.
- **Interazione:** Tutte le azioni di gioco sono accessibili solo tramite mouse (eccetto input nome/hostname tramite tastiera).
- **Polling API:** Le chiamate API di polling verso i router reali devono essere eseguite periodicamente in loop asincrono, senza bloccare la UI.
- **Documentazione:** Tutto il codice deve essere abbondantemente commentato e documentato secondo le best practice Python (PEP8, docstring, esempi d’uso dove utile).
- **Mockup:** La UI deve essere fedele ai mockup grafici allegati o descritti nel GDD.
- **Glossario e tutorial:** Devono essere integrati e accessibili in-game tramite pulsanti o menu.
- **Debug terminale:** Oltre alle API, anche la selezione di router/interfacce deve stampare a terminale gli ID e lo stato per facilitare il debug.
- **Architettura:** Prevedere una chiara separazione tra logica di gioco, interfaccia utente e gestione delle API.

---

## Regole per Copilot e AI Assistant

1. **Rispetta il GDD:** Tutte le implementazioni e suggerimenti devono essere coerenti con le specifiche e le regole descritte nel GDD.
2. **Mouse-driven:** Tutte le azioni di gioco (claim, attivazione/disattivazione interfacce, info, glossario, tutorial) devono essere accessibili solo tramite mouse, eccetto l’inserimento di nome/hostname che avviene tramite tastiera.
3. **Debug API:** Ogni chiamata API (claim, interfaccia, hostname, stato) deve essere stampata a terminale in modo conciso: solo metodo, endpoint, status code e, in caso di errore, il messaggio di errore.
4. **API RESTCONF:** Tutte le chiamate API devono essere indirizzate solo ai 4 router fisici reali, utilizzando la logica di VRF per virtualizzare la griglia NxN.
5. **Polling asincrono:** Le chiamate API di polling verso i router reali devono essere eseguite periodicamente in loop asincrono, senza bloccare la UI.
6. **Modularità:** Il codice deve essere suddiviso in moduli separati per logica di gioco, gestione API, rendering UI, gestione eventi, glossario/tutorial, e configurazione.
7. **Compatibilità:** Il gioco deve funzionare su Windows, macOS e Linux senza modifiche sostanziali.
8. **Documentazione:** Tutto il codice deve essere abbondantemente commentato e documentato secondo le best practice Python (PEP8, docstring, esempi d’uso dove utile).
9. **UI fedele ai mockup:** La UI deve essere fedele ai mockup grafici allegati o descritti nel GDD.
10. **Glossario e tutorial:** Devono essere integrati e accessibili in-game tramite pulsanti o menu.
11. **Debug terminale:** Oltre alle API, anche la selezione di router/interfacce deve stampare a terminale gli ID e lo stato per facilitare il debug.
12. **No shortcut tastiera:** Non devono essere implementate shortcut da tastiera per azioni di gioco.
13. **Gestione errori:** In caso di errore API, la UI mostra l’ultimo stato valido e segnala l’errore all’utente.
14. **Requisiti tecnici:** Utilizzare Python 3.x, Pygame, e fornire un file requirements.txt aggiornato.
15. **Suggerimento struttura file:**
    - `main.py`: entrypoint, ciclo principale e inizializzazione.
    - `config.py`: parametri di configurazione e costanti.
    - `api.py`: gestione delle chiamate RESTCONF e debug API.
    - `router_grid.py`: logica della griglia, assegnazione ID, gestione router e interfacce.
    - `ui.py`: rendering grafico, gestione pulsanti, popup, feedback visivi.
    - `events.py`: gestione eventi mouse, input nome/hostname.
    - `glossary.py`: gestione glossario e tutorial interattivo.
    - `audio.py`: gestione effetti sonori e musica.
    - `utils.py`: funzioni di utilità generiche.
    - `requirements.txt`: dipendenze Python.
    - `README.md`: istruzioni di avvio e note tecniche.

---

### [26/05/2025] Click destro: inventario router

- Al click destro su un router nella griglia, la UI mostra un popup riassuntivo dell'inventario del router selezionato.
  - Il popup inventario mostra: hostname, stato claim (TUO/No/Altro), token disponibili, ID router, stato e VLAN di tutte le interfacce, stato neighborship di ogni link.
  - Il popup si chiude con un click sinistro fuori dal popup.
- Il click sinistro mantiene il comportamento attuale (claim/interfaccia).
- La logica è documentata in ui.py e events.py.

---

## [26/05/2025] Miglioramento logica hostname in polling API

- **Sezione 8: Motore API del Gioco**
  - Aggiornata la descrizione della logica di polling per l'hostname:
    - Ora il client imposta sempre l'hostname a '?' se l'interfaccia Loopback{group_id} non è presente o il campo description è vuoto.
    - L'hostname viene aggiornato solo se il campo description è presente e non vuoto.
    - Questo garantisce che la UI mostri sempre un valore coerente e mai stringhe vuote o valori obsoleti.

- **Sezione 6: UI & Grafica**
  - Chiarito che il box hostname sotto il router mostra sempre il valore aggiornato dal polling API, oppure '?' se non disponibile.
  - Aggiornata la descrizione della barra superiore: ora visualizza solo i token e il timer del giocatore corrente.

- **Sezione 13: Requisiti di Stile e Qualità del Codice**
  - Specificato che la logica di estrazione dell'hostname deve essere robusta rispetto a dati assenti o vuoti nelle risposte API.

- **Changelog**
  - [26/05/2025] Migliorata la robustezza della logica di visualizzazione hostname nella UI: ora viene sempre mostrato il valore corretto o un fallback sicuro ('?').

## [26/05/2025] Sincronizzazione hostname in tempo reale nella UI

- **Sezione 6: UI & Grafica**
  - La UI ora aggiorna e visualizza l'hostname di ogni router in tempo reale, sincronizzandolo ad ogni frame con lo stato più recente ottenuto dal polling API.
  - Il box hostname sotto il router mostra sempre il valore aggiornato o '?' se non disponibile, senza ritardi o desincronizzazioni.

- **Sezione 8: Motore API del Gioco**
  - Chiarito che la funzione di aggiornamento della UI richiama la logica di polling API ad ogni frame, garantendo la coerenza tra stato reale e visualizzazione.

- **Changelog**
  - [26/05/2025] La visualizzazione dell'hostname nella UI è ora sempre aggiornata in tempo reale grazie alla chiamata continua di update_from_api().

## [26/05/2025] Rimozione riferimenti ai token degli altri giocatori

- **Sezione 4: Gameplay e Funzionalità Principali**
  - Ogni giocatore vede e gestisce solo i propri token nella UI. I token degli altri giocatori non sono più visibili o mostrati.

- **Sezione 6: UI & Grafica**
  - La UI mostra solo il numero di token e il timer del giocatore locale. I token degli altri giocatori non sono mai visualizzati.
  - Aggiornata la descrizione della barra superiore: ora visualizza solo i token e il timer del giocatore corrente.

- **Mockup**
  - Aggiornati i mockup testuali per riflettere che solo i token del giocatore locale sono visibili.

- **Changelog**
  - [26/05/2025] Rimossi tutti i riferimenti e la visualizzazione dei token degli altri giocatori dalla UI e dal GDD. Ora ogni giocatore vede solo i propri token e timer.

## [26/05/2025] Claim router tramite parsing nomegiocatore nella description della loopback

- **Sezione 4: Gameplay e Funzionalità Principali**
  - Un router è considerato claimato dal giocatore locale solo se il campo description della sua interfaccia loopback è nel formato `nomegiocatore_hostnameRouterVirtuale` **e il `nomegiocatore` coincide esattamente con quello inserito dal giocatore locale**.
  - Se il nomegiocatore nella description è diverso dal nome inserito dal giocatore locale, il router è considerato sempre non claimato (colore grigio nella UI, azioni non permesse).
  - Il claim non è più gestito solo localmente, ma sincronizzato tramite la description della loopback letta via API.

- **Sezione 6: UI & Grafica**
  - La colorazione e lo stato claim dei router sono determinati dal confronto tra il nomegiocatore locale e quello letto dalla description della loopback.
  - Un router con description valorizzata ma nomegiocatore diverso da quello locale appare sempre come non claimato (grigio) e non può essere gestito dal giocatore locale.

- **Sezione 8: Motore API del Gioco**
  - La logica di claim di un router si basa ora sul parsing del campo description della loopback: se il nomegiocatore letto coincide con quello locale, il router risulta claimato dal giocatore. Altrimenti, è sempre considerato libero per il client locale.
  - Aggiornata la descrizione del formato della description: sempre `nomegiocatore_hostnameRouterVirtuale`.

- **Changelog**
  - [26/05/2025] Il claim dei router è ora determinato dal parsing del campo description della loopback, in formato `nomegiocatore_hostnameRouterVirtuale`, e sincronizzato tra tutti i client tramite API. Un router con nomegiocatore diverso da quello locale è sempre considerato non claimato dal client locale.

## [26/05/2025] Consolidamento regole claim, colore e sincronizzazione hostname

- **Claim router:** Un router è considerato claimato dal giocatore locale solo se il campo description della sua interfaccia loopback è nel formato `nomegiocatore_hostnameRouterVirtuale` **e il `nomegiocatore` coincide esattamente con quello inserito dal giocatore locale**. In tutti gli altri casi (description mancante, vuota, o nomegiocatore diverso), il router è considerato non claimato dal client locale.
- **Colore router:** Un router non claimato (cioè non claimato dal giocatore locale) viene sempre visualizzato di colore grigio (`config.GRAY`) nella UI, indipendentemente dal contenuto del campo hostname/description. Solo i router effettivamente claimati dal giocatore locale sono colorati con il colore del player.
- **Hostname:** L'hostname mostrato nella UI è sempre quello letto via polling API dal campo description della loopback, oppure '?' se non disponibile. La sincronizzazione è in tempo reale.
- **Token:** La UI mostra solo i token e il timer del giocatore locale. I token degli altri giocatori non sono mai visibili.
- **Nome giocatore:** Il nome del giocatore locale viene visualizzato nella UI sopra i token, in alto a sinistra, e viene troncato con '...' se troppo lungo per lo spazio disponibile.
- **Sincronizzazione:** Tutta la logica di claim, colore e hostname è sincronizzata tra client e router reali tramite API, senza stato locale persistente.
- **UI:** La logica di disegno dei router nella UI è:
    - Se `claimed_by` è None → colore grigio
    - Se `claimed_by` è 0 (player locale) → colore player 0
    - (Altri player non sono mai visualizzati in questa versione)

- **Legenda:**
  - In basso nella UI è sempre presente una legenda che spiega i colori e i simboli.
  - La legenda mostra solo:
    - Grigio: router non claimato
    - Colore player: router claimato dal giocatore locale
  - Non sono più presenti riferimenti o colori relativi ad altri giocatori.

- **Changelog**
  - [26/05/2025] Consolidate e chiarite tutte le regole di claim, colore, hostname e token nel GDD. La UI e la logica sono ora perfettamente allineate alle specifiche.
  - [26/05/2025] Il nome del giocatore locale viene ora visualizzato nella UI sopra i token, in alto a sinistra, e viene troncato con '...' se troppo lungo per lo spazio disponibile.

- **Schema ASCII di un router nella UI:**

  Esempio di rappresentazione di un router con le frecce delle interfacce e il box hostname:

  ```
      ↑
    ┌───┐
←  │  ●  │  →
    └───┘
      ↓
     [hostname]
  ```

  Dove:
  - Il cerchio pieno (●) rappresenta il router.
  - Le frecce (↑, ↓, ←, →) rappresentano le interfacce nord, sud, ovest, est.
  - Il box rettangolare sotto il router mostra l'hostname.
  - Il colore del cerchio indica lo stato claim (grigio = non claimato, colore player = claimato dal giocatore locale).
  - Le frecce sono colorate (verde = up, rosso = down, giallo = non configurata, giallo evidenziato all'hover).

  Esempio con tutte le frecce attive (up):

  ```
      ↑
    ┌───┐
←  │  ●  │  →
    └───┘
      ↓
     [Router1]
  ```

  Esempio con alcune interfacce down (rosse):

  ```
      ↑
    ┌───┐
X  │  ●  │  →
    └───┘
      ↓
     [Router2]
  ```
  (dove X indica una freccia rossa, cioè interfaccia down)

  Nota: la rappresentazione grafica reale è in pixel-art, ma lo schema ASCII aiuta a comprendere la disposizione degli elementi nella UI.

---

## 11.1 Mockup e schermate ASCII della UI

Di seguito alcuni esempi di schermate ASCII che illustrano la disposizione degli elementi principali della UI, lo stato dei router, la visualizzazione dei token, del timer, del nome giocatore e della legenda.

### Schermata principale: griglia router 4x4 (esempio semplificato)

```
╔════════════════════════════════════════════════════════════════════╗
║  Giocatore: Alice      Token: ●●●●   Timer: 08s                  ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                  ║
║      ↑           ↑           ↑           ↑                       ║
║    ┌───┐       ┌───┐       ┌───┐       ┌───┐                     ║
║ ← │ ● │ →   ← │ ● │ →   ← │ ● │ →   ← │ ● │ →                   ║
║    └───┘       └───┘       └───┘       └───┘                     ║
║      ↓           ↓           ↓           ↓                       ║
║   [R1]        [R2]        [R3]        [R4]                      ║
║                                                                  ║
║      ↑           ↑           ↑           ↑                       ║
║    ┌───┐       ┌───┐       ┌───┐       ┌───┐                     ║
║ ← │ ● │ →   ← │ ● │ →   ← │ ● │ →   ← │ ● │ →                   ║
║    └───┘       └───┘       └───┘       └───┘                     ║
║      ↓           ↓           ↓           ↓                       ║
║   [R5]        [R6]        [R7]        [R8]                      ║
║                                                                  ║
║      ↑           ↑           ↑           ↑                       ║
║    ┌───┐       ┌───┐       ┌───┐       ┌───┐                     ║
║ ← │ ● │ →   ← │ ● │ →   ← │ ● │ →   ← │ ● │ →                   ║
║    └───┘       └───┘       └───┘       └───┘                     ║
║      ↓           ↓           ↓           ↓                       ║
║   [R9]       [R10]       [R11]       [R12]                      ║
║                                                                  ║
║      ↑           ↑           ↑           ↑                       ║
║    ┌───┐       ┌───┐       ┌───┐       ┌───┐                     ║
║ ← │ ● │ →   ← │ ● │ →   ← │ ● │ →   ← │ ● │ →                   ║
║    └───┘       └───┘       └───┘       └───┘                     ║
║      ↓           ↓           ↓           ↓                       ║
║  [R13]      [R14]      [R15]      [R16]                         ║
║                                                                  ║
╚════════════════════════════════════════════════════════════════════╝
Legenda: ● grigio = router non claimato, ● blu = router claimato dal giocatore locale
         ↑/→/↓/← verdi = interfaccia up, rosse = interfaccia down, gialle = non configurata
         [Rx] = hostname del router (o '?' se non disponibile)

```

### Esempio di router claimato e interfacce up/down

```
      ↑
    ┌───┐
X  │ ● │  →
    └───┘
      ↓
   [Router2]
```
Dove:
- ● blu = router claimato dal giocatore locale
- X = freccia rossa (interfaccia ovest down)
- → = freccia verde (interfaccia est up)
- ↑, ↓ = altre interfacce (colore variabile)
- [Router2] = hostname letto via API

### Barra superiore con nome giocatore troncato

```
Giocatore: SuperLongNa...   Token: ●●●   Timer: 04s
```

### Legenda in basso

```
Legenda: ● grigio = router non claimato, ● blu = router claimato dal giocatore locale
         ↑/→/↓/← verdi = interfaccia up, rosse = interfaccia down, gialle = non configurata
         [Rx] = hostname del router (o '?' se non disponibile)
```

### Esempio di router con hostname mancante

```
      ↑
    ┌───┐
←  │ ● │  →
    └───┘
      ↓
     [?]
```

---

## 4. Gameplay e Funzionalità Principali

- All’avvio della partita, il gioco chiede al giocatore di inserire il proprio nome (max 10 caratteri).
- Quando un giocatore effettua il claim di un router, il campo hostname del router viene impostato nel formato:  
  **nomegiocatore_hostname**  
  Il campo hostname non può superare 10 caratteri.
- Fino a 4 giocatori, ognuno con il proprio client su PC, interagiscono contemporaneamente e indipendentemente con la stessa infrastruttura di rete reale.
- Ogni client legge e scrive lo stato di gioco direttamente sui router tramite API.
- Il gioco è realtime: ogni giocatore può agire in qualsiasi momento, effettuando claim di router non ancora assegnati o abilitando/disabilitando le interfacce dei router di cui è proprietario.
- Ogni azione consuma un token; ogni giocatore inizia con 4 token e ne riceve 1 aggiuntivo **ogni 10 secondi** (timer visibile).
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

## 5. Regole e Parametri

- Ogni azione (claim o abilitazione/disabilitazione interfaccia) consuma un token.
- Ogni giocatore inizia con 4 token.
- **Ogni 10 secondi viene ricaricato 1 token a ogni giocatore.**
- Solo una interfaccia abilitabile/disabilitabile per azione e solo su router propri.
- Mouse/tastiera solo per hostname.
- Stato sempre aggiornato dai dispositivi reali.
- Nome giocatore massimo 10 caratteri.
- Hostname massimo 10 caratteri (inclusi eventuali separatori e nomegiocatore).
- Tutte le interazioni di gioco avvengono tramite mouse: il giocatore può selezionare router, claimare, attivare/disattivare interfacce, aprire popup info, glossario e tutorial solo tramite click o tap.
- L'unico uso della tastiera è per l'inserimento del nome giocatore e dell'hostname quando richiesto (popup di input testuale).
- Non sono previsti shortcut da tastiera per azioni di gioco (claim, attiva interfaccia, info, glossario, tutorial, ecc.): tutte queste azioni sono accessibili solo tramite pulsanti o click nella UI.
- La UI mostra sempre pulsanti o icone cliccabili per ogni azione disponibile.

---

## 6. UI & Grafica

- **Gioco 2D, schermo intero, stile retro gaming pixel-art**
- **Palette colori:** Pastello (esempi: azzurro chiaro, rosa, lilla, verde menta, giallo pallido)
- UI adattiva, leggibile, centrata, senza overflow
- Visualizzazione dello stato in tempo reale tramite letture dai dispositivi
- Stato token, timer, azioni disponibili e stato dei router sempre visibili e aggiornati dinamicamente
- Visualizzazione grafica dei link attivi tra router con neighborship di routing attiva
- Hostname router sempre visibile
- ID router solo a terminale per debug
- Glossario accessibile dal menu e in-game
- **Un router di cui non è stato fatto il claim viene visualizzato di colore grigio nella UI.**

### 6.1 Dettaglio: Regole di disegno di un router nella UI

Ogni router nella UI viene rappresentato secondo queste regole grafiche:

- **Forma base:**
  - Cerchio pieno, dimensione adattiva in base alla griglia e alla risoluzione.
  - Colore:
    - Grigio (libero, non claimato; ovvero nessun giocatore ha ancora effettuato il claim sul router)
    - Blu (claimato da un giocatore, colore del giocatore)
    - Bordo giallo spesso 3 pixel se router obiettivo già claimato
- **Interfacce:**
  - Quattro frecce spesse (5px) orientate verso nord, sud, est, ovest, sempre visibili.
  - Le frecce sono disegnate **all'interno** del cerchio del router, puntando dal bordo verso il centro.
  - Colore frecce:
    - Verde (interfaccia up)
    - Rosso (interfaccia down)
    - Giallo (interfaccia non configurata)
  - Quando il mouse passa sopra una freccia, questa viene evidenziata in giallo.
  - Le frecce sono disegnate in modo da non sovrapporsi al cerchio del router.
- **Link attivi:**
  - Linee tratteggiate tra i router con neighborship attiva, colore verde.
  - Le linee sono disegnate in modo da non sovrapporsi al cerchio del router.
  - Le linee sono bidirezionali e mostrano lo stato attivo della connessione.
- **Router obiettivo:**
  - Se il router è un obiettivo del livello, il suo bordo è evidenziato in giallo spesso 3 pixel.
  - Il colore del bordo giallo non cambia in base al claim del router.
- **Stato del router:**
  - Se il router è claimato, il suo colore di sfondo è quello del giocatore che lo ha claimato.
  - Se il router non è claimato, il colore di sfondo è grigio.
- **Stato delle interfacce:**
  - Le frecce delle interfacce sono sempre visibili, ma il loro colore cambia in base allo stato:
    - Verde se l'interfaccia è attiva (up, cioè 'admin up' secondo lo stato appreso dalla chiamata API ricorrente)
    - Rosso se l'interfaccia è inattiva (down, cioè 'admin down' secondo lo stato appreso dalla chiamata API ricorrente)
- **Hostname:**
  - Box rettangolare adattivo sempre visibile sotto ogni router, con bordo bianco e sfondo scuro.
  - Testo hostname sempre centrato e mai troncato.
  - Il box mostra sempre il valore aggiornato dal polling API, oppure '?' se non disponibile, senza ritardi o desincronizzazioni.
- **Feedback visivo:**
  - Quando un router viene claimato, il colore del cerchio cambia immediatamente e viene mostrato un messaggio di conferma.
  - Quando un’interfaccia viene attivata/disattivata, il colore della freccia cambia in tempo reale.
- **Hover e click:**
  - Al passaggio del mouse su un router, il suo colore di sfondo diventa leggermente più chiaro per indicare che è selezionato.
  - Al click su un router:
    - Se il router non è claimato, viene avviata la procedura di claim.
    - Se il router è già claimato dal giocatore locale, il click non mostra più la finestra informativa (popup) ma non fa nulla (o in futuro potrà attivare altre azioni contestuali).
- **ID router:**
  - Gli ID (global_id, local_id, group_id) non sono visibili nella UI, ma vengono stampati a terminale per debug quando si seleziona il router.
- **Posizionamento:**
  - Il router è centrato nella cella della griglia, con padding per evitare sovrapposizioni.
- **Legenda:**
  - In basso nella UI è sempre presente una legenda che spiega i colori e i simboli.
  - La legenda mostra solo:
    - Grigio: router non claimato
    - Colore player: router claimato dal giocatore locale
  - Non sono più presenti riferimenti o colori relativi ad altri giocatori.

#### Aggiornamenti e miglioramenti UI (storico changelog integrato)

- La visualizzazione dell'hostname nella UI è sempre aggiornata in tempo reale grazie alla chiamata continua di update_from_api().
- Il box hostname sotto il router mostra sempre il valore aggiornato o '?' se non disponibile, senza ritardi o desincronizzazioni.
- La UI mostra solo il numero di token e il timer del giocatore locale. I token degli altri giocatori non sono mai visualizzati.
- Ogni giocatore vede e gestisce solo i propri token nella UI. I token degli altri giocatori non sono più visibili o mostrati.
- La barra superiore visualizza solo i token e il timer del giocatore corrente.
- Un router è considerato claimato dal giocatore locale solo se il campo description della sua interfaccia loopback è nel formato `nomegiocatore_hostnameRouterVirtuale` e il `nomegiocatore` coincide esattamente con quello inserito dal giocatore locale. Se il nomegiocatore nella description è diverso dal nome inserito dal giocatore locale, il router è considerato sempre non claimato (colore grigio nella UI, azioni non permesse).
- Il claim non è più gestito solo localmente, ma sincronizzato tramite la description della loopback letta via API.
- La colorazione e lo stato claim dei router sono determinati dal confronto tra il nomegiocatore locale e quello letto dalla description della loopback.
- Un router con description valorizzata ma nomegiocatore diverso da quello locale appare sempre come non claimato (grigio) e non può essere gestito dal giocatore locale.
- La logica di claim di un router si basa ora sul parsing del campo description della loopback: se il nomegiocatore letto coincide con quello locale, il router risulta claimato dal giocatore. Altrimenti, è sempre considerato libero per il client locale.
- La logica di estrazione hostname è robusta rispetto a dati assenti o vuoti nelle risposte API: il client imposta sempre l'hostname a '?' se l'interfaccia Loopback{group_id} non è presente o il campo description è vuoto.
- L'hostname viene aggiornato solo se il campo description è presente e non vuoto.
- Il nome del giocatore locale viene visualizzato nella UI sopra i token, in alto a sinistra, e viene troncato con '...' se troppo lungo per lo spazio disponibile.

---

## 7. Dettaglio: Sistema di ID dei Router

### Tipologie di ID
- **ID globale (global_id):**
  - Ogni router riceve un ID progressivo unico da 1 a N*N, assegnato riga per riga nella griglia.
  - Serve per identificare in modo univoco ogni router nella rete e per debug.
  - il global_id ha scarso valore pratico per il gioco.
- **ID locale (local_id):**
  - All’interno di ogni gruppo 2x2 di router, ogni router riceve un local_id da 1 a 4 secondo uno schema a scacchiera (1,2,3,4).
  - Utilizzato per la corrispondenza con la numerazione delle interfacce e per le chiamate API.
  - Il local_id rappresenta l'identificativo del router reale.
- **ID gruppo (group_id):**
  - Ogni gruppo 2x2 di router riceve un group_id progressivo.
  - Serve per identificare i router che fanno parte dello stesso gruppo logico (ad esempio per le chiamate API alle LoopbackX).
  - Il group_id rappresenta la vrf (Virtual Routing and Forwarding) del router reale.

### Regole di visualizzazione e utilizzo
- Gli ID (global_id, local_id, group_id) **non sono visibili nella UI** accanto ai router durante il gioco normale.
- Quando si clicca su un router, i suoi ID vengono stampati a terminale per scopi di debug e sviluppo.
- In modalità API, gli ID sono utilizzati per:
  - Costruire l’indirizzo IP/hostname per la chiamata RESTCONF (es: https://198.18.1.1X dove X è il local_id).
  - Identificare l’interfaccia LoopbackX (dove X è il group_id) per recuperare l’hostname dinamico tramite API.
- In modalità tutorial, gli ID sono usati solo internamente e non sono mai mostrati all’utente.

### Assegnazione degli ID (algoritmo)
- All’avvio della partita, dopo la creazione della griglia, viene eseguita l’assegnazione:
  - global_id: progressivo da 1 a N*N, riga per riga.
  - group_id: assegnato a blocchi 2x2 a scacchiera, non per riga. Ogni blocco 2x2 di router adiacenti condivide lo stesso group_id, che viene incrementato da sinistra a destra e dall'alto verso il basso.
  - local_id: da 1 a 4 all’interno di ogni blocco 2x2 secondo uno schema a scacchiera (1,2,3,4).

### Esempio pratico
- In una griglia 4x4:
  - global_id: 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16
  - group_id:
    1 1 2 2
    1 1 2 2
    3 3 4 4
    3 3 4 4
  - local_id: 1,2,3,4 in ogni blocco 2x2

- La funzione generate_ids in utils.py implementa questa logica.

### Debug e sviluppo
- Per facilitare il debug, ogni volta che si seleziona un router, i suoi ID vengono stampati a terminale.
- Questo aiuta a verificare la corretta corrispondenza tra UI, logica di gioco e chiamate API.

---

## 8. Motore API del Gioco
### Comportamento delle API
Il client del gioco interagisce con i router reali tramite API RESTCONF, utilizzando le seguenti regole e logiche:
### Comportamento delle API
- **Chiamate API periodiche:**  
  Le chiamate API verso i router reali NON vengono attivate dal passaggio del mouse, ma vengono effettuate periodicamente dal client sin dall'inizio della partita (es. ogni 3 secondi).
- **Memorizzazione locale:**  
  Tutte le informazioni rilevanti recuperate dalle API (hostname, stato delle interfacce, stato delle neighborship) vengono memorizzate localmente dal client.
- **Comportamento UI al passaggio del mouse:**  
  Quando il mouse passa sopra un router, viene visualizzato l’hostname che è già stato recuperato dal ciclo periodico di query API.  
  Non viene effettuata alcuna chiamata API al momento dell’interazione dell’utente.
- **Aggiornamento informazioni:**  
  Le informazioni mostrate in UI sono aggiornate periodicamente in base alla frequenza delle chiamate API di polling.  
  In caso di perdita temporanea di connessione o errore nelle API, le informazioni rimangono quelle dell’ultimo ciclo di polling riuscito.
- **API asincrone:**  
  Le chiamate API sono asincrone e non bloccano l'interfaccia utente.  
  Il client continua a funzionare normalmente anche se una chiamata API fallisce o impiega più tempo del previsto.

### Logica di recupero hostname
- **Obiettivo:**  
  Recuperare l'hostname configurato sul router reale per visualizzarlo nella UI.
- **Interfaccia Loopback:**
  - Ogni router ha un'interfaccia loopback configurata con un nome specifico: `LoopbackY`, dove `Y` è il `group_id` del router.
  - Questa interfaccia viene utilizzata per identificare il router e recuperare l'hostname.
### Chiamata API per hostname
- **Endpoint RESTCONF:**
  - URL: `https://198.18.1.1X/restconf/data/ietf-interfaces:interfaces` dove `X` è il `local_id` del router selezionato.
  - Autenticazione: Basic Auth (username: `cisco`, password: `C1sco12345`).
  - Content-Type: `application/yang-data+json`
- **Logica di ricerca hostname:**
  - Viene cercata l'interfaccia `LoopbackY` dove `Y` è il `group_id` del router.
  - Il campo `description` di questa interfaccia viene utilizzato come hostname da mostrare nella UI.
- **Esempio di chiamata:**
  - Per un router con `local_id=3` e `group_id=2`:
    - URL: `https://198.18.1.13/restconf/data/ietf-interfaces:interfaces`
    - Si cerca l'interfaccia `Loopback2` e si legge il campo `description`.
- **Fallback:**
  - Se la chiamata fallisce o l'interfaccia non è presente, viene mostrato un hostname di default (`?`) oppure l'ultimo valore di hostname disponibile.

Questa logica consente di visualizzare in tempo reale l'hostname configurato realmente sul router (in base all’ultimo polling riuscito), favorendo apprendimento e troubleshooting.

### Logica di settaggio hostname
- **Obiettivo:**  
  Permettere ai giocatori di impostare l'hostname del router reale tramite l'interfaccia loopback.
- **Interfaccia Loopback:**
  - Ogni router ha un'interfaccia loopback configurata con un nome specifico: `LoopbackY`, dove `Y` è il `group_id` del router.
  - Questa interfaccia viene utilizzata per identificare il router e impostare l'hostname.
### Chiamata API per impostare hostname
- **Endpoint RESTCONF:**
  - URL: `https://198.18.1.1X/restconf/data/ietf-interfaces:interfaces/interface=LoopbackY`
  - Autenticazione: Basic Auth (username: `cisco`, password: `C1sco12345`).
  - Content-Type: `application/yang-data+json`
  - metodo: 'PUT'
- **Payload:**
    - Il payload deve contenere il campo `description` con il nuovo hostname.
    - Esempio di payload:
        ```json
            {
            "interface": [
                {
                "name": "Loopback1",
                "type": "iana-if-type:softwareLoopback",
                "description": "nomegiocatore_hostname"
                }
            ]
            }
        ```
- **Esempio di chiamata:**
  - Per un router con `local_id=3` e `group_id=2`, per impostare l'hostname a `Alice_Router`:
    - URL: `https://198.18.1.13/restconf/data/ietf-interfaces:interfaces/interface=Loopback2`
- **Esecuzione:**
  - Quando un giocatore effettua il claim di un router, il client invia questa chiamata API per impostare l'hostname.
  - Se la chiamata ha successo, l'hostname viene aggiornato. Non avviene nessuna memorizzazione locale dell'hostname.

### 8.1 Ottenimento della tabella di routing di un router (modalità API)

Per ottenere la tabella di routing di un router reale, il client deve effettuare la seguente chiamata API RESTCONF:

```
restconf/data/ietf-routing:routing-state/routing-instance
```

Questa chiamata restituisce lo stato di routing, inclusa la tabella di routing attuale del router.

> **Nota:** In futuro verranno aggiunti esempi pratici di risposta dell’API e di parsing delle rotte rilevanti.

---

## 9. Dettaglio: Collegamento Fisico e Logico dei Router (VLAN e link tra router)

### Collegamento fisico
- Ogni router reale è fisicamente connesso alla rete tramite la sua interfaccia **GigabitEthernet1**.

### Collegamento logico tramite VLAN
- Tutti i link tra router (ovvero le interfacce nord, sud, est, ovest nel gioco) sono realizzati tramite **interfacce logiche VLAN** (sub-interface) sulla stessa GigabitEthernet1.
- **Ciascun link tra due router** all’interno di un gruppo 2x2 è rappresentato da una VLAN univoca.

  - **Regola generale**:  
    Il numero VLAN è creato concatenando **group_id** + **local_id_A** + **local_id_B**, dove A e B sono i due router collegati.  
    L’ordine non conta, il link è bidirezionale.
    **local_id_A** è sempre inferiore a  **local_id_B**

  - **Esempi**:  
    - _VLAN 312_ rappresenta il link nel gruppo 3 tra router 1 e router 2 (e viceversa, il link è bidirezionale).
    - _VLAN 434_ rappresenta nel gruppo 4 il link tra router 3 e router 4 (e viceversa).

#### Mappatura e gestione dei link
- Ogni interfaccia logica di collegamento (n/s/e/w nel gioco) corrisponde a una sub-interface configurata su GigabitEthernet1, con il numero VLAN che rappresenta univocamente il link tra i due router del gruppo.
- Il link è **bidirezionale** e il numero VLAN è lo stesso su entrambi i router coinvolti.
- Quando un link viene “attivato” o “disattivato” nel gioco, la relativa sub-interface (es: `GigabitEthernet1.312`) viene abilitata/disabilitata via API.
- La UI riflette lo stato up/down della VLAN (interfaccia logica/link) con le frecce verdi/rosse.
- L’identificativo VLAN può essere mostrato a scopo didattico nel glossario o in una schermata avanzata/debug.

**Stato neighborship di routing:**  
Se una neighborship di routing è attiva su un link, il campo `description` della relativa sub-interface sarà impostato a `UP`.  
Se il campo `description` della sub-interface è vuoto, significa che non esiste nessuna neighborship attiva su quel link.
Se tra due router esiste una neighborship attiva, la UI mostra una linea tratteggiata verde tra i due router, indicando che il link è attivo e funzionante.

#### Schema esempio

```
Gruppo 3 (group_id = 3):

Routers:
- Router 1 (local_id=1)
- Router 2 (local_id=2)
- Router 3 (local_id=3)
- Router 4 (local_id=4)

Link tra Router 1 e Router 2: VLAN 312 (GigabitEthernet1.312 su entrambi)
Link tra Router 3 e Router 4: VLAN 334 (GigabitEthernet1.334 su entrambi)
Link tra Router 2 e Router 3: VLAN 323 (GigabitEthernet1.323 su entrambi)
...
```


---

## 10. Integrazione con la Rete Reale e Mockup

- Tutto lo stato di gioco è scritto/letto sui dispositivi reali via API.
- Parametri come hostname, stato delle interfacce e neighborship sono aggiornati in tempo reale.
- Le API sono utilizzate per leggere lo stato attuale della rete e per scrivere le modifiche apportate dai giocatori.
- In modalità offline, lo stato è simulato localmente.


---

## 11. Prototipo e Mockup

- Prototipazione con Figma/Excalidraw per griglia, feedback, ecc.



---

## 12. Audio

- Chiptune, SFX
- Musica di sottofondo in stile retro gaming
- Effetti sonori per azioni chiave (claim, attivazione link, errore, successo)
- Feedback audio per azioni di gioco (es. click, attivazione/disattivazione link)
- Effetti sonori per eventi di gioco (es. attivazione di un link, errore, successo)
- Volume regolabile tramite menu opzioni
- Opzioni per disattivare la musica o gli effetti sonori

---


## 13. Requisiti di Stile e Qualità del Codice

- Codice abbondantemente commentato: ogni funzione, classe, modulo e blocco logico deve essere documentato tramite commenti e docstring, per facilitare la comprensione e l’apprendimento.
- Codice pensato come materiale didattico: ogni concetto implementato, pattern o soluzione deve essere spiegato.
- Soluzioni semplici, leggibili e lineari preferite a quelle complesse, salvo necessità tecniche documentate.
- Best practice Python (PEP8), nomi chiari, separazione in moduli, attenzione alla manutenibilità.
- Dove utile, aggiungere esempi d’uso nei commenti/docstring.
- Logica di estrazione hostname robusta rispetto a dati assenti o vuoti nelle risposte API.

---

## 14. Glossario Interattivo in Game

Sezione accessibile dal menu e durante la partita dove il giocatore può consultare i principali concetti di networking:

- **Rete**: Insieme di dispositivi (computer, router, server) collegati tra loro per scambiarsi dati.
- **Router**: Dispositivo che indirizza i pacchetti di dati tra reti diverse.
- **Interfaccia**: Punto di connessione fisica o logica su un router (nord, sud, est, ovest nel gioco).
- **Interfaccia logica (sub-interface)**: Interfaccia virtuale creata su un'interfaccia fisica, identificata dal numero VLAN.
- **VLAN**: Rete virtuale che identifica univocamente un link tra due router reali.
- **Link**: Collegamento tra due dispositivi di rete che permette il passaggio delle informazioni.
- **Neighborship**: Relazione di vicinato tra due router che hanno instaurato una sessione di routing attiva.
- **Disservizio**: Situazione in cui una parte della rete o un link smette di funzionare correttamente.
- **Pacchetto**: Unità di dati che viaggia nella rete.
- **Routing**: Processo con cui un router decide il percorso migliore per un pacchetto.
- **API**: Interfaccia di programmazione delle applicazioni che permette al client di interagire con i router.

---

## 15. Condizione di Vittoria del Livello

La **condizione di vittoria di un livello** viene raggiunta quando, in almeno uno dei router obiettivo, la sua tabella di routing contiene le rotte verso le loopback di **tutti** i router obiettivo.

### Definizione di router obiettivo

I **router obiettivo** sono quelli identificati dalle coppie (groupID, localID) specificate per il livello.  
Esempio:  
- (1,1)  
- (4,1)

### Indirizzamento delle loopback

L’indirizzo IP della loopback per ogni router obiettivo segue la convenzione:
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
In altre parole, la tabella deve contenere tutte le destinazioni del tipo G.0.0. L dove (G,L) sono le coppie dei router obiettivo.

### Nota
- Il controllo della vittoria avviene periodicamente (sincronizzato con il polling delle API).
- La verifica può essere visualizzata nella UI tramite un indicatore di progresso o stato.

---

## 16. Ottenimento della tabella di routing di un router (modalità API)

Per ottenere la tabella di routing di un router reale, il client deve effettuare la seguente chiamata API RESTCONF:

```
restconf/data/ietf-routing:routing-state/routing-instance
```

Questa chiamata restituisce lo stato di routing, inclusa la tabella di routing attuale del router.

> **Nota:** In futuro verranno aggiunti esempi pratici di risposta dell’API e di parsing delle rotte rilevanti.

---

**Nota Bene:**  
Mockup grafici consigliati per la presentazione ufficiale.

---

## Specifiche tecniche

- **Linguaggio:** Python 3.x
- **Libreria grafica:** Pygame (ultima versione stabile)
- **Struttura modulare:** Il codice deve essere suddiviso in moduli separati per logica di gioco, gestione API, rendering UI, gestione eventi, glossario/tutorial, e configurazione.
- **Compatibilità:** Il gioco deve funzionare su Windows, macOS e Linux senza modifiche sostanziali.
- **Gestione dipendenze:** Fornire un file `requirements.txt` con tutte le dipendenze necessarie (incluso Pygame e librerie per richieste HTTP come `requests`).
- **API RESTCONF:** Tutte le chiamate API devono essere indirizzate esclusivamente ai 4 router fisici reali, utilizzando la logica di VRF per virtualizzare la griglia NxN.
- **Debug API:** Ogni chiamata API (claim, interfaccia, hostname, stato) deve essere stampata a terminale in modo conciso: solo metodo, endpoint, status code e, in caso di errore, il messaggio di errore.
- **Interazione:** Tutte le azioni di gioco sono accessibili solo tramite mouse (eccetto input nome/hostname tramite tastiera).
- **Polling API:** Le chiamate API di polling verso i router reali devono essere eseguite periodicamente in loop asincrono, senza bloccare la UI.
- **Documentazione:** Tutto il codice deve essere abbondantemente commentato e documentato secondo le best practice Python (PEP8, docstring, esempi d’uso dove utile).
- **Mockup:** La UI deve essere fedele ai mockup grafici allegati o descritti nel GDD.
- **Glossario e tutorial:** Devono essere integrati e accessibili in-game tramite pulsanti o menu.
- **Debug terminale:** Oltre alle API, anche la selezione di router/interfacce deve stampare a terminale gli ID e lo stato per facilitare il debug.
- **Architettura:** Prevedere una chiara separazione tra logica di gioco, interfaccia utente e gestione delle API.

---

## Regole per Copilot e AI Assistant

1. **Rispetta il GDD:** Tutte le implementazioni e suggerimenti devono essere coerenti con le specifiche e le regole descritte nel GDD.
2. **Mouse-driven:** Tutte le azioni di gioco (claim, attivazione/disattivazione interfacce, info, glossario, tutorial) devono essere accessibili solo tramite mouse, eccetto l’inserimento di nome/hostname che avviene tramite tastiera.
3. **Debug API:** Ogni chiamata API (claim, interfaccia, hostname, stato) deve essere stampata a terminale in modo conciso: solo metodo, endpoint, status code e, in caso di errore, il messaggio di errore.
4. **API RESTCONF:** Tutte le chiamate API devono essere indirizzate solo ai 4 router fisici reali, utilizzando la logica di VRF per virtualizzare la griglia NxN.
5. **Polling asincrono:** Le chiamate API di polling verso i router reali devono essere eseguite periodicamente in loop asincrono, senza bloccare la UI.
6. **Modularità:** Il codice deve essere suddiviso in moduli separati per logica di gioco, gestione API, rendering UI, gestione eventi, glossario/tutorial, e configurazione.
7. **Compatibilità:** Il gioco deve funzionare su Windows, macOS e Linux senza modifiche sostanziali.
8. **Documentazione:** Tutto il codice deve essere abbondantemente commentato e documentato secondo le best practice Python (PEP8, docstring, esempi d’uso dove utile).
9. **UI fedele ai mockup:** La UI deve essere fedele ai mockup grafici allegati o descritti nel GDD.
10. **Glossario e tutorial:** Devono essere integrati e accessibili in-game tramite pulsanti o menu.
11. **Debug terminale:** Oltre alle API, anche la selezione di router/interfacce deve stampare a terminale gli ID e lo stato per facilitare il debug.
12. **No shortcut tastiera:** Non devono essere implementate shortcut da tastiera per azioni di gioco.
13. **Gestione errori:** In caso di errore API, la UI mostra l’ultimo stato valido e segnala l’errore all’utente.
14. **Requisiti tecnici:** Utilizzare Python 3.x, Pygame, e fornire un file requirements.txt aggiornato.
15. **Suggerimento struttura file:**
    - `main.py`: entrypoint, ciclo principale e inizializzazione.
    - `config.py`: parametri di configurazione e costanti.
    - `api.py`: gestione delle chiamate RESTCONF e debug API.
    - `router_grid.py`: logica della griglia, assegnazione ID, gestione router e interfacce.
    - `ui.py`: rendering grafico, gestione pulsanti, popup, feedback visivi.
    - `events.py`: gestione eventi mouse, input nome/hostname.
    - `glossary.py`: gestione glossario e tutorial interattivo.
    - `audio.py`: gestione effetti sonori e musica.
    - `utils.py`: funzioni di utilità generiche.
    - `requirements.txt`: dipendenze Python.
    - `README.md`: istruzioni di avvio e note tecniche.

---

### [26/05/2025] Click destro: inventario router

- Al click destro su un router nella griglia, la UI mostra un popup riassuntivo dell'inventario del router selezionato.
  - Il popup inventario mostra: hostname, stato claim (TUO/No/Altro), token disponibili, ID router, stato e VLAN di tutte le interfacce, stato neighborship di ogni link.
  - Il popup si chiude con un click sinistro fuori dal popup.
- Il click sinistro mantiene il comportamento attuale (claim/interfaccia).
- La logica è documentata in ui.py e events.py.

---

## [26/05/2025] Miglioramento logica hostname in polling API

- **Sezione 8: Motore API del Gioco**
  - Aggiornata la descrizione della logica di polling per l'hostname:
    - Ora il client imposta sempre l'hostname a '?' se l'interfaccia Loopback{group_id} non è presente o il campo description è vuoto.
    - L'hostname viene aggiornato solo se il campo description è presente e non vuoto.
    - Questo garantisce che la UI mostri sempre un valore coerente e mai stringhe vuote o valori obsoleti.

- **Sezione 6: UI & Grafica**
  - Chiarito che il box hostname sotto il router mostra sempre il valore aggiornato dal polling API, oppure '?' se non disponibile.
  - Aggiornata la descrizione della barra superiore: ora visualizza solo i token e il timer del giocatore corrente.

- **Sezione 13: Requisiti di Stile e Qualità del Codice**
  - Specificato che la logica di estrazione dell'hostname deve essere robusta rispetto a dati assenti o vuoti nelle risposte API.

- **Changelog**
  - [26/05/2025] Migliorata la robustezza della logica di visualizzazione hostname nella UI: ora viene sempre mostrato il valore corretto o un fallback sicuro ('?').

## [26/05/2025] Sincronizzazione hostname in tempo reale nella UI

- **Sezione 6: UI & Grafica**
  - La UI ora aggiorna e visualizza l'hostname di ogni router in tempo reale, sincronizzandolo ad ogni frame con lo stato più recente ottenuto dal polling API.
  - Il box hostname sotto il router mostra sempre il valore aggiornato o '?' se non disponibile, senza ritardi o desincronizzazioni.

- **Sezione 8: Motore API del Gioco**
  - Chiarito che la funzione di aggiornamento della UI richiama la logica di polling API ad ogni frame, garantendo la coerenza tra stato reale e visualizzazione.

- **Changelog**
  - [26/05/2025] La visualizzazione dell'hostname nella UI è ora sempre aggiornata in tempo reale grazie alla chiamata continua di update_from_api().

## [26/05/2025] Rimozione riferimenti ai token degli altri giocatori

- **Sezione 4: Gameplay e Funzionalità Principali**
  - Ogni giocatore vede e gestisce solo i propri token nella UI. I token degli altri giocatori non sono più visibili o mostrati.

- **Sezione 6: UI & Grafica**
  - La UI mostra solo il numero di token e il timer del giocatore locale. I token degli altri giocatori non sono mai visualizzati.
  - Aggiornata la descrizione della barra superiore: ora visualizza solo i token e il timer del giocatore corrente.

- **Mockup**
  - Aggiornati i mockup testuali per riflettere che solo i token del giocatore locale sono visibili.

- **Changelog**
  - [26/05/2025] Rimossi tutti i riferimenti e la visualizzazione dei token degli altri giocatori dalla UI e dal GDD. Ora ogni giocatore vede solo i propri token e timer.

## [26/05/2025] Claim router tramite parsing nomegiocatore nella description della loopback

- **Sezione 4: Gameplay e Funzionalità Principali**
  - Un router è considerato claimato dal giocatore locale solo se il campo description della sua interfaccia loopback è nel formato `nomegiocatore_hostnameRouterVirtuale` **e il `nomegiocatore` coincide esattamente con quello inserito dal giocatore locale**.
  - Se il nomegiocatore nella description è diverso dal nome inserito dal giocatore locale, il router è considerato sempre non claimato (colore grigio nella UI, azioni non permesse).
  - Il claim non è più gestito solo localmente, ma sincronizzato tramite la description della loopback letta via API.

- **Sezione 6: UI & Grafica**
  - La colorazione e lo stato claim dei router sono determinati dal confronto tra il nomegiocatore locale e quello letto dalla description della loopback.
  - Un router con description valorizzata ma nomegiocatore diverso da quello locale appare sempre come non claimato (grigio) e non può essere gestito dal giocatore locale.

- **Sezione 8: Motore API del Gioco**
  - La logica di claim di un router si basa ora sul parsing del campo description della loopback: se il nomegiocatore letto coincide con quello locale, il router risulta claimato dal giocatore. Altrimenti, è sempre considerato libero per il client locale.
  - Aggiornata la descrizione del formato della description: sempre `nomegiocatore_hostnameRouterVirtuale`.

- **Changelog**
  - [26/05/2025] Il claim dei router è ora determinato dal parsing del campo description della loopback, in formato `nomegiocatore_hostnameRouterVirtuale`, e sincronizzato tra tutti i client tramite API. Un router con nomegiocatore diverso da quello locale è sempre considerato non claimato dal client locale.

## [26/05/2025] Consolidamento regole claim, colore e sincronizzazione hostname

- **Claim router:** Un router è considerato claimato dal giocatore locale solo se il campo description della sua interfaccia loopback è nel formato `nomegiocatore_hostnameRouterVirtuale` **e il `nomegiocatore` coincide esattamente con quello inserito dal giocatore locale**. In tutti gli altri casi (description mancante, vuota, o nomegiocatore diverso), il router è considerato non claimato dal client locale.
- **Colore router:** Un router non claimato (cioè non claimato dal giocatore locale) viene sempre visualizzato di colore grigio (`config.GRAY`) nella UI, indipendentemente dal contenuto del campo hostname/description. Solo i router effettivamente claimati dal giocatore locale sono colorati con il colore del player.
- **Hostname:** L'hostname mostrato nella UI è sempre quello letto via polling API dal campo description della loopback, oppure '?' se non disponibile. La sincronizzazione è in tempo reale.
- **Token:** La UI mostra solo i token e il timer del giocatore locale. I token degli altri giocatori non sono mai visibili.
- **Nome giocatore:** Il nome del giocatore locale viene visualizzato nella UI sopra i token, in alto a sinistra, e viene troncato con '...' se troppo lungo per lo spazio disponibile.
- **Sincronizzazione:** Tutta la logica di claim, colore e hostname è sincronizzata tra client e router reali tramite API, senza stato locale persistente.
- **UI:** La logica di disegno dei router nella UI è:
    - Se `claimed_by` è None → colore grigio
    - Se `claimed_by` è 0 (player locale) → colore player 0
    - (Altri player non sono mai visualizzati in questa versione)

- **Legenda:**
  - In basso nella UI è sempre presente una legenda che spiega i colori e i simboli.
  - La legenda mostra solo:
    - Grigio: router non claimato
    - Colore player: router claimato dal giocatore locale
  - Non sono più presenti riferimenti o colori relativi ad altri giocatori.

- **Changelog**
  - [26/05/2025] Consolidate e chiarite tutte le regole di claim, colore, hostname e token nel GDD. La UI e la logica sono ora perfettamente allineate alle specifiche.
  - [26/05/2025] Il nome del giocatore locale viene ora visualizzato nella UI sopra i token, in alto a sinistra, e viene troncato con '...' se troppo lungo per lo spazio disponibile.

- **Schema ASCII di un router nella UI:**

  Esempio di rappresentazione di un router con le frecce delle interfacce e il box hostname:

  ```
      ↑
    ┌───┐
←  │  ●  │  →
    └───┘
      ↓
     [hostname]
  ```

  Dove:
  - Il cerchio pieno (●) rappresenta il router.
  - Le frecce (↑, ↓, ←, →) rappresentano le interfacce nord, sud, ovest, est.
  - Il box rettangolare sotto il router mostra l'hostname.
  - Il colore del cerchio indica lo stato claim (grigio = non claimato, colore player = claimato dal giocatore locale).
  - Le frecce sono colorate (verde = up, rosso = down, giallo = non configurata, giallo evidenziato all'hover).

  Esempio con tutte le frecce attive (up):

  ```
      ↑
    ┌───┐
←  │  ●  │  →
    └───┘
      ↓
     [Router1]
  ```

  Esempio con alcune interfacce down (rosse):

  ```
      ↑
    ┌───┐
X  │  ●  │  →
    └───┘
      ↓
     [Router2]
  ```
  (dove X indica una freccia rossa, cioè interfaccia down)

  Nota: la rappresentazione grafica reale è in pixel-art, ma lo schema ASCII aiuta a comprendere la disposizione degli elementi nella UI.

---

## 11.1 Mockup e schermate ASCII della UI

Di seguito alcuni esempi di schermate ASCII che illustrano la disposizione degli elementi principali della UI, lo stato dei router, la visualizzazione dei token, del timer, del nome giocatore e della legenda.

### Schermata principale: griglia router 4x4 (esempio semplificato)

```
╔════════════════════════════════════════════════════════════════════╗
║  Giocatore: Alice      Token: ●●●●   Timer: 08s                  ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                  ║
║      ↑           ↑           ↑           ↑                       ║
║    ┌───┐       ┌───┐       ┌───┐       ┌───┐                     ║
║ ← │ ● │ →   ← │ ● │ →   ← │ ● │ →   ← │ ● │ →                   ║
║    └───┘       └───┘       └───┘       └───┘                     ║
║      ↓           ↓           ↓           ↓                       ║
║   [R1]        [R2]        [R3]        [R4]                      ║
║                                                                  ║
║      ↑           ↑           ↑           ↑                       ║
║    ┌───┐       ┌───┐       ┌───┐       ┌───┐                     ║
║ ← │ ● │ →   ← │ ● │ →   ← │ ● │ →   ← │ ● │ →                   ║
║    └───┘       └───┘       └───┘       └───┘                     ║
║      ↓           ↓           ↓           ↓                       ║
║   [R5]        [R6]        [R7]        [R8]                      ║
║                                                                  ║
║      ↑           ↑           ↑           ↑                       ║
║    ┌───┐       ┌───┐       ┌───┐       ┌───┐                     ║
║ ← │ ● │ →   ← │ ● │ →   ← │ ● │ →   ← │ ● │ →                   ║
║    └───┘       └───┘       └───┘       └───┘                     ║
║      ↓           ↓           ↓           ↓                       ║
║   [R9]       [R10]       [R11]       [R12]                      ║
║                                                                  ║
║      ↑           ↑           ↑           ↑                       ║
║    ┌───┐       ┌───┐       ┌───┐       ┌───┐                     ║
║ ← │ ● │ →   ← │ ● │ →   ← │ ● │ →   ← │ ● │ →                   ║
║    └───┘       └───┘       └───┘       └───┘                     ║
║      ↓           ↓           ↓           ↓                       ║
║  [R13]      [R14]      [R15]      [R16]                         ║
║                                                                  ║
╚════════════════════════════════════════════════════════════════════╝
Legenda: ● grigio = router non claimato, ● blu = router claimato dal giocatore locale
         ↑/→/↓/← verdi = interfaccia up, rosse = interfaccia down, gialle = non configurata
         [Rx] = hostname del router (o '?' se non disponibile)

```

### Esempio di router claimato e interfacce up/down

```
      ↑
    ┌───┐
X  │ ● │  →
    └───┘
      ↓
   [Router2]
```
Dove:
- ● blu = router claimato dal giocatore locale
- X = freccia rossa (interfaccia ovest down)
- → = freccia verde (interfaccia est up)
- ↑, ↓ = altre interfacce (colore variabile)
- [Router2] = hostname letto via API

### Barra superiore con nome giocatore troncato

```
Giocatore: SuperLongNa...   Token: ●●●   Timer: 04s
```

### Legenda in basso

```
Legenda: ● grigio = router non claimato, ● blu = router claimato dal giocatore locale
         ↑/→/↓/← verdi = interfaccia up, rosse = interfaccia down, gialle = non configurata
         [Rx] = hostname del router (o '?' se non disponibile)
```

### Esempio di router con hostname mancante

```
      ↑
    ┌───┐
←  │ ● │  →
    └───┘
      ↓
     [?]
```

---

## 4. Gameplay e Funzionalità Principali

- All’avvio della partita, il gioco chiede al giocatore di inserire il proprio nome (max 10 caratteri).
- Quando un giocatore effettua il claim di un router, il campo hostname del router viene impostato nel formato:  
  **nomegiocatore_hostname**  
  Il campo hostname non può superare 10 caratteri.
- Fino a 4 giocatori, ognuno con il proprio client su PC, interagiscono contemporaneamente e indipendentemente con la stessa infrastruttura di rete reale.
- Ogni client legge e scrive lo stato di gioco direttamente sui router tramite API.
- Il gioco è realtime: ogni giocatore può agire in qualsiasi momento, effettuando claim di router non ancora assegnati o abilitando/disabilitando le interfacce dei router di cui è proprietario.
- Ogni azione consuma un token; ogni giocatore inizia con 4 token e ne riceve 1 aggiuntivo **ogni 10 secondi** (timer visibile).
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

## 5. Regole e Parametri

- Ogni azione (claim o abilitazione/disabilitazione interfaccia) consuma un token.
- Ogni giocatore inizia con 4 token.
- **Ogni 10 secondi viene ricaricato 1 token a ogni giocatore.**
- Solo una interfaccia abilitabile/disabilitabile per azione e solo su router propri.
- Mouse/tastiera solo per hostname.
- Stato sempre aggiornato dai dispositivi reali.
- Nome giocatore massimo 10 caratteri.
- Hostname massimo 10 caratteri (inclusi eventuali separatori e nomegiocatore).
- Tutte le interazioni di gioco avvengono tramite mouse: il giocatore può selezionare router, claimare, attivare/disattivare interfacce, aprire popup info, glossario e tutorial solo tramite click o tap.
- L'unico uso della tastiera è per l'inserimento del nome giocatore e dell'hostname quando richiesto (popup di input testuale).
- Non sono previsti shortcut da tastiera per azioni di gioco (claim, attiva interfaccia, info, glossario, tutorial, ecc.): tutte queste azioni sono accessibili solo tramite pulsanti o click nella UI.
- La UI mostra sempre pulsanti o icone cliccabili per ogni azione disponibile.

---

## 6. UI & Grafica

- **Gioco 2D, schermo intero, stile retro gaming pixel-art**
- **Palette colori:** Pastello (esempi: azzurro chiaro, rosa, lilla, verde menta, giallo pallido)
- UI adattiva, leggibile, centrata, senza overflow
- Visualizzazione dello stato in tempo reale tramite letture dai dispositivi
- Stato token, timer, azioni disponibili e stato dei router sempre visibili e aggiornati dinamicamente
- Visualizzazione grafica dei link attivi tra router con neighborship di routing attiva
- Hostname router sempre visibile
- ID router solo a terminale per debug
- Glossario accessibile dal menu e in-game
- **Un router di cui non è stato fatto il claim viene visualizzato di colore grigio nella UI.**

### 6.1 Dettaglio: Regole di disegno di un router nella UI

Ogni router nella UI viene rappresentato secondo queste regole grafiche:

- **Forma base:**
  - Cerchio pieno, dimensione adattiva in base alla griglia e alla risoluzione.
  - Colore:
    - Grigio (libero, non claimato; ovvero nessun giocatore ha ancora effettuato il claim sul router)
    - Blu (claimato da un giocatore, colore del giocatore)
    - Bordo giallo spesso 3 pixel se router obiettivo già claimato
- **Interfacce:**
  - Quattro frecce spesse (5px) orientate verso nord, sud, est, ovest, sempre visibili.
  - Le frecce sono disegnate **all'interno** del cerchio del router, puntando dal bordo verso il centro.
  - Colore frecce:
    - Verde (interfaccia up)
    - Rosso (interfaccia down)
    - Giallo (interfaccia non configurata)
  - Quando il mouse passa sopra una freccia, questa viene evidenziata in giallo.
  - Le frecce sono disegnate in modo da non sovrapporsi al cerchio del router.
- **Link attivi:**
  - Linee tratteggiate tra i router con neighborship attiva, colore verde.
  - Le linee sono disegnate in modo da non sovrapporsi al cerchio del router.
  - Le linee sono bidirezionali e mostrano lo stato attivo della connessione.
- **Router obiettivo:**
  - Se il router è un obiettivo del livello, il suo bordo è evidenziato in giallo spesso 3 pixel.
  - Il colore del bordo giallo non cambia in base al claim del router.
- **Stato del router:**
  - Se il router è claimato, il suo colore di sfondo è quello del giocatore che lo ha claimato.
  - Se il router non è claimato, il colore di sfondo è grigio.
- **Stato delle interfacce:**
  - Le frecce delle interfacce sono sempre visibili, ma il loro colore cambia in base allo stato:
    - Verde se l'interfaccia è attiva (up, cioè 'admin up' secondo lo stato appreso dalla chiamata API ricorrente)
    - Rosso se l'interfaccia è inattiva (down, cioè 'admin down' secondo lo stato appreso dalla chiamata API ricorrente)
- **Hostname:**
  - Box rettangolare adattivo sempre visibile sotto ogni router, con bordo bianco e sfondo scuro.
  - Testo hostname sempre centrato e mai troncato.
  - Il box mostra sempre il valore aggiornato dal polling API, oppure '?' se non disponibile, senza ritardi o desincronizzazioni.
- **Feedback visivo:**
  - Quando un router viene claimato, il colore del cerchio cambia immediatamente e viene mostrato un messaggio di conferma.
  - Quando un’interfaccia viene attivata/disattivata, il colore della freccia cambia in tempo reale.
- **Hover e click:**
  - Al passaggio del mouse su un router, il suo colore di sfondo diventa leggermente più chiaro per indicare che è selezionato.
  - Al click su un router:
    - Se il router non è claimato, viene avviata la procedura di claim.
    - Se il router è già claimato dal giocatore locale, il click non mostra più la finestra informativa (popup) ma non fa nulla (o in futuro potrà attivare altre azioni contestuali).
- **ID router:**
  - Gli ID (global_id, local_id, group_id) non sono visibili nella UI, ma vengono stampati a terminale per debug quando si seleziona il router.
- **Posizionamento:**
  - Il router è centrato nella cella della griglia, con padding per evitare sovrapposizioni.
- **Legenda:**
  - In basso nella UI è sempre presente una legenda che spiega i colori e i simboli.
  - La legenda mostra solo:
    - Grigio: router non claimato
    - Colore player: router claimato dal giocatore locale
  - Non sono più presenti riferimenti o colori relativi ad altri giocatori.

#### Aggiornamenti e miglioramenti UI (storico changelog integrato)

- La visualizzazione dell'hostname nella UI è sempre aggiornata in tempo reale grazie alla chiamata continua di update_from_api().
- Il box hostname sotto il router mostra sempre il valore aggiornato o '?' se non disponibile, senza ritardi o desincronizzazioni.
- La UI mostra solo il numero di token e il timer del giocatore locale. I token degli altri giocatori non sono mai visualizzati.
- Ogni giocatore vede e gestisce solo i propri token nella UI. I token degli altri giocatori non sono più visibili o mostrati.
- La barra superiore visualizza solo i token e il timer del giocatore corrente.
- Un router è considerato claimato dal giocatore locale solo se il campo description della sua interfaccia loopback è nel formato `nomegiocatore_hostnameRouterVirtuale` e il `nomegiocatore` coincide esattamente con quello inserito dal giocatore locale. Se il nomegiocatore nella description è diverso dal nome inserito dal giocatore locale, il router è considerato sempre non claimato (colore grigio nella UI, azioni non permesse).
- Il claim non è più gestito solo localmente, ma sincronizzato tramite la description della loopback letta via API.
- La colorazione e lo stato claim dei router sono determinati dal confronto tra il nomegiocatore locale e quello letto dalla description della loopback.
- Un router con description valorizzata ma nomegiocatore diverso da quello locale appare sempre come non claimato (grigio) e non può essere gestito dal giocatore locale.
- La logica di claim di un router si basa ora sul parsing del campo description della loopback: se il nomegiocatore letto coincide con quello locale, il router risulta claimato dal giocatore. Altrimenti, è sempre considerato libero per il client locale.
- La logica di estrazione hostname è robusta rispetto a dati assenti o vuoti nelle risposte API: il client imposta sempre l'hostname a '?' se l'interfaccia Loopback{group_id} non è presente o il campo description è vuoto.
- L'hostname viene aggiornato solo se il campo description è presente e non vuoto.
- Il nome del giocatore locale viene visualizzato nella UI sopra i token, in alto a sinistra, e viene troncato con '...' se troppo lungo per lo spazio disponibile.

---

## 7. Dettaglio: Sistema di ID dei Router

### Tipologie di ID
- **ID globale (global_id):**
  - Ogni router riceve un ID progressivo unico da 1 a N*N, assegnato riga per riga nella griglia.
  - Serve per identificare in modo univoco ogni router nella rete e per debug.
  - il global_id ha scarso valore pratico per il gioco.
- **ID locale (local_id):**
  - All’interno di ogni gruppo 2x2 di router, ogni router riceve un local_id da 1 a 4 secondo uno schema a scacchiera (1,2,3,4).
  - Utilizzato per la corrispondenza con la numerazione delle interfacce e per le chiamate API.
  - Il local_id rappresenta l'identificativo del router reale.
- **ID gruppo (group_id):**
  - Ogni gruppo 2x2 di router riceve un group_id progressivo.
  - Serve per identificare i router che fanno parte dello stesso gruppo logico (ad esempio per le chiamate API alle LoopbackX).
  - Il group_id rappresenta la vrf (Virtual Routing and Forwarding) del router reale.

### Regole di visualizzazione e utilizzo
- Gli ID (global_id, local_id, group_id) **non sono visibili nella UI** accanto ai router durante il gioco normale.
- Quando si clicca su un router, i suoi ID vengono stampati a terminale per scopi di debug e sviluppo.
- In modalità API, gli ID sono utilizzati per:
  - Costruire l’indirizzo IP/hostname per la chiamata RESTCONF (es: https://198.18.1.1X dove X è il local_id).
  - Identificare l’interfaccia LoopbackX (dove X è il group_id) per recuperare l’hostname dinamico tramite API.
- In modalità tutorial, gli ID sono usati solo internamente e non sono mai mostrati all’utente.

### Assegnazione degli ID (algoritmo)
- All’avvio della partita, dopo la creazione della griglia, viene eseguita l’assegnazione:
  - global_id: progressivo da 1 a N*N, riga per riga.
  - group_id: assegnato a blocchi 2x2 a scacchiera, non per riga. Ogni blocco 2x2 di router adiacenti condivide lo stesso group_id, che viene incrementato da sinistra a destra e dall'alto verso il basso.
  - local_id: da 1 a 4 all’interno di ogni blocco 2x2 secondo uno schema a scacchiera (1,2,3,4).

### Esempio pratico
- In una griglia 4x4:
  - global_id: 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16
  - group_id:
    1 1 2 2
    1 1 2 2
    3 3 4 4
    3 3 4 4
  - local_id: 1,2,3,4 in ogni blocco 2x2

- La funzione generate_ids in utils.py implementa questa logica.

### Debug e sviluppo
- Per facilitare il debug, ogni volta che si seleziona un router, i suoi ID vengono stampati a terminale.
- Questo aiuta a verificare la corretta corrispondenza tra UI, logica di gioco e chiamate API.

---

## 8. Motore API del Gioco
### Comportamento delle API
Il client del gioco interagisce con i router reali tramite API RESTCONF, utilizzando le seguenti regole e logiche:
### Comportamento delle API
- **Chiamate API periodiche:**  
  Le chiamate API verso i router reali NON vengono attivate dal passaggio del mouse, ma vengono effettuate periodicamente dal client sin dall'inizio della partita (es. ogni 3 secondi).
- **Memorizzazione locale:**  
  Tutte le informazioni rilevanti recuperate dalle API (hostname, stato delle interfacce, stato delle neighborship) vengono memorizzate localmente dal client.
- **Comportamento UI al passaggio del mouse:**  
  Quando il mouse passa sopra un router, viene visualizzato l’hostname che è già stato recuperato dal ciclo periodico di query API.  
  Non viene effettuata alcuna chiamata API al momento dell’interazione dell’utente.
- **Aggiornamento informazioni:**  
  Le informazioni mostrate in UI sono aggiornate periodicamente in base alla frequenza delle chiamate API di polling.  
  In caso di perdita temporanea di connessione o errore nelle API, le informazioni rimangono quelle dell’ultimo ciclo di polling riuscito.
- **API asincrone:**  
  Le chiamate API sono asincrone e non bloccano l'interfaccia utente.  
  Il client continua a funzionare normalmente anche se una chiamata API fallisce o impiega più tempo del previsto.

### Logica di recupero hostname
- **Obiettivo:**  
  Recuperare l'hostname configurato sul router reale per visualizzarlo nella UI.
- **Interfaccia Loopback:**
  - Ogni router ha un'interfaccia loopback configurata con un nome specifico: `LoopbackY`, dove `Y` è il `group_id` del router.
  - Questa interfaccia viene utilizzata per identificare il router e recuperare l'hostname.
### Chiamata API per hostname
- **Endpoint RESTCONF:**
  - URL: `https://198.18.1.1X/restconf/data/ietf-interfaces:interfaces` dove `X` è il `local_id` del router selezionato.
  - Autenticazione: Basic Auth (username: `cisco`, password: `C1sco12345`).
  - Content-Type: `application/yang-data+json`
- **Logica di ricerca hostname:**
  - Viene cercata l'interfaccia `LoopbackY` dove `Y` è il `group_id` del router.
  - Il campo `description` di questa interfaccia viene utilizzato come hostname da mostrare nella UI.
- **Esempio di chiamata:**
  - Per un router con `local_id=3` e `group_id=2`:
    - URL: `https://198.18.1.13/restconf/data/ietf-interfaces:interfaces`
    - Si cerca l'interfaccia `Loopback2` e si legge il campo `description`.
- **Fallback:**
  - Se la chiamata fallisce o l'interfaccia non è presente, viene mostrato un hostname di default (`?`) oppure l'ultimo valore di hostname disponibile.

Questa logica consente di visualizzare in tempo reale l'hostname configurato realmente sul router (in base all’ultimo polling riuscito), favorendo apprendimento e troubleshooting.

### Logica di settaggio hostname
- **Obiettivo:**  
  Permettere ai giocatori di impostare l'hostname del router reale tramite l'interfaccia loopback.
- **Interfaccia Loopback:**
  - Ogni router ha un'interfaccia loopback configurata con un nome specifico: `LoopbackY`, dove `Y` è il `group_id` del router.
  - Questa interfaccia viene utilizzata per identificare il router e impostare l'hostname.
### Chiamata API per impostare hostname
- **Endpoint RESTCONF:**
  - URL: `https://198.18.1.1X/restconf/data/ietf-interfaces:interfaces/interface=LoopbackY`
  - Autenticazione: Basic Auth (username: `cisco`, password: `C1sco12345`).
  - Content-Type: `application/yang-data+json`
  - metodo: 'PUT'
- **Payload:**
    - Il payload deve contenere il campo `description` con il nuovo hostname.
    - Esempio di payload:
        ```json
            {
            "interface": [
                {
                "name": "Loopback1",
                "type": "iana-if-type:softwareLoopback",
                "description": "nomegiocatore_hostname"
                }
            ]
            }
        ```
- **Esempio di chiamata:**
  - Per un router con `local_id=3` e `group_id=2`, per impostare l'hostname a `Alice_Router`:
    - URL: `https://198.18.1.13/restconf/data/ietf-interfaces:interfaces/interface=Loopback2`
- **Esecuzione:**
  - Quando un giocatore effettua il claim di un router, il client invia questa chiamata API per impostare l'hostname.
  - Se la chiamata ha successo, l'hostname viene aggiornato. Non avviene nessuna memorizzazione locale dell'hostname.

### 8.1 Ottenimento della tabella di routing di un router (modalità API)

Per ottenere la tabella di routing di un router reale, il client deve effettuare la seguente chiamata API RESTCONF:

```
restconf/data/ietf-routing:routing-state/routing-instance
```

Questa chiamata restituisce lo stato di routing, inclusa la tabella di routing attuale del router.

> **Nota:** In futuro verranno aggiunti esempi pratici di risposta dell’API e di parsing delle rotte rilevanti.

---

## 9. Dettaglio: Collegamento Fisico e Logico dei Router (VLAN e link tra router)

### Collegamento fisico
- Ogni router reale è fisicamente connesso alla rete tramite la sua interfaccia **GigabitEthernet1**.

### Collegamento logico tramite VLAN
- Tutti i link tra router (ovvero le interfacce nord, sud, est, ovest nel gioco) sono realizzati tramite **interfacce logiche VLAN** (sub-interface) sulla stessa GigabitEthernet1.
- **Ciascun link tra due router** all’interno di un gruppo 2x2 è rappresentato da una VLAN univoca.

  - **Regola generale**:  
    Il numero VLAN è creato concatenando **group_id** + **local_id_A** + **local_id_B**, dove A e B sono i due router collegati.  
    L’ordine non conta, il link è bidirezionale.
    **local_id_A** è sempre inferiore a  **local_id_B**

  - **Esempi**:  
    - _VLAN 312_ rappresenta il link nel gruppo 3 tra router 1 e router 2 (e viceversa, il link è bidirezionale).
    - _VLAN 434_ rappresenta nel gruppo 4 il link tra router 3 e router 4 (e viceversa).

#### Mappatura e gestione dei link
- Ogni interfaccia logica di collegamento (n/s/e/w nel gioco) corrisponde a una sub-interface configurata su GigabitEthernet1, con il numero VLAN che rappresenta univocamente il link tra i due router del gruppo.
- Il link è **bidirezionale** e il numero VLAN è lo stesso su entrambi i router coinvolti.
- Quando un link viene “attivato” o “disattivato” nel gioco, la relativa sub-interface (es: `GigabitEthernet1.312`) viene abilitata/disabilitata via API.
- La UI riflette lo stato up/down della VLAN (interfaccia logica/link) con le frecce verdi/rosse.
- L’identificativo VLAN può essere mostrato a scopo didattico nel glossario o in una schermata avanzata/debug.

**Stato neighborship di routing:**  
Se una neighborship di routing è attiva su un link, il campo `description` della relativa sub-interface sarà impostato a `UP`.  
Se il campo `description` della sub-interface è vuoto, significa che non esiste nessuna neighborship attiva su quel link.
Se tra due router esiste una neighborship attiva, la UI mostra una linea tratteggiata verde tra i due router, indicando che il link è attivo e funzionante.

#### Schema esempio

```
Gruppo 3 (group_id = 3):

Routers:
- Router 1 (local_id=1)
- Router 2 (local_id=2)
- Router 3 (local_id=3)
- Router 4 (local_id=4)

Link tra Router 1 e Router 2: VLAN 312 (GigabitEthernet1.312 su entrambi)
Link tra Router 3 e Router 4: VLAN 334 (GigabitEthernet1.334 su entrambi)
Link tra Router 2 e Router 3: VLAN 323 (GigabitEthernet1.323 su entrambi)
...
```


---

## 10. Integrazione con la Rete Reale e Mockup

- Tutto lo stato di gioco è scritto/letto sui dispositivi reali via API.
- Parametri come hostname, stato delle interfacce e neighborship sono aggiornati in tempo reale.
- Le API sono utilizzate per leggere lo stato attuale della rete e per scrivere le modifiche apportate dai giocatori.
- In modalità offline, lo stato è simulato localmente.


---

## 11. Prototipo e Mockup

- Prototipazione con Figma/Excalidraw per griglia, feedback, ecc.



---

## 12. Audio

- Chiptune, SFX
- Musica di sottofondo in stile retro gaming
- Effetti sonori per azioni chiave (claim, attivazione link, errore, successo)
- Feedback audio per azioni di gioco (es. click, attivazione/disattivazione link)
- Effetti sonori per eventi di gioco (es. attivazione di un link, errore, successo)
- Volume regolabile tramite menu opzioni
- Opzioni per disattivare la musica o gli effetti sonori

---


## 13. Requisiti di Stile e Qualità del Codice

- Codice abbondantemente commentato: ogni funzione, classe, modulo e blocco logico deve essere documentato tramite commenti e docstring, per facilitare la comprensione e l’apprendimento.
- Codice pensato come materiale didattico: ogni concetto implementato, pattern o soluzione deve essere spiegato.
- Soluzioni semplici, leggibili e lineari preferite a quelle complesse, salvo necessità tecniche documentate.
- Best practice Python (PEP8), nomi chiari, separazione in moduli, attenzione alla manutenibilità.
- Dove utile, aggiungere esempi d’uso nei commenti/docstring.
- Logica di estrazione hostname robusta rispetto a dati assenti o vuoti nelle risposte API.

---

## 14. Glossario Interattivo in Game

Sezione accessibile dal menu e durante la partita dove il giocatore può consultare i principali concetti di networking:

- **Rete**: Insieme di dispositivi (computer, router, server) collegati tra loro per scambiarsi dati.
- **Router**: Dispositivo che indirizza i pacchetti di dati tra reti diverse.
- **Interfaccia**: Punto di connessione fisica o logica su un router (nord, sud, est, ovest nel gioco).
- **Interfaccia logica (sub-interface)**: Interfaccia virtuale creata su un'interfaccia fisica, identificata dal numero VLAN.
- **VLAN**: Rete virtuale che identifica univocamente un link tra due router reali.
- **Link**: Collegamento tra due dispositivi di rete che permette il passaggio delle informazioni.
- **Neighborship**: Relazione di vicinato tra due router che hanno instaurato una sessione di routing attiva.
- **Disservizio**: Situazione in cui una parte della rete o un link smette di funzionare correttamente.
- **Pacchetto**: Unità di dati che viaggia nella rete.
- **Routing**: Processo con cui un router decide il percorso migliore per un pacchetto.
- **API**: Interfaccia di programmazione delle applicazioni che permette al client di interagire con i router.

---

## 15. Condizione di Vittoria del Livello

La **condizione di vittoria di un livello** viene raggiunta quando, in almeno uno dei router obiettivo, la sua tabella di routing contiene le rotte verso le loopback di **tutti** i router obiettivo.

### Definizione di router obiettivo

I **router obiettivo** sono quelli identificati dalle coppie (groupID, localID) specificate per il livello.  
Esempio:  
- (1,1)  
- (4,1)

### Indirizzamento delle loopback

L’indirizzo IP della loopback per ogni router obiettivo segue la convenzione:
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
In altre parole, la tabella deve contenere tutte le destinazioni del tipo G.0.0. L dove (G,L) sono le coppie dei router obiettivo.

### Nota
- Il controllo della vittoria avviene periodicamente (sincronizzato con il polling delle API).
- La verifica può essere visualizzata nella UI tramite un indicatore di progresso o stato.

---

## 16. Ottenimento della tabella di routing di un router (modalità API)

Per ottenere la tabella di routing di un router reale, il client deve effettuare la seguente chiamata API RESTCONF:

```
restconf/data/ietf-routing:routing-state/routing-instance
```

Questa chiamata restituisce lo stato di routing, inclusa la tabella di routing attuale del router.

> **Nota:** In futuro verranno aggiunti esempi pratici di risposta dell’API e di parsing delle rotte rilevanti.

---

## Stato UP/DOWN delle interfacce (logica API)

- Lo stato UP/DOWN di ogni interfaccia logica (VLAN) è determinato dal campo `"enabled"` della relativa sub-interface nella risposta API RESTCONF.
- Esempio di risposta API per il router con local_id 1:

```
{
    "name": "GigabitEthernet1.131",
    "type": "iana-if-type:ethernetCsmacd",
    "enabled": false,
    ...
}
```

- In questo esempio, la sub-interface `GigabitEthernet1.131` ha `"enabled": false`, quindi il link tra i router con local_id 1 e 3 (nel group_id 1, VLAN 131) è DOWN e la freccia nella UI sarà rossa.
- Se `"enabled": true`, il link è UP e la freccia nella UI sarà verde.
- Questa logica è implementata in `router_grid.py` nella funzione `update_from_api`.
