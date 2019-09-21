# This is a minimal game - it's just a black screen.
# The code first defines a blank class called MyGame.
# It then creates an object of this class and executes it.

import cdkk


class MyGame(cdkk.PyGameApp):
    pass


MyGame().execute()
