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
