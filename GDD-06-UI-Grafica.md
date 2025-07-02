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
- **Tutti gli input testuali (nome giocatore, hostname) sono visualizzati in tempo reale con cursore lampeggiante, senza placeholder moderni.**
- **I box Giocatore e Token sono identici, affiancati, centrati in alto, con testo centrato e troncamento corretto, senza cerchio token, solo testo e countdown.**
- **Il click su un’interfaccia (rettangolo pixel-art) attiva/disattiva lo stato up/down solo se claimata dal player locale e con token disponibili, mostrando feedback visivo.**
- **Overlay debug opzionale per hitbox interfacce: se abilitato, mostra un rettangolo blu trasparente perfettamente coincidente con la hitbox cliccabile.**
- **Nessun effetto moderno: niente antialias, niente glow, niente gradienti, niente glassmorphism, niente font sans-serif moderno, niente ombre soft.**
- **Nessuna legenda in-game: tutte le regole di colori e simboli sono documentate solo in questo file.**

### 6.1 Dettaglio: Regole di disegno di un router nella UI

Ogni router nella UI viene rappresentato secondo queste regole grafiche:

- **Forma base:**
  - Cerchio pieno, stile pixel-art, dimensione adattiva in base alla griglia e alla risoluzione.
  - Colore:
    - Grigio (libero, non claimato; ovvero nessun giocatore ha ancora effettuato il claim sul router)
    - Blu (claimato da un giocatore, colore del giocatore)
    - Arancione (claimato da altro giocatore)
    - Bordo giallo spesso 3 pixel se router obiettivo, in pixel-art (doppio bordo)
- **Interfacce:**
  - Quattro rettangoli spessi (non più frecce), sprite pixel-art, orientati verso nord, sud, est, ovest, visibili **solo se la VLAN corrispondente è configurata** (cioè esiste un link logico tra router) **e solo se il router adiacente in quella direzione è effettivamente disegnato nella griglia**.
  - I rettangoli sono disegnati in modo che la parte esterna rappresenti il punto di connessione dell'interfaccia logica.
  - **I link attivi (linee tratteggiate verdi) partono dal bordo esterno del rettangolo/interfaccia e non dal centro del router.**
  - I rettangoli sono colorati:
    - Verde (interfaccia up)
    - Rosso (interfaccia down)
    - Giallo (hover su interfaccia: quando il mouse passa sopra un rettangolo, questo viene evidenziato in giallo, indipendentemente dallo stato up/down)
  - Se la VLAN non è configurata, o il router adiacente non è presente nella griglia, il rettangolo non viene disegnato (nessuna interfaccia visibile in quella direzione).
  - I rettangoli sono disegnati in modo da non sovrapporsi al cerchio del router.
  - **La hitbox delle interfacce è pixel-perfect e identica al disegno:** viene usata una superficie temporanea ruotata e controllo alpha per la rilevazione del click, garantendo coerenza totale tra area cliccabile e area visibile.
  - **Debug visivo:** è possibile abilitare un overlay blu trasparente per mostrare la hitbox effettiva delle interfacce durante lo sviluppo.
  - **Il click su un’interfaccia modifica lo stato up/down solo se il router è claimato dal player locale e ci sono token disponibili.**
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
  - Se il router è claimato da altro player, il colore è arancione.
- **Stato delle interfacce:**
  - Le interfacce sono sempre visibili (se configurate), ma il loro colore cambia in base allo stato:
    - Verde se l'interfaccia è attiva (up, cioè 'admin up' secondo lo stato appreso dalla chiamata API ricorrente)
    - Rosso se l'interfaccia è inattiva (down, cioè 'admin down' secondo lo stato appreso dalla chiamata API ricorrente)
    - Giallo se in hover
- **Hostname:**
  - Box rettangolare adattivo sempre visibile sotto ogni router, stile pixel-art (bordi doppi, colori saturi), con bordo bianco e sfondo scuro.
  - Testo hostname sempre centrato, outline nero, e mai troncato.
  - Il box mostra sempre il valore aggiornato dal polling API, oppure '?' se non disponibile, senza ritardi o desincronizzazioni.
  - L'hostname mostrato nella UI è sempre quello letto via polling API dal campo description della loopback, oppure '?' se non disponibile. La sincronizzazione è in tempo reale.
