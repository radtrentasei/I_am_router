## 16. Ottenimento della tabella di routing di un router (modalità API)

Per ottenere la tabella di routing di un router reale, il client deve effettuare la seguente chiamata API RESTCONF:

```
restconf/data/ietf-routing:routing-state/routing-instance
```

Questa chiamata restituisce lo stato di routing, inclusa la tabella di routing attuale del router.

> **Nota:** In futuro verranno aggiunti esempi pratici di risposta dell’API e di parsing delle rotte rilevanti.

---
