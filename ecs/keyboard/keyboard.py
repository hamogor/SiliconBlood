from ecs.keyboard.keyboard_component import KeyboardComponent
import pygame


class KeyboardSystem:
    def __init__(self):
        self.keys_pressed = []

    def update(self, entities):
        current_keys_pressed = []
        self.keys_pressed = []
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                current_keys_pressed.append(event.key)

                self.keys_pressed = current_keys_pressed

                if self.keys_pressed:
                    for e in entities:
                        if e.has(KeyboardComponent):
                            ki = e.get(KeyboardComponent)
                            ki.on_keydown_callback(self.keys_pressed)

    def time_passed(self):
        for event in pygame.event.get():
            if event.type == pygame.key.get_pressed():
                return event.key
        return False

    def get_keys(self):
        return self.keys_pressed
