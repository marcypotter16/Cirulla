from pygame import Vector2

from ConsolePlayer import Player, Bot
from main import Game


class MonteCarlo:
    def __init__(self, total_games: int = 1000000):
        self.player = Bot()
        self.bot = Bot()
        # A match ends when one player reaches 61 points
        self.__bot_score = self.__player_score = 0
        self.scores = Vector2(0, 0)
        self.player_wins = 0
        self.total_games = total_games
        self.game = Game(self.player, self.bot)
    def run(self):
        for _ in range(self.total_games):
            while not any([val >= 61 for val in self.scores]):
                self.game.clever_bot_against_bot()
                self.scores += Vector2(self.game.get_total_scores())
                if self.scores[0] >= 61:
                    self.player_wins += 1
            self.scores = Vector2(0, 0)
        print(f"Su {self.total_games} partite, {self.player_wins} / {self.total_games} ossia {float(self.player_wins) * 100.0 / self.total_games}%")

if __name__ == '__main__':
    m = MonteCarlo(total_games=10000)
    m.run()


