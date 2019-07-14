import pysnooper
import pygame
from ecs.input.keyboard_input_component import KeyboardInputComponent


class KeyboardInputSystem:
    def __init__(self):
        self.keys_pressed = []

    def update(self, entities):
        current_keys_pressed = []

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                current_keys_pressed.append(event.key)

                self.keys_pressed = current_keys_pressed

                if self.keys_pressed:
                    for e in entities:
                        if e.has(KeyboardInputComponent):
                            ki = e.get(KeyboardInputComponent)
                            ki.on_keydown_callback(self.keys_pressed)

                            return True

                return False

    @staticmethod
    def time_passed():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print(event.key)
                return True
            return False

    def get_all_keys_pressed(self):
        return self.keys_pressed


