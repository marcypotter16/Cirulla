from GraphicClasses import GraphicBoard, GraphicBot, GraphicPlayer
import pygame as p


class GraphicGame:
    def __init__(self) -> None:
        p.init()
        self.board = GraphicBoard()
        self.player = GraphicPlayer()
        self.bot = GraphicBot()

        self.turn_count = 0

        # Pygame stuff
        self.clock = p.time.Clock()
        self.window_width = 800
        self.window_height = 600
        self.window = p.display.set_mode((self.window_width, self.window_height))
        self.is_running = False
        self.left_clicked = 0
        self.right_clicked = 0
        self.actions = {"left_click": 0, "right_click": 0}

    def event_handler(self, event):
        if event.type == p.QUIT:
            self.is_running = False
        if event.type == p.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.actions["left_click"] = 1
            if event.button == 3:
                self.actions["right_click"] = 1
        if event.type == p.MOUSEBUTTONUP:
            if event.button == 1:
                self.actions["left_click"] = 0
            if event.button == 3:
                self.actions["right_click"] = 0

    def update(self):
        pass

    def render(self, surface: p.Surface):
        self.board.render(surface)
        self.bot.render(surface)
        self.player.render(surface)

    def play(self):
        self.is_running = True
        while self.is_running:
            self.window.fill((0, 0, 0))  # Fill the window with black color
            self.update()
            self.render(self.window)

            # Handle events
            prev_left_clicked = self.actions["left_click"]
            prev_right_clicked = self.actions["right_click"]
            for event in p.event.get():
                self.event_handler(event)
            self.left_clicked = self.actions["left_click"] - prev_left_clicked
            self.right_clicked = self.actions["right_click"] - prev_right_clicked

            # Update game logic

            # Render graphics

            p.display.flip()  # Update the display

            self.clock.tick(60)  # Limit the frame rate to 60 FPS

        p.quit()

if __name__ == "__main__":
    g = GraphicGame()
    g.play()
        

    