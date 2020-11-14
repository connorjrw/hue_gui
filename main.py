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
        self.Styling = Styling('yellow')
        self.bri_value = 0
        self.styles = self.Styling.get_styles('yellow')
        self.connection_handler = ConnectionHandler(self)

        # Color Buttons
        self.color_btns = [
            ColorBtn('red', '#ff0000', [380, 280], self), ColorBtn('blue', '#0000ff', [275, 70], self),
            ColorBtn('orange', '#ff7700', [170, 175], self), ColorBtn('green', '#00ff00', [275, 280], self),
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
        """Setting color of gui elements based on HUE status"""
        self.light = light
        self.color_update()
        self.bri_update()
        if not self.light.get_status()['on']: # Need to get color as well
            for btn in self.color_btns:
                btn.off()

    def bri_update(self):
        """Set Brightness based on hue"""
        bri_status = self.light.get_status()['bri']
        bri_value = round(bri_status / 256 * 100)
        self.bri_slider.setValue(bri_value)
        self.bri_value = bri_value

    def bri_update_after_on(self):  # work around bug with hue
        self.bri_slider.setValue(self.bri_value)
        self.bri_slider.change_bri(self.bri_value)

    def disabled(self):
        for btn in self.color_btns:
            btn.off()

    def color_update(self):
        current_color = self.light.get_color()
        self.styles = self.Styling.get_styles('#' + current_color)
        self.setStyleSheet(self.styles)

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
                self.color_update()
                self.bri_update_after_on()  # Set brightness to what it was before, cannot trust was api says
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


