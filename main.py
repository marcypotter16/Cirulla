import sys
from Card import Card
from ConsoleGame import Board, Deck
from ConsolePlayer import Bot, Player, PRIMIERA_VALUES


class Game:
    def __init__(self, p1=None, p2=None):
        self.board = Board()
        self.turn_count = 0
        if p1 is not None and p2 is not None:
            self.players = [p1, p2]
        else:
            self.players = [Player("P1"), Bot("P2")]
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
        for p in self.players:
            p.won_cards = []
            p.hand = []
            p.scope = 0
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
        return self.get_total_scores()

    def get_total_scores(self):
        self.p_score = self.b_score = 0
        self.player_cards = self.players[0].won_cards
        self.bot_cards = self.players[1].won_cards
        self.p_diamond_cards = [c for c in self.player_cards if c.seme == 'Q']
        self.b_diamond_cards = [c for c in self.bot_cards if c.seme == 'Q']

        def get_primiera(cards: list):
            best_cards = []
            for suit in ["P", "C", "Q", "F"]:
                l = sorted([c for c in cards if c.seme == suit], key=lambda c: PRIMIERA_VALUES[c.valore], reverse=True)
                if len(l) > 0:
                    best_cards.append(l[0])
            return best_cards, sum([PRIMIERA_VALUES[c.valore] for c in best_cards])
        self.p_primiera, self.p_primiera_score = get_primiera(self.player_cards)
        self.b_primiera, self.b_primiera_score = get_primiera(self.bot_cards)
        l1, l2 = [c for c in self.player_cards if str(c) == '7Q'], [c for c in self.bot_cards if str(c) == '7Q']
        self.p_settebello = l1[0] if len(l1) > 0 else None
        self.b_settebello = l2[0] if len(l2) > 0 else None
        if len(self.player_cards) > 20:
            self.p_score += 1
        elif len(self.player_cards) < 20:
            self.b_score += 1
        if len(self.p_diamond_cards) > 5:
            self.p_score += 1
        elif len(self.p_diamond_cards) < 5:
            self.b_score += 1
        if self.p_primiera_score > self.b_primiera_score:
            self.p_score += 1
        elif self.p_primiera_score < self.b_primiera_score:
            self.b_score += 1
        if self.p_settebello:
            self.p_score += 1
        else:
            self.b_score += 1
        self.p_score += self.players[0].scope
        self.b_score += self.players[1].scope
        return self.p_score, self.b_score

    def clever_bot_against_bot(self):
        for p in self.players:
            p.won_cards = []
            p.hand = []
            p.scope = 0
        self.deck = Deck()
        self.deck.shuffle()
        self.board.cards = []
        self.board.cards.extend(self.deck.draw(4))
        while len(self.deck.cards) > 0:
            self.turn_count += 1
            for p in self.players:
                p.draw_cards(self.deck, 3)
            # Gioca la mano
            for _ in range(3):
                for p in self.players:
                    played_card = p.play_card(p.think(self.board), self.board)
        return self.get_total_scores()

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
