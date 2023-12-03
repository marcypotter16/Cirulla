from States.State import State
from Utils.Text import draw_centered_text

class EndGameState(State):
    def __init__(self, game):
        super().__init__(game)

    def render(self, surface):
        super().render(surface)
        draw_centered_text(self.game.font_big, surface, "Hai vinto?", (255, 255, 255), 0, 0)
