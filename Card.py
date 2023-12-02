UTIL_DICT = {
        1: "A",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "J",
        9: "Q",
        10: "K"
}

REVERSE_UTIL_DICT = {v: k for k, v in UTIL_DICT.items()}

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

class Card:

    def __init__(self, valore = 1, seme: str = "P"):
        if valore in range(1, 11):
            self.valore = valore
        else:
            raise ValueError("Il valore della carta deve essere compreso tra 1 e 10")
        if seme in ["P", "C", "Q", "F"]:
            self.seme = seme
        else:
            raise ValueError("Il seme della carta deve essere P, C, Q o F")

    @staticmethod
    def from_string(string: str):
        return Card(REVERSE_UTIL_DICT.get(string[0]), string[1])
                                                        
    def __str__(self):
        return UTIL_DICT[self.valore] + self.seme
    
    def __eq__(self, __value: object) -> bool:
        return self.valore == __value.valore and self.seme == __value.seme
    
    def __hash__(self):
        return hash((self.valore, self.seme))
    
class Presa:

    def __init__(self, cards: list[Card] | set[Card] | Card) -> None:
        #print([str(c) for c in cards])
        if isinstance(cards, Card):
            self.cards = {cards}
        elif isinstance(cards, set):
            self.cards = cards
        else: 
            self.cards = set(cards)
            #self.cards = [Card(c.valore, c.seme) for c in cards]
        self.valore = sum([c.valore for c in self.cards])

    def calculate_value(self) -> int:
        # Ritorna il valore della presa:
        # 1 punto per ogni carta
        # vari punti per le carte speciali
        s = sum([1 for c in self.cards if c not in CARD_VALUES.keys()])
        return s + sum([CARD_VALUES[str(c)] for c in self.cards if c in CARD_VALUES.keys()])

    def __eq__(self, __value: object) -> bool:
        return self.cards == __value.cards
    
    def __hash__(self) -> int:
        return hash((tuple(self.cards), self.valore))
    
class Hand:

    def __init__(self, capacity = 3):
        self.cards: list[Card] = []
        self.capacity = capacity

    def add(self, card: Card):
        if len(self.cards) < self.capacity:
            self.cards.append(card)
        else:
            raise ValueError("La mano è piena")

    def remove(self, card: Card):
        self.cards.remove(card)

    def __str__(self) -> str:
        s = "["
        for card in self.cards:
            s += str(card) + ", "
        return s[0:-2] + "]"
        
                                                                  
                                                                      
