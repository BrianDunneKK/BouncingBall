# The Sprite_Ball class is now initialised with a velocity. The new update()
# method is called every game loop. It calculates the new positon of the sprite
# based on its velocity.

import cdkk
import pygame

# --------------------------------------------------


class Sprite_Ball(cdkk.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.load_image_from_file(filename)
        self.rect.topleft = (100, 10)
        self.rect.set_velocity(3, 2)
        self.rect.go()

    def update(self):
        super().update()
        self.rect.move_physics()

    def move_down(self):
        self.rect.move_physics(0, 10)

# --------------------------------------------------


class Manager_Ball(cdkk.SpriteManager):
    def __init__(self):
        super().__init__("Ball Manager")
        self.ball = Sprite_Ball("ball_red.png")
        self.add(self.ball)

    def event(self, e):
        dealt_with = super().event(e)
        if not dealt_with and e.type == cdkk.EVENT_GAME_CONTROL:
            if e.action == "MoveDown":
                self.ball.move_down()
                dealt_with = True
        return dealt_with

# --------------------------------------------------


class MyGame(cdkk.PyGameApp):
    def init(self):
        super().init()
        self._ball_mgr = Manager_Ball()
        self.add_sprite_mgr(self._ball_mgr)

        key_map = {
            pygame.K_q: "Quit",
            pygame.K_DOWN: "MoveDown"
        }
        self.event_mgr.event_map(key_event_map=key_map)


app_config = {
    "width": 1200, "height": 920,
    "background_fill": "burlywood",
    "caption": "Bouncing Ball",
    "image_path": "BouncingBall\\Images\\"
}

MyGame(app_config).execute()
