import random
from ConsoleGame import Deck, Board
from Card import Card, Presa

CARD_VALUES = {
    "7Q": 21,
    "7F": 15,
    "7C": 15,
    "7P": 15,
    "AQ": 3,
    "2Q": 3,
    "3Q": 3,
    "4Q": 2,
    "5Q": 2,
    "6Q": 2,
    "8Q": 3,
    "9Q": 3,
    "10Q": 3,
}

PRIMIERA_VALUES = {
    7: 21,
    6: 18,
    1: 16,
    5: 15,
    4: 14,
    3: 13,
    2: 12,
    10: 10,
    9: 10,
    8: 10,
}

class Player:
    def __init__(self, name: str = "Player"):
        self.name = name
        self.hand = []
        self.won_cards = []
        self.scope = 0

    def draw_cards(self, deck: Deck, amount: int):
        cards_to_draw = deck.draw(amount)
        if len(cards_to_draw) + len(self.hand) > 3:
            raise ValueError("Sono state pescate un troppe carte")
        self.hand.extend(cards_to_draw)

    def is_buona_tre(self) -> bool:
        if len(self.hand) == 3:
            if "7C" not in [str(c) for c in self.hand]:
                return sum([c.valore for c in self.hand]) < 10
            else:
                return sum([c.valore for c in self.hand if str(c) != "7C"]) < 9
        return False
    
    def is_buona_dieci(self) -> bool:
        if len(self.hand) == 3:
            cards = [c for c in self.hand if str(c) != "7C"]
            val = cards[0].valore
            return all([c.valore == val for c in cards])
        return False
    
    @staticmethod
    def calculate_best_primiera_card_of_suit(cards: list[Card], suit: str) -> Card:
        cards_of_suit = [c for c in cards if c.seme == suit]
        if len(cards_of_suit) == 0:
            raise ValueError("Non ci sono carte di quel seme")
        return max(cards_of_suit, key=lambda c: PRIMIERA_VALUES[c.valore])

    def evaluate_won_cards_at_endgame(self) -> int:
        s = 0

        # Grande
        if {"8Q", "9Q", "10Q"} <= set([str(c) for c in self.won_cards]):
            s += 5
        
        # Piccola
        if {"1Q", "2Q", "3Q"} <= set([str(c) for c in self.won_cards]):
            s += 3
            for i in range(4, 7):
                if f"{i}Q" in [str(c) for c in self.won_cards]:
                    s += 1
                else: break
        
        # Settebello
        if "7Q" in [str(c) for c in self.won_cards]:
            s += 1

        # Primiera (versione 1)
        suits = ["P", "C", "Q", "F"]
        best_cards = []
        for suit in suits:
            best_card: Card = self.calculate_best_primiera_card_of_suit(self.won_cards, suit)
            best_cards.append(best_card)
        # due 7 e due 6
        if sum([PRIMIERA_VALUES[c.valore] for c in best_cards]) >= 21 * 2 + 18 * 2:
            s += 1

        # Carte
        if len(self.won_cards) >= 21:
            s += 1
        
        # Denari
        if len([c for c in self.won_cards if c.seme == "C"]) >= 6:
            s += 1

        return s + self.scope
    
    def think(self, board: Board) -> Card | None:
        if len(self.hand) == 0:
            return None
        prese_possibili = set(board.calculate_sums())
        
        # Includiamo le prese a 15
        for p in prese_possibili:
            if p.valore <= 15:
                cards = p.cards
                new_p = Presa(cards)
                new_p.valore = 15 - p.valore
                prese_possibili.add(new_p)
        
        # Controlliamo se possiamo prendere e consideriamo il valore delle carte
        best_presa = Presa([])
        best_carta = self.hand[0]
        for card in self.hand:
            for presa in prese_possibili:
                if card.valore == presa.valore:
                    # Se fai scopa la giochi a prescindere
                    if set(presa.cards) == set(board.cards):
                        return card
                    # Se non fai scopa la giochi solo se è la carta migliore
                    presa.add(card)
                    if best_presa.calculate_value() < presa.calculate_value():
                        best_presa = presa
                        best_carta = card
                    presa.remove(card)
        return best_carta
    
    def play_card(self, card: Card, board: Board):
        # Buona tre e dieci
        if self.is_buona_dieci():
            self.scope += 10
        elif self.is_buona_tre():
            self.scope += 3
        # Assi
        if card.valore == 1 and 1 not in [c.valore for c in board.cards] and not board.is_empty():
            self.scope += 1
            self.won_cards.extend(board.cards)
            board.cards = []
        
        else:
            prese_possibili = set(board.calculate_sums())
        
            for p in prese_possibili:
                if p.valore == card.valore or p.valore + card.valore == 15:
                    p.cards.add(card)
                    self.won_cards.extend(p.cards)
                    board.cards = list(set(board.cards) - set(p.cards))
                    # Controllo se ho fatto scopa
                    if len(board.cards) == 0:
                        self.scope += 1
                    break
            else:
                board.cards.append(card)
        self.hand.remove(card)
        return card
            

            

    def __str__(self):
        return f"Player: {self.name}\nHand: {[str(c) for c in self.hand]}\n" +\
            f"Won cards: {[str(c) for c in self.won_cards]}\n" +\
            f"Scope: {self.scope}"
    

class Bot(Player):
    def __init__(self, name: str = "Bot"):
        super().__init__(name=name)
    
    def think(self, board: Board) -> Card:
        return random.choice(self.hand)
    
if __name__ == "__main__":
    p1 = Player()
    p1.hand = [
        Card(1, "Q"),
        Card(1, "F"),
        Card(1, "D")
    ]

    p2 = Player()
    p2.hand = [
        Card(1, "Q"),
        Card(4, "D"),
        Card(3, "D")
    ]

    p3 = Player()
    p3.hand = [
        Card(3, "Q"),
        Card(3, "F"),
        Card(7, "C")
    ]

    p4 = Player()
    p4.hand = [
        Card(2, "F"),
        Card(3, "F"),
        Card(7, "C")
    ]

    players = [p1, p2, p3, p4]
    for p in players:
        print(p.is_buona_tre(), p.is_buona_dieci())