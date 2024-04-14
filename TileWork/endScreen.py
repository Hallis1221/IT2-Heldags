import pygame

class EndScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render('Game Over', True, pygame.Color('black'))
        self.text_rect = self.text.get_rect(center=(400, 300))
        self.info = {}

    def draw(self, screen):
        screen.fill(pygame.Color('white'))
        screen.blit(self.text, self.text_rect)

        if self.info:
            debug_text = ''
            for key, value in self.info.items():
                debug_text += f'{key}: {value} \n'
            font = pygame.font.Font(None, 24)
            debug_surface = font.render(debug_text, True, pygame.Color('black'))
            screen.blit(debug_surface, (10, 10))


    def update(self, dt):
        pass

    def add_info(self, key, value):
        """Add or update debug information."""
        self.info[key] = value