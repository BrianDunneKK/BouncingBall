import random
import pygame
import cdkk
import sys
sys.path.append("pygame-cdkk")


# import random
# import sys
# sys.path.append("../pygame-cdkk")
# from cdkkPyGameApp import *
# from cdkkSpriteExtra import *

# --------------------------------------------------

EVENT_BOUNCE = cdkk.EVENT_NEXT_USER_EVENT
EVENT_SCORE = cdkk.EVENT_NEXT_USER_EVENT + 1


class Sprite_Ball(cdkk.Sprite):
    files = ["ball_red.png", "ball_yellow.png", "ball_green.png",
             "ball_brown.png", "ball_blue.png", "ball_pink.png", "ball_black.png"]

    def __init__(self, value, limits):
        super().__init__(str(value))
        self.value = value
        self.load_image_from_file("Images\\"+self.files[value-1])
        self.rect.left = random.randint(limits.width * 0.2, limits.width * 0.8)
        self.rect.set_speed_angle(value * 3 + 5, random.randint(45, 135))
        self.rect.bounce_cor = self.rect.perfect_bounce
        bounce_event = cdkk.EventManager.create_event(EVENT_BOUNCE, "Boundary")
        bounce_event.uuid = self.uuid
        self.rect.add_limit(cdkk.Physics_Limit(
            limits, cdkk.LIMIT_KEEP_INSIDE, cdkk.AT_LIMIT_BOUNCE, bounce_event))
        self.rect.go()

    def update(self):
        self.rect.move_physics()

# --------------------------------------------------


class Manager_Ball(cdkk.SpriteManager):
    def __init__(self, at_a_time, total, limits, name="Ball Manager"):
        super().__init__(name)
        self._at_a_time = at_a_time
        self._total = total
        self._balls_remaining = total
        self._limits = limits
        self.add_balls()

    def add_balls(self):
        while (len(self.sprites()) < self._at_a_time and self._balls_remaining > 0):
            value = random.randint(1, len(Sprite_Ball.files))
            ball = Sprite_Ball(value, self._limits)
            self.add(ball)
            self._balls_remaining -= 1

    def update(self):
        super().update()
        sprite_collisions = self.find_collisions()
        for sprite, rect in sprite_collisions:
            sprite.rect.dynamic_limit(cdkk.Physics_Limit(
                rect, cdkk.LIMIT_COLLISION, cdkk.AT_LIMIT_BOUNCE))

    def check_bat_hits(self, bat):
        hit_score = 0
        for ball in self.sprites():
            bounce_event = cdkk.EventManager.create_event(EVENT_SCORE, "Bat")
            bounce_event.score = ball.value
            ball.rect.dynamic_limit(cdkk.Physics_Limit(
                bat.rect, cdkk.LIMIT_KEEP_OUTSIDE, cdkk.AT_LIMIT_Y_BOUNCE_Y, bounce_event))
        return hit_score

    @property
    def balls_remaining(self):
        return self._balls_remaining

    def event(self, e):
        if e.type == EVENT_BOUNCE:
            if e.action == "Boundary":
                if e.at_limit_y & cdkk.AT_LIMIT_BOTTOM:
                    self.kill_uuid(e.uuid)
                    self.add_balls()
        elif e.type == cdkk.EVENT_GAME_CONTROL:
            if e.action == "GameOver":
                self._balls_remaining = 0
                self.empty()
            elif e.action == "StartGame":
                self._balls_remaining = self._total
                self.add_balls()
        return False

# --------------------------------------------------


class Sprite_Bat (cdkk.Sprite_Animation):
    def __init__(self, value, limits):
        super().__init__(str(value))
        self.load_animation("Anim Bat", "Images\\bat{0:03d}.png", 7)
        self.set_animation("Anim Bat", cdkk.ANIMATE_SHUTTLE)
        self.rect.centerx = limits.width/2
        self.rect.top = limits.height * 0.9
        self.rect.add_limit(cdkk.Physics_Limit(
            limits, cdkk.LIMIT_KEEP_INSIDE, cdkk.AT_LIMIT_X_HOLD_POS_X))
        self.rect.go()

