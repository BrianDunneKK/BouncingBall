import cdkk


class Manager_Ball(cdkk.SpriteManager):
    def __init__(self):
        super().__init__("Ball Manager")
        self.ball = cdkk.Sprite()
        self.ball.load_image_from_file("ball_red.png")
        self.ball.rect.topleft = (100, 50)
        self.add(self.ball)


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
