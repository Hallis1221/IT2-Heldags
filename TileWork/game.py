import pygame
from TileWork.debug import DebugManager
from TileWork.map import Map

class Game:
    def __init__(self, title="Pygame Tile Framework Game", size=(800, 600), fps=60):
        pygame.init()
        self.title = title
        self.size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True
        self.entities = []
        self.map = None
        self.debug_manager = DebugManager()
        self.show_debug = False

    def start(self):
        """Start the game using the game loop manager."""
        self.run_game_loop()

    def run_game_loop(self):
        """Handle the main game loop."""
        while self.running:
            dt = self.clock.tick(self.fps)
            self.handle_events()
            self.update(dt)
            self.render()

    def handle_events(self):
        """Process all events from the event queue."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.toggle_debug()
            else:
                for entity in self.entities:
                    entity.handle_events(event)


    def toggle_debug(self):
        """Toggle the visibility of the debug screen."""
        self.show_debug = not self.show_debug

    def update(self, dt):
        """Update all entities and game states."""
        if self.show_debug:
            self.debug_manager.add_info('FPS', f'{self.clock.get_fps():.2f}')
            self.debug_manager.add_info('Entities', f'{len(self.entities)}')
            self.debug_manager.add_info('Map', f'{self.map.filename if self.map else "None"}')

            for i, entity in enumerate(self.entities):
                self.debug_manager.add_info(f'Entity_{i}', f'Pos: {entity.position}')

        if self.map:
            self.map.update(dt)
        for entity in self.entities:
            entity.update(dt)
            self.handle_collisions(entity)

    def handle_collisions(self, entity):
        """Check and handle collisions for a given entity."""
        for other in self.entities:
            if other != entity and entity.check_collision_with(other):
                entity.on_collision(other)
        # Example of tile collision checking
        for x in range(entity.rect.left, entity.rect.right, self.map.tile_width):
            for y in range(entity.rect.top, entity.rect.bottom, self.map.tile_height):
                tile = self.map.get_tile_at(x, y)
                if tile and tile.collision:
                    tile.position.x = x
                    tile.position.y = y

                    entity.on_collision(tile)

    def render(self):
        """Render all entities and the map."""
        self.screen.fill((0, 0, 0))  # Clear the screen with black
        if self.map:
            self.map.render(self.screen)
        for entity in self.entities:
            entity.draw(self.screen)

        if self.show_debug:
            self.debug_manager.draw(self.screen)
        
        pygame.display.flip()

    def load_map(self, filename):
        self.map = Map(filename)

    def add_entity(self, entity):
        """Add an entity to the game."""
        self.entities.append(entity)

    def stop(self):
        """Stops the game loop."""
        self.running = False