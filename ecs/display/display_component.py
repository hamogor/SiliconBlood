class DisplayComponent:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.image = sprite.convert()
        self.rect = self.image.get_rect()