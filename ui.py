# ui.py
"""
Rendering grafico, gestione pulsanti, popup, feedback visivi.
"""
import pygame
import math

ARROW_SIZE = 32
ARROW_WIDTH = 5
ROUTER_RADIUS = 48
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

    def render(self):
        # Aggiorna stato router/interfacce da API ogni frame per riflettere cambi in tempo reale
        self.grid.update_from_api()
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
        self.screen.fill(self.config.BACKGROUND)
        self._draw_grid()
        self._draw_links()
        self._draw_legend()
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
        title = self.big_font.render("I am a Router", True, (30,30,30))
        self.screen.blit(title, (self.config.WIDTH//2-title.get_width()//2, 220))
        msg = self.font.render("Premi SPAZIO per continuare", True, (80,80,80))
        self.screen.blit(msg, (self.config.WIDTH//2-msg.get_width()//2, 340))

    def _draw_menu(self):
        self.screen.fill(self.config.BACKGROUND)
        title = self.big_font.render("I am a Router", True, (30,30,30))
        self.screen.blit(title, (self.config.WIDTH//2-title.get_width()//2, 100))
        # Pulsanti menu: Tutorial, Play, Glossario, Credits
        btn_w, btn_h = 320, 60
        btn_x = self.config.WIDTH//2 - btn_w//2
        btn_ys = [220, 310, 400, 490]
        labels = ["Tutorial", "Play the game", "Glossario", "Credits"]
        colors = [(200,200,255), (200,255,200), (255,240,180), (220,220,220)]
        for i, (y, label, col) in enumerate(zip(btn_ys, labels, colors)):
            pygame.draw.rect(self.screen, col, (btn_x, y, btn_w, btn_h), border_radius=12)
            t = self.font.render(label, True, (30,30,30))
            self.screen.blit(t, (btn_x+btn_w//2-t.get_width()//2, y+btn_h//2-t.get_height()//2))
        # Evidenziazione hover
        mx, my = pygame.mouse.get_pos()
        for i, y in enumerate(btn_ys):
            if btn_x <= mx <= btn_x+btn_w and y <= my <= y+btn_h:
                pygame.draw.rect(self.screen, (120,120,255), (btn_x, y, btn_w, btn_h), 4, border_radius=12)

    def _draw_level_select(self):
        self.screen.fill(self.config.BACKGROUND)
        title = self.big_font.render("Seleziona livello", True, (30,30,30))
        self.screen.blit(title, (self.config.WIDTH//2-title.get_width()//2, 120))
        btn_w, btn_h = 260, 60
        btn_x = self.config.WIDTH//2 - btn_w//2
        btn_ys = [240, 320, 400, 480]
        labels = ["Facile (2x2)", "Medio (3x3)", "Difficile (4x4)", "Custom"]
        for i, (y, label) in enumerate(zip(btn_ys, labels)):
            pygame.draw.rect(self.screen, (220,240,255), (btn_x, y, btn_w, btn_h), border_radius=12)
            t = self.font.render(label, True, (30,30,30))
            self.screen.blit(t, (btn_x+btn_w//2-t.get_width()//2, y+btn_h//2-t.get_height()//2))
        # Hover
        mx, my = pygame.mouse.get_pos()
        for i, y in enumerate(btn_ys):
            if btn_x <= mx <= btn_x+btn_w and y <= my <= y+btn_h:
                pygame.draw.rect(self.screen, (120,180,255), (btn_x, y, btn_w, btn_h), 4, border_radius=12)

    def _draw_name_input(self):
        self.screen.fill(self.config.BACKGROUND)
        title = self.big_font.render("Inserisci il tuo nome", True, (30,30,30))
        self.screen.blit(title, (self.config.WIDTH//2-title.get_width()//2, 160))
        box_w, box_h = 340, 60
        box_x = self.config.WIDTH//2 - box_w//2
        box_y = 260
        pygame.draw.rect(self.screen, (255,255,255), (box_x, box_y, box_w, box_h), border_radius=10)
        pygame.draw.rect(self.screen, (30,30,30), (box_x, box_y, box_w, box_h), 2, border_radius=10)
        name = self.name_input_text if self.name_input_active else self.player_name
        t = self.font.render(name, True, (30,30,30))
        self.screen.blit(t, (box_x+20, box_y+box_h//2-t.get_height()//2))
        hint = self.small_font.render("(max 10 caratteri, premi Invio)", True, (80,80,80))
        self.screen.blit(hint, (self.config.WIDTH//2-hint.get_width()//2, box_y+box_h+16))

    def _draw_grid(self):
        size = self.grid.size
        margin_x = 120
        margin_y = 80
        cell_w = (self.config.WIDTH - 2*margin_x) // size
        cell_h = (self.config.HEIGHT - 220) // size
        for idx, router in enumerate(self.grid.routers):
            row, col = router["row"], router["col"]
            if row >= size or col >= size:
                continue  # Visualizza solo i router effettivamente nella griglia attiva
            x = margin_x + col * cell_w + cell_w//2
            y = margin_y + row * cell_h + cell_h//2
            # Colore: grigio se non claimato, colore player se claimato dal player locale, arancione se claimato da altri
            if router["claimed_by"] is None:
                if router.get("claimed_by_name") and router["claimed_by_name"] != self.config.PLAYER_NAME:
                    color = (255, 140, 0)  # arancione per router claimati da altri
                else:
                    color = self.config.GRAY
            else:
                color = self.config.ROUTER_COLORS[router["claimed_by"]]
            if self.hovered_router == idx:
                color = tuple(min(255, c+HOVER_LIGHTEN) for c in color)
            border_color = self.config.YELLOW if (row in self.router_goal or col in self.router_goal) else (255,255,255)
            pygame.draw.circle(self.screen, color, (x, y), ROUTER_RADIUS)
            pygame.draw.circle(self.screen, border_color, (x, y), ROUTER_RADIUS, BORDER_WIDTH)
            # Interfacce
            for d, angle in zip(["N","E","S","W"],[270,0,90,180]):
                iface = router["interfaces"][d]
                if iface["vlan"] is None:
                    continue  # Non disegnare la freccia se la vlan non è configurata
                # Hover: sempre giallo se il mouse è sopra la freccia
                if self.hovered_interface == (idx, d):
                    arrow_col = (200,200,0)
                elif iface["up"]:
                    arrow_col = (0,200,0)
                else:
                    arrow_col = (200,0,0)
                self._draw_arrow(x, y, angle, arrow_col)
            # Hostname box on hover
            if self.hovered_router == idx:
                self._draw_hostname_box(x, y+ROUTER_RADIUS+8, router["hostname"])

    def _draw_arrow(self, x, y, angle, color):
        # Disegna una freccia spessa orientata DENTRO il cerchio
        import math
        rad = math.radians(angle)
        # La linea termina prima della punta per non sovrapporsi
        start_dist = ROUTER_RADIUS - ARROW_SIZE - 8  # 8px di padding dal bordo
        end_dist = ROUTER_RADIUS - 36  # la linea si ferma ancora più prima della punta
        dx = math.cos(rad)
        dy = math.sin(rad)
        start = (x + dx * start_dist, y + dy * start_dist)
        end = (x + dx * end_dist, y + dy * end_dist)
        pygame.draw.line(self.screen, color, start, end, ARROW_WIDTH)
        # Punta grande e ben visibile
        tip = (x + dx * (ROUTER_RADIUS - 18), y + dy * (ROUTER_RADIUS - 18))
        perp1 = math.radians(angle+150)
        p1 = (tip[0]+math.cos(perp1)*16, tip[1]+math.sin(perp1)*16)
        perp2 = math.radians(angle-150)
        p2 = (tip[0]+math.cos(perp2)*16, tip[1]+math.sin(perp2)*16)
        pygame.draw.polygon(self.screen, color, [tip, p1, p2])

    def _draw_links(self):
        # Linee tratteggiate verdi tra router con neighborship attiva
        for link in self.grid.links:
            if link.get("neighborship"):
                idx1, idx2 = link["router_a"], link["router_b"]
                pos1 = self._router_pos(idx1)
                pos2 = self._router_pos(idx2)
                self._draw_dashed_line(self.screen, (0,200,0), pos1, pos2, 10, 10, 3)

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
        margin_x = 120
        margin_y = 80
        cell_w = (self.config.WIDTH - 2*margin_x) // size
        cell_h = (self.config.HEIGHT - 220) // size
        router = self.grid.routers[idx]
        x = margin_x + router["col"] * cell_w + cell_w//2
        y = margin_y + router["row"] * cell_h + cell_h//2
        return (x, y)

    def _draw_hostname_box(self, x, y, hostname):
        text = self.font.render(hostname, True, (255,255,255))
        w, h = text.get_size()
        box = pygame.Rect(x-w//2-8, y, w+16, h+8)
        pygame.draw.rect(self.screen, (30,30,30), box, border_radius=6)
        pygame.draw.rect(self.screen, (255,255,255), box, 2, border_radius=6)
        self.screen.blit(text, (x-w//2, y+4))

    def _draw_legend(self):
        # Legenda in basso
        legend = [
            (self.config.GRAY, "Router libero"),
            (self.config.ROUTER_COLORS[0], "Giocatore 1"),
            (self.config.ROUTER_COLORS[1], "Giocatore 2"),
            (self.config.ROUTER_COLORS[2], "Giocatore 3"),
            (self.config.ROUTER_COLORS[3], "Giocatore 4"),
            ((0,200,0), "Interfaccia up"),
            ((200,0,0), "Interfaccia down"),
            ((200,200,0), "Interfaccia non configurata/hover"),
            ((0,200,0), "Link attivo (neighborship)")
        ]
        y = self.config.HEIGHT - 60
        x = 60
        for color, label in legend:
            pygame.draw.rect(self.screen, color, (x, y, 32, 24))
            text = self.small_font.render(label, True, (30,30,30))
            self.screen.blit(text, (x+40, y+2))
            x += 220

    def _draw_tokens(self):
        # Stato token e timer SOLO per il giocatore locale (player 0)
        pid = 0
        color = self.config.ROUTER_COLORS[pid]
        x = 60
        y = 32
        player_name = self.config.PLAYER_NAME if hasattr(self.config, 'PLAYER_NAME') else ""
        max_width = 120
        if player_name:
            display_name = player_name
            name_text = self.small_font.render(f"Giocatore: {display_name}", True, (30,30,30))
            while name_text.get_width() > max_width and len(display_name) > 1:
                display_name = display_name[:-1]
                name_text = self.small_font.render(f"Giocatore: {display_name}...", True, (30,30,30))
            self.screen.blit(name_text, (x-10, y-32))
        pygame.draw.circle(self.screen, color, (x, y), 18)
        # Token: se tutorial offline, mostra infinito
        if self.glossary.is_in_tutorial():
            text = self.font.render(f"∞ Token", True, (30,30,30))
            self.screen.blit(text, (x-8, y-12))
            ttext = self.small_font.render(f"Modalità tutorial", True, (80,80,80))
            self.screen.blit(ttext, (x-24, y+18))
        else:
            tokens = self.grid.tokens[pid]
            text = self.font.render(f"{tokens} Token", True, (30,30,30))
            self.screen.blit(text, (x-8, y-12))
            timer = self.grid.token_timers[pid]
            ttext = self.small_font.render(f"+1 in {timer}s", True, (80,80,80))
            self.screen.blit(ttext, (x-24, y+18))

    def _draw_feedback(self):
        # Messaggio feedback azione
        if self.last_feedback and self.last_feedback_timer > 0:
            text = self.big_font.render(self.last_feedback, True, (0,0,0))
            w, h = text.get_size()
            self.screen.blit(text, (self.config.WIDTH//2-w//2, 40))

    def _draw_error(self):
        # Messaggio errore
        text = self.big_font.render(self.error_msg, True, (200,0,0))
        w, h = text.get_size()
        self.screen.blit(text, (self.config.WIDTH//2-w//2, 80))

    def _draw_popup(self):
        # Popup info router/interfaccia/inventario/credits
        if self.popup:
            typ, data = self.popup
            if typ == "router":
                idx = data
                router = self.grid.routers[idx]
                lines = [
                    f"Router: {router['hostname']}",
                    f"Claimed by: {router['claimed_by'] if router['claimed_by'] is not None else 'Nessuno'}",
                    f"ID: global={router['global_id']} local={router['local_id']} group={router['group_id']}"
                ]
                for d in ["N","E","S","W"]:
                    iface = router["interfaces"][d]
                    lines.append(f"{d}: {'UP' if iface['up'] else 'DOWN'} VLAN: {iface['vlan']}")
                self._draw_modal(lines)
            elif typ == "interface":
                idx, d = data
                router = self.grid.routers[idx]
                iface = router["interfaces"][d]
                lines = [
                    f"Interfaccia {d}",
                    f"Stato: {'UP' if iface['up'] else 'DOWN'}",
                    f"VLAN: {iface['vlan']}"
                ]
                self._draw_modal(lines)
            elif typ == "router_inventory":
                idx = data
                router = self.grid.routers[idx]
                # Esempio inventario: mostra hostname, stato claim, token, stato interfacce, VLAN, neighborship
                lines = [
                    f"INVENTARIO ROUTER",
                    f"Hostname: {router['hostname']}",
                    f"Claim: {'TUO' if router['claimed_by']==0 else 'No' if router['claimed_by'] is None else 'Altro'}",
                    f"Token: {self.grid.tokens[0]}",
                    f"ID: global={router['global_id']} local={router['local_id']} group={router['group_id']}"
                ]
                for d in ["N","E","S","W"]:
                    iface = router["interfaces"][d]
                    neigh = next((l for l in self.grid.links if (l["router_a"]==idx or l["router_b"]==idx) and l["vlan"]==iface["vlan"]), None)
                    neighb = neigh["neighborship"] if neigh else False
                    lines.append(f"{d}: {'UP' if iface['up'] else 'DOWN'} VLAN: {iface['vlan']} Neigh: {'SI' if neighb else 'NO'}")
                self._draw_modal(lines)
            elif typ == "credits":
                lines = [
                    "CREDITS",
                    "Game Design: A. Apiepoli",
                    "Sviluppo: Team I am a Router",
                    "2025 - Educational Networking Game",
                    "",
                    "Premi ESC o clicca per chiudere"
                ]
                self._draw_modal(lines)

    def _draw_modal(self, lines):
        w = 400
        h = 40 + 32*len(lines)
        x = self.config.WIDTH//2 - w//2
        y = self.config.HEIGHT//2 - h//2
        box = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, (255,255,255), box, border_radius=12)
        pygame.draw.rect(self.screen, (30,30,30), box, 3, border_radius=12)
        for i, line in enumerate(lines):
            text = self.font.render(line, True, (30,30,30))
            self.screen.blit(text, (x+24, y+24+i*32))

    def _draw_glossary(self):
        # Glossario interattivo
        w = 600
        h = 400
        x = self.config.WIDTH//2 - w//2
        y = self.config.HEIGHT//2 - h//2
        box = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, (255,255,255), box, border_radius=16)
        pygame.draw.rect(self.screen, (30,30,30), box, 3, border_radius=16)
        title = self.big_font.render("Glossario", True, (30,30,30))
        self.screen.blit(title, (x+20, y+20))
        for i, (term, desc) in enumerate(self.glossary.terms.items()):
            t = self.small_font.render(f"{term}: {desc}", True, (30,30,30))
            self.screen.blit(t, (x+20, y+80+i*28))

    def _draw_tutorial(self):
        # Tutorial step-by-step interattivo
        w = 700
        h = 220
        x = self.config.WIDTH//2 - w//2
        y = self.config.HEIGHT//2 - h//2
        box = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, (255,255,255), box, border_radius=16)
        pygame.draw.rect(self.screen, (30,30,30), box, 3, border_radius=16)
        step = self.glossary.tutorial_steps[self.glossary.current_step]
        text = self.big_font.render(f"Tutorial - Step {self.glossary.current_step+1}/{len(self.glossary.tutorial_steps)}", True, (30,30,30))
        self.screen.blit(text, (x+20, y+20))
        # Testo multilinea
        lines = step.split(". ")
        for i, line in enumerate(lines):
            t = self.font.render(line, True, (30,30,30))
            self.screen.blit(t, (x+20, y+80+i*32))
        # Pulsanti Avanti/Indietro
        btn_w, btn_h = 120, 40
        btn_y = y+h-60
        btn_prev = pygame.Rect(x+20, btn_y, btn_w, btn_h)
        btn_next = pygame.Rect(x+w-20-btn_w, btn_y, btn_w, btn_h)
        pygame.draw.rect(self.screen, (200,200,255), btn_prev, border_radius=10)
        pygame.draw.rect(self.screen, (200,255,200), btn_next, border_radius=10)
        tprev = self.font.render("Indietro", True, (30,30,30))
        tnext = self.font.render("Avanti", True, (30,30,30))
        self.screen.blit(tprev, (btn_prev.x+btn_w//2-tprev.get_width()//2, btn_prev.y+btn_h//2-tprev.get_height()//2))
        self.screen.blit(tnext, (btn_next.x+btn_w//2-tnext.get_width()//2, btn_next.y+btn_h//2-tnext.get_height()//2))
        # Pulsante Ripeti step
        btn_repeat = pygame.Rect(self.config.WIDTH//2-60, y+h-60, 120, 40)
        pygame.draw.rect(self.screen, (255,220,120), btn_repeat, border_radius=10)
        trepeat = self.font.render("Ripeti step", True, (30,30,30))
        self.screen.blit(trepeat, (btn_repeat.x+btn_repeat.width//2-trepeat.get_width()//2, btn_repeat.y+btn_repeat.height//2-trepeat.get_height()//2))
        self.tutorial_btn_repeat = btn_repeat

    def set_claim_callback(self, callback):
        self.claim_callback = callback

    def handle_mouse(self, pos):
        if self.state == "splash":
            return
        if self.state == "menu":
            btn_w, btn_h = 320, 60
            btn_x = self.config.WIDTH//2 - btn_w//2
            btn_y1 = 220
            btn_y2 = 310
            btn_y3 = 400
            btn_y4 = 490
            mx, my = pos
            if btn_x <= mx <= btn_x+btn_w and btn_y1 <= my <= btn_y1+btn_h:
                self.state = "tutorial"
                self.show_tutorial = True
                return
            if btn_x <= mx <= btn_x+btn_w and btn_y2 <= my <= btn_y2+btn_h:
                self.state = "level"
                return
            if btn_x <= mx <= btn_x+btn_w and btn_y3 <= my <= btn_y3+btn_h:
                self.show_glossary = True
                return
            if btn_x <= mx <= btn_x+btn_w and btn_y4 <= my <= btn_y4+btn_h:
                self._show_credits()
                return
            return
        if self.state == "name":
            self.name_input_active = True
            return
        if self.state in ("tutorial",):
            self.show_tutorial = False
            self.state = "menu"
            return
        idx, d = self._router_at_pos(pos)
        if idx is not None:
            if d is None:
                # Click su router: claim o attivazione interfaccia
                router = self.grid.routers[idx]
                print(f"[DEBUG] Router ID: global={router['global_id']} local={router['local_id']} group={router['group_id']}")
                if router["claimed_by"] is None and router["hostname"] == "Router":
                    # Claim router
                    if self.claim_callback:
                        self.claim_callback(idx)
                else:
                    # Se già claimato o hostname diverso da 'Router', mostra errore
                    self._show_error("Claim possibile solo su router liberi (hostname 'Router')!")
            else:
                # Click su interfaccia
                router = self.grid.routers[idx]
                if router["claimed_by"] is not None:
                    up = not router["interfaces"][d]["up"]
                    ok = self.grid.set_interface(idx, d, up)
                    if ok:
                        self.audio.play("link")
                        self.last_feedback = f"Interfaccia {d} {'UP' if up else 'DOWN'}"
                        self.last_feedback_timer = 60
                    else:
                        self._show_error("Errore API interfaccia")
                else:
                    self._show_error("Claima il router prima!")
        else:
            # Glossario, tutorial, chiudi popup
            if self.popup:
                self.popup = None
            elif self._glossary_button(pos):
                self.show_glossary = True
            elif self._tutorial_button(pos):
                self.show_tutorial = True

    def handle_mouse_button(self, pos, button):
        if self.popup:
            self.popup = None
            return
        if self.state == "splash":
            if button == 1:
                self.state = "menu"
            return
        if self.state == "menu":
            if button == 1:
                btn_w, btn_h = 320, 60
                btn_x = self.config.WIDTH//2 - btn_w//2
                btn_ys = [220, 310, 400, 490]
                mx, my = pos
                for i, y in enumerate(btn_ys):
                    if btn_x <= mx <= btn_x+btn_w and y <= my <= y+btn_h:
                        if i == 0:
                            self.state = "tutorial"
                            self.show_tutorial = True
                        elif i == 1:
                            self.state = "level"
                        elif i == 2:
                            self.show_glossary = True
                        elif i == 3:
                            self._show_credits()
                        return
            return
        if self.state == "level":
            if button == 1:
                btn_w, btn_h = 260, 60
                btn_x = self.config.WIDTH//2 - btn_w//2
                btn_ys = [240, 320, 400, 480]
                mx, my = pos
                for i, y in enumerate(btn_ys):
                    if btn_x <= mx <= btn_x+btn_w and y <= my <= y+btn_h:
                        if i == 0:
                            self.grid.set_size(2)
                        elif i == 1:
                            self.grid.set_size(3)
                        elif i == 2:
                            self.grid.set_size(4)
                        elif i == 3:
                            self.grid.set_size(self._ask_custom_size())
                        self.state = "name"
                        self.name_input_active = True
                        self.name_input_text = ""
                        return
            return
        if self.state != "game":
            return
        idx, d = self._router_at_pos(pos)
        if button == 1:
            if idx is not None:
                if d is None:
                    router = self.grid.routers[idx]
                    print(f"[DEBUG] Router ID: global={router['global_id']} local={router['local_id']} group={router['group_id']}")
                    if router["claimed_by"] is None and router["hostname"] == "Router":
                        if self.claim_callback:
                            self.claim_callback(idx)
                    else:
                        self._show_error("Claim possibile solo su router liberi (hostname 'Router')!")
                else:
                    router = self.grid.routers[idx]
                    if router["claimed_by"] is not None:
                        up = not router["interfaces"][d]["up"]
                        ok = self.grid.set_interface(idx, d, up)
                        if ok:
                            self.audio.play("link")
                            self.last_feedback = f"Interfaccia {d} {'UP' if up else 'DOWN'}"
                            self.last_feedback_timer = 60
                        else:
                            self._show_error("Errore API interfaccia")
                    else:
                        self._show_error("Claima il router prima!")
            else:
                if self.popup:
                    self.popup = None
                elif self._glossary_button(pos):
                    self.show_glossary = True
                elif self._tutorial_button(pos):
                    self.show_tutorial = True
        elif button == 3:
            # Click destro: mostra popup inventario router
            if idx is not None and d is None:
                self.popup = ("router_inventory", idx)

    def _router_at_pos(self, pos):
        # Restituisce (idx, dir) se il mouse è su un router/interfaccia
        size = self.grid.size
        margin_x = 120
        margin_y = 80
        cell_w = (self.config.WIDTH - 2*margin_x) // size
        cell_h = (self.config.HEIGHT - 220) // size
        mx, my = pos
        for idx, router in enumerate(self.grid.routers):
            x = margin_x + router["col"] * cell_w + cell_w//2
            y = margin_y + router["row"] * cell_h + cell_h//2
            dist = math.hypot(mx-x, my-y)
            if dist < ROUTER_RADIUS:
                # Verifica se su una freccia (solo se vlan configurata)
                for d, angle in zip(["N","E","S","W"],[270,0,90,180]):
                    iface = router["interfaces"][d]
                    if iface["vlan"] is None:
                        continue
                    rad = math.radians(angle)
                    # Calcola la posizione della punta della freccia come in _draw_arrow
                    tip_x = x + math.cos(rad) * (ROUTER_RADIUS - 18)
                    tip_y = y + math.sin(rad) * (ROUTER_RADIUS - 18)
                    if math.hypot(mx-tip_x, my-tip_y) < 18:
                        return idx, d
                return idx, None
        return None, None

    def _show_error(self, msg):
        self.error_msg = msg
        self.error_timer = 120
        self.audio.play("error")

    def _glossary_button(self, pos):
        # Area pulsante glossario (in basso a destra)
        x, y = self.config.WIDTH-180, self.config.HEIGHT-60
        w, h = 140, 40
        px, py = pos
        return x <= px <= x+w and y <= py <= y+h

    def _tutorial_button(self, pos):
        # Area pulsante tutorial (in basso a sinistra)
        x, y = 40, self.config.HEIGHT-60
        w, h = 140, 40
        px, py = pos
        return x <= px <= x+w and y <= py <= y+h

    def request_text_input(self, prompt, callback):
        self.input_active = True
        self.input_text = ""
        self.input_callback = callback
        self.input_prompt = prompt

    def _draw_text_input(self):
        # Popup per input testuale generico (nome o hostname)
        w, h = 420, 160
        x = self.config.WIDTH//2 - w//2
        y = self.config.HEIGHT//2 - h//2
        box = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, (255,255,255), box, border_radius=12)
        pygame.draw.rect(self.screen, (30,30,30), box, 3, border_radius=12)
        prompt = self.input_prompt if hasattr(self, 'input_prompt') else "Inserisci testo"
        t = self.font.render(prompt, True, (30,30,30))
        self.screen.blit(t, (x+24, y+24))
        # Box input
        input_box = pygame.Rect(x+24, y+70, w-48, 48)
        pygame.draw.rect(self.screen, (240,240,240), input_box, border_radius=8)
        pygame.draw.rect(self.screen, (30,30,30), input_box, 2, border_radius=8)
        text = self.font.render(self.input_text, True, (30,30,30))
        self.screen.blit(text, (input_box.x+12, input_box.y+input_box.height//2-text.get_height()//2))
        hint = self.small_font.render("(max 10 caratteri, premi Invio)", True, (80,80,80))
        self.screen.blit(hint, (x+24, y+128))

    def handle_key(self, event):
        if self.state == "splash":
            if event.key == pygame.K_SPACE:
                self.state = "menu"
            return
        if self.popup:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self.popup = None
            return
        if self.input_active:
            if event.key == pygame.K_RETURN:
                if self.input_callback:
                    cb = self.input_callback
                    val = self.input_text[:10]
                    self.input_active = False
                    self.input_text = ""
                    self.input_callback = None
                    self.input_prompt = ""
                    cb(val)
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                if len(self.input_text) < 10 and event.unicode.isprintable():
                    self.input_text += event.unicode
            return
        if self.state == "name" and self.name_input_active:
            if event.key == pygame.K_RETURN:
                self.player_name = self.name_input_text[:10]
                self.name_input_active = False
                self.state = "game"
            elif event.key == pygame.K_BACKSPACE:
                self.name_input_text = self.name_input_text[:-1]
            else:
                if len(self.name_input_text) < 10 and event.unicode.isprintable():
                    self.name_input_text += event.unicode

    def update_hover(self, mouse_pos):
        if self.state != "game":
            self.hovered_router = None
            self.hovered_interface = None
            return
        idx, d = self._router_at_pos(mouse_pos)
        self.hovered_router = idx
        self.hovered_interface = (idx, d) if (idx is not None and d is not None) else None
