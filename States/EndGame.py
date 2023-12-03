from States.State import State
from Utils.Text import draw_centered_text
import pygame as p

class EndGameState(State):
    def __init__(self, game):
        super().__init__(game)

    def render(self, surface):
        super().render(surface)
        draw_centered_text(self.game.font_big, surface, "Hai vinto?", (255, 255, 255), p.Rect((0, 0), (self.game.SCREEN_W, self.game.SCREEN_H)))
