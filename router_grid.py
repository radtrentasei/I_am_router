# router_grid.py
"""
Gestione della griglia NxN, assegnazione ID, stato router/interfacce, logica VRF.
"""
from utils import generate_ids
import time
import threading

class RouterGrid:
    def __init__(self, config, api):
        self.config = config
        self.api = api
        self.size = config.GRID_SIZE
        self.routers = self._init_routers()
        self.links = self._init_links()
        self.tokens = self.config.MAX_TOKENS  # Solo giocatore locale (indice 0)
        self.token_timer = 0
        self.last_token_time = time.time()
        self.goal_routers = self._goal_routers()

    def _init_routers(self):
        routers = []
        ids = generate_ids(self.size)
        for row in range(self.size):
            for col in range(self.size):
                idx = row * self.size + col
                router = {
                    "row": row,
                    "col": col,
                    "global_id": ids[idx]["global_id"],
                    "group_id": ids[idx]["group_id"],
                    "local_id": ids[idx]["local_id"],
                    "claimed_by": None,
                    "claimed_by_name": None,
                    "hostname": "Router",  # GDD: hostname iniziale deve essere "Router"
                    "interfaces": {d: {"up": False, "vlan": None} for d in ["N", "S", "E", "W"]},
                }
                routers.append(router)
        # Assegna le VLAN alle interfacce
        for idx, router in enumerate(routers):
            row, col = router["row"], router["col"]
            neighbors = {
                "N": (row-1, col),
                "S": (row+1, col),
                "E": (row, col+1),
                "W": (row, col-1)
            }
            for d, (nrow, ncol) in neighbors.items():
                if 0 <= nrow < self.size and 0 <= ncol < self.size:
                    nidx = nrow * self.size + ncol
                    neighbor = routers[nidx]
                    vlan = self._vlan(router, neighbor)
                    router["interfaces"][d]["vlan"] = vlan
        return routers

    def _init_links(self):
        links = []
        size = self.size
        for idx, router in enumerate(self.routers):
            row, col = router["row"], router["col"]
            neighbors = []
            if row > 0:
                neighbors.append((row-1, col))
            if row < size-1:
                neighbors.append((row+1, col))
            if col > 0:
                neighbors.append((row, col-1))
            if col < size-1:
                neighbors.append((row, col+1))
            for nrow, ncol in neighbors:
                nidx = nrow * size + ncol
                if 0 <= nidx < len(self.routers):  # Fix: controlla che l'indice sia valido
                    vlan = self._vlan(router, self.routers[nidx])
                    link = {
                        "router_a": idx,
                        "router_b": nidx,
                        "vlan": vlan,
                        "neighborship": False
                    }
                    # Evita duplicati (link bidirezionali)
                    if not any(l for l in links if (l["router_a"], l["router_b"]) == (nidx, idx)):
                        links.append(link)
        return links

    def _vlan(self, r1, r2):
        # Regola aggiornata (GDD 27/05/2025):
        # - Se i router sono dello stesso gruppo: VLAN = group_id + local_id min + local_id max
        # - Se i router sono di gruppi diversi: VLAN = group_id min + local_id max + local_id min
        if r1["group_id"] == r2["group_id"]:
            gid = r1["group_id"]
            lmin = min(r1["local_id"], r2["local_id"])
            lmax = max(r1["local_id"], r2["local_id"])
            return int(f"{gid}{lmin}{lmax}")
        else:
            gid_min = min(r1["group_id"], r2["group_id"])
            lmin = min(r1["local_id"], r2["local_id"])
            lmax = max(r1["local_id"], r2["local_id"])
            return int(f"{gid_min}{lmax}{lmin}")

    def _opposite_dir(self, d):
        return {"N":"S", "S":"N", "E":"W", "W":"E"}[d]

    def claim_router(self, router_idx, hostname):
        """
        GDD: Claim di un router secondo le regole specificate.
        Solo il giocatore locale può claimare router.
        """
        router = self.routers[router_idx]
        player_name = self.config.PLAYER_NAME
        # GDD: Un router può essere claimato solo se claimed_by is None E hostname == 'Router'
        if (router["claimed_by"] is None and 
            router["hostname"] == "Router" and 
            self.tokens > 0):
            # GDD: Consuma token prima della chiamata API
            self.tokens -= 1
            ok = self.api.claim_router(router["local_id"], router["group_id"], player_name, hostname)
            if ok:
                router["claimed_by"] = 0  # Sempre 0 per giocatore locale
                router["hostname"] = f"{player_name}_{hostname}"
            else:
                # GDD: Se la chiamata API fallisce, restituisce il token
                self.tokens += 1
            return ok
        return False

    def set_interface(self, router_idx, direction, up):
        """
        GDD: Attiva/disattiva interfaccia solo se il router è claimato dal giocatore locale.
        """
        router = self.routers[router_idx]
        vlan = router["interfaces"][direction]["vlan"]
        # Solo se claimato dal giocatore locale e ha token
        if router["claimed_by"] == 0 and self.tokens > 0:
            # GDD: Consuma token prima della chiamata API
            self.tokens -= 1
            ok = self.api.set_interface(router["local_id"], vlan, up)
            if ok:
                router["interfaces"][direction]["up"] = up
            else:
                # GDD: Se la chiamata API fallisce, restituisce il token
                self.tokens += 1
            return ok
        return False

    def claim_router_async(self, router_idx, hostname, callback=None):
        """Versione asincrona del claim router."""
        def worker():
            result = self.claim_router(router_idx, hostname)
            if callback:
                callback(result)
        threading.Thread(target=worker, daemon=True).start()

    def set_interface_async(self, router_idx, direction, up, callback=None):
        def worker():
            result = self.set_interface(router_idx, direction, up)
            if callback:
                callback(result)
        threading.Thread(target=worker, daemon=True).start()

    def update_from_api(self):
        """
        Aggiorna lo stato del router leggendo hostname e stato claim dalla description della loopback.
        L'hostname è sempre aggiornato in tempo reale dal polling API.
        Il claim è determinato dal parsing della description: solo se il nomegiocatore coincide con quello locale il router è considerato claimato.
        Se il router è claimato da un altro giocatore, claimed_by_name viene impostato e la UI lo mostra arancione.
        """
        for idx, router in enumerate(self.routers):
            local_id = router["local_id"]
            group_id = router["group_id"]
            data = self.api.poll_data.get(local_id)
            hostname = "?"  # GDD: "?" se non disponibile dal polling API
            claimed_by = None
            claimed_by_name = None
            if data:
                interfaces = data.get("ietf-interfaces:interfaces", {}).get("interface", [])
                for iface in interfaces:
                    if iface.get("name") == f"Loopback{group_id}":
                        desc = iface.get("description")
                        if desc is not None and desc != "":
                            hostname = str(desc)
                            # GDD: parsing del formato nomegiocatore_hostname
                            if "_" in hostname:
                                parts = hostname.split("_", 1)
                                if len(parts) == 2:
                                    nomegiocatore, routername = parts[0], parts[1]
                                    # GDD: router claimato dal giocatore locale solo se nomegiocatore coincide
                                    if nomegiocatore == self.config.PLAYER_NAME:
                                        claimed_by = 0  # player locale
                                        claimed_by_name = nomegiocatore
                                    else:
                                        # GDD: router claimato da altro giocatore (arancione in UI)
                                        claimed_by = 1  # altro player 
                                        claimed_by_name = nomegiocatore
                        else:
                            # GDD: Se non c'è description, hostname default è "Router"
                            hostname = "Router"
                        break
                else:
                    # GDD: Se non c'è la loopback, hostname default è "Router"
                    hostname = "Router"
            router["hostname"] = hostname
            router["claimed_by"] = claimed_by
            router["claimed_by_name"] = claimed_by_name
            # Stato interfacce logiche (VLAN)
            if data:
                interfaces = data.get("ietf-interfaces:interfaces", {}).get("interface", [])
                for d in ["N","S","E","W"]:
                    vlan = router["interfaces"][d]["vlan"]
                    found = False
                    if vlan:
                        for iface in interfaces:
                            if iface.get("name") == f"GigabitEthernet1.{vlan}":
                                router["interfaces"][d]["up"] = iface.get("enabled", False)
                                found = True
                                # Neighborship: description="UP" indica neighborship attiva
                                for link in self.links:
                                    if link["vlan"] == vlan:
                                        link["neighborship"] = iface.get("description","") == "UP"
                                break
                    if not found:
                        router["interfaces"][d]["up"] = False

    def update_tokens(self):
        """
        GDD: Ricarica token ogni 10 secondi, massimo 4 per il giocatore locale.
        """
        now = time.time()
        if self.tokens < self.config.MAX_TOKENS:
            elapsed = now - self.last_token_time
            if elapsed >= self.config.TOKEN_RECHARGE_TIME:
                self.tokens += 1
                self.last_token_time = now
            self.token_timer = max(0, int(self.config.TOKEN_RECHARGE_TIME - elapsed))
        else:
            self.token_timer = 0

    def _goal_routers(self):
        # Esempio: router obiettivo agli angoli
        return [0, self.size-1]

    def check_win(self):
        # Condizione di vittoria: almeno un router obiettivo ha tutte le rotte verso le loopback degli altri router obiettivo
        # (placeholder: sempre False)
        return False

    def set_size(self, size):
        """Imposta la dimensione della griglia e reinizializza lo stato dei router."""
        self.size = size
        self.routers = self._init_routers()
        self.links = self._init_links()
        # Reinizializza token del giocatore locale
        self.tokens = self.config.MAX_TOKENS
        self.token_timer = 0
        self.last_token_time = time.time()

    # ...altre funzioni per gestione stato, debug...
