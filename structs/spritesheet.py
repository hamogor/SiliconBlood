import pygame
from settings import TILESIZE


class Spritesheet:
    def __init__(self, file_name):
        self.sprite_sheet = file_name.convert()

        self.tiledict = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                         'e': 5, 'f': 6, 'g': 7, 'h': 8,
                         'i': 9, 'j': 10, 'k': 11, 'l': 12,
                         'm': 13, 'n': 14, 'o': 15, 'p': 16}

    def get_image(self, col, row, width=TILESIZE, height=TILESIZE, scale=None):

        image_list = []

        image = pygame.Surface([width, height]).convert()

        #image.blit(self.sprite_sheet, (0, 0), (self.tiledict[col]*width, row*height, width, height))

        if scale:
            new_h, new_w = scale
            image = pygame.transform.scale(image, (new_h, new_w))

        image_list.append(image)

        return image_list
