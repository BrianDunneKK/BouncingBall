import cdkk
import pygame
import random

# --------------------------------------------------


class Sprite_Ball(cdkk.Sprite):
    files = ["ball_red.png", "ball_yellow.png", "ball_green.png", "ball_brown.png",
             "ball_blue.png", "ball_pink.png", "ball_black.png"]

    def __init__(self, value, limits):
        super().__init__()
        self.load_image_from_file(self.files[value - 1])
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
    def __init__(self, limits, total, at_a_time):
        super().__init__("Ball Manager")
        self._limits = limits
        self._at_a_time = at_a_time
        self._total = total
        self.balls_left = total
        self.add_balls()

    def add_balls(self):
        current_balls = len(self.sprites())
        new_balls = self._at_a_time - current_balls
        if new_balls > self.balls_left:
            new_balls = self.balls_left

        for i in range(new_balls):
            value = random.randint(1, len(Sprite_Ball.files))
            ball = Sprite_Ball(value, self._limits)
            self.add(ball)
            self.balls_left -= 1

    def event(self, e):
        dealt_with = super().event(e)
        if not dealt_with and e.type == cdkk.EVENT_GAME_CONTROL:
            if e.action == "Boundary":
                if e.at_limit_y & cdkk.AT_LIMIT_BOTTOM:
                    self.kill_uuid(e.info["ball_id"])
                    self.add_balls()
        return dealt_with

    def check_bat_hits(self, bat):
        for ball in self.sprites():
            ball.rect.dynamic_limit(cdkk.Physics_Limit(
                bat.rect, cdkk.LIMIT_KEEP_OUTSIDE, cdkk.AT_LIMIT_Y_BOUNCE_Y))

# --------------------------------------------------


class Sprite_Bat(cdkk.Sprite):
    def __init__(self, limits):
        super().__init__("Bat")
        self.load_image_from_file("bat.png")
        self.rect.centerx = limits.width / 2
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
                x, y = e.info["pos"]
                self._bat.rect.move_to(x, None)
                dealt_with = True
        return dealt_with

# --------------------------------------------------


class Manager_Scoreboard(cdkk.SpriteManager):
    def __init__(self, limits, game_time):
        super().__init__("Scoreboard Manager")
        self._game_time = game_time

        text_style = {"fillcolour": None, "outlinecolour": None,
                      "align_horiz": "L", "width": 200, "height": 35}

        tb_score = cdkk.Sprite_TextBox("Score", style=text_style)
        tb_score.set_text_format("Score: {0}", 0)
        tb_score.rect.midleft = (limits.width * 0.1, limits.height * 0.05)
        self.add(tb_score)
        self.score = 0

        self._timer = cdkk.Timer(self._game_time, cdkk.EVENT_GAME_TIMER_1)
        tb_time_left = cdkk.Sprite_TextBox("Time Left", style=text_style)
        tb_time_left.set_text_format("Time Left: {0:0.1f}", 0)
        tb_time_left.rect.center = (limits.width * 0.45, limits.height * 0.05)
        self.add(tb_time_left)

        tb_balls_left = cdkk.Sprite_TextBox("Balls Left", style=text_style)
        tb_balls_left.set_text_format("Balls Left: {0}", 0)
        tb_balls_left.rect.midright = (
            limits.width * 0.85, limits.height * 0.05)
        self.add(tb_balls_left)
        self.balls_left = 0

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, new_score):
        self._score = new_score
        self.sprite("Score").set_text(self.score)

    @property
    def balls_left(self):
        return self._balls_left

    @balls_left.setter
    def balls_left(self, new_balls_left):
        self._balls_left = new_balls_left
        self.sprite("Balls Left").set_text(self.balls_left)

    def update(self):
        super().update()
        self.sprite("Time Left").set_text(self._timer.time_left)

# --------------------------------------------------


class MyGame(cdkk.PyGameApp):
    def init(self):
        super().init()
        self._ball_mgr = Manager_Ball(self.boundary, 10, 3)
        self.add_sprite_mgr(self._ball_mgr)
        self._bat_mgr = Manager_Bat(self.boundary)
        self.add_sprite_mgr(self._bat_mgr)
        self._scoreboard_mgr = Manager_Scoreboard(self.boundary, 15)
        self.add_sprite_mgr(self._scoreboard_mgr)

        key_map = {
            pygame.K_q: "Quit",
            pygame.K_s: "StartGame"
        }
        self.event_mgr.event_map(key_event_map=key_map)

    def update(self):
        super().update()
        bat = self.sprite("Bat Manager", "Bat")
        self._ball_mgr.check_bat_hits(bat)
        self._scoreboard_mgr.balls_left = self._ball_mgr.balls_left


app_config = {
    "width": 1200,
    "height": 920,
    "background_fill": "burlywood",
    "caption": "Bouncing Ball",
    "image_path": "BouncingBall\\Images\\",
    "auto_start": False,
}

MyGame(app_config).execute()
