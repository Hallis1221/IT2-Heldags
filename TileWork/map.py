from pygame.time import Clock
import pygame
import json
from TileWork.tile import Tile

DEFAULT_MAP = {
    "width": 10,
    "height": 10,
    "tileWidth": 32,
    "tileHeight": 32,
    "animationSpeed": 1,
    "tiles": [
        [
            [0] * 25 for _ in range(25)
        ]
    ],
    "tileset": {
        "0": {"type": "color", "value": "#333333", "collision": False, "name": "Open Space"},
        "1": {"type": "color", "value": "#ffffff", "collision": True, "name": "Wall"}
    }
}


class Map:
    def __init__(self, filename=None):
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
        """Load the map from a JSON file or use the default map if no file is provided."""
        if self.filename:
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                print("File not found. Using default map.")
                data = DEFAULT_MAP
        else:
            print("No file provided. Using default map.")
            data = DEFAULT_MAP

        self.tile_width = data['tileWidth']
        self.tile_height = data['tileHeight']
        self.width = data['width']
        self.height = data['height']
        self.animation_speed = 1000 / data['animationSpeed']  # Convert to milliseconds

        # Load the tileset information
        for key, value in data['tileset'].items():
            image = pygame.image.load(value['value']) if value['type'] == 'image' else None
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

        try:
            tile = self.tile_layers[self.current_layer][tile_y][tile_x]
            return tile if tile.collision else None
        except IndexError:
            return None
            