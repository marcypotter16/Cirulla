from Game import Game
from Tween.pygame_test_tween import TweenTestState


if __name__ == "__main__":
    g = Game()
    test = TweenTestState(g)
    g.push_state(test)
    g.game_loop()
    