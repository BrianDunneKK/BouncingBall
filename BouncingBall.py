# To Do: Scoreboard items cropped. Game Over off centre

import random
import sys
sys.path.append("../pygame-cdkk")
from cdkkPyGameApp import *

### --------------------------------------------------

EVENT_BOUNCE = EVENT_NEXT_USER_EVENT
EVENT_SCORE = EVENT_NEXT_USER_EVENT + 1

class Sprite_Ball(Sprite):
    files = ["ball_red.png", "ball_yellow.png", "ball_green.png", "ball_brown.png", "ball_blue.png", "ball_pink.png", "ball_black.png"]

    def __init__(self, value, limits):
        super().__init__(str(value))        
        self.value = value
        self.load_image("Images\\"+self.files[value-1])
        self.rect.left = random.randint(limits.width * 0.2, limits.width * 0.8)
        self.rect.set_speed_angle(value * 3 + 5, random.randint(45, 135))
        self.rect.bounce_cor = self.rect.perfect_bounce
        bounce_event = EventManager.create_event(EVENT_BOUNCE, "Boundary")
        bounce_event.uuid = self.uuid
        self.rect.add_limit(Physics_Limit(limits, LIMIT_KEEP_INSIDE, AT_LIMIT_BOUNCE, bounce_event))
        self.rect.go()
    
    def update(self):
        self.rect.move_physics()
    
### --------------------------------------------------

class Manager_Ball(SpriteManager):
    def __init__(self, at_a_time, total, limits, name = "Ball Manager"):
        super().__init__(name)
        self._at_a_time = at_a_time
        self._total = total
        self._balls_remaining = total
        self._limits = limits
        self.add_balls()

    def add_balls(self):
        while (len(self.sprites()) < self._at_a_time and self._balls_remaining > 0):
            value = random.randint(1,len(Sprite_Ball.files))
            ball = Sprite_Ball(value, self._limits)
            self.add(ball)
            self._balls_remaining -= 1

    def update(self):
        super().update()
        sprite_collisions = self.find_collisions()
        for sprite, rect in sprite_collisions:
            sprite.rect.dynamic_limit(Physics_Limit(rect, LIMIT_COLLISION, AT_LIMIT_BOUNCE))

    def check_bat_hits(self, bat):
        hit_score = 0 
        for ball in self.sprites():
            bounce_event = EventManager.create_event(EVENT_SCORE, "Bat")
            bounce_event.score = ball.value
            ball.rect.dynamic_limit(Physics_Limit(bat.rect, LIMIT_KEEP_OUTSIDE, AT_LIMIT_Y_BOUNCE_Y, bounce_event))
        return hit_score

    @property
    def balls_remaining(self):
        return self._balls_remaining
    
    def event(self, e):
        if e.type == EVENT_BOUNCE:
            if e.action == "Boundary":
                if e.at_limit_y & AT_LIMIT_BOTTOM:
                    self.kill_uuid(e.uuid)
                    self.add_balls()
        elif e.type == EVENT_GAME_CONTROL:
            if e.action == "GameOver":
                self._balls_remaining = 0
                self.empty()
            elif e.action == "StartGame":
                self._balls_remaining = self._total
                self.add_balls()
        return False

### --------------------------------------------------

class Sprite_Bat (Sprite_Animation):
    def __init__(self, value, limits, filename):
        super().__init__(str(value))
        self.load_image(filename)
        self.rect.centerx = limits.width/2
        self.rect.top = limits.height * 0.9
        self.load_animation("Anim Bat", "Images\\bat{0:03d}.png", 7)
        self.set_animation("Anim Bat", ANIMATE_SHUTTLE)
        self.rect.add_limit(Physics_Limit(limits, LIMIT_KEEP_INSIDE, AT_LIMIT_X_HOLD_POS_X))
        self.rect.go()

### --------------------------------------------------

class Manager_Bat(SpriteManager):
    def __init__(self, filename, limits, name = "Bat Manager"):
        super().__init__(name)
        self.add(Sprite_Bat("Bat", limits, filename))

    def event(self, e):
        dealt_with = False
        if e.type == EVENT_GAME_CONTROL:
            if e.action == "MouseMotion":
                x, y = e.info['pos']
                y = self.sprite("Bat").rect.centery
                self.sprite("Bat").rect.centerx = x
                self.sprite("Bat").rect.apply_limits()
                dealt_with = True
        return dealt_with

### --------------------------------------------------

class Manager_Scoreboard(SpriteManager):
    def __init__(self, game_time, limits, name = "Scoreboard Manager"):
        super().__init__(name)
        self._score = 0
        self._game_time = game_time

        self.add(Sprite_TextBox("Score"))
        self.sprite("Score").setup_text(36, "black", "Score: {0}")
        self.score = 0
        self.sprite("Score").rect.midleft = (limits.width * 0.05, limits.height * 0.05)

        self._timer = Timer(self._game_time, EVENT_GAME_TIMER_1)
        self.add(Sprite_TextBox("Time Left"))
        self.sprite("Time Left").setup_text(36, "black", "Time Left: {0:0.1f}")
        self.sprite("Time Left").set_text(0)
        self.sprite("Time Left").rect.center = (limits.width * 0.45, limits.height * 0.05)

        self.add(Sprite_TextBox("Balls Left"))
        self.sprite("Balls Left").setup_text(36, "black", "Balls Left: {0}")
        self.sprite("Balls Left").set_text(0)
        self.sprite("Balls Left").rect.midright = (limits.width * 0.85, limits.height * 0.05)

        self._game_over = Sprite_TextBox("Game Over")
        self._game_over.setup_text(72, "red3")
        self._game_over.text = "Game Over"
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
        elif e.type == EVENT_GAME_CONTROL:
            if e.action == "GameOver":
                self.add(self._game_over) # Display Game Over
            elif e.action == "StartGame":
                self.score = 0
                self._timer.start()
                self.remove(self._game_over) # Hide Game Over
        return False


### --------------------------------------------------

class BouncingBallApp(PyGameApp):
    def init(self):
        size = (1200, 800)
        super().init(size)
        pygame.display.set_caption("Bouncing Ball")
        self.background_fill = "burlywood"
        self.add_sprite_mgr(Manager_Ball(3, 10, self.boundary))
        self.add_sprite_mgr(Manager_Bat("Images\\bat128x10.png", self.boundary))
        self.add_sprite_mgr(Manager_Scoreboard(15, self.boundary))
        self.event_mgr.keyboard_event(pygame.K_q, "Quit")
        self.event_mgr.keyboard_event(pygame.K_r, "StartGame")
        self.event_mgr.user_event(EVENT_GAME_TIMER_1, "GameOver")

    def update(self):
        super().update()
        self.sprite_mgr("Ball Manager").check_bat_hits(self.sprite("Bat Manager", "Bat"))
        self.sprite_mgr("Scoreboard Manager").sprite("Balls Left").set_text(self.sprite_mgr("Ball Manager").balls_remaining)

### --------------------------------------------------

theApp = BouncingBallApp()
theApp.execute()
