class DisplayComponent:
    def __init__(self, x, y, sprite, alpha=False):
        self.x = x
        self.y = y
        if not alpha:
            self.sprite = sprite.convert()
        else:
            self.sprite = sprite.convert_alpha()
        self.image = sprite.convert()
        self.rect = self.image.get_rect()
