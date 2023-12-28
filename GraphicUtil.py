from Card import Card


__eng_dict = {
    "P": "Spades",
    "C": "Hearts",
    "Q": "Diamonds",
    "F": "Clubs"
}

CARD_PATHS = {"back": "./Art/Backs/back_0.png"}

for i in range(1, 11):
    for s in ["P", "C", "Q", "F"]:
        card = Card(i, s)
        CARD_PATHS[str(card)] = f"./Art/{__eng_dict[s]}/{__eng_dict[s]}_card_{str(card.valore if card.valore < 8 else card.valore + 1).zfill(2)}.png"
d = {
    'd': 'Q',
    'c': 'F',
    'h': 'C',
    's': 'P'
}
vals = {
    1: 'a',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: '10',
    11: 'j',
    12: 'q',
    13: 'k'
}
# Uncomment this to use the other set of cards
# for i in range(1, 11):
#     for s in ['c', 'h', 's', 'd']:
#         card = Card(i, d.get(s))
#         CARD_PATHS[str(card)] = f"./Art2/{s}{vals.get(i)}.png"

if __name__ == "__main__":
    print(CARD_PATHS)
