import time
from Generic.CyclicList import CyclicList
from Generic.Stack import Stack
from GraphicClasses import GraphicBot, GraphicCard, GraphicDeck, GraphicPlayer, GraphicBoard
from States.State import State
import pygame as p

from Utils.Text import draw_text
from Utils.Timer import Timer

class GameState(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.player = GraphicPlayer(game)
        self.bot = GraphicBot(game, show_hand=False)
        self.board = GraphicBoard(game)
        self.deck = GraphicDeck(game, position=(200, game.GAME_H // 2 - 75), card_dimensions=(100, 150))
        self.deck.shuffle()
        self.timer = Timer()
        self.turn_count: int = 0
        self.states = CyclicList()
        self.states.add("BeginTurn")
        for _ in range(3):
            self.states.add("PlayerTurn")
            self.states.add("BotTurn")
        self.states.set_current(0)
        print([s for s in self.states.items])

    def render(self, surface):
        super().render(surface)
        self.board.render(surface)
        self.deck.render(surface)
        self.bot.render(surface)
        self.player.render(surface)
        draw_text(self.game.font_medium, surface, f"Turno {self.turn_count // 2 + 1}", (255, 255, 255), 0, 0)
        # Debug
        draw_text(self.game.font_small, surface, self.board, (255, 255, 255), 0, 20)
        draw_text(self.game.font_small, surface, self.timer.finished, (255, 255, 255), 0, 40)
        draw_text(self.game.font_medium, surface, str(self.states.get_current()), (255, 255, 255), 0, 60)

    def update(self, delta_time):
        super().update(delta_time)
        self.board.update()
        self.deck.update()
        if self.states.get_current() == "BeginTurn":
            self.player.draw_cards(self.deck, 3)
            self.bot.draw_cards(self.deck, 3)
            # Add 4 cards at the beginning of the game
            if self.turn_count == 0:
                self.board.cards.extend([GraphicCard.from_card(c, self.game) for c in self.deck.draw(4)])
            self.board.rearrange()
            self.states.next()
        if self.states.get_current() == "PlayerTurn":
            self.update_player(delta_time)
        if self.states.get_current() == "BotTurn":
            self.update_bot(delta_time)
        self.timer.update(delta_time)

    def update_player(self, delta_time):
        self.player.update()
        for card in self.player.graphic_hand.cards:
            if card.dropped:
                if self.board.rect.collidepoint(card.rect.center):
                    self.player.play_card(card, self.board)
                    self.turn_count += 1
                    self.states.next()
                else:
                    card.snap_back()

    def update_bot(self, delta_time):
        self.bot.update()
        # self.timer.start(1)
        # if self.timer.finished:
        #     print("AAAAAAAAAAAAAAAAAAAAAAAAAA")
        #     print(self.bot.play_card(self.bot.think(self.board), self.board))
        #     self.turn_count += 1
        #     self.states.next()
        print(self.bot.play_card(self.bot.think(self.board), self.board))
        self.turn_count += 1
        print(self.states.get_current())
        self.states.next()
        print(self.states.get_current())

