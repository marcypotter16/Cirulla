from Game import Game
from States.GameState import GameState

g = Game()
game_state = GameState(g)
g.state_stack.push(game_state)
g.game_loop()