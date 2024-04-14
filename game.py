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

class Ghost(BaseEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = (0, 255, 0)
        self.direction = (1, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.size[0] // 2)


def main():
    game = Game(title="My Tile-based Game", size=(800, 800), fps=60)
    game.load_map("level.json")  # Make sure the path matches your map file's location

    player = Player(color=(255, 0, 0), size=(32, 32))
    player.position = (3*32, 3*32)
    player.onGameEnd = game.end

    ghost = Ghost(position=(8*32, 8*32), size=(32, 32), moveGoalEntity=player)
    randomGhost = Ghost(position=(5*32, 5*32), size=(32, 32), randomMove=True, maxPos=(800, 800))

    ghost.endOnCollision = True
    game.add_entity(player)
    game.add_entity(randomGhost)
    game.add_entity(ghost)



    # Start the game loop
    game.start()

if __name__ == "__main__":
    main()
