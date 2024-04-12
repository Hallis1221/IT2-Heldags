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

    def update(self, dt):
        self.move(*self.direction)

        if self.is_colliding:
            self.direction = (-self.direction[0], -self.direction[1])
        

    def on_collision(self, other):
        self.position.x -= self.moves[-1][0] * self.size[0]
        self.position.y -= self.moves[-1][1] * self.size[1]
        self.rect.topleft = self.position
        self.moves.pop()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.size[0] // 2)

    def handle_events(self, event):
        pass

    def check_collision_with(self, other):
        return self.rect.colliderect(other.rect)


def main():
    game = Game(title="My Tile-based Game", size=(800, 800), fps=60)
    game.load_map("level.json")  # Make sure the path matches your map file's location

    player = Player(color=(255, 0, 0), size=(32, 32))
    ghost = Ghost(position=(5*32, 5*32), size=(32, 32))
    player.position = (3*32, 3*32)
    game.add_entity(player)
    game.add_entity(ghost)



    # Start the game loop
    game.start()

if __name__ == "__main__":
    main()
