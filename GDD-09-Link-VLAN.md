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
    - il local_id più piccolo tra i due router se il link è tra due router dello stesso gruppo seguito dal local_id più grande tra i due router
    - il local_id più grande tra i due router se il link è tra due router di gruppi diversi seguito dal group_id del router con group_id più piccolo.
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

**Stato neighborship di routing:**  
Se una neighborship di routing è attiva su un link, il campo `description` della relativa sub-interface sarà impostato a `UP`.  
Se il campo `description` della sub-interface è vuoto, significa che non esiste nessuna neighborship attiva su quel link.
Se tra due router esiste una neighborship attiva, la UI mostra una linea tratteggiata verde tra i due router, indicando che il link è attivo e funzionante.

**Stato UP/DOWN delle interfacce (aggiornamento 26/05/2025):**  
- Lo stato UP di un'interfaccia logica (VLAN) è determinato dal campo `enabled` della relativa sub-interface nella risposta API RESTCONF.
- Se la sub-interface esiste e `enabled` è `true`, l'interfaccia è considerata **UP** (freccia verde nella UI).
- Se la sub-interface non esiste o `enabled` è `false`, l'interfaccia è considerata **DOWN** (freccia rossa nella UI).
- Questa logica è implementata in `router_grid.py` nella funzione `update_from_api`.

