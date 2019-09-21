import cdkk
import pygame

### --------------------------------------------------

class MyGame(cdkk.PyGameApp):
    pass

### --------------------------------------------------

app_config = {
    "width":1200, "height":920,
    "background_fill":"burlywood",
    "caption":"Bouncing Ball",
    "auto_start":True
    }

theGame = MyGame()
theGame.execute()
