# api.py
"""
Gestione delle chiamate RESTCONF verso i router reali e debug API.
"""
import requests
import threading
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class APIDriver:
    def __init__(self, config):
        self.config = config
        self.last_poll = 0
        self.poll_data = {}
        self.lock = threading.Lock()
        self.poll_thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.poll_thread.start()

    def poll(self):
        # Polling asincrono: la logica è gestita dal thread
        pass

    def _poll_loop(self):
        while True:
            now = time.time()
            if now - self.last_poll >= self.config.API_POLL_INTERVAL:
                self._poll_routers()
                self.last_poll = now
            time.sleep(0.1)

    def _poll_routers(self):
        # Esegue polling su tutti i router reali
        for local_id in range(1, 5):
            url = f"https://198.18.128.1{local_id}/restconf/data/ietf-interfaces:interfaces"
            try:
                resp = requests.get(url, auth=("cisco", "C1sco12345"), headers={"Accept": "application/yang-data+json"}, verify=False, timeout=2)
                self.api_debug_print(url, "GET", None, resp)
                with self.lock:
                    self.poll_data[local_id] = resp.json() if resp.ok else None
            except Exception as e:
                self.api_debug_print(url, "GET", None, str(e))

    def claim_router(self, local_id, group_id, player_name, hostname):
        url = f"https://198.18.128.1{local_id}/restconf/data/ietf-interfaces:interfaces/interface=Loopback{group_id}"
        description = f"{player_name}_{hostname}"
        payload = {
            "interface": [
                {
                    "name": f"Loopback{group_id}",
                    "type": "iana-if-type:softwareLoopback",
                    "description": description
                }
            ]
        }
        print(f"[API DEBUG] CLAIM PUT {url}\nPayload: {payload}")  # LOG VISIBILE
        try:
            resp = requests.put(url, json=payload, auth=("cisco", "C1sco12345"), headers={"Content-Type": "application/yang-data+json"}, verify=False, timeout=2)
            self.api_debug_print(url, "PUT", payload, resp)
            return resp.ok
        except Exception as e:
            self.api_debug_print(url, "PUT", payload, str(e))
            return False

    def set_interface(self, local_id, vlan, up):
        # Attiva/disattiva interfaccia logica (VLAN) via RESTCONF secondo specifica GDD
        url = f"https://198.18.128.1{local_id}/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1.{vlan}"
        payload = {
            "interface": [
                {
                    "name": f"GigabitEthernet1.{vlan}",
                    "type": "iana-if-type:ethernetCsmacd",
                    "enabled": up
                }
            ]
        }
        print(f"[API DEBUG] INTERFACE PUT {url}\nPayload: {payload}")
        try:
            resp = requests.put(url, json=payload, auth=("cisco", "C1sco12345"), headers={"Content-Type": "application/yang-data+json"}, verify=False, timeout=2)
            self.api_debug_print(url, "PUT", payload, resp)
            return resp.ok
        except Exception as e:
            self.api_debug_print(url, "PUT", payload, str(e))
            return False

    def api_debug_print(self, endpoint, method, payload, response):
        if isinstance(response, requests.Response):
            print(f"[API] {method} {endpoint} - Status: {response.status_code}")
            if not response.ok:
                print(f"  [API ERROR] {response.text}")
        else:
            print(f"[API] {method} {endpoint} - ERROR: {response}")
