# entity.py
import pygame
import random
import time

class BaseEntity:
    def __init__(self, maxPos=(0, 0), image_path=None, color=None, position=(0, 0), size=(32, 32), velocity=(0, 0), collision=True, moveGoalEntity=None, randomMove=False, onGameEnd=None, label=None):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.size = size
        self.color = color
        self.image = pygame.image.load(image_path) if image_path else None
        self.rect = pygame.Rect(position, size)
        self.collision = collision
        self.randomMove = randomMove
        self.moveGoalEntity = moveGoalEntity
        self.moves = []
        self.maxPos = maxPos
        self.onGameEnd = onGameEnd
        self.label = label

        if self.randomMove and not moveGoalEntity:
            self.moveGoal = pygame.Vector2(random.randint(0, maxPos[0]), random.randint(0, maxPos[1]))
        else:
            self.moveGoal = moveGoalEntity.position if moveGoalEntity else None

    def update(self, dt):
        if self.randomMove or self.moveGoal:
            self.moveGoal = self.moveGoalEntity.position if self.moveGoalEntity else self.moveGoal

            if self.position.distance_to(self.moveGoal) < 2 and self.randomMove:
                self.moveGoal = pygame.Vector2(random.randint(0, self.maxPos[0]), random.randint(0, self.maxPos[1]))
            elif self.position.distance_to(self.moveGoal) < 2:
                self.moveGoal = None
            else:
                self.move_towards(self.moveGoal)

        # Update position based on velocity.
        self.position += self.velocity * dt
        self.rect.topleft = self.position

    def move(self, dx, dy):
        self.moves.append((dx, dy))
        self.position.x += dx * self.size[0]
        self.position.y += dy * self.size[1]
        self.rect.topleft = self.position

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.position)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        if self.label:
            self.draw_label(screen)

    def draw_label(self, screen):
        font_size = self.size[1]  # Start with the height of the entity as font size
        font = pygame.font.Font(None, font_size)
        label_surface = font.render(self.label, True, pygame.Color('black'))
        
        # Scale font size down until it fits within the entity's width
        while label_surface.get_width() > self.size[0]:
            font_size -= 1
            font = pygame.font.Font(None, font_size)
            label_surface = font.render(self.label, True, pygame.Color('black'))
        
        label_rect = label_surface.get_rect(center=self.rect.center)
        screen.blit(label_surface, label_rect)

    def handle_events(self, event):
        pass

    def move_towards(self, goal):
        if self.position == goal:
            return

        direction = goal - self.position
        direction.normalize_ip()
        self.velocity = direction * 100

    def check_collision_with(self, other):
        return self.rect.colliderect(other.rect)

    def on_collision(self, other, game):
        if not self.collision or not other.collision:
            return

        if hasattr(other, 'endOnCollision') and other.endOnCollision:
            if self.onGameEnd:
                self.onGameEnd()

        if len(self.moves) == 0:
            return

        self.position.x -= self.moves[-1][0] * self.size[0]
        self.position.y -= self.moves[-1][1] * self.size[1]
        self.rect.topleft = self.position
        self.moves.pop()

        if self.velocity.x != 0:
            self.velocity.x = -self.velocity.x
        if self.velocity.y != 0:
            self.velocity.y = -self.velocity.y

        if self.randomMove:
            self.moveGoal = pygame.Vector2(random.randint(0, self.maxPos[0]), random.randint(0, self.maxPos[1]))


class BlinkingEntity(BaseEntity):
    def __init__(self, blink_duration=3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blink_duration = blink_duration
        self.food_color = self.color
        self.hindrance_color = (128, 128, 128)
        self.blinking = False
        self.convert = False
        self.blink_start_time = 0

    def start_blinking(self):
        self.blinking = True
        self.blink_start_time = time.time()

    def update(self, dt):
        if self.blinking:
            elapsed_time = time.time() - self.blink_start_time
            if int(elapsed_time * 10) % 10 < 5:
                self.color = self.food_color
            else:
                self.color = self.hindrance_color

            if elapsed_time >= self.blink_duration:
                self.blinking = False
                self.convert = True
        super().update(dt)
