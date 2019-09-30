import cdkk


class MyGame(cdkk.PyGameApp):
    pass


app_config = {
    "width": 1200, "height": 920,
    "background_fill": "burlywood",
    "caption": "Bouncing Ball"
}

MyGame(app_config).execute()
