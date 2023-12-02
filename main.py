import sys
from Card import Card
from ConsoleGame import Board, Deck
from ConsolePlayer import Bot, Player


class Game:
    def __init__(self):
        self.board = Board()
        self.turn_count = 0
        self.players = [Bot("P1"), Bot("P2")]
        self.deck: Deck = Deck()
        self.deck.shuffle()
        print(self.deck)

    def play(self):
        print("\nBenvenuto a Cirulla!\n")
        print(
            "Opzioni:\n\t1. Bot vs Bot\n\t2. Gioca contro il bot\n\t3. Gioca contro il bot furbo (non ancora implementata)\n\t4. Gioca contro un altro giocatore (non ancora implementata)\n")
        scelta = input("Inserire scelta (un inserimento non valido chiude il programma): ")
        if scelta == "1":
            self.bot_vs_bot()
        elif scelta == "2":
            self.play_against_bot()
        else:
            sys.exit(0)

    def bot_vs_bot(self):
        self.board.cards.extend(self.deck.draw(4))
        while len(self.deck.cards) > 0:
            self.turn_count += 1
            print(f"\nTurno {self.turn_count}\n")
            print("Board:" + str(self.board))
            for p in self.players:
                p.draw_cards(self.deck, 3)
                print("\n" + str(p))
            # Gioca la mano
            for _ in range(3):
                input()
                for p in self.players:
                    played_card = p.play_card(p.think(self.board), self.board)
                    print(f"Player {p.name} played {played_card}")
                print("Board:" + str(self.board))
        for p in self.players:
            print(p)
            print(f"Player: {p.name} ha fatto " + str(p.evaluate_won_cards_at_endgame()) + " punti.")

    def clever_bot_against_bot(self):
        pass

    def play_against_bot(self):
        # Il setup è uguale a bot vs bot
        self.board.cards.extend(self.deck.draw(4))
        while len(self.deck.cards) > 0:
            self.turn_count += 1
            print(f"\nTurno {self.turn_count}\n")
            print("Board:" + str(self.board) + "\n")
            for p in self.players:
                p.draw_cards(self.deck, 3)
            print(self.players[0])
            # Qui però deve giocare l'utente
            for _ in range(3):
                ok = False
                while not ok:
                    stringa = input("Inserire carta da giocare: ")
                    if stringa in [str(c) for c in self.players[0].hand]:
                        played_card = self.players[0].play_card(Card.from_string(stringa), self.board)
                        print(f"Hai giocato {played_card}\n\n")
                        ok = True
                    else:
                        print("Carta non valida, riprovare.\n")
                bot_card = self.players[1].play_card(self.players[1].think(self.board), self.board)
                print(f"Bot ha giocato {bot_card}\n\n")
                print("Board:" + str(self.board) + "\n")
        for i, p in enumerate(self.players):
            print(p)
            if i == 0:
                print("Hai fatto " + str(p.evaluate_won_cards_at_endgame()) + " punti.")
            else:
                print(f"Player {p.name} ha fatto " + str(p.evaluate_won_cards_at_endgame()) + " punti.")


if __name__ == "__main__":
    g = Game()
    g.play()
