# Checkers AI (Dama Italiana)

**Autore:** Federica Di Dio 

**Corso:** Intelligenza Artificiale - Università degli Studi di Catania - Laurea Magistrale in Informatica

Un'implementazione del gioco della dama in Python che permette a un utente umano di sfidare un agente intelligente basato sull'algoritmo Minimax con potatura α-β.

## Caratteristiche
* **Motore AI**: Utilizza l'algoritmo Minimax per determinare la mossa ottimale, anticipando le contromosse dell'avversario.
* **Ottimizzazione**: Implementa la potatura α-β per esplorare l'albero delle decisioni, scartando rami non promettenti per ridurre i tempi di calcolo.
* **Euristiche Avanzate**: La funzione di valutazione calcola il punteggio pesando il materiale e il vantaggio posizionale (avanzamento verso la promozione a dama).
* **Robustezza**: Gestione degli errori di input tramite blocchi try-except e controllo della validità delle mosse per garantire il rispetto rigoroso delle regole.

## Logica del Progetto

Il gioco è modellato su una scacchiera 8x8 con una gerarchia di valori per valutare le configurazioni:
* **Pedina**: 10 punti base + bonus avanzamento.
* **Dama**: 20 punti base + bonus posizionale raddoppiato.
* **Stati Terminali**: Valori infiniti assegnati per vittoria o sconfitta per terminare la ricorsione.

La profondità di ricerca standard è impostata a 4, garantendo una risposta immediata.

## Come avviare il gioco
1. Assicurati di avere Python installato.
2. Scarica il file `dama.py`.
3. Avvia il gioco da terminale: `python dama.py`

## Istruzioni di gioco

Quando è il tuo turno, inserisci le coordinate della mossa nel formato:
`riga_partenza colonna_partenza riga_destinazione colonna_destinazione`

*(Esempio: `5 1 4 2` per muovere dalla cella (5,1) alla (4,2))*.

## Documentazione

Per un'analisi approfondita della modellazione del problema, della struttura del software e dei dettagli matematici dell'algoritmo, consulta la *[Relazione di Progetto]* inclusa nel repository.
