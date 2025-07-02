# config.py
"""
Contiene parametri di configurazione e costanti globali.
"""

class Config:
    WIDTH = 1680  # aumentato per maggiore spazio
    HEIGHT = 1000  # aumentato per maggiore spazio
    FPS = 60
    GRID_SIZE = 4  # Default
    API_POLL_INTERVAL = 3  # secondi
    TOKEN_RECHARGE_TIME = 10  # secondi
    MAX_TOKENS = 4
    ROUTER_COLORS = [
        (100, 149, 237),  # blu giocatore 1
        (255, 105, 180),  # rosa giocatore 2
        (186, 85, 211),   # lilla giocatore 3
        (152, 251, 152),  # verde menta giocatore 4
    ]
    GRAY = (180, 180, 180)
    YELLOW = (255, 215, 0)
    BACKGROUND = (245, 245, 245)
    FONT = "freesansbold.ttf"
    PLAYER_NAME = ""  # Nome del giocatore locale, impostato runtime
    ORANGE = (255, 140, 0)  # arancione per claim altro player
    # ...altre costanti e parametri...
