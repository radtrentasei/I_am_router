# main.py
"""
Entrypoint del gioco 'I am a Router'.
Inizializza Pygame, carica la configurazione, avvia il ciclo principale e gestisce la schermata iniziale.
"""
import os
import pygame
from config import Config
from ui import GameUI
from events import EventManager
from router_grid import RouterGrid
from api import APIDriver
from glossary import Glossary
from audio import AudioManager

# Forza il driver audio dummy su Linux/WSL/ambienti senza audio
if not os.environ.get("SDL_AUDIODRIVER"):
    os.environ["SDL_AUDIODRIVER"] = "dummy"


def main():
    pygame.init()
    config = Config()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("I am a Router")
    clock = pygame.time.Clock()

    # Inizializza moduli
    api = APIDriver(config)
    grid = RouterGrid(config, api)
    glossary = Glossary(config)
    audio = AudioManager(config)
    ui = GameUI(config, screen, grid, glossary, audio)
    events = EventManager(config, ui, grid, api, glossary, audio)
    ui.set_claim_callback(events.claim_router)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                ui.handle_key(event)
                if ui.state == "game" and Config.PLAYER_NAME != ui.player_name:
                    Config.PLAYER_NAME = ui.player_name
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ui.handle_mouse_button(event.pos, event.button)
            else:
                events.handle(event)
        if ui.state == "game" and Config.PLAYER_NAME != ui.player_name:
            Config.PLAYER_NAME = ui.player_name
        ui.update_hover(pygame.mouse.get_pos())
        api.poll()  # Polling asincrono (gestito internamente)
        ui.update()
        ui.render()
        pygame.display.flip()
        clock.tick(config.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

# Gestione modalità custom: popup pixel-art per selezione dimensione griglia
# (Popup e logica già in ui.py, qui serve solo adattare la griglia)
# Se la UI imposta grid.size tramite set_size(), la UI e la logica si adattano dinamicamente.
# Nessuna modifica necessaria qui: la logica custom è demandata a ui.py e RouterGrid.set_size().
