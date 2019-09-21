# The update() method in the MyGame is called every game loop. It finds the bat
# sprite and passes it to the new check_for_hits() method in the Manager_Bat
# class.
# The check_for_hits() method create a "dynamic limit" that causes the ball to
# bounce off of the bat.

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

    def check_bat_hits(self, bat):
        for ball in self.sprites():
            ball.rect.dynamic_limit(cdkk.Physics_Limit(
                bat.rect, cdkk.LIMIT_KEEP_OUTSIDE, cdkk.AT_LIMIT_Y_BOUNCE_Y))

# --------------------------------------------------


class Sprite_Bat (cdkk.Sprite):
    def __init__(self, limits):
        super().__init__("Bat")
        self.load_image_from_file("bat.png")
        self.rect.centerx = limits.width/2
        self.rect.top = limits.height * 0.9
        self.rect.add_limit(cdkk.Physics_Limit(
            limits, cdkk.LIMIT_KEEP_INSIDE, cdkk.AT_LIMIT_X_HOLD_POS_X))

# --------------------------------------------------


class Manager_Bat(cdkk.SpriteManager):
    def __init__(self, limits, name="Bat Manager"):
        super().__init__(name)
        self._bat = Sprite_Bat(limits)
        self.add(self._bat)

    def event(self, e):
        dealt_with = False
        if e.type == cdkk.EVENT_GAME_CONTROL:
            if e.action == "MouseMotion":
                x, y = e.info['pos']
                self._bat.rect.move_to(x, None)
                dealt_with = True
        return dealt_with

# --------------------------------------------------


class MyGame(cdkk.PyGameApp):
    def init(self):
        super().init()
        self._ball_mgr = Manager_Ball(self.boundary)
        self.add_sprite_mgr(self._ball_mgr)
        self._bat_mgr = Manager_Bat(self.boundary)
        self.add_sprite_mgr(self._bat_mgr)

        key_map = {
            pygame.K_q: "Quit",
            pygame.K_s: "StartGame",
            pygame.K_b: "CreateBall"
        }
        self.event_mgr.event_map(key_event_map=key_map)

    def update(self):
        super().update()
        bat = self.sprite("Bat Manager", "Bat")
        self._ball_mgr.check_bat_hits(bat)


app_config = {
    "width": 1200, "height": 920,
    "background_fill": "burlywood",
    "caption": "Bouncing Ball",
    "image_path": "BouncingBall\\Images\\",
    "auto_start": False
}

MyGame(app_config).execute()
