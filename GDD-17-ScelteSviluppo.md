# GDD-17-Scelte di Sviluppo Software

Questo documento raccoglie tutte le principali scelte di sviluppo software adottate nel progetto "I am a Router".

## 1. Linguaggio e Framework
- **Linguaggio principale:** Python 3
- **Libreria grafica:** pygame per la UI 2D e la gestione degli eventi
- **Standard di codifica:** PEP8, con alcune eccezioni per leggibilità didattica

## 2. Architettura e Modularità
- **Separazione netta tra logica di gioco (router_grid.py) e rendering/UI (ui.py)**
- **Gestione della configurazione** centralizzata in `config.py`
- **Audio** gestito tramite modulo dedicato `audio.py`
- **Glossario e tutorial** integrati tramite `glossary.py`
- **API RESTCONF** simulate/locali per la comunicazione con i router virtuali

## 3. Logica di Claim e Stato Router
- Il claim di un router si basa sul parsing del campo `description` della loopback: solo se il nomegiocatore coincide con quello locale il router risulta claimato dal giocatore.
- I router claimati da altri giocatori sono visualizzati in arancione, quelli liberi in grigio, quelli propri nel colore player.
- L'hostname viene aggiornato solo se il campo description è presente e non vuoto, altrimenti viene mostrato `?`.
- **Claim router:** Un router è considerato claimato dal giocatore locale solo se il campo description della sua interfaccia loopback è nel formato `nomegiocatore_hostnameRouterVirtuale` **e il `nomegiocatore` coincide esattamente con quello inserito dal giocatore locale**. In tutti gli altri casi (description mancante, vuota, o nomegiocatore diverso), il router è considerato non claimato dal client locale.

## 4. Interfacce e VLAN
- Le frecce delle interfacce (N/S/E/W) sono disegnate **solo se la VLAN è configurata** (cioè esiste un link logico tra router).
- Il colore delle frecce è:
  - Verde se l'interfaccia è up
  - Rosso se down
  - Giallo se il mouse è sopra la freccia (hover), indipendentemente dallo stato up/down
- La posizione della freccia per l'hover è calcolata esattamente come nel rendering, per coerenza visiva e funzionale.

## 5. UI e UX
- UI in stile retro pixel-art, palette pastello
- Griglia adattiva in base alla dimensione selezionata
- Legenda sempre visibile in basso, aggiornata in base alle regole cromatiche
- Popup testuali generici per input nome/hostname
- Feedback visivo immediato per claim, errori, cambi stato interfaccia
- Solo i token e il timer del giocatore locale sono visibili
- Hostname sempre visibile sotto ogni router

## 6. Sincronizzazione e Aggiornamento Stato
- Polling continuo delle API per aggiornare stato router/interfacce/token in tempo reale
- Nessuna gestione locale "stale" dello stato: la UI riflette sempre lo stato reale lato backend

## 7. Gestione errori e robustezza
- Errori di claim, API o input sono sempre mostrati a schermo con messaggio rosso
- La logica di estrazione hostname è robusta rispetto a dati assenti o vuoti
- Nessun crash blocking: errori gestiti sempre con fallback visivo

## 8. Altre scelte
- Tutti gli ID router sono visibili solo a terminale per debug
- Nessun riferimento a token o timer di altri giocatori nella UI
- Tutte le regole di rendering e logica sono documentate e mantenute in sync con il GDD

---

**Ultimo aggiornamento:** 26/05/2025
