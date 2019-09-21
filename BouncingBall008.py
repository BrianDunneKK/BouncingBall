# The key "b" is mapped to a new action called "CreateBall".
# The Manager_Ball deals with CreateBall by creating a new ball each time the
# event action is received. The colour of the ball is now random.
# The __init__() method in Sprite_Ball now calls go() so that the ball starts
# moving as soon as it is created.
# The start_game() and move_down() methods in Sprite_Ball are not needed any
# more and are deleted.

import cdkk
import pygame
import random

# --------------------------------------------------


class Sprite_Ball(cdkk.Sprite):
    files = ["ball_red.png", "ball_yellow.png", "ball_green.png", "ball_brown.png",
             "ball_blue.png", "ball_pink.png", "ball_black.png"]

    def __init__(self, value):
        super().__init__()
        self.load_image_from_file(self.files[value-1])
        self.rect.left = random.randint(50, 500)
        self.rect.top = 10
        self.rect.set_speed_angle(4, 45)
        self.rect.go()

    def update(self):
        super().update()
        self.rect.move_physics()

# --------------------------------------------------


class Manager_Ball(cdkk.SpriteManager):
    def __init__(self):
        super().__init__("Ball Manager")

    def event(self, e):
        dealt_with = super().event(e)
        if not dealt_with and e.type == cdkk.EVENT_GAME_CONTROL:
            if e.action == "CreateBall":
                ball = Sprite_Ball(random.randint(1, len(Sprite_Ball.files)))
                self.add(ball)
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
