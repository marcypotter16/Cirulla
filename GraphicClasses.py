from Card import Card, Hand
from ConsoleGame import Board, Deck
from Game import Game
from GraphicUtil import CARD_PATHS
import pygame as p

from ConsolePlayer import Bot, Player
from Utils.Text import draw_centered_text, draw_text


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
        self.flipped = False

    def move(self, x: int, y: int):
        self.position = x, y
        self.rect = p.Rect(self.position, (self.width, self.height))

    def snap_back(self):
        self.game.tweener.add_tween(self, "position", p.Vector2(self.position), p.Vector2(self.position_before_drag), 0.2, on_finish=self.on_snap_back_finish, motion="ease_in_out_cubic")

    def on_snap_back_finish(self):
        self.move(*self.position)

    def on_tween_to_finish(self, callable: callable = None):
        self.move(*self.position)
        if callable:
            callable()

    def tween_to(self, x: int, y: int, duration: float = 0.2, on_finish: callable = None):
        self.game.tweener.add_tween(self, "position", p.Vector2(self.position), p.Vector2(x, y), duration, on_finish=lambda: self.on_tween_to_finish(on_finish), motion="ease_in_out_cubic")
    
    def drop(self):
        self.position_before_drag = self.position

    def move_center(self, x: int, y: int):
        self.move(x - self.width // 2, y - self.height // 2)

    def render(self, surface: p.Surface):
        surface.blit(self.sprite, self.position)

    def flip(self):
        """
        Flip the card from back to front and viceversa
        """
        self.flipped = not self.flipped
        if self.flipped:
            self.sprite = p.image.load(CARD_PATHS["back"])
        else:
            self.sprite = p.image.load(CARD_PATHS[str(self)])
        self.sprite = p.transform.scale(self.sprite, (self.width, self.height))

    def update(self):
        if self.rect.collidepoint(self.game.mousepos):
            # print(f"Mouse is over the card {self}")
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

    @staticmethod
    def from_card(card: Card, game: Game):
        """
        Create a GraphicCard from a Card
        """
        if card is not None:
            return GraphicCard(game, card.valore, card.seme)
        return None


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

    def rearrange(self, then: callable = None):
        for i, card in enumerate(self.cards):
            card.tween_to(self.topleft[0] + i * card.width, self.topleft[1], on_finish=then)
            card.drop()

class GraphicDeck(Deck):
    def __init__(self, game: Game, size=40, position: tuple[int, int] = (0, 0), card_dimensions: tuple[int, int] = (50, 75)):
        super().__init__(size)
        self.game = game
        self.position = position
        self.dimensions = card_dimensions
        self.sprite = p.image.load(CARD_PATHS["back"])
        self.sprite = p.transform.scale(self.sprite, self.dimensions)
        self.rect = p.Rect(self.position, self.dimensions)
        
    def update(self):
        pass

    def render(self, surface: p.Surface):
        surface.blit(self.sprite, self.position)
        draw_centered_text(self.game.font_medium, surface, str(len(self.cards)), (255, 255, 255), self.rect)


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
        self.show_hand = True

    def add_card(self, card: GraphicCard | list[GraphicCard]):
        if isinstance(card, list):
            if len(self.cards) + len(card) <= self.capacity:
                if not self.show_hand:
                    for c in card:
                        c.flip()
                self.cards.extend(card)
                for i, c in enumerate(self.cards):
                    c.move(self.topleft[0] + i * c.width, self.topleft[1])
            else: raise ValueError("Mano piena")
        else:
            card.move(self.topleft[0] + len(self.cards) * card.width, self.topleft[1])
            card.flip()
            self.cards.append(card)
        
        
    def rearrange(self):
        for i, card in enumerate(self.cards):
            card.move(self.topleft[0] + i * card.width, self.topleft[1])
            card.drop() # Drop the card so that it can be snapped back to its original position
        
    def set_card_back(self, value: bool):
        if value:
            for c in self.cards:
                if not c.flipped:
                    c.flip()
        self.show_hand = value
        

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
        super().__init__()
        self.game = game
        self.graphic_hand: GraphicHand = GraphicHand(game, topleft=(0, 500))
        self.graphic_hand.topleft = (self.game.GAME_W // 2 - self.graphic_hand.dimensions[0] // 2, self.game.GAME_H - self.graphic_hand.dimensions[1])
        self.graphic_hand.rect = p.Rect(self.graphic_hand.topleft, self.graphic_hand.dimensions)
        self.hand = self.graphic_hand.cards
        self.scope_text = "Scope: 0"
        self.scope_text_rect = p.Rect(self.graphic_hand.rect)
        self.scope_text_rect.left += 300
        pos = p.Vector2(self.graphic_hand.rect.right + 50, self.graphic_hand.rect.top - 20)
        self.graphic_won_cards = GraphicWonCards(game, position=pos, dimensions=(50, 75), label="Carte vinte")
        # This is for the last take (the last to take a card takes everything on the board)
        self.has_taken_last_turn = False
 
    def render(self, surface: p.Surface):
        self.graphic_hand.render(surface)
        draw_centered_text(self.game.font_medium, surface, self.scope_text, (255, 255, 255), self.scope_text_rect)
        self.graphic_won_cards.render(surface)

    def update(self):
        self.graphic_hand.update()
        self.graphic_won_cards.update()
   
    def draw_cards(self, deck: Deck, amount: int):
        self.graphic_hand.add_card([GraphicCard.from_card(c, self.game) for c in deck.draw(amount)])

    def play_card(self, card: GraphicCard, board: Board):
        if card.flipped:
            card.flip()
        # Buona tre e dieci
        if self.is_buona_dieci():
            self.scope += 10
        elif self.is_buona_tre():
            self.scope += 3
        # Assi
        if card.valore == 1 and 1 not in [c.valore for c in board.cards] and not board.is_empty():
            print("Scopa con l'asso")
            self.scope += 1
            self.won_cards.extend(board.cards)
            self.graphic_won_cards.add_cards(board.cards)
            self.won_cards.append(card)
            self.graphic_won_cards.add_cards(card)
            board.cards = []
        
        else:
            prese_possibili = set(board.calculate_sums())
        
            for p in prese_possibili:
                if p.valore == card.valore or p.valore + card.valore == 15:
                    self.has_taken_last_turn = True
                    p.cards.add(card)
                    self.won_cards.extend(p.cards)
                    self.graphic_won_cards.add_cards(list(p.cards))
                    board.cards = list(set(board.cards) - set(p.cards))
                    # Controllo se ho fatto scopa
                    if len(board.cards) == 0:
                        print("Scopa!")
                        self.scope += 1
                    break
            else:
                self.has_taken_last_turn = False
                board.cards.append(card)
        self.hand.remove(card)
        board.rearrange()
        self.graphic_won_cards.rearrange()
        return card


class GraphicBot(GraphicPlayer, Bot):
    def __init__(self, game: Game, show_hand: bool = True, smart: bool = False):
        super().__init__(game)
        # Move the hand to the top of the screen
        self.graphic_hand.topleft = (self.game.GAME_W // 2 - self.graphic_hand.dimensions[0] // 2, 0)
        self.graphic_hand.rect = p.Rect(self.graphic_hand.topleft, self.graphic_hand.dimensions)
        self.graphic_hand.rearrange()
        # Adjust the scope text position
        self.scope_text_rect = p.Rect(self.graphic_hand.rect)
        self.scope_text_rect.left += 300
        # Adjust the position of the won cards
        pos = p.Vector2(self.graphic_hand.rect.right + 50, self.graphic_hand.rect.top)
        self.graphic_won_cards = GraphicWonCards(game, position=pos, dimensions=(50, 75), label="Carte vinte", show_back=True)
        # Set the hand to show the back of the cards
        self.graphic_hand.set_card_back(show_hand)
        self.show_hand = show_hand
        
        self.is_smart = smart

        self.has_played_card = False

    def render(self, surface: p.Surface):
        GraphicPlayer.render(self, surface)

    def update(self):
        # GraphicPlayer.update(self)
        self.graphic_hand.update()
        self.graphic_won_cards.update()

    def play_card(self, card: GraphicCard, board: Board, then: callable = None):
        if card.flipped:
            card.flip()
        # Find the target coordinates in the board:
        #   - x: the center of the board
        #   - y: the top of the board
        x = board.rect.centerx
        y = board.rect.top
        # Tween the card to the target coordinates
        def on_finish():
            GraphicPlayer.play_card(self, card, board)
            board.rearrange()
            if then:
                then()
            self.has_played_card = False
        card.tween_to(x, y, duration=1.0, on_finish=on_finish)
        # card2 = Bot.play_card(self, card, board)
        #board.rearrange()
        return card

    def think(self, board: Board) -> GraphicCard:
        if not self.is_smart:
            return Bot.think(self, board)
        else:
            return GraphicPlayer.think(self, board)
        

class GraphicWonCards:
    def __init__(self, game: Game, position: tuple[int, int] = (0, 0), dimensions: tuple[int, int] = (100, 150), label: str = "Carte", show_back: bool = True) -> None:
        self.game = game
        self.cards: list[GraphicCard] = []
        self.position = position
        self.width, self.height = dimensions
        self.rect = p.Rect(self.position, (self.width, self.height))
        self.label = label
        self.show_back = show_back

    def render(self, surface: p.Surface):
        p.draw.rect(surface, (255, 255, 255), self.rect, 1)
        draw_text(self.game.font_small, surface, self.label, (255, 255, 255), self.rect.left - 5, self.rect.bottom + 10)
        for card in self.cards:
            card.render(surface)
        draw_centered_text(self.game.font_medium, surface, f"{len(self.cards)}", (0, 255, 0), self.rect)

    def update(self):
        pass

    def add_cards(self, cards: GraphicCard | list[GraphicCard]):
        if isinstance(cards, list):
            if self.show_back:
                for c in cards:
                    if not c.flipped:
                        c.flip()
            self.cards.extend(cards)
            # for card in cards:
                # card.tween_to(self.position[0], self.position[1])
        else:
            if self.show_back:
                if not cards.flipped:
                    cards.flip()
            self.cards.append(cards)
            # cards.tween_to(self.position[0], self.position[1])
    
    def rearrange(self):
        # Stack the cards vertically
        for i, card in enumerate(self.cards):
            card.tween_to(self.position[0], self.position[1] + i * 2)
            card.drop()
    

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