# --------------------------------------------------


class Manager_Bat(cdkk.SpriteManager):
    def __init__(self, limits, name="Bat Manager"):
        super().__init__(name)
        self.add(Sprite_Bat("Bat", limits))

    def event(self, e):
        dealt_with = False
        if e.type == cdkk.EVENT_GAME_CONTROL:
            if e.action == "MouseMotion":
                x, y = e.info['pos']
                y = self.sprite("Bat").rect.centery
                self.sprite("Bat").rect.centerx = x
                self.sprite("Bat").rect.apply_limits()
                dealt_with = True
        return dealt_with

# --------------------------------------------------


class Manager_Scoreboard(cdkk.SpriteManager):
    def __init__(self, game_time, limits, name="Scoreboard Manager"):
        super().__init__(name)
        self._game_time = game_time

        text_style = {"fillcolour": None, "outlinecolour": None,
                      "align_horiz": "L", "width": 200, "height": 35}

        self._score = cdkk.Sprite_TextBox("Score", style=text_style)
        self._score.set_text_format("Score: {0}", 0)
        self._score.rect.midleft = (limits.width * 0.1, limits.height * 0.05)
        self.add(self._score)
        self.score = 0

        self._timer = cdkk.Timer(self._game_time, cdkk.EVENT_GAME_TIMER_1)
        self._time_left = cdkk.Sprite_TextBox("Time Left", style=text_style)
        self._time_left.set_text_format("Time Left: {0:0.1f}", 0)
        self._time_left.rect.center = (
            limits.width * 0.45, limits.height * 0.05)
        self.add(self._time_left)

        self._balls_left = cdkk.Sprite_TextBox("Balls Left", style=text_style)
        self._balls_left.set_text_format("Balls Left: {0}", 0)
        self._balls_left.rect.midright = (
            limits.width * 0.85, limits.height * 0.05)
        self.add(self._balls_left)

        self._game_over = cdkk.Sprite_GameOver(limits)
        self._game_over.rect.center = (limits.width * 0.5, limits.height * 0.5)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, new_score):
        self._score = new_score
        self.sprite("Score").set_text(self.score)

    def update(self):
        super().update()
        self.sprite("Time Left").set_text(self._timer.time_left)

    def event(self, e):
        if e.type == EVENT_SCORE:
            self.score = self.score + e.score
        elif e.type == cdkk.EVENT_GAME_CONTROL:
            if e.action == "GameOver":
                self.add(self._game_over)  # Display Game Over
            elif e.action == "StartGame":
                self.score = 0
                self._timer.start()
                self.remove(self._game_over)  # Hide Game Over
        return False

# --------------------------------------------------


class BouncingBallApp(cdkk.PyGameApp):
    def init(self):
        size = (1200, 800)
        super().init(size)
        pygame.display.set_caption("Bouncing Ball")
        self.background_fill = "burlywood"
        self.add_sprite_mgr(Manager_Ball(3, 10, self.boundary))
        self.add_sprite_mgr(Manager_Bat(self.boundary))
        self.add_sprite_mgr(Manager_Scoreboard(15, self.boundary))
        self.event_mgr.keyboard_event(pygame.K_q, "Quit")
        self.event_mgr.keyboard_event(pygame.K_r, "StartGame")
        self.event_mgr.user_event(cdkk.EVENT_GAME_TIMER_1, "GameOver")

    def update(self):
        super().update()
        self.sprite_mgr("Ball Manager").check_bat_hits(
            self.sprite("Bat Manager", "Bat"))
        self.sprite_mgr("Scoreboard Manager").sprite("Balls Left").set_text(
            self.sprite_mgr("Ball Manager").balls_remaining)

# --------------------------------------------------


theApp = BouncingBallApp()
theApp.execute()
