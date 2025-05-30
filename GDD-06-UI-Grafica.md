# 6. UI e Grafica

- **Gioco 2D, schermo intero, stile retro gaming pixel-art 16-bit**
- **Palette colori:** Pastello (esempi: azzurro chiaro, rosa, lilla, verde menta, giallo pallido)
- UI adattiva, leggibile, centrata, senza overflow
- Visualizzazione dello stato in tempo reale tramite letture dai dispositivi
- Stato token, timer, azioni disponibili e stato dei router sempre visibili e aggiornati dinamicamente
- Visualizzazione grafica dei link attivi tra router con neighborship di routing attiva
- Hostname router sempre visibile
- ID router solo a terminale per debug
- Glossario accessibile dal menu e in-game
- **Un router di cui non è stato fatto il claim viene visualizzato di colore grigio nella UI.**
- La colorazione e lo stato claim dei router sono determinati dal confronto tra il nomegiocatore locale e quello letto dalla description della loopback.
- Un router con description valorizzata ma nomegiocatore diverso da quello locale appare sempre come non claimato (grigio) e non può essere gestito dal giocatore locale.

### 6.1 Dettaglio: Regole di disegno di un router nella UI

Ogni router nella UI viene rappresentato secondo queste regole grafiche:

- **Forma base:**
  - Cerchio pieno, stile pixel-art, dimensione adattiva in base alla griglia e alla risoluzione.
  - Colore:
    - Grigio (libero, non claimato; ovvero nessun giocatore ha ancora effettuato il claim sul router)
    - Blu (claimato da un giocatore, colore del giocatore)
    - Bordo giallo spesso 3 pixel se router obiettivo già claimato, in pixel-art (doppio bordo)
- **Interfacce:**
  - Quattro frecce spesse (5px), sprite pixel-art, orientate verso nord, sud, est, ovest, visibili **solo se la VLAN corrispondente è configurata** (cioè esiste un link logico tra router) **e solo se il router adiacente in quella direzione è effettivamente disegnato nella griglia**.
  - Le frecce sono disegnate in modo che la punta rappresenti il punto di connessione dell'interfaccia logica.
  - **I link attivi (linee tratteggiate verdi) partono dal simbolo della freccia/interfaccia e non dal centro del router.**
  - Le frecce sono colorate:
    - Verde (interfaccia up)
    - Rosso (interfaccia down)
    - Giallo (hover su interfaccia: quando il mouse passa sopra una freccia, questa viene evidenziata in giallo, indipendentemente dallo stato up/down)
  - Se la VLAN non è configurata, o il router adiacente non è presente nella griglia, la freccia non viene disegnata (nessuna interfaccia visibile in quella direzione).
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
  - Box rettangolare adattivo sempre visibile sotto ogni router, stile pixel-art (bordi doppi, colori saturi), con bordo bianco e sfondo scuro.
  - Testo hostname sempre centrato, outline nero, e mai troncato.
  - Il box mostra sempre il valore aggiornato dal polling API, oppure '?' se non disponibile, senza ritardi o desincronizzazioni.
  - L'hostname mostrato nella UI è sempre quello letto via polling API dal campo description della loopback, oppure '?' se non disponibile. La sincronizzazione è in tempo reale.
- **Feedback visivo:**
  - Quando un router viene claimato, il colore del cerchio cambia immediatamente e viene mostrato un messaggio di conferma in stile pixel-art.
  - Quando un’interfaccia viene attivata/disattivata, il colore della freccia cambia in tempo reale.
- **Hover e click:**
  - Al passaggio del mouse su un router, il suo colore di sfondo diventa leggermente più chiaro per indicare che è selezionato, con effetto pixel-art (nessun glow/ombra soft).
  - Al click su un router:
    - Se il router non è claimato, viene avviata la procedura di claim.
    - Se il router è già claimato dal giocatore locale, il click non mostra più la finestra informativa (popup) ma non fa nulla (o in futuro potrà attivare altre azioni contestuali).
- **ID router:**
  - Gli ID (global_id, local_id, group_id) non sono visibili nella UI, ma vengono stampati a terminale per debug quando si seleziona il router.
- **Posizionamento:**
  - Il router è centrato nella cella della griglia, con padding per evitare sovrapposizioni.
- **Colore router:** Un router non claimato (cioè non claimato dal giocatore locale) viene sempre visualizzato di colore grigio (`config.GRAY`) nella UI, indipendentemente dal contenuto del campo hostname/description. Solo i router effettivamente claimati dal giocatore locale sono colorati con il colore del player.
- **Legenda:**
  - In basso nella UI NON è più presente una legenda: tutte le regole di colori e simboli sono documentate solo in questo file e non più mostrate in-game.
  - Non sono più presenti riferimenti o colori relativi ad altri giocatori.
  - I router claimati da altri giocatori (cioè con claimed_by_name valorizzato e diverso dal player locale) sono visualizzati in **arancione** nella griglia.
  - I router claimati dal giocatore locale sono colorati secondo il colore del player.
  - I router non claimati restano grigi.
  - La legenda UI deve riflettere questa distinzione cromatica.

