# pactroll.py
import pygame
import random
from TileWork.game import Game
from TileWork.entity import BlinkingEntity, BaseEntity

class Food(BlinkingEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(blink_duration=3, *args, **kwargs)
        self.food_color = (255, 255, 0)
        self.hindrance_color = (128, 128, 128)
        self.color = self.food_color

class Hindrance(BaseEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = (128, 128, 128)

class Troll(BaseEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = 2

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.velocity = pygame.Vector2(-1*self.speed, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.velocity = pygame.Vector2(1*self.speed, 0)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.velocity = pygame.Vector2(0, -1*self.speed)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.velocity = pygame.Vector2(0, 1*self.speed)

    def update(self, dt):
        self.position += self.velocity * self.size[0] * dt
        self.rect.topleft = self.position

def create_random_position(size, excluded_positions, width, height):
    while True:
        x = random.randint(0, width - 1) * size[0]
        y = random.randint(0, height - 1) * size[1]
        pos = (x, y)
        if pos not in excluded_positions:
            return pygame.Vector2(pos)

def main():
    game = Game(title="PacTroll", size=(800, 800), fps=60)
    
    # Initialize map
    game.load_map()

    # Center of the map
    center_position = (game.size[0] // 2, game.size[1] // 2)

    # Create Troll
    troll = Troll(position=center_position, size=(32, 32), color=(0, 255, 0), label="T")
    troll.velocity = pygame.Vector2(1, 0)
    troll.onGameEnd = game.end

    # Create Food items at random positions
    food_items = []
    excluded_positions = {tuple(troll.position)}
    for _ in range(3):
        pos = create_random_position(troll.size, excluded_positions, 25, 25)
        food = Food(position=pos, size=(32, 32), label="M")
        food_items.append(food)
        game.add_entity(food)
        excluded_positions.add(tuple(pos))

    hindrances = []

    def game_loop(elapsed, game_instance):
        nonlocal food_items, hindrances

        for food in food_items:
            if troll.check_collision_with(food) and not food.blinking:
                game_instance.score += 1

                food.start_blinking()

                new_food_pos = create_random_position(troll.size, excluded_positions, 25, 25)
                new_food = Food(position=new_food_pos, size=(32, 32), label="M")
                food_items.append(new_food)
                game_instance.add_entity(new_food)
                excluded_positions.add(tuple(new_food_pos))

                troll.speed += 0.1
                break

        for food in food_items[:]:
            if food.blinking:
                food.update(elapsed)
            if food.convert:
                new_hindrance = Hindrance(position=food.position, size=(32, 32), label="H")
                hindrances.append(new_hindrance)
                game_instance.add_entity(new_hindrance)
                food_items.remove(food)
                game_instance.remove_entity(food)

        if troll.position.x < 0 or troll.position.x >= game_instance.size[0] or troll.position.y < 0 or troll.position.y >= game_instance.size[1]:
            game_instance.end()

        for hindrance in hindrances:
            if troll.check_collision_with(hindrance):
                game_instance.end()

    game.definedGameloop = game_loop
    game.add_entity(troll)

    game.start()

if __name__ == "__main__":
    main()
