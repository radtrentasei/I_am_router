# 7. Specifiche tecniche di implementazione

## 7. Specifiche Tecniche: Sistema di ID dei Router

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
  - Le chiamate API sono asincrone e non bloccano l'interfaccia utente.  
  Il client continua a funzionare normalmente anche se una chiamata API fallisce o impiega più tempo del previsto.
  - La logica di claim di un router si basa ora sul parsing del campo description della loopback: se il nomegiocatore letto coincide con quello locale, il router risulta claimato dal giocatore. Altrimenti, è sempre considerato libero per il client locale.
  - Aggiornata la descrizione del formato della description: sempre `nomegiocatore_hostnameRouterVirtuale`.
### Logica di recupero hostname
- **Obiettivo:**  
  Recuperare l'hostname configurato sul router reale per visualizzarlo nella UI.
- **Interfaccia Loopback:**
  - Ogni router ha un'interfaccia loopback configurata con un nome specifico: `LoopbackY`, dove `Y` è il `group_id` del router.
  - Questa interfaccia viene utilizzata per identificare il router e recuperare l'hostname.
  - Il claim dei router è determinato dal parsing del campo description della loopback, in formato `nomegiocatore_hostnameRouterVirtuale`, e sincronizzato tra tutti i client tramite API. Un router con nomegiocatore diverso da quello locale è sempre considerato non claimato dal client locale.
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

## Claim di un router: regole di claimabilità (aggiornamento)

- Un router può essere claimato **solo** se entrambe le seguenti condizioni sono vere:
    1. `claimed_by is None` (nessun giocatore lo ha già claimato)
    2. `hostname == 'Router'` (il router è ancora nello stato iniziale, non personalizzato)
- Se una di queste condizioni non è soddisfatta (ad esempio, il router ha già un hostname diverso da 'Router' oppure è già claimato), il tentativo di claim viene bloccato dalla UI e viene mostrato un messaggio di errore: "Claim possibile solo su router liberi (hostname 'Router')!".
- Questo comportamento è implementato sia nella gestione del click che nella logica di claim, garantendo coerenza tra frontend e backend.

### Flusso aggiornato:
1. L'utente clicca su un router.
2. Se il router è claimabile (vedi regole sopra), viene richiesto l'inserimento dell'hostname tramite popup.
3. Se il router non è claimabile, viene mostrato un errore e il claim non viene avviato.

Questa regola garantisce che solo i router effettivamente "liberi" e non personalizzati possano essere claimati, come da design di gioco.

## Claim di un router: consumo token

- L'azione di claim di un router consuma **1 token** del giocatore all'avvio dell'azione (subito dopo il click e la conferma dell'hostname).
- Se la chiamata API RESTCONF per il claim fallisce (ad esempio per errore di rete o permessi), il token viene **restituito** automaticamente al giocatore.
- Se la chiamata ha successo, il token rimane consumato e il router viene claimato.

Questo comportamento garantisce coerenza con le altre azioni di gioco che consumano token (es. attivazione interfacce).

### Flusso aggiornato:
1. L'utente clicca su un router claimabile e inserisce l'hostname.
2. Viene scalato 1 token dal totale del giocatore.
3. Se la chiamata API va a buon fine, il router viene claimato e il token rimane consumato.
4. Se la chiamata API fallisce, il token viene restituito e viene mostrato un errore.

## Ricarica automatica dei token

- Ogni giocatore riceve automaticamente **1 token ogni 10 secondi**.
- Il numero massimo di token accumulabili per ciascun giocatore è **4**.
- Se il giocatore ha già 4 token, il timer di ricarica si ferma fino a quando non viene consumato almeno un token.
- Il timer di ricarica riprende automaticamente appena il numero di token scende sotto il massimo.

Questa regola si applica sia in partita che in modalità tutorial (se non diversamente specificato).

## 9. Dettaglio: Collegamento Fisico e Logico dei Router (VLAN e link tra router)

### Collegamento fisico
- Ogni router reale è fisicamente connesso alla rete tramite la sua interfaccia **GigabitEthernet1**.

### Collegamento logico tramite VLAN
- Tutti i link tra router (ovvero le interfacce nord, sud, est, ovest nel gioco) sono realizzati tramite **interfacce logiche VLAN** (sub-interface) sulla stessa GigabitEthernet1.
- **Ciascun link tra due router** all’interno è rappresentato da una VLAN univoca.

  - **Regola generale**:  
    Il numero VLAN è creato concatenando **group_id** + **local_id_A** + **local_id_B**, dove A e B sono i due router collegati.  
    L’ordine non conta, il link è bidirezionale.
    **local_id_A** è sempre inferiore a  **local_id_B**

  - **Esempi**:  
    - _VLAN 312_ rappresenta il link nel gruppo 3 tra router 1 e router 2 (e viceversa, il link è bidirezionale).
    - _VLAN 434_ rappresenta nel gruppo 4 il link tra router 3 e router 4 (e viceversa).

