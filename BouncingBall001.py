# Add the app_config dictionary and pass it to the MyGame constructor to
# configure the screen size, background colour and title.

# The available configuration options are: caption, width, height, full_screen,
# background_fill, frame_rate, slow_update_time, scroll_time, key_repeat_time,
# auto_start, image_path

import cdkk


class MyGame(cdkk.PyGameApp):
    pass


app_config = {
    "width": 1200, "height": 920,
    "background_fill": "burlywood",
    "caption": "Bouncing Ball"
}

MyGame(app_config).execute()
