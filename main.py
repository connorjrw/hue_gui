import sys

from PyQt5.QtWidgets import *

from Widgets.color_btns import ColorBtn
from Widgets.connection_handler import ConnectionHandler
from Widgets.sliders import *
from hue import *
from styling import *


class Window(QMainWindow):
    def __init__(self, bridge):
        super().__init__()
        self.setWindowTitle("Disco Phillip"), self.setGeometry(100, 100, 650, 350)
        self.color_btns = []
        self.bridge = bridge
        self.light = Light(self.bridge, 1)
        self.connection_handler = ConnectionHandler(self)
        self.Styling = Styling('yellow')
        self.styles = self.Styling.get_styles('yellow')

        # Color Buttons
        self.color_btns = [
            ColorBtn('red', '#ff0000', [380, 280], self), ColorBtn('blue', '#0000ff', [275, 70], self),
            ColorBtn('green', '#ff7700', [170, 175], self), ColorBtn('orange', '#00ff00', [275, 280], self),
            ColorBtn('pink', '#ff00ff', [380, 175], self), ColorBtn('purple', '#7700ff', [380, 70], self),
            ColorBtn('purple', '#7700ff', [380, 70], self), ColorBtn('lightblue', '#00ffff', [170, 70], self),
            ColorBtn('yellow', '#ffff00', [170, 280], self)
        ]

        # White on/off button, in the middle of colored button
        self.on_off_button = QPushButton("", self)
        self.on_off_button.setStyleSheet("background-color : white; color : white; border:black")
        self.on_off_button.clicked.connect(self.on_off)
        self.on_off_button.setGeometry(275, 175, 100, 100)

        # Brightness Slider(Horizontal), Speed slider (Vertical)
        self.bri_slider = BrightnessSlider([170, 40, 310, 20], 100, "brightness_slider", self)
        self.speed_slider = SpeedSlider([135, 75, 20, 300], "speed_slider", 0, 50, self)

        # Stylesheet for sliders
        self.setStyleSheet(self.styles)

        # Attempt Connection to bridge
        self.connection_handler.connect_bridge('Disconnected. Click to connect')

        # Show gui
        self.update()
        self.show()

    def set_light(self, light):
        """Setting color of lights in GUI based on HUE status"""
        self.light = light
        if not self.light.get_status()['on']: # Need to get color as well
            for btn in self.color_btns:
                btn.off()

    def disabled(self):
        for btn in self.color_btns:
            btn.off()

    def on_off(self):
        """Turn light on/off"""
        try:
            light_on = self.light.get_status()['on']
            if light_on:
                for btn in self.color_btns:
                    btn.off()
                self.light.off()
            else:
                for btn in self.color_btns:
                    btn.on()
                self.light.on()
        except GenericHueError as e:
            self.connection_handler.update_status(str(e))
            self.connection_handler.set_color(Qt.red)
        except (TypeError, KeyError, UnauthorizedUserError):
            self.connection_handler.set_color(Qt.red)
            self.connection_handler.update_status('Not Connected')


main_bridge = Bridge()
App = QApplication(sys.argv)
window = Window(main_bridge)
sys.exit(App.exec())


