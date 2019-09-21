import random
import sys
sys.path.append("../pygame-cdkk")
from cdkkPyGameApp import *

### --------------------------------------------------

class Sprite_Ball(Sprite):
    def __init__(self, limits):
        super().__init__("")        
        self.load_image_from_file("Images\\ball_red.png")
        speed = random.randint(5, 20)
        self.rect.set_velocity(speed, speed)
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
            ball = Sprite_Ball(self._limits)
            self.add(ball)

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
