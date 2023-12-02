from Database.cards import cards
from Models.CardInfo import CardInfo


def card_from_string(line, _id) -> CardInfo:
    split_line = line.split(",")
    return CardInfo(split_line[0], int(split_line[1]), split_line[2], _id=_id)


def deck_from_file(filename: str) -> list[CardInfo]:
    with open(filename, "r") as file:
        lines = file.readlines()
        deck = []
        for i, line in enumerate(lines):
            # deck.append(card_from_string(line, i))
            deck.append(cards[i + 1])
        return deck


if __name__ == "__main__":
    print([card.name for card in deck_from_file("../cards.txt")])
