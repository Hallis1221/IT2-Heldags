import pygame

class DebugManager:
    def __init__(self):
        self.debug_info = {}

    def add_info(self, key, value):
        """Add or update debug information."""
        self.debug_info[key] = value

    def remove_info(self, key):
        """Remove information from the debug display."""
        if key in self.debug_info:
            del self.debug_info[key]

    def draw(self, screen):
        """Draw the debug information on the screen."""
        debug_text = ''
        for key, value in self.debug_info.items():
            debug_text += f'{key}: {value} \n'
        font = pygame.font.Font(None, 24)
        debug_surface = font.render(debug_text, True, pygame.Color('black'))
        screen.blit(debug_surface, (10, 10))
