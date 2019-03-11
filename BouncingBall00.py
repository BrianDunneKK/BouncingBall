import sys
sys.path.append("../pygame-cdkk")
from cdkkPyGameApp import *

### --------------------------------------------------

class BouncingBallApp(PyGameApp):
    def init(self):
        size = (1200, 800)
        super().init(size)
        pygame.display.set_caption("Bouncing Ball")
        self.background_fill = "burlywood"
        self.event_mgr.keyboard_event(pygame.K_q, "Quit")

### --------------------------------------------------

theApp = BouncingBallApp()
theApp.execute()
