from TileWork.game import Game
from TileWork.entity import BaseEntity
import pygame

class Player(BaseEntity):
    def handle_events(self, event):
        print(self.position)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.position[0] > 0:
                self.move(-1, 0)
            elif event.key == pygame.K_RIGHT and self.position[0] < 800 - 32:
                self.move(1, 0)
            elif event.key == pygame.K_UP and self.position[1] > 0:
                self.move(0, -1)
            elif event.key == pygame.K_DOWN and self.position[1] < 800 - 32:
                self.move(0, 1)


def main():
    game = Game(title="My Tile-based Game", size=(800, 800), fps=60)
    game.load_map("manic_level.json")  # Make sure the path matches your map file's location

    player = Player(color=(255, 0, 0), size=(32, 32))
    player.position = (3*32, 3*32)
    player.onGameEnd = game.end

    game.add_entity(player)

    # Start the game loop
    game.start()

if __name__ == "__main__":
    main()
