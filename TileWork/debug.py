import pygame

class DebugManager:
    def __init__(self):
        self.debug_info = {}

    def add_info(self, key, value):
        self.debug_info[key] = value

    def remove_info(self, key):
        if key in self.debug_info:
            del self.debug_info[key]

    def draw(self, screen):
        font = pygame.font.Font(None, 24)
        y_offset = 10
        for key, value in self.debug_info.items():
            debug_text = f'{key}: {value}'
            debug_surface = font.render(debug_text, True, pygame.Color('black'))
            screen.blit(debug_surface, (10, y_offset))
            y_offset += debug_surface.get_height() + 2
