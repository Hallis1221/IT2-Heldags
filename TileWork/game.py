import pygame
from TileWork.debug import DebugManager
from TileWork.endScreen import EndScreen
from TileWork.map import Map
import time

class Game:
    def __init__(self, title="Pygame Tile Framework Game", size=(800, 600), fps=60, gameLoop=lambda _,___:___):
        pygame.init()
        self.title = title
        self.size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True
        self.entities = []
        self.text = []
        self.map = None
        self.debug_manager = DebugManager()
        self.endscreen = EndScreen()
        self.show_debug = True
        self.show_end_screen = False
        self.definedGameloop = gameLoop
        self.score = 0

    def start(self):
        """Start the game using the game loop manager."""
        self.run_game_loop()

    def run_game_loop(self):
        """Handle the main game loop."""
        startedAt = time.time()
        
        while self.running:
            dt = self.clock.tick(self.fps)
            elapsed = time.time()-startedAt
            self.handle_events()
            self.update(dt)
            self.definedGameloop(elapsed,self)
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
            self.debug_manager.add_info('Score', f'{self.score}')
                
        if self.show_end_screen:
            self.endscreen.add_info('Score', f'{self.score}')
            self.endscreen.update(dt)
        elif self.map:
            self.map.update(dt)
        for entity in self.entities:
            entity.update(dt)
            self.handle_collisions(entity)

    def handle_collisions(self, entity):
        """Check and handle collisions for a given entity."""
        for other in self.entities:
            if other != entity and entity.check_collision_with(other):
                entity.on_collision(other,self)

        for x in range(entity.rect.left, entity.rect.right, self.map.tile_width):
            for y in range(entity.rect.top, entity.rect.bottom, self.map.tile_height):
                tile = self.map.get_tile_at(x, y)
                if tile and tile.collision:
                    tile.position.x = x
                    tile.position.y = y

                    entity.on_collision(tile,self)

    def render(self):
        """Render all entities and the map."""
        self.screen.fill((0, 0, 0))  # Clear the screen with black
        if self.map:
            self.map.render(self.screen)
        for entity in self.entities:
            entity.draw(self.screen)

        if self.show_debug:
            self.debug_manager.draw(self.screen)
        
        if self.show_end_screen:
            self.endscreen.draw(self.screen)
        
        pygame.display.flip()

    def load_map(self, filename):
        self.map = Map(filename)

    def add_entity(self, entity):
        """Add an entity to the game."""
        entity.maxPos = pygame.Vector2((self.map.height*self.map.tile_height, self.map.width*self.map.tile_width))
        self.entities.append(entity)

    def remove_entity(self, entity):
        """Remove an entity from the game."""
        self.entities.remove(entity)
        
        
    def end(self):
        """End the game. Display a end game message with the option to restart."""
        self.show_end_screen = True
        
    def stop(self):
        """Stops the game loop."""
        self.running = False