## 11. Prototipo e Mockup

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

## 11.2 Tutorial Step-by-Step (Modalità Offline)

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
