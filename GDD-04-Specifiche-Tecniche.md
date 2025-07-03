# GDD-04-Specifiche-Tecniche

## 1. Sistema di ID dei Router

### 1.1 Tipologie di ID
- **ID globale (global_id)**:
  - Ogni router riceve un ID progressivo unico da 1 a N*N, assegnato riga per riga nella griglia
  - Serve per identificare in modo univoco ogni router nella rete e per debug
  - Il global_id ha scarso valore pratico per il gioco

- **ID locale (local_id)**:
  - All'interno di ogni gruppo 2x2 di router, ogni router riceve un local_id da 1 a 4 secondo uno schema a scacchiera
  - Utilizzato per la corrispondenza con la numerazione delle interfacce e per le chiamate API
  - Il local_id rappresenta l'identificativo del router reale

- **ID gruppo (group_id)**:
  - Ogni gruppo 2x2 di router riceve un group_id progressivo
  - Serve per identificare i router dello stesso gruppo logico (per le chiamate API alle LoopbackX)
  - Il group_id rappresenta la VRF (Virtual Routing and Forwarding) del router reale

### 1.2 Regole di Utilizzo
- Gli ID **non sono visibili nella UI** durante il gioco normale
- Quando si clicca su un router, i suoi ID vengono stampati a terminale per debug
- In modalità API, gli ID sono utilizzati per:
  - Costruire l'indirizzo IP/hostname per la chiamata RESTCONF (es: https://198.18.128.1X dove X è il local_id)
  - Identificare l'interfaccia LoopbackX (dove X è il group_id) per recuperare l'hostname dinamico

### 1.3 Assegnazione degli ID
- **global_id**: progressivo da 1 a N*N, riga per riga
- **group_id**: assegnato a blocchi 2x2 a scacchiera, incrementato da sinistra a destra e dall'alto verso il basso
- **local_id**: da 1 a 4 all'interno di ogni blocco 2x2 secondo schema a scacchiera

### 1.4 Esempio Pratico (Griglia 4x4)
```
global_id: 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16

group_id:
1 1 2 2
1 1 2 2  
3 3 4 4
3 3 4 4

local_id: 1,2,3,4 in ogni blocco 2x2
```

## 2. Sistema API RESTCONF

### 2.1 Comportamento delle API
- **Chiamate periodiche**: Le API vengono chiamate periodicamente (es. ogni 3 secondi), NON al passaggio del mouse
- **Memorizzazione locale**: Tutte le informazioni (hostname, stato interfacce, neighborship) sono memorizzate localmente
- **UI non bloccante**: Il passaggio del mouse mostra informazioni già recuperate dal polling periodico
- **API asincrone**: Non bloccano l'interfaccia utente, il client funziona anche se le API falliscono

### 2.2 Autenticazione
- **Metodo**: Basic Auth
- **Username**: `cisco`
- **Password**: `C1sco12345`
- **Content-Type**: `application/yang-data+json`

### 2.3 Logica di Recupero Hostname
**Obiettivo**: Recuperare l'hostname configurato sul router reale per visualizzarlo nella UI.

**Interfaccia Loopback**:
- Ogni router ha un'interfaccia loopback: `LoopbackY`, dove `Y` è il `group_id` del router
- Utilizzata per identificare il router e recuperare l'hostname
- Il claim è determinato dal parsing del campo `description` della loopback in formato `nomegiocatore_hostnameRouterVirtuale`

**Chiamata API per hostname**:
```
GET https://198.18.128.1X/restconf/data/ietf-interfaces:interfaces
```
dove `X` è il `local_id` del router.

**Logica di ricerca**:
- Viene cercata l'interfaccia `LoopbackY` dove `Y` è il `group_id` del router
- Il campo `description` di questa interfaccia viene utilizzato come hostname
- **Fallback**: Se la chiamata fallisce, viene mostrato '?' o l'ultimo valore disponibile

### 2.4 Logica di Settaggio Hostname
**Chiamata API per impostare hostname**:
```
PUT https://198.18.128.1X/restconf/data/ietf-interfaces:interfaces/interface=LoopbackY
```

