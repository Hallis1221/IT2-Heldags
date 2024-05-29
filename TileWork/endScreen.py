import pygame

class EndScreen:
    def __init__(self, size=(640, 480)):
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render('Game Over', True, pygame.Color('black'))
        self.text_rect = self.text.get_rect(center=(size[0] // 2, size[1] // 2))
        self.info = {}

    def draw(self, screen):
        screen.fill(pygame.Color('white'))
        screen.blit(self.text, self.text_rect)

        if self.info:
            y_offset = self.text_rect.bottom + 20
            for key, value in self.info.items():
                debug_text = f'{key}: {value}'
                font = pygame.font.Font(None, 24)
                debug_surface = font.render(debug_text, True, pygame.Color('black'))
                screen.blit(debug_surface, (10, y_offset))
                y_offset += debug_surface.get_height() + 2

    def update(self, dt):
        pass

    def add_info(self, key, value):
        self.info[key] = value
