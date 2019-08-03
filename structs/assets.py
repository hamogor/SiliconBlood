import pygame
from settings import *


class Tileset:
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()

        self.tiledict = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                         'e': 5, 'f': 6, 'g': 7, 'h': 8,
                         'i': 9, 'j': 10, 'k': 11, 'l': 12,
                         'm': 13, 'n': 14, 'o': 15, 'p': 16}

    def get_image(self, column, row, width=32,
                  height=32, scale=None):
        image_list = []
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0),
                   (self.tiledict[column] * width,
                    row * height,
                    width, height))

        image.set_colorkey(LIGHTGREY)
        if scale:
            (new_w, new_h) = scale
            image = pygame.transform.scale(image, (new_w, new_h))
        image_list.append(image)
        return image_list


class Assets:
    def __init__(self):

        # complete sound list
        self.snd_list = []

        self.load_assets()

    def load_assets(self):
        self.wall = Tileset("assets/wall_test.png")

        self.S_WALL_00 = self.wall.get_image('a', 0, 16, 16, (32, 32))[0]
        self.S_WALL_01 = self.wall.get_image('a', 0, 16, 16, (32, 32))[0]
        self.S_WALL_02 = self.wall.get_image('a', 0, 16, 16, (32, 32))[0]
        self.S_WALL_03 = self.wall.get_image('a', 2, 16, 16, (32, 32))[0]
        self.S_WALL_04 = self.wall.get_image('a', 0, 16, 16, (32, 32))[0]
        self.S_WALL_05 = self.wall.get_image('c', 1, 16, 16, (32, 32))[0]
        self.S_WALL_06 = self.wall.get_image('a', 0, 16, 16, (32, 32))[0]
        self.S_WALL_07 = self.wall.get_image('c', 1, 16, 16, (32, 32))[0]
        self.S_WALL_08 = self.wall.get_image('a', 0, 16, 16, (32, 32))[0]
        self.S_WALL_09 = self.wall.get_image('c', 2, 16, 16, (32, 32))[0]
        self.S_WALL_10 = self.wall.get_image('b', 2, 16, 16, (32, 32))[0]
        self.S_WALL_11 = self.wall.get_image('b', 2, 16, 16, (32, 32))[0]
        self.S_WALL_12 = self.wall.get_image('c', 0, 16, 16, (32, 32))[0]
        self.S_WALL_13 = self.wall.get_image('c', 1, 16, 16, (32, 32))[0]
        self.S_WALL_14 = self.wall.get_image('b', 0, 16, 16, (32, 32))[0]
        self.S_WALL_15 = self.wall.get_image('c', 3, 16, 16, (32, 32))[0]

        self.wall_dict = {

            0: self.S_WALL_00,
            1: self.S_WALL_01,
            2: self.S_WALL_02,
            3: self.S_WALL_03,
            4: self.S_WALL_04,
            5: self.S_WALL_05,
            6: self.S_WALL_06,
            7: self.S_WALL_07,
            8: self.S_WALL_08,
            9: self.S_WALL_09,
            10: self.S_WALL_10,
            11: self.S_WALL_11,
            12: self.S_WALL_12,
            13: self.S_WALL_13,
            14: self.S_WALL_14,
            15: self.S_WALL_15

        }

