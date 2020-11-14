from PyQt5.QtCore import Qt, QRunnable, QThreadPool
from PyQt5.QtWidgets import QSlider
from hue import *


class BrightnessSlider(QSlider):
    def __init__(self, geo, value, object_name, parent):
        super().__init__(Qt.Horizontal, parent)
        self.parent = parent
        self.old_val = value
        self.light = parent.light
        self.connection_handler = parent.connection_handler
        self.setObjectName(object_name)
        self.setGeometry(geo[0], geo[1], geo[2], geo[3])
        self.setValue(value)
        self.valueChanged[int].connect(self.change_bri)

    def change_bri(self, value):
        try:
            new_val = value / 100
            new_val = new_val * 256
            self.parent.bri_value = value # Store value once changed
            self.light.brightness(round(new_val))
            self.old_val = new_val
        except UnauthorizedUserError:
            self.connection_handler.update_status('Not Connected! Press Link Button')
        except GenericHueError:
            pass # Temp


class SpeedSlider(QSlider):
    def __init__(self, geo, object_name, value, max, parent):
        super().__init__(Qt.Vertical, parent)
        self.speed = 50
        self.light = parent.light
        self.strobe_worker = StrobeWorker(self.light, 50)
        self.thread_pool = QThreadPool()
        self.setObjectName(object_name)
        self.setGeometry(geo[0], geo[1], geo[2], geo[3])
        self.setValue(value)
        self.setMaximum(max)
        self.valueChanged[int].connect(self.strobe)

    def strobe(self, value):
        value = 50 - value
        if self.speed == 50 and value < 50:
            self.strobe_worker = StrobeWorker(self.light, value)
            self.thread_pool.start(self.strobe_worker)
        self.speed = value
        self.strobe_worker.change_speed(value)


class StrobeWorker(QRunnable):
    # run strobe as a thread
    def __init__(self, light, speed):
        super(StrobeWorker, self).__init__()
        self.light = light
        self.speed = speed

    def run(self):
        try:
            # Clean this up, should be able to get colours from color_btns list
            colors = ['#ff0000', '#0000ff', '#ff7700', '#00ff00', '#ff00ff', '#7700ff', '#7700ff', '#00ffff', '#ffff00']
            self.light.strobe_start(colors, self.speed, False)
        except UnauthorizedUserError:
            print('Unauthorized')

    def change_speed(self, speed):
        self.speed = speed * 0.09
        self.light.strobe_speed(self.speed)
