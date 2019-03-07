import sys
sys.path.append("../pygame-cdkk")
from PyGameApp import *

### --------------------------------------------------

class Sprite_Ball(Sprite):
    def __init__(self, limits):
        super().__init__()
        self.load_image("Images\\ball_red.png")
        self.rect.set_velocity(10, 10)
        self.rect.bounce_cor = self.rect.perfect_bounce
        self.rect.add_limit(Physics_Limit(limits, LIMIT_KEEP_INSIDE, AT_LIMIT_BOUNCE))
        self.rect.go()
    
    def update(self):
        self.rect.move_physics()

### --------------------------------------------------

class Manager_Ball(SpriteManager):
    def __init__(self, limits, name = "Ball Manager"):
        super().__init__(name)
        ball = Sprite_Ball(limits)
        self.add(ball)

### --------------------------------------------------

class BouncingBallApp(PyGameApp):
    def init(self):
        size = (1200, 800)
        super().init(size)
        pygame.display.set_caption("Bouncing Ball")
        self.background_fill = "burlywood"
        self.add_sprite_mgr(Manager_Ball(self.boundary))
        self.event_mgr.keyboard_event(pygame.K_q, "Quit")

### --------------------------------------------------

theApp = BouncingBallApp()
theApp.execute()
