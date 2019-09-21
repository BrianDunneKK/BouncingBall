# The MyGame class passes the size of the window when creating Manager_Ball,
# and it passes the size to Sprite_Ball.
# The __init__() method in Sprite_Ball adds a limit to its movement, bouncing
# off the window boundary. The ball now moves at a random angle and the X
# position is spread across the width of the window. The speed of the ball is
# now based on its value.

import cdkk
import pygame
import random

# --------------------------------------------------


class Sprite_Ball(cdkk.Sprite):
    files = ["ball_red.png", "ball_yellow.png", "ball_green.png", "ball_brown.png",
             "ball_blue.png", "ball_pink.png", "ball_black.png"]

    def __init__(self, value, limits):
        super().__init__()
        self.load_image_from_file(self.files[value-1])
        self.rect.left = random.randint(limits.width * 0.2, limits.width * 0.8)
        self.rect.top = 10
        speed = value * 3 + 5
        angle = random.randint(45, 135)
        self.rect.set_speed_angle(speed, angle)
        self.rect.bounce_cor = self.rect.perfect_bounce
        self.rect.add_limit(cdkk.Physics_Limit(
            limits, cdkk.LIMIT_KEEP_INSIDE, cdkk.AT_LIMIT_BOUNCE))
        self.rect.go()

    def update(self):
        super().update()
        self.rect.move_physics()

# --------------------------------------------------


class Manager_Ball(cdkk.SpriteManager):
    def __init__(self, limits):
        super().__init__("Ball Manager")
        self._limits = limits

    def event(self, e):
        dealt_with = super().event(e)
        if not dealt_with and e.type == cdkk.EVENT_GAME_CONTROL:
            if e.action == "CreateBall":
                ball = Sprite_Ball(random.randint(
                    1, len(Sprite_Ball.files)), self._limits)
                self.add(ball)
                dealt_with = True
        return dealt_with

# --------------------------------------------------


class MyGame(cdkk.PyGameApp):
    def init(self):
        super().init()
        self._ball_mgr = Manager_Ball(self.boundary)
        self.add_sprite_mgr(self._ball_mgr)

        key_map = {
            pygame.K_q: "Quit",
            pygame.K_s: "StartGame",
            pygame.K_b: "CreateBall"
        }
        self.event_mgr.event_map(key_event_map=key_map)


app_config = {
    "width": 1200, "height": 920,
    "background_fill": "burlywood",
    "caption": "Bouncing Ball",
    "image_path": "BouncingBall\\Images\\",
    "auto_start": False
}

MyGame(app_config).execute()
