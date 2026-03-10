# Implementazione del gioco della dama: IA vs giocatore umano
# La scacchiera è rappresentata come una matrice 8x8 con i seguenti valori:
# 0 = vuoto, 1 = pedina giocatore, 2 = pedina IA, 3 = dama giocatore, 4 = dama IA

import copy # Serve per fare le copie della scacchiera
import random # Serve per le scelte casuali

class Dama: # Classe per la dama

    def __init__(self):
        # Inizializza la scacchiera 8x8
        # 0 = vuoto, 1 = pedina giocatore, 2 = pedina IA, 3 = dama giocatore, 4 = dama IA
        self.board = [
            [2,0,2,0,2,0,2,0],
            [0,2,0,2,0,2,0,2],
            [2,0,2,0,2,0,2,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1],
        ]
        self.turno = 1  # 1 = umano, 2 = IA

    def stampa(self): # stampa
        print("  0 1 2 3 4 5 6 7")
        for i, riga in enumerate(self.board):
            print(i, end=" ")
            for cella in riga:
                simboli = {0:".", 1:"○", 2:"●", 3:"⚪", 4:"⚫"}
                print(simboli[cella], end=" ")
            print()

    # Controlla se una posizione è interna alla scacchiera
    def dentro(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    # Determina se il gioco è finito per un dato giocatore (nessuna mossa disponibile)
    def game_over_for_player(self, player_id):
        return not self.mosse(player_id)

    # Mosse del giocatore (umano)
    def mosse(self, player):
        moves = []
        for r in range(8):
            for c in range(8):
                if player == 1 and self.board[r][c] in (1,3):
                    moves += self.mosse_pedina(r, c)
                if player == 2 and self.board[r][c] in (2,4):
                    moves += self.mosse_pedina(r, c)
        return moves

    # Mosse per la pedina
    def mosse_pedina(self, r, c):
        piece = self.board[r][c]
        directions = []
        if piece in (1, 3):  # giocatore
            directions += [(-1, -1), (-1, 1)]
        if piece in (2, 4):  # IA
            directions += [(1, -1), (1, 1)]
        if piece in (3, 4):  # dame
            directions += [(1, -1), (1, 1), (-1, -1), (-1, 1)]
        moves = []

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # Mossa semplice
            if self.dentro(nr, nc) and self.board[nr][nc] == 0:
                moves.append(((r, c), (nr, nc)))
            # Tentativo di salto
            nr2, nc2 = r + 2*dr, c + 2*dc
            if self.dentro(nr2, nc2) and self.board[nr][nc] != 0:
                # Deve saltare un pezzo avversario
                if (piece in (1,3) and self.board[nr][nc] in (2,4)) or \
                   (piece in (2,4) and self.board[nr][nc] in (1,3)):
                    if self.board[nr2][nc2] == 0: # La casella di atterraggio deve essere vuota
                        moves.append(((r, c), (nr2, nc2)))
        return moves

    # Applica una mossa
    def muovi(self, move):
        (r1, c1), (r2, c2) = move
        piece = self.board[r1][c1]
        self.board[r1][c1] = 0
        self.board[r2][c2] = piece
        # Controlla se è stato un salto e rimuovi il pezzo saltato
        if abs(r2 - r1) == 2: # Se la riga è cambiata di 2, è un salto
            self.board[(r1+r2)//2][(c1+c2)//2] = 0 # Rimuovi il pezzo intermedio
        # Promozione a dama quando una pedina raggiunge l'ultima riga
        if piece == 1 and r2 == 0: # pedina giocatore raggiunge la riga 0
            self.board[r2][c2] = 3
        if piece == 2 and r2 == 7: # pedina IA raggiunge la riga 7
            self.board[r2][c2] = 4

    # Valutazione per l'IA (aggiornata per considerare vittoria/sconfitta e posizione)
    def valuta(self):
        punteggio = 0
        ia_pieces = 0
        human_pieces = 0
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == 2: # pedina IA
                    punteggio += 10 # Punteggio base per pedina
                    ia_pieces += 1
                elif self.board[r][c] == 4: # dama IA
                    punteggio += 20 # Punteggio più alto per dama
                    ia_pieces += 1
                elif self.board[r][c] == 1: # pedina giocatore
                    punteggio -= 10
                    human_pieces += 1
                elif self.board[r][c] == 3: # dama giocatore
                    punteggio -= 20
                    human_pieces += 1

        # Vantaggio di posizione (semplice) --> incoraggia l'IA a muoversi in avanti
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == 2: # pedina IA
                    punteggio += r # pedine IA più avanti valgono di più
                if self.board[r][c] == 4: # dama IA
                    punteggio += r * 2 # dame IA più avanti valgono ancora di più
                if self.board[r][c] == 1: # pedina giocatore
                    punteggio -= (7 - r) # pedine giocatore più indietro valgono di meno per l'umano
                if self.board[r][c] == 3: # dama giocatore
                    punteggio -= (7 - r) * 2

        # Controllo delle condizioni di vittoria/sconfitta basate sui pezzi
        if human_pieces == 0: # Se il giocatore umano non ha pezzi, l'IA vince
            return float('inf')
        if ia_pieces == 0: # Se l'IA non ha pezzi, il giocatore umano vince
            return -float('inf')

        # Controllo delle condizioni di vittoria/sconfitta basate sulle mosse disponibili
        if self.game_over_for_player(1): # Se il giocatore umano non ha mosse disponibili, l'IA vince
            return float('inf')
        if self.game_over_for_player(2): # Se l'IA non ha mosse disponibili, il giocatore umano vince
            return -float('inf')
        return punteggio

    # Minimax con potatura alfa-beta
    def minimax(self, depth, maximizing_player, alpha=-float('inf'), beta=float('inf')):
        # Condizioni di terminazione della ricorsione
        if depth == 0 or self.game_over_for_player(1) or self.game_over_for_player(2):
            return self.valuta()
        if maximizing_player: # Turno dell'IA (giocatore 2) --> cerca di massimizzare il punteggio
            max_eval = -float('inf')
            current_player_moves = self.mosse(2)
            # Se non ci sono mosse disponibili per l'IA, il gioco è finito per questo ramo
            if not current_player_moves: 
                return self.valuta()
            for move in current_player_moves:
                temp_board = copy.deepcopy(self) # Crea una copia della scacchiera per simulare la mossa
                temp_board.muovi(move)
                evaluation = temp_board.minimax(depth - 1, False, alpha, beta) # Passa al giocatore minimizzante (umano)
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha: # Potatura alfa-beta
                    break 
            return max_eval
        else: # Turno del giocatore umano (giocatore 1) --> cerca di minimizzare il punteggio dell'IA
            min_eval = float('inf')
            current_player_moves = self.mosse(1)
            # Se non ci sono mosse disponibili per l'umano, il gioco è finito per questo ramo
            if not current_player_moves: 
                return self.valuta()
            for move in current_player_moves:
                temp_board = copy.deepcopy(self)
                temp_board.muovi(move)
                evaluation = temp_board.minimax(depth - 1, True, alpha, beta) # Passa al giocatore massimizzante (IA)
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha: # Potatura alfa-beta
                    break 
            return min_eval

    # Aggiorna mossa_ia per usare minimax con alfa-beta
    def mossa_ia(self, depth=4): # Profondità di ricerca predefinita
        mosse_disponibili = self.mosse(2)
        if not mosse_disponibili:
            return None # Nessuna mossa disponibile per l'IA
        best_score = -float('inf')
        best_move = random.choice(mosse_disponibili) # Inizializza con una mossa casuale come fallback
        for move in mosse_disponibili:
            copia = copy.deepcopy(self)
            copia.muovi(move)
            # Dopo la mossa dell'IA, è il turno dell'umano (minimizing_player).
            # Chiamiamo minimax con depth-1 perché una mossa è già stata fatta.
            # L'IA cerca di massimizzare il proprio punteggio, quindi valuta la mossa
            # basandosi sul risultato del turno dell'umano (che minimizzerà).
            score = copia.minimax(depth - 1, False) 
            if score > best_score:
                best_score = score
                best_move = move
            elif score == best_score: # Se i punteggi sono uguali, scegli casualmente per varietà
                if random.random() < 0.5:
                    best_move = move
        return best_move

def main():

    gioco = Dama()

    while True:

        gioco.stampa()

        if gioco.turno == 1: # Turno del giocatore umano
            
            print("Turno del giocatore (○ e  ⚪)")
            print("Inserisci riga_sorgente colonna_sorgente riga_dest colonna_dest (separati da spazio, tipo così: 5 1 4 2)")

            try:
                r1, c1, r2, c2 = map(int, input().split())
                move = ((r1, c1), (r2, c2))
                # Controlla se la mossa è valida per il giocatore corrente
                if move in gioco.mosse(1): 
                    gioco.muovi(move)
                    if gioco.game_over_for_player(2): # Se l'IA non ha mosse dopo la mossa umana
                        print("Complimenti! Hai vinto!")
                        break
                    gioco.turno = 2 # Passa il turno all'IA
                else:
                    print("Mossa non valida! Riprova.")
            except ValueError:
                print("Formato non valido! Assicurati di inserire 4 numeri separati da spazi.")
            except Exception as e:
                print(f"Si è verificato un errore: {e}")

        else: # Turno dell'IA
            print("Turno IA (● e ⚫)")
            m = gioco.mossa_ia()
            if m: # Se l'IA ha una mossa disponibile
                print(f"L'IA muove da {m[0]} a {m[1]}")
                gioco.muovi(m)
                if gioco.game_over_for_player(1): # Se il giocatore umano non ha mosse dopo la mossa dell'IA
                    print("L'IA ha vinto! Riprova.")
                    break
                gioco.turno = 1 # Passa il turno al giocatore umano
            else:
                print("L'IA non ha mosse disponibili. Il giocatore umano vince!")
                break


if __name__ == "__main__":
    main()