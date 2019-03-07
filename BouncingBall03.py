import sys
sys.path.append("../pygame-cdkk")
import random
from PyGameApp import *

### --------------------------------------------------

class Sprite_Ball(Sprite):
    files = ["ball_red.png", "ball_yellow.png", "ball_green.png", "ball_brown.png", "ball_blue.png", "ball_pink.png", "ball_black.png"]

    def __init__(self, value, limits):
        super().__init__(str(value))        
        self.value = value
        self.load_image("Images\\"+self.files[value-1])
        self.rect.left = random.randint(0,limits.width-self.rect.width)
        self.rect.top = random.randint(0,limits.height-self.rect.height)
        self.rect.set_speed_angle(value + 5, random.randint(45, 135))
        self.rect.bounce_cor = self.rect.perfect_bounce
        self.rect.add_limit(Physics_Limit(limits, LIMIT_KEEP_INSIDE, AT_LIMIT_BOUNCE))
        self.rect.go()

    def update(self):
        self.rect.move_physics()

### --------------------------------------------------

class Manager_Ball(SpriteManager):
    def __init__(self, total, limits, name = "Ball Manager"):
        super().__init__(name)
        self._total = total
        self._limits = limits
        self.add_balls()

    def add_balls(self):
        while (len(self.sprites()) < self._total):
            value = random.randint(1,len(Sprite_Ball.files))
            ball = Sprite_Ball(value, self._limits)
            self.add(ball)

    def update(self):
        super().update()
        sprite_collisions = self.find_collisions()
        for sprite, rect in sprite_collisions:
            sprite.rect.dynamic_limit(Physics_Limit(rect, LIMIT_COLLISION, AT_LIMIT_BOUNCE))

### --------------------------------------------------

class BouncingBallApp(PyGameApp):
    def init(self):
        size = (1200, 800)
        super().init(size)
        pygame.display.set_caption("Bouncing Ball")
        self.background_fill = "burlywood"
        self.add_sprite_mgr(Manager_Ball(13, self.boundary))
        self.event_mgr.keyboard_event(pygame.K_q, "Quit")

### --------------------------------------------------

theApp = BouncingBallApp()
theApp.execute()
