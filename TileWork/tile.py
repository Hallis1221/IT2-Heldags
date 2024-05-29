import pygame

class Tile:
    """Represents a single tile on the map."""
    def __init__(self, tile_type, image=None, color=None, collision=False, name="", position=(0, 0), size=(32, 32)):
        self.tile_type = tile_type
        self.image = image
        self.color = color
        self.collision = collision
        self.name = name
        self.size = size
        self.position = pygame.Vector2(position)

    def draw(self, screen, x, y, width, height):
        """Draw the tile on the screen."""
        if self.tile_type == 'image' and self.image:
            screen.blit(self.image, (x, y))
        elif self.tile_type == 'color' and self.color:
            pygame.draw.rect(screen, self.color, pygame.Rect(x, y, width, height))

    def collides_at(self, x, y):
        """Check if the given pixel coordinates collide with the tile."""
        return self.collision and self.position.x <= x < self.position.x + self.size[0] and self.position.y <= y < self.position.y + self.size[1]
