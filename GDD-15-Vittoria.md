## 15. Condizione di Vittoria del Livello

La **condizione di vittoria di un livello** viene raggiunta quando, in almeno uno dei router obiettivo, la sua tabella di routing contiene le rotte verso le loopback di **tutti** i router obiettivo.

### Definizione di router obiettivo

I **router obiettivo** sono quelli identificati dalle coppie (groupID, localID) specificate per il livello.  
Esempio:  
- (1,1)  
- (4,1)

### Indirizzamento delle loopback

L’indirizzo IP della loopback per ogni router obiettivo segue la convenzione:
```
G.0.0.L
```
dove:
- **G** = groupID del router
- **L** = localID del router

Esempi:
- Router obiettivo (1,1): loopback 1.0.0.1
- Router obiettivo (4,1): loopback 4.0.0.1

### Regola di vittoria

La vittoria si ottiene quando, **in almeno uno dei router obiettivo**, nella sua tabella di routing sono presenti tutte le rotte verso le loopback degli altri router obiettivo del livello (inclusa la propria).  
In altre parole, la tabella deve contenere tutte le destinazioni del tipo G.0.0. L dove (G,L) sono le coppie dei router obiettivo.

### Nota
- Il controllo della vittoria avviene periodicamente (sincronizzato con il polling delle API).
- La verifica può essere visualizzata nella UI tramite un indicatore di progresso o stato.

---
