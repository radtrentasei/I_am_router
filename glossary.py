# glossary.py
"""
Gestione del glossario e tutorial interattivo.
"""
class Glossary:
    def __init__(self, config):
        self.config = config
        self.terms = {
            "Rete": "Insieme di dispositivi collegati per scambiarsi dati.",
            "Router": "Dispositivo che indirizza i pacchetti tra reti diverse.",
            "Interfaccia": "Punto di connessione fisica o logica su un router.",
            "Interfaccia logica (sub-interface)": "Interfaccia virtuale su una fisica, identificata dal numero VLAN.",
            "VLAN": "Rete virtuale che identifica univocamente un link tra due router reali.",
            "Link": "Collegamento tra due dispositivi di rete.",
            "Neighborship": "Relazione di vicinato tra due router con sessione di routing attiva.",
            "Disservizio": "Parte della rete o link non funzionante.",
            "Pacchetto": "Unità di dati che viaggia nella rete.",
            "Routing": "Processo di scelta del percorso migliore per un pacchetto.",
            "API": "Interfaccia di programmazione per interagire con i router.",
        }
        self.tutorial_steps = [
            "Benvenuto nel tutorial! Inserisci il tuo nome (max 10 caratteri).",
            "Clicca su un router grigio per claimarlo. Il router diventerà del tuo colore e riceverai conferma.",
            "Clicca sulle frecce del router claimato per attivare (verde) o disattivare (rosso) le interfacce. Ogni azione consuma un token.",
            "Se non hai token, attendi il timer per ricaricarne uno. I token degli altri giocatori non sono mai visibili.",
            "Passa il mouse sopra un router per vedere il box hostname aggiornato.",
            "Attiva le interfacce di due router adiacenti per vedere una linea tratteggiata verde (neighborship attiva).",
            "La vittoria si ottiene quando almeno un router obiettivo ha tutte le rotte verso le loopback degli altri router obiettivo.",
            "Consulta il glossario in basso a destra per chiarimenti sui termini tecnici.",
            "Tutorial completato! Ora puoi giocare liberamente o ripetere gli step."
        ]
        self.current_step = 0
        self.visible = False
        self.tutorial_visible = False
        self.tutorial_offline = False  # True se in modalità tutorial offline
        self.simulated_state = {}      # Stato simulato locale per il tutorial

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def show_tutorial(self):
        self.tutorial_visible = True
        self.current_step = 0

    def hide_tutorial(self):
        self.tutorial_visible = False
        self.current_step = 0

    def next_tutorial_step(self):
        if self.current_step < len(self.tutorial_steps) - 1:
            self.current_step += 1

    def prev_tutorial_step(self):
        if self.current_step > 0:
            self.current_step -= 1

    def is_tutorial_completed(self):
        return self.current_step >= len(self.tutorial_steps) - 1

    def reset_tutorial(self):
        self.current_step = 0
        self.tutorial_visible = True

    def start_tutorial_offline(self):
        self.tutorial_offline = True
        self.simulated_state = {
            "routers": {},
            "links": {},
            "tokens": 99,  # Token illimitati
            "timer": None,
        }
        self.reset_tutorial()

    def end_tutorial_offline(self):
        self.tutorial_offline = False
        self.simulated_state = {}
        self.hide_tutorial()

    def is_in_tutorial(self):
        return self.tutorial_offline

    def get_current_tutorial_text(self):
        """Restituisce il testo del tutorial step corrente."""
        if 0 <= self.current_step < len(self.tutorial_steps):
            return self.tutorial_steps[self.current_step]
        return "Tutorial completato!"

    def repeat_step(self):
        # Permette di ripetere lo step corrente (può essere usato dalla UI)
        pass  # Logica custom se serve

    def can_consume_token(self):
        # Nel tutorial offline non si consumano token
        return not self.tutorial_offline

    def is_glossary_always_accessible(self):
        # Nel tutorial il glossario è sempre accessibile
        return self.tutorial_offline or self.visible