#### Aggiornamenti e miglioramenti UI (storico changelog integrato)

- Rimossa la chiamata a `update_links()` dalla UI (`ui.py`): la logica di aggiornamento dei link attivi (neighborship) è ora gestita unicamente dalla funzione `update_from_api()` in `router_grid.py`.
- Non esiste più una funzione `update_links()` in `RouterGrid` e nessuna chiamata a tale funzione è necessaria.
- L'aggiornamento dello stato dei link (campo `neighborship` nei link) avviene automaticamente durante il polling API, insieme all'aggiornamento delle interfacce.
- Nessuna modifica visiva o di gameplay per l'utente finale: la sincronizzazione tra interfacce e link resta garantita.

- La visualizzazione dell'hostname nella UI è sempre aggiornata in tempo reale grazie alla chiamata continua di update_from_api().
- Il box hostname sotto il router mostra sempre il valore aggiornato o '?' se non disponibile, senza ritardi o desincronizzazioni.
- La UI mostra solo il numero di token e il timer del giocatore locale. I token degli altri giocatori non sono mai visualizzati.
- Ogni giocatore vede e gestisce solo i propri token nella UI. I token degli altri giocatori non sono più visibili o mostrati.
- La barra superiore visualizza solo i token e il timer del giocatore corrente.
- La UI mostra solo i token e il timer del giocatore locale. I token degli altri giocatori non sono mai visibili.
- Un router è considerato claimato dal giocatore locale solo se il campo description della sua interfaccia loopback è nel formato `nomegiocatore_hostnameRouterVirtuale` e il `nomegiocatore` coincide esattamente con quello inserito dal giocatore locale. Se il nomegiocatore nella description è diverso dal nome inserito dal giocatore locale, il router è considerato sempre non claimato (colore grigio nella UI, azioni non permesse).
- Il claim non è più gestito solo localmente, ma sincronizzato tramite la description della loopback letta via API.
- La colorazione e lo stato claim dei router sono determinati dal confronto tra il nomegiocatore locale e quello letto dalla description della loopback.
- Un router con description valorizzata ma nomegiocatore diverso da quello locale appare sempre come non claimato (grigio) e non può essere gestito dal giocatore locale.
- La logica di claim di un router si basa ora sul parsing del campo description della loopback: se il nomegiocatore letto coincide con quello locale, il router risulta claimato dal giocatore. Altrimenti, è sempre considerato libero per il client locale.
- La logica di estrazione hostname è robusta rispetto a dati assenti o vuoti nelle risposte API: il client imposta sempre l'hostname a '?' se l' interfaccia Loopback{group_id} non è presente o il campo description è vuoto.
- L'hostname viene aggiornato solo se il campo description è presente e non vuoto.
- Il nome del giocatore locale viene visualizzato nella UI sopra i token, in alto a sinistra, e viene troncato con '...' se troppo lungo per lo spazio disponibile.
- La legenda dei colori e simboli NON è più presente nella schermata di gioco. Tutte le informazioni sui colori e simboli sono ora documentate solo in questo file e non più mostrate in-game.
- Le frecce delle interfacce (N/S/E/W) sono disegnate SOLO se la VLAN è configurata e il router adiacente è presente nella griglia, come sprite pixel-art.
- Quando il mouse passa sopra una freccia/interfaccia, la freccia viene colorata di giallo (200,200,0) indipendentemente dallo stato up/down, con effetto pixel-art.
- La logica di hover e hit detection delle frecce è identica a quella di disegno, garantendo coerenza visiva e funzionale.
- La schermata di gioco è ora più pulita, senza legenda, come da ultime specifiche.
- L'interfaccia grafica è stata aggiornata:
  - Tutti gli elementi (router, frecce, box, menu, popup, feedback, input, splash) sono ora sprite o forme in pixel-art 16-bit, con bordi doppi, dithering, ombre a gradini, colori saturi, outline testo.
  - Rimossi tutti gli effetti moderni: niente antialias, niente glow, niente gradienti, niente glassmorphism, niente font sans-serif moderno, niente ombre soft.
  - Nessuno sfondo datacenter: lo sfondo è ora un colore pieno coerente con la palette pixel-art.

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

## 8.1 Mockup e schermate ASCII della UI

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

### Barra superiore con nome giocatore troncato e token

```
╔════════════════════════════════════════════════════════════════════╗
║  [ Giocatore: SuperLongNa... ]  [ Token: 3   +1 in 04s ]         ║
╠════════════════════════════════════════════════════════════════════╣
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
         [Token: N   +1 in XXs] = box token in alto a sinistra, senza cerchio
```

### Legenda in basso

