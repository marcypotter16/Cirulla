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

class Card:

    def __init__(self, valore = 1, seme: str = "P"):
        self.valore = valore
        self.seme = seme
                                                        
    def __str__(self):
        return UTIL_DICT[self.valore] + self.seme
    
    def __eq__(self, __value: object) -> bool:
        return self.valore == __value.valore and self.seme == __value.seme
    
class Presa:

    def __init__(self, cards: list[Card] | set[Card] | Card) -> None:
        if isinstance(cards, Card):
            self.cards = {cards}
        elif isinstance(cards, set):
            self.cards = cards
        else:
            self.cards = set(cards)
        self.valore = sum([c.valore for c in self.cards])

    def __eq__(self, __value: object) -> bool:
        return self.cards == __value.cards
        
                                                                  
                                                                      
