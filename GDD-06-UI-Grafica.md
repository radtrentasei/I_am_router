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
  - Quattro frecce spesse (5px) orientate verso nord, sud, est, ovest, visibili **solo se la VLAN corrispondente è configurata** (cioè esiste un link logico tra router).
  - Le frecce sono disegnate **all'interno** del cerchio del router, puntando dal bordo verso il centro.
  - Colore frecce:
    - Verde (interfaccia up)
    - Rosso (interfaccia down)
    - **Giallo (hover su interfaccia: quando il mouse passa sopra una freccia, questa viene evidenziata in giallo, indipendentemente dallo stato up/down)**
  - Se la VLAN non è configurata, la freccia non viene disegnata (nessuna interfaccia visibile in quella direzione).
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
  - I router claimati da altri giocatori (cioè con claimed_by_name valorizzato e diverso dal player locale) sono visualizzati in **arancione** nella griglia.
  - I router claimati dal giocatore locale sono colorati secondo il colore del player.
  - I router non claimati restano grigi.
  - La legenda UI deve riflettere questa distinzione cromatica.

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
- La logica di estrazione hostname è robusta rispetto a dati assenti o vuoti nelle risposte API: il client imposta sempre l'hostname a '?' se l' interfaccia Loopback{group_id} non è presente o il campo description è vuoto.
- L'hostname viene aggiornato solo se il campo description è presente e non vuoto.
- Il nome del giocatore locale viene visualizzato nella UI sopra i token, in alto a sinistra, e viene troncato con '...' se troppo lungo per lo spazio disponibile.

### Esempio di mockup ASCII della griglia e legenda UI

```
Legenda: ● grigio = router libero   ● blu = tuo router   ● arancione = router claimato da altri
         ↑/→/↓/← verdi = interfaccia up   rosse = interfaccia down   gialle = hover/non configurata
         [Rx] = hostname del router (o '?' se non disponibile)

      ↑         ↑         ↑         ↑
    ┌───┐    ┌───┐    ┌───┐    ┌───┐
←  │ ● │  →← │ ● │  →← │ ● │  →← │ ● │  →
    └───┘    └───┘    └───┘    └───┘
      ↓         ↓         ↓         ↓
   [Router1] [PlayerA_R2] [PlayerB_R3] [Router4]

      ↑         ↑         ↑         ↑
    ┌───┐    ┌───┐    ┌───┐    ┌───┐
←  │ ● │  →← │ ● │  →← │ ● │  →← │ ● │  →
    └───┘    └───┘    └───┘    └───┘
      ↓         ↓         ↓         ↓
   [Router5] [PlayerA_R6] [PlayerB_R7] [Router8]

Legenda colori:
- ● grigio: router non claimato
- ● blu: router claimato dal giocatore locale
- ● arancione: router claimato da altro giocatore
- ↑/→/↓/← verdi: interfaccia up
- ↑/→/↓/← rosse: interfaccia down
- **↑/→/↓/← gialle: hover/interfaccia non configurata**

Esempio dettagliato di router:

      ↑
    ┌───┐
←  │ ● │  →
    └───┘
      ↓
   [PlayerA_R2]

- In questo esempio:
  - Il router centrale è claimato dal player locale (blu)
  - L'interfaccia nord è up (freccia verde)
  - L'interfaccia ovest è down (freccia rossa)
  - L'interfaccia est è up (freccia verde)
  - L'interfaccia sud è down (freccia rossa)
  - Sotto il router è visibile l'hostname aggiornato
```
