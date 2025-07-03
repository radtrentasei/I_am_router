# README.md

# I am a Router

Gioco educativo multiplayer per imparare i fondamenti del networking su router reali tramite API RESTCONF.

## Avvio rapido

1. Crea e attiva un virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Installa le dipendenze:
   ```sh
   pip install -r requirements.txt
   ```
3. Avvia il gioco:
   ```sh
   python main.py
   ```

## Struttura del progetto
- `main.py`: entrypoint e ciclo principale
- `config.py`: configurazione e costanti
- `api.py`: gestione RESTCONF e debug API
- `router_grid.py`: logica griglia e router
- `ui.py`: rendering grafico e UI
- `events.py`: gestione eventi
- `glossary.py`: glossario e tutorial
- `audio.py`: effetti sonori e musica
- `utils.py`: funzioni di utilità
- `requirements.txt`: dipendenze Python

## Documentazione (GDD)
Il Game Design Document è organizzato in 5 sezioni principali:
- `GDD-01-Panoramica.md`: Titolo, visione generale, target e obiettivi
- `GDD-02-Gameplay.md`: Meccaniche di gioco, regole, tutorial e condizioni di vittoria
- `GDD-03-Design-UI.md`: Interfaccia utente, grafica e stile pixel-art
- `GDD-04-Specifiche-Tecniche.md`: Sistema API, architettura e implementazione
- `GDD-05-Appendici.md`: Audio, glossario, qualità del codice e scelte di sviluppo

## Note
- Tutte le azioni di gioco sono solo tramite mouse (eccetto input nome/hostname)
- Ogni chiamata API viene stampata a terminale per debug
- Compatibile con Windows, macOS, Linux
