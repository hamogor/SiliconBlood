from settings import WIDTH, HEIGHT
import pygame


class TransitionComponent:
    def __init__(self):
        self.fade = pygame.Surface((WIDTH, HEIGHT))
        self.fade.fill((0, 0, 0))
        self.fade.set_alpha(0)
        self.alpha = 0
        self.fade_state = 1
        self.transition = False