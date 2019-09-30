import cdkk

# --------------------------------------------------


class Sprite_Ball(cdkk.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.load_image_from_file(filename)
        self.rect.topleft = (100, 10)

# --------------------------------------------------


class Manager_Ball(cdkk.SpriteManager):
    def __init__(self):
        super().__init__("Ball Manager")
        self.ball = Sprite_Ball("ball_red.png")
        self.add(self.ball)

# --------------------------------------------------


class MyGame(cdkk.PyGameApp):
    def init(self):
        super().init()
        self._ball_mgr = Manager_Ball()
        self.add_sprite_mgr(self._ball_mgr)


app_config = {
    "width": 1200, "height": 920,
    "background_fill": "burlywood",
    "caption": "Bouncing Ball",
    "image_path": "BouncingBall\\Images\\"
}

MyGame(app_config).execute()
