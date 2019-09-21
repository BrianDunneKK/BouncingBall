# The Sprite_Ball nows posts a new "Boundary" event when it hits the window
# boundary. The event includes a unique ID for the ball.
# The Manager_Ball class deals with this event by deleting the ball.

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
        bounce_event = cdkk.EventManager.gc_event(
            "Boundary", ball_id=self.uuid)
        self.rect.add_limit(cdkk.Physics_Limit(
            limits, cdkk.LIMIT_KEEP_INSIDE, cdkk.AT_LIMIT_BOUNCE, bounce_event))
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
            if e.action == "Boundary":
                if e.at_limit_y & cdkk.AT_LIMIT_BOTTOM:
                    self.kill_uuid(e.info["ball_id"])
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
