import sys
sys.path.append("../pygame-cdkk")
import random
from cdkkPyGameApp import *

### --------------------------------------------------

class Sprite_Bat (Sprite):
    def __init__(self, value, limits, filename):
        super().__init__(str(value))
        self.load_image(filename)
        self.rect.centerx = limits.width/2
        self.rect.top = limits.height * 0.9
        self.load_image("Images\\bat000.png")
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

class BouncingBallApp(PyGameApp):
    def init(self):
        size = (1200, 800)
        super().init(size)
        pygame.display.set_caption("Bouncing Ball")
        self.background_fill = "burlywood"
        self.add_sprite_mgr(Manager_Bat("Images\\bat128x10.png", self.boundary))
        self.event_mgr.keyboard_event(pygame.K_q, "Quit")

### --------------------------------------------------

theApp = BouncingBallApp()
theApp.execute()
