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
