from PyQt5.QtWidgets import QPushButton

from hue import UnauthorizedUserError, GenericHueError


class ColorBtn(QPushButton):
    def __init__(self, color, hex_color, pos, parent):
        super().__init__("", parent)
        self.connection_handler = parent.connection_handler
        self.parent = parent
        self.light = parent.light
        self.color_btns = parent.color_btns
        self.color = color
        self.Styling = parent.Styling
        self.styles = parent.styles
        self.hex_color = hex_color
        self.setStyleSheet(f'background-color : {hex_color};')
        self.setGeometry(pos[0], pos[1], 100, 100)
        self.clicked.connect(lambda: self.change_color())

    def change_color(self):
        try:
            if not self.light.get_status()['on']:
                for btn in self.parent.color_btns:
                    btn.on()
                self.light.on()
            self.light.color(self.hex_color)
            self.styles = self.Styling.get_styles(self.hex_color)
            self.parent.setStyleSheet(self.styles)

        except UnauthorizedUserError:
            self.connection_handler.update_message('Not Connected')
        except GenericHueError as e:
            self.connection_handler.update_message(str(e))

    def off(self):
        self.setStyleSheet('background-color : grey;')
        self.styles = self.Styling.get_styles('grey')
        self.parent.setStyleSheet(self.styles)

    def on(self):
        self.setStyleSheet(f'background-color : {self.hex_color};')