import pygame
import json
from pygame.time import Clock

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

class Map:
    def __init__(self, filename):
        self.tile_layers = []
        self.tileset = {}
        self.tile_width = 0
        self.tile_height = 0
        self.width = 0
        self.height = 0
        self.animation_speed = 0  
        self.current_layer = 0
        self.clock = Clock()
        self.time_since_last_animation = 0
        self.filename = filename
        self.load()

    def load(self):
        """Load the map from a JSON file."""
        with open(self.filename, 'r') as f:
            data = json.load(f)

        self.tile_width = data['tileWidth']
        self.tile_height = data['tileHeight']
        self.width = data['width']
        self.height = data['height']
        self.animation_speed = 1000 / data['animationSpeed']  # Convert to milliseconds

        # Load the tileset information
        for key, value in data['tileset'].items():
            if value['type'] == 'image':
                image = pygame.image.load(value['value'])
            else:
                image = None
            color = value['value'] if value['type'] == 'color' else None
            tile = Tile(value['type'], image, color, value['collision'], value['name'])
            self.tileset[key] = tile

        # Load all layers
        self.tile_layers = [
            [
                [self.tileset[str(tile_id)] for tile_id in row]
                for row in layer
            ]
            for layer in data['tiles']
        ]

    def render(self, screen):
        """Render the current map layer on the screen."""
        for y, row in enumerate(self.tile_layers[self.current_layer]):
            for x, tile in enumerate(row):
                tile.draw(screen, x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height)

    def update(self, dt):
        """Update the map state for animations."""
        self.time_since_last_animation += dt
        if self.time_since_last_animation >= self.animation_speed:
            self.time_since_last_animation = 0
            self.current_layer = (self.current_layer + 1) % len(self.tile_layers)

    def get_tile_at(self, pixel_x, pixel_y):
        """Return the tile at the given pixel coordinates."""
        tile_x = pixel_x // self.tile_width
        tile_y = pixel_y // self.tile_height

        tile = self.tile_layers[self.current_layer][tile_y][tile_x]
        return tile if tile.collision else None