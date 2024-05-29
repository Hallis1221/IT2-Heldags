# manic_mansion.py
import pygame
import random
import json
from TileWork.game import Game
from TileWork.entity import BaseEntity, BlinkingEntity

class Human(BaseEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = 100
        self.carrying_sheep = False

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.velocity = pygame.Vector2(-1, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.velocity = pygame.Vector2(1, 0)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.velocity = pygame.Vector2(0, -1)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.velocity = pygame.Vector2(0, 1)

    def update(self, dt):
        self.position += self.velocity * self.speed * dt
        self.rect.topleft = self.position

class Ghost(BaseEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = (255, 0, 0)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() 

    def update(self, dt):
        next_position = self.position + self.velocity * dt
        tile_x = int(next_position.x // 32)
        tile_y = int(next_position.y // 32)

        # Check if the next position is out of bounds or in a safe zone
        if tile_x < 0 or tile_x >= 25 or tile_y < 0 or tile_y >= 20 or game_map[tile_y][tile_x] in [1, 2]:
            # Change direction
            self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() 
        else:
            self.position = next_position
            self.rect.topleft = self.position

class Sheep(BlinkingEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(blink_duration=3, *args, **kwargs)
        self.food_color = (255, 255, 0)
        self.hindrance_color = (128, 128, 128)
        self.color = self.food_color

class Obstacle(BaseEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = (0, 0, 255)

def create_random_position(size, excluded_positions, width, height, game_map, zone=None):
    while True:
        x = random.randint(0, width - 1) * size[0]
        y = random.randint(0, height - 1) * size[1]
        tile_x = x // 32
        tile_y = y // 32
        if (x, y) not in excluded_positions:
            if zone == "left_safe_zone" and game_map[tile_y][tile_x] == 1:
                return pygame.Vector2(x, y)
            elif zone == "right_safe_zone" and game_map[tile_y][tile_x] == 2:
                return pygame.Vector2(x, y)
            elif zone is None and game_map[tile_y][tile_x] == 0:
                return pygame.Vector2(x, y)

def main():
    global game_map

    game = Game(title="Manic Mansion", size=(800, 640), fps=60)
    game.load_map("manic_level.json")

    # Load map data
    with open("manic_level.json") as f:
        map_data = json.load(f)
    game_map = map_data["tiles"][0]

    # Create Human
    human_start_position = (50, 320)
    human = Human(position=human_start_position, size=(32, 32), color=(0, 255, 0), label="H")
    human.velocity = pygame.Vector2(0, 0)
    human.onGameEnd = game.end

    # Create Ghosts, Obstacles, and Sheep
    entities = []
    excluded_positions = {tuple(human.position)}

    # Ghosts
    for _ in range(1):
        pos = create_random_position(human.size, excluded_positions, 25, 20, game_map)
        ghost = Ghost(position=pos, size=(32, 32), label="G")
        entities.append(ghost)
        game.add_entity(ghost)
        excluded_positions.add(tuple(pos))

    # Obstacles
    for _ in range(3):
        pos = create_random_position(human.size, excluded_positions, 25, 20, game_map)
        obstacle = Obstacle(position=pos, size=(32, 32), label="O")
        entities.append(obstacle)
        game.add_entity(obstacle)
        excluded_positions.add(tuple(pos))

    # Sheep
    sheep_list = []
    for _ in range(3):
        pos = create_random_position(human.size, excluded_positions, 25, 20, game_map, zone="right_safe_zone")
        sheep = Sheep(position=pos, size=(32, 32), label="S")
        sheep_list.append(sheep)
        game.add_entity(sheep)
        excluded_positions.add(tuple(pos))

    def is_in_left_safe_zone(position):
        tile_x = int(position.x // 32)
        tile_y = int(position.y // 32)
        return game_map[tile_y][tile_x] == 1

    def is_in_right_safe_zone(position):
        tile_x = int(position.x // 32)
        tile_y = int(position.y // 32)
        return game_map[tile_y][tile_x] == 2

    def game_loop(elapsed, game_instance):
        nonlocal sheep_list, entities

        # Handle collisions and game logic
        for sheep in sheep_list:
            if human.check_collision_with(sheep):
                if not human.carrying_sheep:
                    human.carrying_sheep = True
                    sheep_list.remove(sheep)
                    game_instance.remove_entity(sheep)
                    human.speed *= 0.5

        for entity in entities:
            if isinstance(entity, Ghost) and human.check_collision_with(entity):
                game_instance.end()
            elif isinstance(entity, Obstacle) and human.check_collision_with(entity):
                human.velocity = pygame.Vector2(0, 0)  # Block human movement

        # Handle return to safe zone with sheep
        if human.carrying_sheep and is_in_left_safe_zone(human.position):
            game_instance.score += 1
            human.carrying_sheep = False
            human.speed = 100

            # Add new sheep
            new_sheep_pos = create_random_position(human.size, excluded_positions, 25, 20, game_map, zone="right_safe_zone")
            new_sheep = Sheep(position=new_sheep_pos, size=(32, 32), label="S")
            sheep_list.append(new_sheep)
            game_instance.add_entity(new_sheep)
            excluded_positions.add(tuple(new_sheep_pos))

            # Add new ghost
            new_ghost_pos = create_random_position(human.size, excluded_positions, 25, 20, game_map)
            new_ghost = Ghost(position=new_ghost_pos, size=(32, 32), label="G")
            entities.append(new_ghost)
            game_instance.add_entity(new_ghost)
            excluded_positions.add(tuple(new_ghost_pos))

            # Add new obstacle
            new_obstacle_pos = create_random_position(human.size, excluded_positions, 25, 20, game_map)
            new_obstacle = Obstacle(position=new_obstacle_pos, size=(32, 32), label="O")
            entities.append(new_obstacle)
            game_instance.add_entity(new_obstacle)
            excluded_positions.add(tuple(new_obstacle_pos))

        if human.position.x < 0 or human.position.x >= game_instance.size[0] or human.position.y < 0 or human.position.y >= game_instance.size[1]:
            human.velocity = pygame.Vector2(0, 0)  # Block human movement

        # Update all entities
        for entity in entities:
            entity.update(elapsed)

    game.definedGameloop = game_loop
    game.add_entity(human)

    game.start()

if __name__ == "__main__":
    main()