- **Feedback visivo:**
  - Quando un router viene claimato, il colore del cerchio cambia immediatamente e viene mostrato un messaggio di conferma in stile pixel-art.
  - Quando un’interfaccia viene attivata/disattivata, il colore della freccia cambia in tempo reale e viene mostrato un feedback testuale.
- **Hover e click:**
  - Al passaggio del mouse su un router, il suo colore di sfondo diventa leggermente più chiaro per indicare che è selezionato, con effetto pixel-art (nessun glow/ombra soft).
  - Al click su un router:
    - Se il router non è claimato, viene avviata la procedura di claim.
    - Se il router è già claimato dal giocatore locale, il click non mostra più la finestra informativa (popup) ma non fa nulla (o in futuro potrà attivare altre azioni contestuali).
- **ID router:**
  - Gli ID (global_id, local_id, group_id) non sono visibili nella UI, ma vengono stampati a terminale per debug quando si seleziona il router.
- **Posizionamento:**
  - Il router è centrato nella cella della griglia, con padding per evitare sovrapposizioni.
- **Colore router:** Un router non claimato (cioè non claimato dal giocatore locale) viene sempre visualizzato di colore grigio (`config.GRAY`) nella UI, indipendentemente dal contenuto del campo hostname/description. Solo i router effettivamente claimati dal giocatore locale sono colorati con il colore del player. I router claimati da altri giocatori sono arancioni.
- **Legenda:**
  - In basso nella UI NON è più presente una legenda: tutte le regole di colori e simboli sono documentate solo in questo file e non più mostrate in-game.
  - Non sono più presenti riferimenti o colori relativi ad altri giocatori.
  - I router claimati da altri giocatori (cioè con claimed_by_name valorizzato e diverso dal player locale) sono visualizzati in **arancione** nella griglia.
  - I router claimati dal giocatore locale sono colorati secondo il colore del player.
  - I router non claimati restano grigi.
  - La legenda UI deve riflettere questa distinzione cromatica.

### 6.2 Box Giocatore e Token

- I due box sono affiancati, con la stessa larghezza (adattiva, ma identica), stessa altezza, stesso bordo doppio, stesso font e padding.
- Il testo all'interno è centrato verticalmente e orizzontalmente.
- Il box Token non ha più il cerchio, solo testo e countdown integrato.
- Se il nome giocatore è troppo lungo, viene troncato con '...'.
- Il layout si adatta alla larghezza della finestra, ma i due box restano sempre identici come dimensione e stile.

### 6.3 Modalità Custom: selezione numero router

- Oltre alle modalità predefinite (4x4, 5x5, 6x6), il gioco offre una modalità **Custom**.
- In modalità Custom, il giocatore può scegliere la dimensione della griglia di router (NxN) tramite un popup o selettore numerico prima di iniziare la partita.
- La UI mostra un popup pixel-art che permette di selezionare un valore N compreso tra 2 e 8 (inclusi), con pulsanti + e - oppure un campo numerico.
- Dopo la conferma, la griglia viene generata con NxN router e tutte le regole di visualizzazione, claim, interfacce e link si adattano automaticamente alla nuova dimensione.
- Tutti i mockup e le regole di disegno restano invariati, ma la griglia si adatta dinamicamente alla dimensione scelta.

### 6.4 Sintesi delle condizioni di visibilità
- Un'interfaccia è visibile solo se:
  - La VLAN è configurata
  - Il router adiacente è presente nella griglia
- Un link attivo è visibile solo se:
  - Entrambi i router sono visibili nella griglia
  - Esiste una neighborship attiva tra i due router

### 6.5 Mockup e schermate ASCII della UI

(Mockup e ASCII invariati, vedere sezione precedente per esempi di layout, box, router, interfacce, link, hostname, claim, colori, feedback, modalità custom.)

---

**Tutte le regole e i comportamenti descritti sono ora implementati e rispettati nella UI e nella logica di gioco.**