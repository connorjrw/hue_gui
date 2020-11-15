from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from custom_errors import *


class ConnectionHandler:

    def __init__(self, parent, status_color=Qt.red, status_text='Disconnected'):
        self.parent = parent
        self.bridge = parent.bridge
        self.light = parent.light
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(650, 450)
        self.label.setPixmap(canvas)
        parent.setCentralWidget(self.label)
        self.painter = QtGui.QPainter(self.label.pixmap())
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing)
        self.painter.setBrush(QtGui.QBrush(status_color, Qt.SolidPattern))
        self.painter.drawEllipse(QtCore.QPoint(20, 430), 10, 10)
        self.painter.end()

        self.connection_label = ClickableLabel(self.label_onclick, status_text, self.parent)
        self.connection_label.adjustSize()
        self.connection_label.move(38, 422)

    def update_message(self, message):
        self.connection_label.setText(message)
        self.connection_label.adjustSize()

    def set_color(self, status_color):
        """
        Sets color and repaints status ellipse
        """
        self.painter = QtGui.QPainter(self.label.pixmap())
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing)
        self.painter.setBrush(QtGui.QBrush(status_color, Qt.SolidPattern))
        self.painter.drawEllipse(QtCore.QPoint(20, 430), 10, 10)
        self.painter.end()
        self.parent.update()

    def update_status(self, error_msg, is_error):
        """
        Change text on status label

        :param error_msg: Text to display
        """
        if is_error:
            self.set_color(Qt.red)
        else:
            self.set_color(Qt.green)
        self.connection_label.setText(error_msg)
        self.connection_label.adjustSize()
        self.parent.update()

    def label_onclick(self, event):
        button = event.button()
        modifiers = event.modifiers()
        if modifiers == Qt.NoModifier and button == Qt.LeftButton:
            self.connect_bridge('Link Button not Pressed!')

    def connect_bridge(self, error_message):
        """
        Attempt connection to Bridge

        :param error_message: Text to display if connection unsuccesfull

        """
        try:
            self.bridge.connect()
            self.update_status('Connected', False)
            self.parent.set_light(self.light)
        except (LinkButtonNotPressedError, UnauthorizedUserError):
            self.update_status(error_message, True)
            self.parent.disabled()
        except GenericHueError as e:
            self.update_status(str(e), True)
            self.parent.disabled()


class ClickableLabel(QtWidgets.QLabel):
    """
    Create a label that is clickable
    """
    def __init__(self, when_clicked, text, parent):
        QtWidgets.QLabel.__init__(self, parent)
        self._whenClicked = when_clicked

    def mouseReleaseEvent(self, event):
        self._whenClicked(event)