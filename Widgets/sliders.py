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
            self.light.brightness(round(new_val))
            self.parent.bri_value = value # Store value once changed
            self.old_val = new_val
        except UnauthorizedUserError:
            self.connection_handler.update_status('Not Connected! Press Link Button', True)
            self.setValue(0) # Disable slider from being moved if error
        except GenericHueError as e:
            self.setValue(0)
            self.connection_handler.update_status(str(e), True)
        except DeviceIsOffError:  # Act as disabled by setting value to what it was previously
            self.setValue(0)


class SpeedSlider(QSlider):
    def __init__(self, geo, object_name, value, max, parent):
        super().__init__(Qt.Vertical, parent)
        self.speed = 50
        self.light = parent.light
        self.strobe_worker = StrobeWorker(self.light, 50, self)
        self.thread_pool = QThreadPool()
        self.setObjectName(object_name)
        self.setGeometry(geo[0], geo[1], geo[2], geo[3])
        self.setValue(value)
        self.setMaximum(max)
        self.valueChanged[int].connect(self.strobe)

    def strobe(self, value):
        try:
            value = 50 - value
            if self.speed == 50 and value < 50:
                self.strobe_worker = StrobeWorker(self.light, value, self)
                self.thread_pool.start(self.strobe_worker)
            self.speed = value
            self.strobe_worker.change_speed(value)
        except (GenericHueError, UnauthorizedUserError) as e:
            self.connection_handler.update_status(str(e), True)
        except DeviceIsOffError: # Don't care if device is off, just don't take any action
            pass


class StrobeWorker(QRunnable):
    # run strobe as a thread
    def __init__(self, light, speed, parent):
        super(StrobeWorker, self).__init__()
        self.light = light
        self.speed = speed
        self.parent = parent

    def run(self):
        try:
            # Clean this up, should be able to get colours from color_btns list
            colors = ['#ff0000', '#0000ff', '#ff7700', '#00ff00', '#ff00ff', '#7700ff', '#7700ff', '#00ffff', '#ffff00']
            self.light.strobe_start(colors, self.speed, False)
        except UnauthorizedUserError:
            print('Unauthorized')
        except DeviceIsOffError:
            pass

    def change_speed(self, speed):
        if self.light.get_status()['on']:
            self.speed = speed * 0.09
            self.light.strobe_speed(self.speed)
        else:
            self.parent.setValue(0)
