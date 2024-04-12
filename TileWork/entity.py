import pygame

class BaseEntity:
    def __init__(self, image_path=None, color=None, position=(0, 0), size=(32, 32), velocity=(0, 0)):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.size = size
        self.color = color
        self.image = pygame.image.load(image_path) if image_path else None
        self.rect = pygame.Rect(position, size)
        self.is_colliding = False
        self.moves = []

    def update(self, dt):
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

    def check_collision_with(self, other):
        return self.rect.colliderect(other.rect)


    def on_collision(self, other):
        print(f'{self} collided with {other}. Undoing move.')
        if len(self.moves) == 0:
            return
        self.position.x -= self.moves[-1][0] * self.size[0]
        self.position.y -= self.moves[-1][1] * self.size[1]
        self.rect.topleft = self.position
        self.moves.pop()

        pass
