from GraphicClasses import GraphicPlayer, GraphicBoard
from States.State import State
import pygame as p

from Utils.Text import draw_text


class GameState(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.player = GraphicPlayer(game)
        self.board = GraphicBoard(game)

    def render(self, surface):
        super().render(surface)
        draw_text(self.game.font_medium, surface, self.game.mousepos, (255, 255, 255), 0, 0)
        self.board.render(surface)
        self.player.render(surface)

    def update(self, delta_time):
        super().update(delta_time)
        self.board.update()
        self.player.update()
        for card in self.player.graphic_hand.cards:
            if card.dropped:
                if self.board.rect.collidepoint(card.rect.center):
                    self.player.play_card(card, self.board)
                else:
                    card.snap_back()