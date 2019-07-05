from constants import *
from display.display import DisplaySystem
from display.display_component import DisplayComponent
from input.keyboard import KeyboardInputSystem, KeyboardInputComponent
from ecs.entity import Entity
from ecs.container import Container
import sys
import pygame


class Player(Entity):
    def __init__(self):
        super().__init__(DisplayComponent(S_PLAYER, 0, 0))
        KeyboardInputComponent(self._process_input)
        
    def _process_input(self, key_pressed):
        dc = self.get(DisplayComponent)
        if key_pressed in MOVE_N:
            dc.y -= 1
        elif key_pressed in MOVE_S:
            dc.y += 1
        elif key_pressed in MOVE_W:
            dc.x -= 1
        elif key_pressed in MOVE_E:
            dc.x += 1
        elif key_pressed in MOVE_NW:
            dc.x -= 1
            dc.y -= 1
        elif key_pressed in MOVE_NE:
            dc.x += 1
            dc.y -= 1
        elif key_pressed in MOVE_SW:
            dc.x -= 1
            dc.y += 1
        elif key_pressed in MOVE_SE:
            dc.x += 1
            dc.y += 1


class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        self.player = Player()
        self.game_over = False

        self.display_system = DisplaySystem()
        self.keyboard_input_system = KeyboardInputSystem()

        self.container = Container()

        self.container.add_system(self.keyboard_input_system)
        self.container.add_system(self.display_system)
        self.container.add_entity(self.player)

    def game_loop(self):
        self.container.update()

        while not self.game_over:
            self.check_for_game_over()
            time_passed = self.check_if_time_passed()

            if time_passed:
                self.container.update()
            else:
                self.keyboard_input_system.update(self.container._entities)
                self.display_system.update(self.container._entities)

    def check_for_game_over(self):
        keys_pressed = [e for e in self.keyboard_input_system.get_all_keys_pressed() if e == QUIT]
        if keys_pressed:
            self.game_over = True

    def check_if_time_passed(self):
        all_keys_pressed = self.keyboard_input_system.get_all_keys_pressed()

        keys_pressed = [e for e in all_keys_pressed
                        if e == MOVE_N or e == MOVE_S or e == MOVE_W or e == MOVE_E]

        return keys_pressed


if __name__ == '__main__':
    Main().game_loop()
