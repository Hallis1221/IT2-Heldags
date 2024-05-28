from TileWork.game import Game
from TileWork.entity import BaseEntity
import pygame
import random

class Snake(BaseEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body = [self.position.copy()]
        self.direction = pygame.Vector2(1, 0)
        self.grow_on_update = False

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.direction.x != 1:
                self.direction = pygame.Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT and self.direction.x != -1:
                self.direction = pygame.Vector2(1, 0)
            elif event.key == pygame.K_UP and self.direction.y != 1:
                self.direction = pygame.Vector2(0, -1)
            elif event.key == pygame.K_DOWN and self.direction.y != -1:
                self.direction = pygame.Vector2(0, 1)

    def update(self, dt):
        if self.grow_on_update:
            self.body.append(self.body[-1].copy())
            self.grow_on_update = False

        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = self.body[i - 1].copy()

        self.body[0] += self.direction * self.size[0]
        self.position = self.body[0].copy()
        self.rect.topleft = self.position

    def grow(self):
        self.grow_on_update = True

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, self.color, (*segment, *self.size))

class Food(BaseEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.relocate()

    def relocate(self):
        self.position = pygame.Vector2(
            random.randint(0, 24) * self.size[0],
            random.randint(0, 24) * self.size[1]
        )
        self.rect.topleft = self.position

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

def main():
    game = Game(title="Snake Game", size=(800, 800), fps=10)
    game.load_map("empty_level.json") 

    snake = Snake(color=(0, 255, 0), size=(32, 32))
    food = Food(color=(255, 0, 0), size=(32, 32))

    game.add_entity(snake)
    game.add_entity(food)

    def game_loop(elapsed, game):
        if snake.position == food.position:
            snake.grow()
            food.relocate()

        if snake.position.x < 0 or snake.position.x >= game.size[0] or \
           snake.position.y < 0 or snake.position.y >= game.size[1]:
            game.end()

        for segment in snake.body[1:]:
            if snake.position == segment:
                game.end()

    game.definedGameloop = game_loop
    game.start()

if __name__ == "__main__":
    main()