```
Legenda: ● grigio = router non claimato, ● blu = router claimato dal giocatore locale
         ↑/→/↓/← verdi = interfaccia up, rosse = interfaccia down, gialle = non configurata
         [Rx] = hostname del router (o '?' se non disponibile)
         [Token: N   +1 in XXs] = box token in alto a sinistra, senza cerchio
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

### 6.2 Regole dettagliate di disegno: link e interfacce

#### Interfacce (frecce/rette pixel-art)
- Ogni interfaccia (N, S, E, W) viene rappresentata come un rettangolo colorato (non più una freccia) in stile pixel-art, con:
  - Colore verde brillante (`(0, 200, 0)`) se l'interfaccia è UP
  - Colore rosso (`(220, 0, 0)`) se l'interfaccia è DOWN
  - Colore giallo (`(255, 220, 40)`) se il mouse è in hover su quella interfaccia
  - Bordo bianco spesso e outline nero per garantire leggibilità su qualsiasi sfondo
- Il rettangolo dell'interfaccia è disegnato:
  - Solo se la VLAN è configurata (cioè esiste un link logico tra router)
  - Solo se il router adiacente in quella direzione è effettivamente presente nella griglia
  - Posizionato in modo che non si sovrapponga mai al cerchio del router
  - Dimensioni tipiche: lunghezza 36px, larghezza 14px, con angolo e posizione calcolati rispetto al centro del router e alla direzione
- L'effetto hover (giallo) ha priorità su qualsiasi altro stato

#### Link attivi (tra router)
- I link attivi (neighborship) sono rappresentati da una linea spessa, verde brillante (`(0, 200, 0)`), con:
  - Bordo bianco spesso (10px) sotto la linea
  - Bordo nero sottile (4px) sopra il bordo bianco
  - Linea centrale verde (6px)
  - Effetto "glow" pixel-art dato dalla sovrapposizione dei bordi
- La linea parte sempre dal bordo esterno del rettangolo interfaccia di ciascun router, non dal centro del router né dalla punta di una freccia
- La linea non si sovrappone mai al cerchio/interfaccia del router: viene calcolato un margine visivo (tipicamente 18px) per lasciare spazio tra la linea e il router
- La linea viene disegnata solo se entrambi i router sono visibili nella griglia
- La linea è bidirezionale e rappresenta lo stato attivo della connessione (neighborship)
- Se uno dei due router non è visibile nella griglia, il link non viene disegnato
- Non sono mai disegnate linee che attraversano o si sovrappongono a router o interfacce
- Le linee sono sempre orizzontali o verticali (mai diagonali), collegate tra interfacce adiacenti

#### Sintesi delle condizioni di visibilità
- Un'interfaccia è visibile solo se:
  - La VLAN è configurata
  - Il router adiacente è presente nella griglia
- Un link attivo è visibile solo se:
  - Entrambi i router sono visibili nella griglia
  - Esiste una neighborship attiva tra i due router

#### Mockup: dimensione e stile dei box Giocatore e Token

```
╔════════════════════════════════════════════════════════════════════╗
║  [ Giocatore: SuperLongNa... ]  [ Token: 3   +1 in 04s ]         ║
╠════════════════════════════════════════════════════════════════════╣
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
         [Token: N   +1 in XXs] = box token in alto a sinistra, senza cerchio
```

- Entrambi i box devono avere la stessa larghezza e altezza, stile e padding:
- Esempio di mockup con box identici (stessa dimensione, font, bordo, padding):

```
╔════════════════════════════════════════════════════════════════════╗
║  ┌────────────────────────────┐  ┌────────────────────────────┐  ║
║  │ Giocatore: SuperLongNa...  │  │ Token: 3   +1 in 04s      │  ║
║  └────────────────────────────┘  └────────────────────────────┘  ║
╠════════════════════════════════════════════════════════════════════╣
```

- I due box sono affiancati, con la stessa larghezza (adattiva, ma identica), stessa altezza, stesso bordo doppio, stesso font e padding.
- Il testo all'interno è centrato verticalmente e orizzontalmente.
- Il box Token non ha più il cerchio, solo testo e countdown integrato.
- Se il nome giocatore è troppo lungo, viene troncato con '...'.
- Il layout si adatta alla larghezza della finestra, ma i due box restano sempre identici come dimensione e stile.

Aggiornare la UI e la logica di disegno per garantire che i due box siano sempre identici in dimensione e stile, come da mockup sopra.

## 6.3 Modalità Custom: selezione numero router

- Oltre alle modalità predefinite (4x4, 5x5, 6x6), il gioco offre una modalità **Custom**.
- In modalità Custom, il giocatore può scegliere la dimensione della griglia di router (NxN) tramite un popup o selettore numerico prima di iniziare la partita.
- La UI mostra un popup pixel-art che permette di selezionare un valore N compreso tra 2 e 8 (inclusi), con pulsanti + e - oppure un campo numerico.
- Dopo la conferma, la griglia viene generata con NxN router e tutte le regole di visualizzazione, claim, interfacce e link si adattano automaticamente alla nuova dimensione.
- Tutti i mockup e le regole di disegno restano invariati, ma la griglia si adatta dinamicamente alla dimensione scelta.

### Mockup selezione Custom

```
╔════════════════════════════════════════════════════════════════════╗
║  Seleziona dimensione griglia router: [ 5 ]   [-] [+]   OK       ║
╚════════════════════════════════════════════════════════════════════╝
```

- Dopo la selezione, la schermata di gioco mostra la griglia NxN scelta dal giocatore.
- Tutte le regole di claim, token, interfacce, link e obiettivi restano valide per qualsiasi dimensione.