# reset_game.py
"""
Script di reset per lo stato del gioco "I am a Router".
- Imposta la description di tutte le Loopback su "Router"
- Disabilita tutte le sub-interface di Gi1 (VLAN) su tutti i router reali (local_id 1-4)
"""
import requests
import urllib3
import concurrent.futures
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

AUTH = ("cisco", "C1sco12345")
HEADERS = {"Content-Type": "application/yang-data+json"}


def get_interfaces(local_id):
    """Recupera tutte le interfacce esistenti su un router reale."""
    url = f"https://198.18.128.1{local_id}/restconf/data/ietf-interfaces:interfaces"
    try:
        resp = requests.get(url, auth=AUTH, headers={"Accept": "application/yang-data+json"}, verify=False, timeout=3)
        if resp.ok:
            data = resp.json()
            return data.get("ietf-interfaces:interfaces", {}).get("interface", [])
        else:
            print(f"[ERROR] GET interfaces router {local_id}: {resp.status_code}")
            return []
    except Exception as e:
        print(f"[ERROR] GET interfaces router {local_id}: {e}")
        return []


def reset_loopbacks(local_id, interfaces):
    tasks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for iface in interfaces:
            name = iface.get("name", "")
            if name.startswith("Loopback"):
                url = f"https://198.18.128.1{local_id}/restconf/data/ietf-interfaces:interfaces/interface={name}"
                payload = {
                    "interface": [
                        {
                            "name": name,
                            "type": "iana-if-type:softwareLoopback",
                            "description": "Router"
                        }
                    ]
                }
                tasks.append(executor.submit(_put_interface, url, payload, name, local_id))
        concurrent.futures.wait(tasks)


def reset_subinterfaces(local_id, interfaces):
    tasks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for iface in interfaces:
            name = iface.get("name", "")
            if name.startswith("GigabitEthernet1."):
                url = f"https://198.18.128.1{local_id}/restconf/data/ietf-interfaces:interfaces/interface={name}"
                payload = {
                    "interface": [
                        {
                            "name": name,
                            "type": "iana-if-type:ethernetCsmacd",
                            "enabled": False
                        }
                    ]
                }
                tasks.append(executor.submit(_put_interface, url, payload, name, local_id))
        concurrent.futures.wait(tasks)


def _put_interface(url, payload, name, local_id):
    try:
        resp = requests.put(url, json=payload, auth=AUTH, headers=HEADERS, verify=False, timeout=2)
        print(f"[RESET] {name} router {local_id}: {resp.status_code}")
    except Exception as e:
        print(f"[ERROR] {name} router {local_id}: {e}")


def main():
    for local_id in range(1, 5):
        print(f"--- Reset router {local_id} ---")
        interfaces = get_interfaces(local_id)
        reset_loopbacks(local_id, interfaces)
        reset_subinterfaces(local_id, interfaces)


if __name__ == "__main__":
    main()
