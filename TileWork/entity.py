import pygame
import random

class BaseEntity:
    def __init__(self, maxPos=(0,0), image_path=None, color=None, position=(0, 0), size=(32, 32), velocity=(0, 0), collision=True, moveGoalEntity=None, randomMove=False,onGameEnd=None):
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

        if (randomMove and not moveGoalEntity):
            self.moveGoal = pygame.Vector2(random.randint(0, maxPos[0]), random.randint(0, maxPos[1]))
        else:
            self.moveGoal = moveGoalEntity.position if moveGoalEntity else None

    def update(self, dt):
        if (self.randomMove or self.moveGoal):
            self.moveGoal = self.moveGoalEntity.position if self.moveGoalEntity else self.moveGoal

            if (self.position.distance_to(self.moveGoal) < 2 and self.randomMove):
                self.moveGoal = pygame.Vector2(random.randint(0, self.maxPos[0]), random.randint(0, self.maxPos[1])) if self.randomMove else None
            else:
                self.move_towards(self.moveGoal)

        self.position += self.velocity * (dt / 1000.0)  # Convert dt to seconds for movement
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


    def on_collision(self, other):

        if (not self.collision) or (not other.collision):
            return
        
        if hasattr(other, 'endOnCollision') and other.endOnCollision and not hasattr(self, 'endOnCollision') and not hasattr(self, 'ignoreEndOnCollision'):
            print(f'{self} collided with {other}. Ending game.')
            if hasattr(self, 'onGameEnd'):
                self.onGameEnd()

            
        print(f'{self} collided with {other}. Undoing move.')
        if len(self.moves) == 0:
            return
        self.position.x -= self.moves[-1][0] * self.size[0]
        self.position.y -= self.moves[-1][1] * self.size[1]
        self.rect.topleft = self.position
        self.moves.pop()

        # if moving towards a random goal, change the goal
        if self.randomMove:
            self.moveGoal = pygame.Vector2(random.randint(0, self.maxPos[0]), random.randint(0, self.maxPos[1]))


        pass
