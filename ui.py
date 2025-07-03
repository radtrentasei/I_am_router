# ui.py
"""
Rendering grafico, gestione pulsanti, popup, feedback visivi.
"""
import pygame
import math
import time

# Parametri di default per router/interfacce
INTERFACE_SIZE = 32  # Era ARROW_SIZE
INTERFACE_WIDTH = 5  # Era ARROW_WIDTH
ROUTER_RADIUS_BASE = 48
BORDER_WIDTH = 3
HOVER_LIGHTEN = 30

class GameUI:
    def __init__(self, config, screen, grid, glossary, audio):
        self.config = config
        self.screen = screen
        self.grid = grid
        self.glossary = glossary
        self.audio = audio
        self.font = pygame.font.Font(config.FONT, 20)
        self.small_font = pygame.font.Font(config.FONT, 16)
        self.big_font = pygame.font.Font(config.FONT, 32)
        self.selected_router = None
        self.hovered_router = None
        self.hovered_interface = None
        self.popup = None
        self.error_msg = None
        self.error_timer = 0
        self.show_glossary = False
        self.show_tutorial = False
        self.tutorial_step = 0
        self.legend_rect = None
        self.router_goal = [0, self.grid.size-1]  # esempio: router obiettivo agli estremi
        self.last_feedback = None
        self.last_feedback_timer = 0
        self.claim_callback = None  # Callback per il claim router
        self.state = "splash"  # splash, menu, name, level, game, tutorial
        self.menu_selected = None
        self.level_selected = None
        self.player_name = ""
        self.name_input_active = False
        self.name_input_text = ""
        self.input_active = False
        self.input_text = ""
        self.input_callback = None
        self.input_prompt = ""

    def update(self):
        # Aggiorna timer feedback/errori
        if self.error_timer > 0:
            self.error_timer -= 1
        if self.last_feedback_timer > 0:
            self.last_feedback_timer -= 1
        # Aggiorna stato router/interfacce da API
        # Blocca update_from_api e update_tokens se tutorial offline
        if self.glossary.is_in_tutorial():
            return
        self.grid.update_from_api()
        self.grid.update_tokens()

    def _draw_background(self):
        # Sfondo rimosso: nessun disegno, funzione vuota
        pass

    def render(self):
        # Sfondo base
        self.screen.fill(self.config.BACKGROUND)
        self._draw_background()
        # Aggiorna stato router/interfacce da API ogni frame per riflettere cambi in tempo reale
        self.grid.update_from_api()
        self._draw_player_token_boxes()  # Box Giocatore/Token sempre in alto
        # Attiva/disattiva name_input_active in base allo stato
        self.name_input_active = (self.state == "name")
        if self.state == "splash":
            self._draw_splash()
            return
        if self.state == "menu":
            self._draw_menu()
            return
        if self.state == "level":
            self._draw_level_select()
            return
        if self.state == "name":
            self._draw_name_input()
            return
        if self.state == "glossary":
            self._draw_glossary()
            return
        self._draw_grid()
        self._draw_links()
        self._draw_tokens()
        self._draw_feedback()
        if self.popup:
            self._draw_popup()
        if self.show_glossary:
            self._draw_glossary()
        if self.show_tutorial:
            self._draw_tutorial()
        if self.error_msg and self.error_timer > 0:
            self._draw_error()
        if self.input_active:
            self._draw_text_input()

    def _draw_splash(self):
        self.screen.fill(self.config.BACKGROUND)
        # Titolo pixelart: effetto outline e ombra
        title = self.big_font.render("I am a Router", True, (255,255,255))
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            self.screen.blit(self.big_font.render("I am a Router", True, (30,30,30)), (self.config.WIDTH//2-title.get_width()//2+dx, 220+dy))
        self.screen.blit(title, (self.config.WIDTH//2-title.get_width()//2, 220))
        # Box pixelart per messaggio
        msg = self.font.render("Premi SPAZIO per continuare", True, (255,255,255))
        box = pygame.Rect(self.config.WIDTH//2-msg.get_width()//2-16, 340, msg.get_width()+32, 48)
        pygame.draw.rect(self.screen, (40,40,60), box)
        pygame.draw.rect(self.screen, (255,255,255), box, 2)
        pygame.draw.rect(self.screen, (30,30,30), box, 1)
        self.screen.blit(msg, (self.config.WIDTH//2-msg.get_width()//2, 340+12))

    def _draw_menu(self):
        self.screen.fill(self.config.BACKGROUND)
        # Titolo pixelart
        title = self.big_font.render("I am a Router", True, (255,255,255))
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            self.screen.blit(self.big_font.render("I am a Router", True, (30,30,30)), (self.config.WIDTH//2-title.get_width()//2+dx, 100+dy))
        self.screen.blit(title, (self.config.WIDTH//2-title.get_width()//2, 100))
        # Pulsanti pixelart
        btn_w, btn_h = 320, 60
        btn_x = self.config.WIDTH//2 - btn_w//2
        btn_ys = [220, 310, 400, 490]
        labels = ["Tutorial", "Play the game", "Glossario", "Credits"]
        colors = [(60,60,120), (60,120,60), (120,100,40), (80,80,80)]
        for i, (y, label, col) in enumerate(zip(btn_ys, labels, colors)):
            box = pygame.Rect(btn_x, y, btn_w, btn_h)
            pygame.draw.rect(self.screen, col, box)
            pygame.draw.rect(self.screen, (255,255,255), box, 2)
            pygame.draw.rect(self.screen, (30,30,30), box, 1)
            t = self.font.render(label, True, (255,255,255))
            self.screen.blit(t, (btn_x+btn_w//2-t.get_width()//2, y+btn_h//2-t.get_height()//2))
        # Evidenziazione hover pixelart
        mx, my = pygame.mouse.get_pos()
        for i, y in enumerate(btn_ys):
            if btn_x <= mx <= btn_x+btn_w and y <= my <= y+btn_h:
                pygame.draw.rect(self.screen, (255,255,0), (btn_x, y, btn_w, btn_h), 3)

    def _draw_level_select(self):
        self.screen.fill(self.config.BACKGROUND)
        title = self.big_font.render("Seleziona livello", True, (255,255,255))
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            self.screen.blit(self.big_font.render("Seleziona livello", True, (30,30,30)), (self.config.WIDTH//2-title.get_width()//2+dx, 120+dy))
        self.screen.blit(title, (self.config.WIDTH//2-title.get_width()//2, 120))
        btn_w, btn_h = 260, 60
        btn_x = self.config.WIDTH//2 - btn_w//2
        btn_ys = [240, 320, 400, 480]
        labels = ["Facile (2x2)", "Medio (3x3)", "Difficile (4x4)", "Estremo (8x8)"]
        for i, (y, label) in enumerate(zip(btn_ys, labels)):
            box = pygame.Rect(btn_x, y, btn_w, btn_h)
            pygame.draw.rect(self.screen, (60,60,120), box)
            pygame.draw.rect(self.screen, (255,255,255), box, 2)
            pygame.draw.rect(self.screen, (30,30,30), box, 1)
            t = self.font.render(label, True, (255,255,255))
            self.screen.blit(t, (btn_x+btn_w//2-t.get_width()//2, y+btn_h//2-t.get_height()//2))
        # Hover pixelart
        mx, my = pygame.mouse.get_pos()
        for i, y in enumerate(btn_ys):
            if btn_x <= mx <= btn_x+btn_w and y <= my <= y+btn_h:
                pygame.draw.rect(self.screen, (255,255,0), (btn_x, y, btn_w, btn_h), 3)

    def _draw_name_input(self):
        self.screen.fill(self.config.BACKGROUND)
        title = self.big_font.render("Inserisci il tuo nome", True, (255,255,255))
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            self.screen.blit(self.big_font.render("Inserisci il tuo nome", True, (30,30,30)), (self.config.WIDTH//2-title.get_width()//2+dx, 160+dy))
        self.screen.blit(title, (self.config.WIDTH//2-title.get_width()//2, 160))
        box_w, box_h = 340, 60
        box_x = self.config.WIDTH//2 - box_w//2
        box_y = 260
        box = pygame.Rect(box_x, box_y, box_w, box_h)
        pygame.draw.rect(self.screen, (40,40,60), box)
        pygame.draw.rect(self.screen, (255,255,255), box, 2)
        pygame.draw.rect(self.screen, (30,30,30), box, 1)
        # Mostra sempre il testo in inserimento con cursore lampeggiante
        name = self.name_input_text
        # Cursore lampeggiante ogni 500ms
        show_cursor = int(time.time()*2) % 2 == 0
        display_text = name + ("_" if show_cursor else " ")
        t = self.font.render(display_text, True, (255,255,255))
        self.screen.blit(t, (box_x+20, box_y+box_h//2-t.get_height()//2))
        hint = self.small_font.render("(max 10 caratteri, premi Invio)", True, (200,200,200))
        self.screen.blit(hint, (self.config.WIDTH//2-hint.get_width()//2, box_y+box_h+16))

    def _get_adaptive_router_radius(self):
        # Calcola il raggio del router in base alla dimensione della griglia
        size = self.grid.size
        margin_x = 120
        margin_y = 80
        cell_w = (self.config.WIDTH - 2*margin_x) // size
        cell_h = (self.config.HEIGHT - 220) // size
        # Il router deve stare comodo nella cella, lasciando spazio per interfacce e box hostname
        r = min(cell_w, cell_h) // 2 - 18
        return max(18, min(r, 48))  # Limite minimo/massimo

    def _get_adaptive_interface_size(self):
        """
        Restituisce (lunghezza, larghezza) del rettangolo interfaccia in base alla dimensione della griglia.
        Le interfacce devono essere proporzionate rispetto al router e alla cella, per evitare accavallamenti.
        In modalità Estremo (8x8) le interfacce sono più piccole per garantire leggibilità.
        """
        size = self.grid.size
        margin_x = 120
        margin_y = 80
        cell_w = (self.config.WIDTH - 2*margin_x) // size
        cell_h = (self.config.HEIGHT - 220) // size
        router_radius = self._get_adaptive_router_radius()
        if size >= 8:
            rect_len = min(int(router_radius * 0.9), int(min(cell_w, cell_h) * 0.45))
            rect_w = max(6, int(router_radius * 0.22))
        else:
            rect_len = min(int(router_radius * 1.2), int(min(cell_w, cell_h) * 0.6))
            rect_w = max(10, int(router_radius * 0.35))
        return rect_len, rect_w

    def _draw_grid(self):
        size = self.grid.size
        margin_x = 60  # ridotto per più spazio
        margin_y = 40  # ridotto per più spazio
        cell_w = (self.config.WIDTH - 2*margin_x) // size
        cell_h = (self.config.HEIGHT - 160) // size  # meno spazio per barra superiore
        ROUTER_W = ROUTER_H = self._get_adaptive_router_radius() * 2
        for idx, router in enumerate(self.grid.routers):
            row, col = router["row"], router["col"]
            x = margin_x + col * cell_w + cell_w//2
            y = margin_y + row * cell_h + cell_h//2
            if not (0 <= row < size and 0 <= col < size):
                continue
            # Colore router secondo GDD-03-Design-UI.md
            if router["claimed_by"] is None:
                # GDD: Grigio per router libero, non claimato da nessun giocatore
                color = self.config.GRAY
            elif router["claimed_by"] == 0:
                # GDD: Blu per router claimato dal giocatore locale
                color = self.config.ROUTER_COLORS[0]  # Blu del giocatore locale
            else:
                # GDD: Arancione per router claimato da altro giocatore
                color = self.config.ORANGE
            # GDD: Bordo giallo spesso 3px se router obiettivo 
            # TODO: Implementare logica corretta basata su (groupID, localID) invece di indici semplici
            border_col = self.config.YELLOW if (row in self.router_goal or col in self.router_goal) else (255,255,255)
            # Rettangolo pixel-art router
            rect = pygame.Rect(x-ROUTER_W//2, y-ROUTER_H//2, ROUTER_W, ROUTER_H)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, border_col, rect, 3)
            pygame.draw.rect(self.screen, (30,30,30), rect, 1)
            # Interfacce: rettangoli pixel-art
            for d, angle in zip(["N","E","S","W"],[270,0,90,180]):
                iface = router["interfaces"][d]
                if iface["vlan"] is None:
                    continue
                nrow, ncol = row, col
                if d == "N": nrow -= 1
                elif d == "S": nrow += 1
                elif d == "E": ncol += 1
                elif d == "W": ncol -= 1
                if not (0 <= nrow < size and 0 <= ncol < size):
                    continue
                if self.hovered_interface == (idx, d):
                    rect_col = (255, 220, 40)
                elif iface["up"]:
                    rect_col = (0, 200, 0)
                else:
                    rect_col = (220, 0, 0)
                rect_len, rect_w = self._get_adaptive_interface_size()
                # Distanza extra in modalità Estremo
                extra_dist = 0
                if size >= 8:
                    extra_dist = int(ROUTER_W * 0.18)  # aumenta la distanza del rettangolo dall'esterno del router
                rad = math.radians(angle)
                cx = x + int(math.cos(rad)*(ROUTER_W//2-24 + extra_dist))
                cy = y + int(math.sin(rad)*(ROUTER_H//2-24 + extra_dist))
                dx = int(math.cos(rad)*rect_len//2)
                dy = int(math.sin(rad)*rect_len//2)
                rect_center = (cx+dx, cy+dy)
                iface_rect = pygame.Rect(0, 0, rect_len, rect_w)
                iface_rect.center = rect_center
                pygame.draw.rect(self.screen, (255,255,255), iface_rect.inflate(4,4))
                pygame.draw.rect(self.screen, (0,0,0), iface_rect.inflate(8,8))
                pygame.draw.rect(self.screen, rect_col, iface_rect)
            # GDD: Hostname box sempre visibile sotto ogni router
            self._draw_hostname_box_pixel(x, y+ROUTER_H//2+8, router["hostname"])

    def _draw_player_token_boxes(self):
        # Box Giocatore e Token affiancati, identici, centrati in alto, stile pixel-art
        box_w, box_h = 280, 56
        pad = 24
        y = 16
        total_w = box_w*2 + pad
        x0 = self.config.WIDTH//2 - total_w//2
        # Box Giocatore
        name = self.player_name
        label = f"Giocatore: {name}"
        if len(label) > 22:
            label = label[:19] + '...'
        rect_player = pygame.Rect(x0, y, box_w, box_h)
        pygame.draw.rect(self.screen, (40,40,60), rect_player)
        pygame.draw.rect(self.screen, (255,255,255), rect_player, 2)
        pygame.draw.rect(self.screen, (30,30,30), rect_player, 1)
        t = self.font.render(label, True, (255,255,255))
        self.screen.blit(t, (rect_player.x+box_w//2-t.get_width()//2, rect_player.y+box_h//2-t.get_height()//2))
        # Box Token - GDD: Solo token del giocatore locale
        tokens = self.grid.tokens  # Ora è un singolo valore, non array
        countdown = self.grid.token_timer  # Ora è un singolo valore
        token_text = f"Token: {tokens}"
        if countdown > 0:
            token_text += f"   +1 in {countdown}s"
        rect_token = pygame.Rect(x0+box_w+pad, y, box_w, box_h)
        pygame.draw.rect(self.screen, (40,40,60), rect_token)
        pygame.draw.rect(self.screen, (255,255,255), rect_token, 2)
        pygame.draw.rect(self.screen, (30,30,30), rect_token, 1)
        t2 = self.font.render(token_text, True, (255,255,255))
        self.screen.blit(t2, (rect_token.x+box_w//2-t2.get_width()//2, rect_token.y+box_h//2-t2.get_height()//2))

    def _draw_links(self):
        # Linee tratteggiate pixel-art tra router con neighborship attiva
        for link in self.grid.links:
            if link.get("neighborship"):
                idx1, idx2 = link["router_a"], link["router_b"]
                r1 = self.grid.routers[idx1]
                r2 = self.grid.routers[idx2]
                size = self.grid.size
                if not (0 <= r1["row"] < size and 0 <= r1["col"] < size):
                    continue
                if not (0 <= r2["row"] < size and 0 <= r2["col"] < size):
                    continue
                dx = r2["col"] - r1["col"]
                dy = r2["row"] - r1["row"]
                if abs(dx) + abs(dy) != 1:
                    continue  # solo orizzontali/verticali
                x1, y1 = self._router_pos(idx1)
                x2, y2 = self._router_pos(idx2)
                # Calcola punto di partenza/arrivo dal bordo esterno dell’interfaccia
                if dx == 1:
                    x1 += self._get_adaptive_router_radius()
                    x2 -= self._get_adaptive_router_radius()
                elif dx == -1:
                    x1 -= self._get_adaptive_router_radius()
                    x2 += self._get_adaptive_router_radius()
                elif dy == 1:
                    y1 += self._get_adaptive_router_radius()
                    y2 -= self._get_adaptive_router_radius()
                elif dy == -1:
                    y1 -= self._get_adaptive_router_radius()
                    y2 += self._get_adaptive_router_radius()
                link_color = (0, 200, 0)
                self._draw_dashed_line(self.screen, link_color, (x1, y1), (x2, y2), dash_length=16, space_length=10, width=6)
            else:
                # ...existing code for dashed line if needed...
                pass

    def _draw_dashed_line(self, surf, color, start, end, dash_length, space_length, width):
        # Utility per linee tratteggiate
        x1, y1 = start
        x2, y2 = end
        dl = math.hypot(x2-x1, y2-y1)
        dx = (x2-x1)/dl
        dy = (y2-y1)/dl
        n = int(dl // (dash_length+space_length))
        for i in range(n):
            sx = x1 + (dash_length+space_length)*i*dx
            sy = y1 + (dash_length+space_length)*i*dy
            ex = sx + dash_length*dx
            ey = sy + dash_length*dy
            pygame.draw.line(surf, color, (sx,sy), (ex,ey), width)

    def _router_pos(self, idx):
        size = self.grid.size
        margin_x = 60  # uguale a _draw_grid
        margin_y = 40  # uguale a _draw_grid
        cell_w = (self.config.WIDTH - 2*margin_x) // size
        cell_h = (self.config.HEIGHT - 160) // size
        router = self.grid.routers[idx]
        x = margin_x + router["col"] * cell_w + cell_w//2
        y = margin_y + router["row"] * cell_h + cell_h//2
        return (x, y)

    # Deprecata: sostituita da _draw_player_token_boxes()
    def _draw_tokens(self):
        pass

    def set_claim_callback(self, callback):
        self.claim_callback = callback

    def update_hover(self, mouse_pos):
        # Aggiorna hovered_router e hovered_interface in base alla posizione del mouse
        self.hovered_router = None
        self.hovered_interface = None
        size = self.grid.size
        margin_x = 60  # uguale a _draw_grid
        margin_y = 40  # uguale a _draw_grid
        cell_w = (self.config.WIDTH - 2*margin_x) // size
        cell_h = (self.config.HEIGHT - 160) // size
        ROUTER_W = ROUTER_H = self._get_adaptive_router_radius() * 2
        mx, my = mouse_pos
        for idx, router in enumerate(self.grid.routers):
            row, col = router["row"], router["col"]
            x = margin_x + col * cell_w + cell_w//2
            y = margin_y + row * cell_h + cell_h//2
            rect = pygame.Rect(x-ROUTER_W//2, y-ROUTER_H//2, ROUTER_W, ROUTER_H)
            if rect.collidepoint(mx, my):
                self.hovered_router = idx
            # Interfacce
            for d, angle in zip(["N","E","S","W"],[270,0,90,180]):
                iface = router["interfaces"][d]
                if iface["vlan"] is None:
                    continue
                nrow, ncol = row, col
                if d == "N": nrow -= 1
                elif d == "S": nrow += 1
                elif d == "E": ncol += 1
                elif d == "W": ncol -= 1
                if not (0 <= nrow < size and 0 <= ncol < size):
                    continue
                rect_len, rect_w = self._get_adaptive_interface_size()
                rad = math.radians(angle)
                cx = x + int(math.cos(rad)*(ROUTER_W//2-24))
                cy = y + int(math.sin(rad)*(ROUTER_H//2-24))
                dx = int(math.cos(rad)*rect_len//2)
                dy = int(math.sin(rad)*rect_len//2)
                rect_center = (cx+dx, cy+dy)
                iface_rect = pygame.Rect(0, 0, rect_len, rect_w)
                iface_rect.center = rect_center
                if iface_rect.collidepoint(mx, my):
                    self.hovered_interface = (idx, d)

    def handle_mouse_button(self, pos, button):
        # Gestione click su router/interfacce/popup
        self.update_hover(pos)
        if self.popup:
            # Gestione popup custom/modalità
            # ...gestione popup custom se necessario...
            return
        if self.hovered_interface and self.state == "game":
            idx, direction = self.hovered_interface
            router = self.grid.routers[idx]
            player_id = router["claimed_by"]
            # Solo se claimato dal player locale e token > 0
            if (router["claimed_by"] == 0 and 
                self.config.PLAYER_NAME == router.get("claimed_by_name") and 
                self.grid.tokens > 0):
                up = router["interfaces"][direction]["up"]
                def feedback_cb(ok):
                    if ok:
                        self.last_feedback = f"Interfaccia {'attivata' if not up else 'disattivata'}"
                    else:
                        self.last_feedback = "Errore attivazione interfaccia"
                    self.last_feedback_timer = 60
                self.grid.set_interface_async(idx, direction, not up, callback=feedback_cb)
            else:
                self.last_feedback = "Solo il player che ha claimato può modificare l'interfaccia e servono token"
                self.last_feedback_timer = 60
            return
        if self.hovered_router is not None and self.state == "game":
            idx = self.hovered_router
            router = self.grid.routers[idx]
            # GDD: Controllo regole di claimabilità
            if router["claimed_by"] is None and router["hostname"] == "Router":
                if self.claim_callback:
                    self.claim_callback(idx)
            else:
                # GDD: Mostra errore se il router non è claimabile
                if router["claimed_by"] is not None:
                    self._show_error("Router già claimato!")
                elif router["hostname"] != "Router":
                    self._show_error("Claim possibile solo su router liberi (hostname 'Router')!")
            return
        if self.state == "level":
            # Gestione click sui pulsanti livello
            btn_w, btn_h = 260, 60
            btn_x = self.config.WIDTH//2 - btn_w//2
            btn_ys = [240, 320, 400, 480]
            levels = [2, 3, 4, 8]
            mx, my = pos
            for i, y in enumerate(btn_ys):
                if btn_x <= mx <= btn_x+btn_w and y <= my <= y+btn_h:
                    self.grid.set_size(levels[i])
                    self.state = "game"
                    return
        
        if self.state == "menu":
            # GDD: Gestione click sui pulsanti del menu principale
            btn_w, btn_h = 320, 60
            btn_x = self.config.WIDTH//2 - btn_w//2
            btn_ys = [220, 310, 400, 490]
            # labels = ["Tutorial", "Play the game", "Glossario", "Credits"]
            mx, my = pos
            for i, y in enumerate(btn_ys):
                if btn_x <= mx <= btn_x+btn_w and y <= my <= y+btn_h:
                    if i == 0:  # Tutorial
                        self.state = "tutorial"
                        self.glossary.show_tutorial()
                        self.glossary.tutorial_offline = True
                    elif i == 1:  # Play the game
                        self.state = "name"
                    elif i == 2:  # Glossario
                        self.state = "glossary"
                    elif i == 3:  # Credits
                        pass  # Per ora non implementato
                    return
        
        if self.state == "tutorial":
            # GDD: Gestione click sui pulsanti del tutorial
            box_w, box_h = 800, 400
            box_x = self.config.WIDTH//2 - box_w//2
            box_y = 150
            btn_w, btn_h = 120, 40
            btn_y = box_y + box_h + 20
            
            mx, my = pos
            
            # Pulsante Indietro
            prev_x = box_x
            prev_btn = pygame.Rect(prev_x, btn_y, btn_w, btn_h)
            if prev_btn.collidepoint(mx, my):
                self.glossary.prev_tutorial_step()
                return
            
            # Pulsante Avanti
            next_x = box_x + box_w - btn_w
            next_btn = pygame.Rect(next_x, btn_y, btn_w, btn_h)
            if next_btn.collidepoint(mx, my):
                self.glossary.next_tutorial_step()
                return
            
            # Pulsante Esci
            exit_x = box_x + box_w//2 - btn_w//2
            exit_btn = pygame.Rect(exit_x, btn_y, btn_w, btn_h)
            if exit_btn.collidepoint(mx, my):
                self.state = "menu"
                self.glossary.hide_tutorial()
                self.glossary.tutorial_offline = False
                return

    def handle_key(self, event):
        # Gestione input tastiera per menu, nome, popup, ecc.
        # Esempio base: ESC per uscire dai popup, ENTER per confermare input
        if self.popup:
            # Rimosso: gestione popup custom/modalità
            return
        if self.state == "name":
            if event.key == pygame.K_RETURN:
                self.player_name = self.name_input_text
                self.state = "level"
            elif event.key == pygame.K_BACKSPACE:
                self.name_input_text = self.name_input_text[:-1]
            else:
                if len(self.name_input_text) < 16 and event.unicode.isprintable():
                    self.name_input_text += event.unicode
        if self.state == "splash":
            if event.key == pygame.K_SPACE:
                self.state = "menu"  # GDD: Va al menu principale, non direttamente al nome
            return
        # ...altre logiche di navigazione/menu...
        if self.input_active:
            if event.key == pygame.K_RETURN:
                if self.input_callback:
                    self.input_callback(self.input_text)
                self.input_active = False
                self.input_text = ""
                self.input_prompt = ""
                self.input_callback = None
                return
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                if len(self.input_text) < 24 and event.unicode.isprintable():
                    self.input_text += event.unicode
            return

    def request_text_input(self, prompt, callback):
        self.input_active = True
        self.input_prompt = prompt
        self.input_text = ""
        self.input_callback = callback

    def _draw_hostname_box_pixel(self, x, y, hostname):
        text = self.font.render(hostname, True, (255,255,255))
        w, h = text.get_size()
        box = pygame.Rect(x-w//2-8, y, w+16, h+10)
        pygame.draw.rect(self.screen, (40,40,60), box)
        pygame.draw.rect(self.screen, (255,255,255), box, 2)
        pygame.draw.rect(self.screen, (30,30,30), box, 1)
        self.screen.blit(text, (x-w//2, y+5))

    def _draw_feedback(self):
        # Mostra messaggi di feedback temporanei (es: claim riuscito)
        if self.last_feedback and self.last_feedback_timer > 0:
            text = self.font.render(self.last_feedback, True, (255,255,0))
            w, h = text.get_size()
            x = self.config.WIDTH//2 - w//2
            y = 60
            box = pygame.Rect(x-16, y-8, w+32, h+16)
            pygame.draw.rect(self.screen, (40,40,60), box)
            pygame.draw.rect(self.screen, (255,255,255), box, 2)
            pygame.draw.rect(self.screen, (30,30,30), box, 1)
            self.screen.blit(text, (x, y))

    def _draw_text_input(self):
        # Popup pixel-art per input testuale
        prompt = self.input_prompt
        text = self.input_text
        font = self.font
        w_prompt, h_prompt = font.size(prompt)
        # Cursore lampeggiante ogni 500ms
        show_cursor = int(time.time()*2) % 2 == 0
        display_text = text + ("_" if show_cursor else " ")
        w_text, h_text = font.size(display_text)
        box_w = max(w_prompt, w_text) + 48
        box_h = h_prompt + h_text + 40
        x = self.config.WIDTH//2 - box_w//2
        y = self.config.HEIGHT//2 - box_h//2
        box = pygame.Rect(x, y, box_w, box_h)
        pygame.draw.rect(self.screen, (40,40,60), box)
        pygame.draw.rect(self.screen, (255,255,255), box, 2)
        pygame.draw.rect(self.screen, (30,30,30), box, 1)
        prompt_surf = font.render(prompt, True, (255,255,255))
        self.screen.blit(prompt_surf, (x+box_w//2-w_prompt//2, y+16))
        text_surf = font.render(display_text, True, (255,255,0))
        self.screen.blit(text_surf, (x+box_w//2-w_text//2, y+24+h_prompt))

    def _show_error(self, msg, duration=90):
        self.error_msg = msg
        self.error_timer = duration

    def _draw_error(self):
        """GDD: Mostra messaggio di errore in stile pixel-art rosso."""
        if self.error_msg and self.error_timer > 0:
            text = self.font.render(self.error_msg, True, (255,255,255))
            w, h = text.get_size()
            x = self.config.WIDTH//2 - w//2
            y = 120  # Sotto i box giocatore/token
            box = pygame.Rect(x-16, y-8, w+32, h+16)
            # GDD: Box rosso pixel-art per errori
            pygame.draw.rect(self.screen, (150, 40, 40), box)
            pygame.draw.rect(self.screen, (255,100,100), box, 2)
            pygame.draw.rect(self.screen, (100,20,20), box, 1)
            self.screen.blit(text, (x, y))

    def _draw_tutorial(self):
        """GDD: Modalità tutorial offline - implementazione step-by-step."""
        self.screen.fill(self.config.BACKGROUND)
        
        # Titolo tutorial
        title = self.big_font.render("Tutorial - I am a Router", True, (255,255,255))
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            self.screen.blit(self.big_font.render("Tutorial - I am a Router", True, (30,30,30)), 
                           (self.config.WIDTH//2-title.get_width()//2+dx, 50+dy))
        self.screen.blit(title, (self.config.WIDTH//2-title.get_width()//2, 50))
        
        # Box principale tutorial
        box_w, box_h = 800, 400
        box_x = self.config.WIDTH//2 - box_w//2
        box_y = 150
        box = pygame.Rect(box_x, box_y, box_w, box_h)
        pygame.draw.rect(self.screen, (40,40,60), box)
        pygame.draw.rect(self.screen, (255,255,255), box, 2)
        pygame.draw.rect(self.screen, (30,30,30), box, 1)
        
        # Contenuto del tutorial
        step_text = self.glossary.get_current_tutorial_text()
        y_offset = box_y + 30
        for line in step_text.split('\n'):
            if line.strip():
                text = self.font.render(line.strip(), True, (255,255,255))
                self.screen.blit(text, (box_x + 20, y_offset))
                y_offset += 30
        
        # Pulsanti navigazione
        btn_w, btn_h = 120, 40
        btn_y = box_y + box_h + 20
        
        # Pulsante Indietro
        prev_x = box_x
        prev_btn = pygame.Rect(prev_x, btn_y, btn_w, btn_h)
        pygame.draw.rect(self.screen, (60,60,120), prev_btn)
        pygame.draw.rect(self.screen, (255,255,255), prev_btn, 2)
        prev_text = self.font.render("Indietro", True, (255,255,255))
        self.screen.blit(prev_text, (prev_x + btn_w//2 - prev_text.get_width()//2, 
                                   btn_y + btn_h//2 - prev_text.get_height()//2))
        
        # Pulsante Avanti
        next_x = box_x + box_w - btn_w
        next_btn = pygame.Rect(next_x, btn_y, btn_w, btn_h)
        pygame.draw.rect(self.screen, (60,120,60), next_btn)
        pygame.draw.rect(self.screen, (255,255,255), next_btn, 2)
        next_text = self.font.render("Avanti", True, (255,255,255))
        self.screen.blit(next_text, (next_x + btn_w//2 - next_text.get_width()//2, 
                                   btn_y + btn_h//2 - next_text.get_height()//2))
        
        # Pulsante Esci
        exit_x = box_x + box_w//2 - btn_w//2
        exit_btn = pygame.Rect(exit_x, btn_y, btn_w, btn_h)
        pygame.draw.rect(self.screen, (120,60,60), exit_btn)
        pygame.draw.rect(self.screen, (255,255,255), exit_btn, 2)
        exit_text = self.font.render("Esci", True, (255,255,255))
        self.screen.blit(exit_text, (exit_x + btn_w//2 - exit_text.get_width()//2, 
                                   btn_y + btn_h//2 - exit_text.get_height()//2))
        
        # Gestione hover sui pulsanti
        mx, my = pygame.mouse.get_pos()
        if prev_btn.collidepoint(mx, my):
            pygame.draw.rect(self.screen, (255,255,0), prev_btn, 3)
        elif next_btn.collidepoint(mx, my):
            pygame.draw.rect(self.screen, (255,255,0), next_btn, 3)
        elif exit_btn.collidepoint(mx, my):
            pygame.draw.rect(self.screen, (255,255,0), exit_btn, 3)