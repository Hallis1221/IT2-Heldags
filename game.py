from TileWork.game import Game
from TileWork.entity import BaseEntity
import pygame

class Player(BaseEntity):
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move(-1, 0)  # Move left
            elif event.key == pygame.K_RIGHT:
                self.move(1, 0)
            elif event.key == pygame.K_UP:
                self.move(0, -1)
            elif event.key == pygame.K_DOWN:
                self.move(0, 1)

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                self.velocity.x = 0  # Stop moving


def main():
    game = Game(title="My Tile-based Game", size=(800, 800), fps=60)
    game.load_map("level.json")  # Make sure the path matches your map file's location

    player = Player(color=(255, 0, 0), size=(32, 32))
    player.position = (3*32, 3*32)
    game.add_entity(player)



    # Start the game loop
    game.start()

if __name__ == "__main__":
    main()
