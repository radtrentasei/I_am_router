# ui.py
"""
Rendering grafico, gestione pulsanti, popup, feedback visivi.
"""
import pygame
import pygame.gfxdraw
import math

# Parametri di default per router/interfacce
ARROW_SIZE = 32
ARROW_WIDTH = 5
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
        labels = ["Facile (2x2)", "Medio (3x3)", "Difficile (4x4)", "Custom"]
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
        name = self.name_input_text if self.name_input_active else self.player_name
        t = self.font.render(name, True, (255,255,255))
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
        """
        size = self.grid.size
        margin_x = 120
        margin_y = 80
        cell_w = (self.config.WIDTH - 2*margin_x) // size
        cell_h = (self.config.HEIGHT - 220) // size
        router_radius = self._get_adaptive_router_radius()
        # La lunghezza dell'interfaccia deve essere circa metà del diametro del router, ma non più lunga del 60% della cella
        rect_len = min(int(router_radius * 1.2), int(min(cell_w, cell_h) * 0.6))
        rect_w = max(10, int(router_radius * 0.35))  # Spessore proporzionale
        return rect_len, rect_w

    def _draw_grid(self):
        size = self.grid.size
        margin_x = 120
        margin_y = 80
        cell_w = (self.config.WIDTH - 2*margin_x) // size
        cell_h = (self.config.HEIGHT - 220) // size
        ROUTER_RADIUS = self._get_adaptive_router_radius()
        for idx, router in enumerate(self.grid.routers):
            row, col = router["row"], router["col"]
            x = margin_x + col * cell_w + cell_w//2
            y = margin_y + row * cell_h + cell_h//2
            # Disegna solo router "visibili" nella griglia corrente
            if not (0 <= row < size and 0 <= col < size):
                continue
            # Router: cerchio con bordo sfumato e glow su hover
            router_px = ROUTER_RADIUS * 2
            surf = pygame.Surface((router_px, router_px), pygame.SRCALPHA)
            color = (180, 180, 180) if router["claimed_by"] is None else self.config.ROUTER_COLORS[router["claimed_by"]]
            if router.get("claimed_by_name") and router["claimed_by_name"] != self.config.PLAYER_NAME:
                color = (255, 140, 0)
            pygame.draw.circle(surf, color, (router_px//2, router_px//2), router_px//2-2)
            # Dithering bordo
            for i in range(0, 360, 12):
                rad = math.radians(i)
                dx = int((router_px//2-2)*math.cos(rad))
                dy = int((router_px//2-2)*math.sin(rad))
                surf.set_at((router_px//2+dx, router_px//2+dy), (220,220,220))
            # Bordo doppio
            border_col = self.config.YELLOW if (row in self.router_goal or col in self.router_goal) else (255,255,255)
            pygame.draw.circle(surf, border_col, (router_px//2, router_px//2), router_px//2-1, 2)
            pygame.draw.circle(surf, (30,30,30), (router_px//2, router_px//2), router_px//2, 1)
            # Glow su hover: alone pixelato
            if self.hovered_router == idx:
                pygame.draw.circle(surf, (255,255,255,80), (router_px//2, router_px//2), router_px//2, 2)
            # Scala up la superficie per effetto pixelart
            scale = (ROUTER_RADIUS*2, ROUTER_RADIUS*2)
            surf_big = pygame.transform.scale(surf, scale)
            self.screen.blit(surf_big, (x-ROUTER_RADIUS, y-ROUTER_RADIUS))
            # Interfacce: disegna solo un rettangolo colorato invece della freccia
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
                # Calcola la posizione e dimensione del rettangolo interfaccia in modo adattivo
                rect_len, rect_w = self._get_adaptive_interface_size()
                rad = math.radians(angle)
                cx = x + int(math.cos(rad)*(ROUTER_RADIUS-24))
                cy = y + int(math.sin(rad)*(ROUTER_RADIUS-24))
                dx = int(math.cos(rad)*rect_len//2)
                dy = int(math.sin(rad)*rect_len//2)
                rect_center = (cx+dx, cy+dy)
                rect = pygame.Rect(0, 0, rect_len, rect_w)
                rect.center = rect_center
                # Bordo bianco e outline nero
                pygame.draw.rect(self.screen, (255,255,255), rect.inflate(4,4), border_radius=6)
                pygame.draw.rect(self.screen, (0,0,0), rect.inflate(8,8), border_radius=8)
                pygame.draw.rect(self.screen, rect_col, rect, border_radius=6)
            # Hostname box pixelart con bordo doppio
            if self.hovered_router == idx:
                self._draw_hostname_box_pixel(x, y+ROUTER_RADIUS+8, router["hostname"])

    def _draw_hostname_box_pixel(self, x, y, hostname):
        text = self.font.render(hostname, True, (255,255,255))
        w, h = text.get_size()
        box = pygame.Rect(x-w//2-8, y, w+16, h+10)
        pygame.draw.rect(self.screen, (40,40,60), box)
        pygame.draw.rect(self.screen, (255,255,255), box, 2)
        pygame.draw.rect(self.screen, (30,30,30), box, 1)
        self.screen.blit(text, (x-w//2, y+5))

    def _draw_arrow_aa(self, x, y, angle, color, width=ARROW_WIDTH):
        # Freccia anti-aliased
        import math
        import pygame.gfxdraw
        rad = math.radians(angle)
        start_dist = self._get_adaptive_router_radius() - ARROW_SIZE - 8
        end_dist = self._get_adaptive_router_radius() - 36
        dx = math.cos(rad)
        dy = math.sin(rad)
        start = (int(x + dx * start_dist), int(y + dy * start_dist))
        end = (int(x + dx * end_dist), int(y + dy * end_dist))
        # Linea principale
        for w in range(-width//2, width//2+1):
            ox = int(-dy*w)
            oy = int(dx*w)
            pygame.gfxdraw.line(self.screen, start[0]+ox, start[1]+oy, end[0]+ox, end[1]+oy, color)
        # Punta
        tip = (int(x + dx * (self._get_adaptive_router_radius() - 18)), int(y + dy * (self._get_adaptive_router_radius() - 18)))
        perp1 = math.radians(angle+150)
        p1 = (int(tip[0]+math.cos(perp1)*16), int(tip[1]+math.sin(perp1)*16))
        perp2 = math.radians(angle-150)
        p2 = (int(tip[0]+math.cos(perp2)*16), int(tip[1]+math.sin(perp2)*16))
        pygame.gfxdraw.filled_trigon(self.screen, tip[0], tip[1], p1[0], p1[1], p2[0], p2[1], color)
        pygame.gfxdraw.aatrigon(self.screen, tip[0], tip[1], p1[0], p1[1], p2[0], p2[1], color)

    def _draw_links(self):
        # Linee tratteggiate verdi tra router con neighborship attiva
        for link in self.grid.links:
            if link.get("neighborship"):
                idx1, idx2 = link["router_a"], link["router_b"]
                r1 = self.grid.routers[idx1]
                r2 = self.grid.routers[idx2]
                # Verifica che entrambi i router siano visibili nella griglia
                size = self.grid.size
                if not (0 <= r1["row"] < size and 0 <= r1["col"] < size):
                    continue
                if not (0 <= r2["row"] < size and 0 <= r2["col"] < size):
                    continue
                dx = r2["col"] - r1["col"]
                dy = r2["row"] - r1["row"]
                if abs(dx) + abs(dy) != 1:
                    continue  # solo adiacenti
                if dx == 1:
                    d1, d2 = "E", "W"
                elif dx == -1:
                    d1, d2 = "W", "E"
                elif dy == 1:
                    d1, d2 = "S", "N"
                else:
                    d1, d2 = "N", "S"
                x1, y1 = self._router_pos(idx1)
                x2, y2 = self._router_pos(idx2)
                angle_map = {"N":270, "E":0, "S":90, "W":180}
                a1 = angle_map[d1]
                a2 = angle_map[d2]
                rect_len = 36
                rect_w = 14
                rad1 = math.radians(a1)
                rad2 = math.radians(a2)
                margin = 18
                offset = (rect_len // 2) + rect_w // 2 + margin
                start = (
                    int(x1 + math.cos(rad1)*(self._get_adaptive_router_radius()-24 + offset)),
                    int(y1 + math.sin(rad1)*(self._get_adaptive_router_radius()-24 + offset))
                )
                end = (
                    int(x2 + math.cos(rad2)*(self._get_adaptive_router_radius()-24 + offset)),
                    int(y2 + math.sin(rad2)*(self._get_adaptive_router_radius()-24 + offset))
                )
                link_color = (0, 200, 0)
                # Bordo bianco spesso sotto la linea
                pygame.draw.line(self.screen, (255,255,255), start, end, 10)
                # Bordo nero sottile
                pygame.draw.line(self.screen, (0,0,0), start, end, 4)
                # Linea centrale verde
                pygame.draw.line(self.screen, link_color, start, end, 6)
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
        margin_x = 120
        margin_y = 80
        cell_w = (self.config.WIDTH - 2*margin_x) // size
        cell_h = (self.config.HEIGHT - 220) // size
        router = self.grid.routers[idx]
        x = margin_x + router["col"] * cell_w + cell_w//2
        y = margin_y + router["row"] * cell_h + cell_h//2
        return (x, y)

    def _draw_tokens(self):
        # Stato token e timer SOLO per il giocatore locale (player 0)
        pid = 0
        color = self.config.ROUTER_COLORS[pid]
        x = 60
        y = 32
        player_name = self.player_name
        # Prepara testo nome troncato se troppo lungo
        max_name_len = 16
        display_name = player_name
        if len(display_name) > max_name_len:
            display_name = display_name[:max_name_len-3] + '...'
        name_text = self.font.render(f"Giocatore: {display_name}", True, (0,0,0))
        token_text = self.font.render("Token: ", True, (0,0,0))
        tokens = self.grid.tokens[pid]
        token_val_text = self.font.render(f"{tokens}", True, (30,30,30))
        timer = self.grid.token_timers[pid]
        timer_text = self.small_font.render(f"+1 in {timer}s", True, (80,80,80))
        # Calcola larghezza box: la maggiore tra box Giocatore e box Token
        content_w1 = name_text.get_width() + 24
        content_w2 = token_text.get_width() + token_val_text.get_width() + timer_text.get_width() + 24
        box_w = max(content_w1, content_w2)
        box_h = max(name_text.get_height(), token_text.get_height(), token_val_text.get_height()) + 16
        # Box Giocatore
        box1_rect = pygame.Rect(x, y, box_w, box_h)
        pygame.draw.rect(self.screen, (255, 255, 180), box1_rect)
        pygame.draw.rect(self.screen, (255,255,255), box1_rect, 2)
        pygame.draw.rect(self.screen, (0,0,0), box1_rect, 2)
        # Testo centrato
        self.screen.blit(name_text, (box1_rect.x + (box_w - name_text.get_width())//2, box1_rect.y + (box_h - name_text.get_height())//2))
        # Box Token affiancato
        box2_rect = pygame.Rect(x + box_w + 24, y, box_w, box_h)
        pygame.draw.rect(self.screen, (255, 255, 180), box2_rect)
        pygame.draw.rect(self.screen, (255,255,255), box2_rect, 2)
        pygame.draw.rect(self.screen, (0,0,0), box2_rect, 2)
        # Testo Token centrato orizzontalmente
        total_token_w = token_text.get_width() + token_val_text.get_width() + timer_text.get_width() + 12
        tx = box2_rect.x + (box_w - total_token_w)//2
        self.screen.blit(token_text, (tx, box2_rect.y + (box_h - token_text.get_height())//2))
        tx += token_text.get_width()
        self.screen.blit(token_val_text, (tx, box2_rect.y + (box_h - token_val_text.get_height())//2))
        tx += token_val_text.get_width() + 8
        self.screen.blit(timer_text, (tx, box2_rect.y + (box_h - timer_text.get_height())//2 + 2))
        # Modalità tutorial: mostra infinito
        if self.glossary.is_in_tutorial():
            inf_text = self.font.render(f"∞", True, (30,30,30))
            self.screen.blit(inf_text, (box2_rect.x+box2_rect.width-36, box2_rect.y+4))

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
        # Word wrap del testo step
        max_width = w - 40
        font = self.font
        def wrap_text(text, font, max_width):
            words = text.split()
            lines = []
            current = ""
            for word in words:
                test = current + (" " if current else "") + word
                if font.size(test)[0] <= max_width:
                    current = test
                else:
                    if current:
                        lines.append(current)
                    current = word
            if current:
                lines.append(current)
            return lines
        lines = []
        for part in step.split(". "):
            lines.extend(wrap_text(part, font, max_width))
        for i, line in enumerate(lines):
            t = font.render(line, True, (30,30,30))
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
                        # Controlla se il fallimento è dovuto a token esauriti
                        player_id = router["claimed_by"]
                        if player_id is not None and self.grid.tokens[player_id] <= 0:
                            self._show_error("Token esauriti! Azione non consentita.")
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
                            self.state = "glossary"
                            self.show_glossary = False
                        elif i == 3:
                            self._show_credits()
                        return
            return
        if self.state == "glossary":
            # Chiudi glossario con click
            self.state = "menu"
            return
        if self.state == "tutorial":
            # Gestione click sui pulsanti Avanti/Indietro/Ripeti step
            w = 700
            h = 220
            x = self.config.WIDTH//2 - w//2
            y = self.config.HEIGHT//2 - h//2
            btn_w, btn_h = 120, 40
            btn_y = y+h-60
            btn_prev = pygame.Rect(x+20, btn_y, btn_w, btn_h)
            btn_next = pygame.Rect(x+w-20-btn_w, btn_y, btn_w, btn_h)
            btn_repeat = pygame.Rect(self.config.WIDTH//2-60, y+h-60, 120, 40)
            mx, my = pos
            if btn_prev.collidepoint(mx, my):
                if self.glossary.current_step > 0:
                    self.glossary.current_step -= 1
                return
            if btn_next.collidepoint(mx, my):
                if self.glossary.current_step < len(self.glossary.tutorial_steps)-1:
                    self.glossary.current_step += 1
                return
            if btn_repeat.collidepoint(mx, my):
                # Logica per ripetere lo step: resetta eventuale stato simulato
                if hasattr(self.glossary, 'reset_tutorial_step'):
                    self.glossary.reset_tutorial_step(self.glossary.current_step)
                return
            # Click fuori dai pulsanti: chiudi tutorial
            self.show_tutorial = False
            self.state = "menu"
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
                            # Controlla se il fallimento è dovuto a token esauriti
                            player_id = router["claimed_by"]
                            if player_id is not None and self.grid.tokens[player_id] <= 0:
                                self._show_error("Token esauriti! Azione non consentita.")
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
        ROUTER_RADIUS = self._get_adaptive_router_radius()
        for idx, router in enumerate(self.grid.routers):
            x = margin_x + router["col"] * cell_w + cell_w//2
            y = margin_y + router["row"] * cell_h + cell_h//2
            dist = math.hypot(mx-x, my-y)
            if dist < ROUTER_RADIUS:
                # Verifica se su una interfaccia (rettangolo pixel-art)
                for d, angle in zip(["N","E","S","W"],[270,0,90,180]):
                    iface = router["interfaces"][d]
                    if iface["vlan"] is None:
                        continue
                    rect_len, rect_w = self._get_adaptive_interface_size()
                    rad = math.radians(angle)
                    cx = x + int(math.cos(rad)*(ROUTER_RADIUS-24))
                    cy = y + int(math.sin(rad)*(ROUTER_RADIUS-24))
                    dx = int(math.cos(rad)*rect_len//2)
                    dy = int(math.sin(rad)*rect_len//2)
                    rect_center = (cx+dx, cy+dy)
                    # Hitbox precisa: creo una superficie temporanea ruotata e controllo il punto
                    import pygame
                    surf = pygame.Surface((rect_len, rect_w), pygame.SRCALPHA)
                    rect = pygame.Rect(0, 0, rect_len, rect_w)
                    rect.center = (rect_len//2, rect_w//2)
                    pygame.draw.rect(surf, (255,255,255), rect)
                    surf_rot = pygame.transform.rotate(surf, -angle)
                    surf_rect = surf_rot.get_rect(center=rect_center)
                    if surf_rect.collidepoint(mx, my):
                        # Controllo anche il pixel alpha per evitare errori ai bordi
                        local_x = mx - surf_rect.left
                        local_y = my - surf_rect.top
                        if 0 <= local_x < surf_rot.get_width() and 0 <= local_y < surf_rot.get_height():
                            if surf_rot.get_at((int(local_x), int(local_y))).a > 10:
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
        # Gestione universale ESC: torna sempre indietro di uno stato
        if event.key == pygame.K_ESCAPE:
            if self.input_active:
                self.input_active = False
                self.input_text = ""
                self.input_callback = None
                self.input_prompt = ""
                return
            if self.popup:
                self.popup = None
                return
            if self.show_glossary:
                self.show_glossary = False
                return
            if self.show_tutorial:
                self.show_tutorial = False
                self.state = "menu"
                return
            if self.state == "game":
                self.state = "level"
                return
            if self.state == "level":
                self.state = "menu"
                return
            if self.state == "name":
                self.state = "level"
                return
            if self.state == "menu":
                self.state = "splash"
                return
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

    def _draw_hostname_box_glass(self, x, y, hostname):
        # Box hostname effetto vetro (glassmorphism)
        text = self.font.render(hostname, True, (255,255,255))
        w, h = text.get_size()
        box = pygame.Rect(x-w//2-12, y, w+24, h+14)
        glass = pygame.Surface((w+24, h+14), pygame.SRCALPHA)
        glass.fill((80, 80, 120, 120))
        pygame.draw.rect(glass, (200,200,255,60), glass.get_rect(), border_radius=10)
        pygame.draw.rect(glass, (255,255,255,120), glass.get_rect(), 2, border_radius=10)
        self.screen.blit(glass, (x-w//2-12, y))
        self.screen.blit(text, (x-w//2, y+7))

    def _ask_custom_size(self):
        # Popup pixel-art per selezione dimensione griglia custom (NxN)
        # Blocca la UI finché non viene scelto il valore
        running = True
        n = 5  # valore iniziale di default
        min_n, max_n = 2, 8
        clock = pygame.time.Clock()
        while running:
            self.screen.fill(self.config.BACKGROUND)
            # Popup box
            w, h = 420, 180
            x = self.config.WIDTH//2 - w//2
            y = self.config.HEIGHT//2 - h//2
            box = pygame.Rect(x, y, w, h)
            pygame.draw.rect(self.screen, (255,255,255), box, border_radius=14)
            pygame.draw.rect(self.screen, (30,30,30), box, 3, border_radius=14)
            # Titolo
            title = self.font.render("Seleziona dimensione griglia router", True, (30,30,30))
            self.screen.blit(title, (x + w//2 - title.get_width()//2, y + 24))
            # Valore N
            n_box = pygame.Rect(x + w//2 - 40, y + 70, 80, 56)
            pygame.draw.rect(self.screen, (255,255,180), n_box, border_radius=10)
            pygame.draw.rect(self.screen, (255,255,255), n_box, 2, border_radius=10)
            pygame.draw.rect(self.screen, (0,0,0), n_box, 2, border_radius=10)
            n_text = self.big_font.render(str(n), True, (30,30,30))
            self.screen.blit(n_text, (n_box.x + n_box.width//2 - n_text.get_width()//2, n_box.y + n_box.height//2 - n_text.get_height()//2))
            # Pulsanti - e +
            btn_w, btn_h = 48, 48
            btn_minus = pygame.Rect(n_box.x - btn_w - 16, n_box.y + 4, btn_w, btn_h)
            btn_plus = pygame.Rect(n_box.x + n_box.width + 16, n_box.y + 4, btn_w, btn_h)
            pygame.draw.rect(self.screen, (200,200,255), btn_minus, border_radius=10)
            pygame.draw.rect(self.screen, (200,255,200), btn_plus, border_radius=10)
            minus_text = self.big_font.render("-", True, (30,30,30))
            plus_text = self.big_font.render("+", True, (30,30,30))
            self.screen.blit(minus_text, (btn_minus.x + btn_w//2 - minus_text.get_width()//2, btn_minus.y + btn_h//2 - minus_text.get_height()//2))
            self.screen.blit(plus_text, (btn_plus.x + btn_w//2 - plus_text.get_width()//2, btn_plus.y + btn_h//2 - plus_text.get_height()//2))
            # Pulsante OK
            ok_w, ok_h = 100, 44
            ok_box = pygame.Rect(x + w//2 - ok_w//2, y + h - 56, ok_w, ok_h)
            pygame.draw.rect(self.screen, (255,220,120), ok_box, border_radius=10)
            ok_text = self.font.render("OK", True, (30,30,30))
            self.screen.blit(ok_text, (ok_box.x + ok_w//2 - ok_text.get_width()//2, ok_box.y + ok_h//2 - ok_text.get_height()//2))
            # Aggiorna display
            pygame.display.flip()
            # Gestione eventi
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    if btn_minus.collidepoint(mx, my):
                        if n > min_n:
                            n -= 1
                    elif btn_plus.collidepoint(mx, my):
                        if n < max_n:
                            n += 1
                    elif ok_box.collidepoint(mx, my):
                        running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                    elif event.key == pygame.K_LEFT and n > min_n:
                        n -= 1
                    elif event.key == pygame.K_RIGHT and n < max_n:
                        n += 1
            clock.tick(30)
        return n

    def _show_credits(self):
        """
        Mostra un popup pixel-art con i credits del gioco, stile identico a glossario/tutorial.
        Chiusura con ESC o click.
        """
        self.popup = ("credits", None)
