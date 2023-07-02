import pystray
from pathlib import Path
from PIL import Image, ImageDraw

class Icon():
    def __init__(self, hide_callback, show_callback):
        self.name = 'Monero Subscription Wallet'
        self.width = 64
        self.height = 64
        self.color1 = 'black'
        self.color2 = 'white'
        self._menu = None
        self.hide_callback = hide_callback
        self.show_callback = show_callback
        self._icon = self.create()

    def image(self):
        # Generate an image and draw a pattern
        image = Image.open('icon.ico')

        return image

    def create(self):
        return pystray.Icon(self.name, icon=self.image(), menu=self.menu())

    def menu(self):
        if not self._menu:
            self._menu = pystray.Menu(
                pystray.MenuItem('Hide', self.hide_callback),
                pystray.MenuItem('Show', self.show_callback)
            )
        return self._menu

    def stop(self):
        self._icon.stop()

    def thread_run(self):
        self._icon.run()