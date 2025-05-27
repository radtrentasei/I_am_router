# events.py
"""
Gestione degli eventi mouse e input nome/hostname.
"""
import pygame

class EventManager:
    def __init__(self, config, ui, grid, api, glossary, audio):
        self.config = config
        self.ui = ui
        self.grid = grid
        self.api = api
        self.glossary = glossary
        self.audio = audio
        self.input_active = False
        self.input_text = ""
        self.input_callback = None
        self.claim_router_idx = None
        self.claim_player_id = 0  # Per demo: sempre player 0

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Gestione click sinistro/destro
            self.ui.handle_mouse_button(event.pos, event.button)
        # Rimuovi gestione KEYDOWN per input nome (ora in GameUI)

    def request_text_input(self, callback):
        self.input_active = True
        self.input_text = ""
        self.input_callback = callback

    def claim_router(self, idx):
        # Richiede input hostname, poi effettua il claim
        self.claim_router_idx = idx
        def on_hostname_input(hostname):
            player_id = self.claim_player_id
            hostname = hostname[:10]
            ok = self.grid.claim_router(idx, player_id, hostname)
            if ok:
                self.audio.play("claim")
                print(f"[DEBUG] Claim router {idx} da player {player_id} hostname={self.grid.config.PLAYER_NAME}_{hostname}")
            else:
                self.ui._show_error("Errore API claim router")
                print(f"[DEBUG] Claim fallito per router {idx}")
        self.ui.request_text_input("Inserisci hostname per il router", on_hostname_input)
