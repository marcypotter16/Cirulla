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

if __name__ == "__main__":
    print(CARD_PATHS)
