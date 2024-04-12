import pygame

class GameLoop:
    def __init__(self, game):
        self.game = game

    def start(self):
        """Start the game loop."""
        while self.game.running:
            command = self.game.event_manager.process_events()
            if command == 'QUIT':
                self.game.stop()

            self.game.update()
            self.game.render()
            pygame.display.flip()
            self.game.clock.tick(self.game.fps)
