from Card import Card, Hand
from ConsoleGame import Board
from Game import Game
from GraphicUtil import CARD_PATHS
import pygame as p

from ConsolePlayer import Player


class GraphicCard(Card):
    def __init__(self, game: Game, valore: int, seme: str, position: tuple[int, int] = (0, 0),
                 dimensions: tuple[int, int] = (50, 75)):
        super().__init__(valore, seme)
        self.game = game
        self.sprite = p.image.load(CARD_PATHS[str(self)])
        self.position = position
        self.width, self.height = dimensions
        self.sprite = p.transform.scale(self.sprite, (self.width, self.height))
        self.rect = p.Rect(self.position, (self.width, self.height))
        self.being_dragged = False
        self.dropped = False
        self.position_before_drag = position

    def move(self, x: int, y: int):
        self.position = x, y
        self.rect = p.Rect(self.position, (self.width, self.height))

    def snap_back(self):
        self.move(*self.position_before_drag)
    
    def drop(self):
        self.position_before_drag = self.position

    def move_center(self, x: int, y: int):
        self.move(x - self.width // 2, y - self.height // 2)

    def render(self, surface: p.Surface):
        surface.blit(self.sprite, self.position)

    def update(self):
        if self.rect.collidepoint(self.game.mousepos):
            print(f"Mouse is over the card {self}")
            dropped_this_frame = self.dropped
            if self.game.clicked_sx == 1:
                print(f"Mouse clicked on the card {self}")
                self.being_dragged = True
                self.position_before_drag = self.position
            elif self.game.clicked_sx == -1:
                print(f"{self} dropped")
                self.being_dragged = False
                self.dropped = True
            self.dropped = self.dropped and not dropped_this_frame
        if self.being_dragged:
            self.move_center(*self.game.mousepos)


class GraphicBoard(Board):
    def __init__(self, game: Game, card_dimensions: tuple[int, int] = (50, 75)):
        super().__init__()
        self.game = game
        self.topleft = game.GAME_W // 2 - card_dimensions[0] * 10 // 2, game.GAME_H // 2 - card_dimensions[1] // 2
        self.dimensions = (card_dimensions[0] * 10, card_dimensions[1])
        self.rect = p.Rect(self.topleft, self.dimensions)

    def render(self, surface: p.Surface):
        # For debugging purposes
        p.draw.rect(surface, (255, 255, 255), self.rect, 1)
        for i, card in enumerate(self.cards):
            # card.position = (i * card.width, 0)
            card.render(surface)

    def play_card(self, card: GraphicCard):
        self.play_card(card)
        card.move(self.topleft[0] + (len(self.cards) - 1) * card.width, self.topleft[1])
        card.drop()

    def update(self):
        pass

    def rearrange(self):
        for i, card in enumerate(self.cards):
            card.move(self.topleft[0] + i * card.width, self.topleft[1])
            card.drop()


class GraphicHand(Hand):
    def __init__(self, game: Game, capacity=3, topleft: tuple[int, int] = (0, 0), card_dimensions: tuple[int, int] = (50, 75)):
        """
        topleft: the position of the first card
        card_dimensions: the dimensions of the card
        """
        super().__init__(capacity)
        self.game = game
        self.topleft = topleft
        self.dimensions = (card_dimensions[0] * capacity, card_dimensions[1])
        self.rect = p.Rect(self.topleft, self.dimensions)

    def add_card(self, card: GraphicCard | list[GraphicCard]):
        if len(self.cards) < self.capacity:
            if isinstance(card, list):
                self.cards.extend(card)
                for i, c in enumerate(self.cards):
                    c.move(self.topleft[0] + i * c.width, self.topleft[1])
            else:
                card.move(self.topleft[0] + len(self.cards) * card.width, self.topleft[1])
                self.cards.append(card)
        else:
            raise ValueError("Mano piena")
        

    def render(self, surface: p.Surface):
        # For debugging purposes
        p.draw.rect(surface, (255, 255, 255), self.rect, 1)
        # Render the cards
        for c in self.cards:
            # c.position = (self.topleft[0] + j * c.width, self.topleft[1])
            c.render(surface)

    def update(self):
        for c in self.cards:
            c.update()


class GraphicPlayer(Player):
    def __init__(self, game: Game):
        self.game = game
        self.won_cards: list[Card] = []
        self.graphic_hand: GraphicHand = GraphicHand(game, topleft=(0, 500))
        self.graphic_hand.topleft = (self.game.GAME_W // 2 - self.graphic_hand.dimensions[0] // 2, self.game.GAME_H - self.graphic_hand.dimensions[1])
        self.graphic_hand.rect = p.Rect(self.graphic_hand.topleft, self.graphic_hand.dimensions)
        # For debugging purposes
        self.graphic_hand.add_card(GraphicCard(game, 1, "P"))
        self.graphic_hand.add_card(GraphicCard(game, 2, "C"))
        self.graphic_hand.add_card(GraphicCard(game, 1, "Q"))
        self.hand = self.graphic_hand.cards
        self.scope = 0

    def render(self, surface: p.Surface):
        self.graphic_hand.render(surface)

    def update(self):
        self.graphic_hand.update()

    def play_card(self, card: Card, board: Board):
        card = super().play_card(card, board)
        board.rearrange()
        return card


class GraphicBot:
    def __init__(self):
        # Add your code here
        pass

    def render(self, surface: p.Surface):
        # Add your code here
        pass


if __name__ == "__main__":
    # Use pygame to test all the cards
    cards = []
    g = Game()
    for i in range(1, 11):
        for s in ["P", "C", "Q", "F"]:
            cards.append(GraphicCard(g, i, s))

    for i, card in enumerate(cards):
        row = i // 10  # Calculate the row number
        col = i % 10  # Calculate the column number
        card.position = (col * card.width, row * card.height)  # Adjust the position based on row and column
    while g.running:
        g.get_events()
        g.mousepos = p.mouse.get_pos()
        for card in cards:
            card.update()
            card.render(g.game_canvas)
        p.display.update()
        g.clock.tick(g.fps)