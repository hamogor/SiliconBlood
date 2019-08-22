class DisplayComponent:
    def __init__(self, sprite, x, y, alpha=False):
        self.x = x
        self.y = y
        if not alpha:
            self.sprite = sprite.convert()
        else:
            self.sprite = sprite.convert_alpha()
