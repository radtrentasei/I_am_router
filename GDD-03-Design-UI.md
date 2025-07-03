# GDD-03-Design-UI

## 1. Stile Grafico Generale

### 1.1 Caratteristiche Principali
- **Gioco 2D, schermo intero, stile retro gaming pixel-art 16-bit**
- **Palette colori**: Pastello (azzurro chiaro, rosa, lilla, verde menta, giallo pallido)
- **Nessun effetto moderno**: Niente antialias, glow, gradienti, glassmorphism, font sans-serif moderno, ombre soft
- UI adattiva, leggibile, centrata, senza overflow
- **Nessuna legenda in-game**: Tutte le regole di colori e simboli sono documentate solo in questo file

### 1.2 Principi di Design
- Visualizzazione dello stato in tempo reale tramite letture dai dispositivi
- Stato token, timer, azioni disponibili e stato dei router sempre visibili e aggiornati dinamicamente
- Visualizzazione grafica dei link attivi tra router con neighborship di routing attiva
- Hostname router sempre visibile, ID router solo a terminale per debug
- Glossario accessibile dal menu e in-game

## 2. Sistema di Colorazione Router

### 2.1 Regole di Colore
- **Grigio**: Router libero, non claimato da nessun giocatore
- **Blu**: Router claimato dal giocatore locale (colore del giocatore)
- **Arancione**: Router claimato da altro giocatore
- **Bordo giallo spesso 3px**: Router obiettivo (indipendentemente dal claim)

### 2.2 Determinazione dello Stato
- La colorazione è determinata dal confronto tra il nomegiocatore locale e quello letto dalla description della loopback
- Un router con description valorizzata ma nomegiocatore diverso da quello locale appare come non claimato (grigio) e non può essere gestito dal giocatore locale

## 3. Rappresentazione Grafica dei Router

### 3.1 Forma Base
- **Cerchio pieno, stile pixel-art**, dimensione adattiva in base alla griglia e risoluzione
- Colore secondo le regole definite sopra
- Bordo giallo pixel-art (doppio bordo) se router obiettivo

### 3.2 Interfacce (Rettangoli)
- **Quattro rettangoli spessi** (non frecce), sprite pixel-art, orientati verso nord, sud, est, ovest
- Visibili **solo se**:
  - La VLAN corrispondente è configurata (esiste un link logico)
  - Il router adiacente in quella direzione è presente nella griglia
- **Colorazione**:
  - **Verde**: interfaccia up (admin up)
  - **Rosso**: interfaccia down (admin down)
  - **Giallo**: hover (indipendentemente dallo stato up/down)

### 3.3 Posizionamento e Hitbox
- I rettangoli sono disegnati senza sovrapporsi al cerchio del router
- I link attivi (linee tratteggiate verdi) partono dal bordo esterno del rettangolo
- **Hitbox pixel-perfect**: usa superficie temporanea ruotata e controllo alpha per rilevazione click
- **Debug visivo opzionale**: overlay blu trasparente per mostrare hitbox durante sviluppo

### 3.4 Hostname Box
- **Box rettangolare adattivo** sempre visibile sotto ogni router
- Stile pixel-art: bordi doppi, colori saturi, bordo bianco, sfondo scuro
- **Testo**: sempre centrato, outline nero, mai troncato
- Mostra valore aggiornato dal polling API o '?' se non disponibile
- Sincronizzazione in tempo reale senza ritardi

### 3.5 Link Attivi
- **Linee tratteggiate verdi** tra router con neighborship attiva
- Disegnate senza sovrapporsi ai cerchi dei router
- Bidirezionali, mostrano stato attivo della connessione

## 4. Interfaccia Utente

### 4.1 Box Giocatore e Token
- **Due box affiancati**: Giocatore e Token
- Stessa larghezza (adattiva ma identica), stessa altezza, stesso bordo doppio
- **Posizione**: centrati in alto
- **Contenuto**: testo centrato verticalmente e orizzontalmente
- **Box Token**: solo testo e countdown, senza cerchio
- **Troncamento**: nome giocatore troncato con '...' se troppo lungo

### 4.2 Input Testuali
- **Tutti gli input** (nome giocatore, hostname) visualizzati in tempo reale
- **Cursore lampeggiante**, senza placeholder moderni
- **Popup pixel-art**: box colorato, doppio bordo, input testuale, palette pastello

### 4.3 Feedback Visivo
- **Ogni azione** mostra messaggio di feedback in stile pixel-art
- **Box colorati**: testo outline, nessun effetto moderno
- **Errori**: sempre mostrati con messaggio rosso pixel-art
- **Hover**: colore leggermente più chiaro per router selezionati (effetto pixel-art)

### 4.4 Interazioni
- **Click su router libero**: avvia procedura di claim
- **Click su router claimato dal giocatore**: nessuna azione (per ora)
- **Click su interfaccia**: attiva/disattiva solo se router claimato e token disponibili
- **Feedback immediato**: freccia verde/rossa, token decrementato, messaggio pixel-art

## 5. Layout Responsivo

### 5.1 Modalità Estremo (8x8)
- **Interfacce più piccole** e ben distanziate dal router
- **Adattamento automatico** per garantire leggibilità e separazione visiva
- Tutte le regole di rendering restano invariate

### 5.2 Modalità Custom
- **Popup pixel-art** per selezione dimensione griglia (2x2 a 8x8)
- **Pulsanti + e -** oppure campo numerico
- **Adattamento dinamico** di tutte le regole di visualizzazione

## 6. Condizioni di Visibilità

### 6.1 Interfacce
Un'interfaccia è visibile solo se:
- La VLAN è configurata
- Il router adiacente è presente nella griglia

### 6.2 Link Attivi
Un link attivo è visibile solo se:
- Entrambi i router sono visibili nella griglia
- Esiste una neighborship attiva tra i due router

## 7. Schermata Principale

### 7.1 Splashscreen
- **Stile pixel-art 16-bit**: logo, titolo
- **Pulsanti**: "Gioca", "Tutorial", "Glossario"
- **Estetica**: colori saturi, doppio bordo, outline testo

### 7.2 Layout Principale
```
┌─────────────────────────────────────────┐
│  [Giocatore: Nome] [Token: 4 | 10s]     │
│                                         │
│    ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐   │
│    │  R  │  │  R  │  │  R  │  │  R  │   │
│    └─────┘  └─────┘  └─────┘  └─────┘   │
│   hostname  hostname hostname hostname   │
│                                         │
│    ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐   │
│    │  R  │  │  R  │  │  R  │  │  R  │   │
│    └─────┘  └─────┘  └─────┘  └─────┘   │
│   hostname  hostname hostname hostname   │
│                                         │
│                                         │
│                            [Glossario]  │
└─────────────────────────────────────────┘
```

### 7.3 Elementi UI Sempre Presenti
- **Box Giocatore e Token**: in alto a sinistra
- **Griglia Router**: centrata, con hostname sotto ogni router
- **Pulsante Glossario**: sempre accessibile
- **Messaggi di feedback**: overlay temporanei pixel-art

---