**Payload di esempio**:
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

**Esecuzione**: Quando un giocatore effettua il claim, il client invia questa chiamata per impostare l'hostname.

### 2.5 Regole di Claimabilità
Un router può essere claimato **solo** se:
1. `claimed_by is None` (nessun giocatore lo ha già claimato)
2. `hostname == 'Router'` (router nello stato iniziale)

**Consumo token**: L'azione di claim consuma 1 token all'avvio. Se la chiamata API fallisce, il token viene restituito automaticamente.

## 3. Collegamento Fisico e Logico dei Router

### 3.1 Collegamento Fisico
- Ogni router reale è fisicamente connesso tramite interfaccia **GigabitEthernet1**

### 3.2 Collegamento Logico tramite VLAN
- Tutti i link tra router sono realizzati tramite **interfacce logiche VLAN** (sub-interface) sulla stessa GigabitEthernet1
- Ciascun link è rappresentato da una VLAN univoca

### 3.3 Numerazione delle VLAN
La VLAN che identifica il link logico tra due router viene calcolata come:
- Si prende il router con group_id più piccolo (in caso di parità, quello con local_id più piccolo)
- La VLAN è composta da:
  - Il group_id del router con group_id più piccolo
  - Il local_id più piccolo seguito dal local_id più grande (stesso gruppo)
  - Il local_id più grande seguito dal local_id del secondo router + group_id (gruppi diversi)

**Esempi pratici**:
- Router (1,1) e (2,1): VLAN = 112
- Router (1,1) e (3,1): VLAN = 113  
- Router (2,1) e (1,2): VLAN = 121
- Router (4,1) e (3,2): VLAN = 143

### 3.4 Gestione dei Link
- Ogni interfaccia logica (n/s/e/w nel gioco) corrisponde a una sub-interface su GigabitEthernet1
- Il link è **bidirezionale** con stesso numero VLAN su entrambi i router
- L'attivazione/disattivazione modifica la relativa sub-interface via API
- La UI riflette lo stato up/down con frecce verdi/rosse

### 3.5 Chiamata API per Abilitare/Disabilitare Interfaccia
```
PUT https://198.18.128.1X/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1.VLAN
```

**Payload per abilitare**:
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

**Payload per disabilitare**:
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

### 3.6 Stato UP/DOWN delle Interfacce
- Lo stato UP è determinato dal campo `enabled` della sub-interface nella risposta API RESTCONF
- Se la sub-interface esiste e `enabled` è `true`: interfaccia **UP** (freccia verde)
- Se non esiste o `enabled` è `false`: interfaccia **DOWN** (freccia rossa)

### 3.7 Stato Neighborship di Routing
- Se una neighborship è attiva su un link, il campo `description` della sub-interface sarà `UP`
- Se il campo `description` è vuoto, non esiste neighborship attiva
- Se tra due router esiste neighborship attiva, la UI mostra una linea tratteggiata verde

## 4. Ottenimento Tabella di Routing

### 4.1 Chiamata API
Per ottenere la tabella di routing di un router reale:
```
GET https://198.18.128.1X/restconf/data/ietf-routing:routing-state/routing-instance
```

Questa chiamata restituisce lo stato di routing, inclusa la tabella di routing attuale del router.

### 4.2 Verifica Condizione di Vittoria
- Il controllo della vittoria avviene periodicamente, sincronizzato con il polling delle API
- La verifica può essere visualizzata nella UI tramite indicatore di progresso o stato

## 5. Gestione Token

### 5.1 Ricarica Automatica
- Ogni giocatore riceve automaticamente **1 token ogni 10 secondi**
- Numero massimo accumulabile: **4 token**
- Se già a 4 token, il timer si ferma fino al consumo di almeno 1 token
- Il timer riprende automaticamente appena i token scendono sotto il massimo

### 5.2 Consumo Token
- **Claim router**: consuma 1 token all'avvio dell'azione
- **Attivazione/disattivazione interfaccia**: consuma 1 token
- Se l'API fallisce, il token viene restituito automaticamente

---