### Numerazione delle VLAN (aggiornamento 26/05/2025)

- La VLAN che identifica il link logico tra due router di gruppi diversi viene calcolata come:
  - Si prende il router con group_id più piccolo (in caso di parità, quello con local_id più piccolo).
  - La VLAN è composta da: 
    - il group_id del router con group_id più piccolo
    - il local_id più piccolo tra i due router se il link è tra due router dello stesso gruppo seguito dal local_id più grande tra i due router seguito dal group_id
    - il local_id più grande tra i due router se il link è tra due router di gruppi diversi seguito dal local_id del secondo router e dal group_id del router con group_id più piccolo.
  - Esempi pratici:
    - Tra un router (1,1) e un router (2,1): VLAN = 112
    - Tra un router (1,1) e un router (3,1): VLAN = 113
    - Tra un router (2,1) e un router (1,2): VLAN = 121
    - Tra un router (4,1) e un router (3,2): VLAN = 143
    - Tra un router (3,1) e un router (1,3): VLAN = 131
    - Tra un router (4,1) e un router (2,3): VLAN = 142
- Questa regola garantisce che la numerazione sia univoca e simmetrica tra i due router coinvolti.

#### Mappatura e gestione dei link
- Ogni interfaccia logica di collegamento (n/s/e/w nel gioco) corrisponde a una sub-interface configurata su GigabitEthernet1, con il numero VLAN che rappresenta univocamente il link tra i due router del gruppo.
- Il link è **bidirezionale** e il numero VLAN è lo stesso su entrambi i router coinvolti.
- Quando un link viene “attivato” o “disattivato” nel gioco, la relativa sub-interface (es: `GigabitEthernet1.312`) viene abilitata/disabilitata via API.
- La UI riflette lo stato up/down della VLAN (interfaccia logica/link) con le frecce verdi/rosse.
- L’identificativo VLAN può essere mostrato a scopo didattico nel glossario o in una schermata avanzata/debug.

### Chiamata API per abilitare/disabilitare una interfaccia (enable/disable)
- **Endpoint RESTCONF:**
  - URL: `https://198.18.1.1X/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1.VLAN` dove `X` è il `local_id` del router e `VLAN` è il numero della sub-interface da modificare (es: `GigabitEthernet1.112`).
  - Autenticazione: Basic Auth (username: `cisco`, password: `C1sco12345`).
  - Content-Type: `application/yang-data+json`
  - Metodo: `PUT`
- **Payload:**
    - Il payload deve contenere il campo `enabled` impostato a `true` (per abilitare) o `false` (per disabilitare) l'interfaccia.
    - Esempio di payload per abilitare:
      ```json
      {
        "interface": [
          {
            "name": "GigabitEthernet1.112",
            "type": "iana-if-type:ethernetCsmacd",
            "enabled": true
          }
        ]
      }
      ```
    - Esempio di payload per disabilitare:
      ```json
      {
        "interface": [
          {
            "name": "GigabitEthernet1.112",
            "type": "iana-if-type:ethernetCsmacd",
            "enabled": false
          }
        ]
      }
      ```
- **Esecuzione:**
  - Quando un giocatore attiva o disattiva una interfaccia tramite la UI, il client invia questa chiamata API per modificare lo stato della sub-interface corrispondente.
  - Se la chiamata ha successo, lo stato dell'interfaccia viene aggiornato e la UI riflette il nuovo stato (freccia verde o rossa).
  - Se la chiamata fallisce, viene mostrato un messaggio di errore e lo stato rimane invariato.

**Stato neighborship di routing:**  
Se una neighborship di routing è attiva su un link, il campo `description` della relativa sub-interface sarà impostato a `UP`.  
Se il campo `description` della sub-interface è vuoto, significa che non esiste nessuna neighborship attiva su quel link.
Se tra due router esiste una neighborship attiva, la UI mostra una linea tratteggiata verde tra i due router, indicando che il link è attivo e funzionante.

**Stato UP/DOWN delle interfacce (aggiornamento 26/05/2025):**  
- Lo stato UP di un'interfaccia logica (VLAN) è determinato dal campo `enabled` della relativa sub-interface nella risposta API RESTCONF.
- Se la sub-interface esiste e `enabled` è `true`, l'interfaccia è considerata **UP** (freccia verde nella UI).
- Se la sub-interface non esiste o `enabled` è `false`, l'interfaccia è considerata **DOWN** (freccia rossa nella UI).
- Questa logica è implementata in `router_grid.py` nella funzione `update_from_api`.

## 16. Ottenimento della tabella di routing di un router (modalità API)

Per ottenere la tabella di routing di un router reale, il client deve effettuare la seguente chiamata API RESTCONF:

```
restconf/data/ietf-routing:routing-state/routing-instance
```

Questa chiamata restituisce lo stato di routing, inclusa la tabella di routing attuale del router.

> **Nota:** In futuro verranno aggiunti esempi pratici di risposta dell’API e di parsing delle rotte rilevanti.

---



---
