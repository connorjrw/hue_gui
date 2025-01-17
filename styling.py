class Styling:
    def __init__(self, color):
        self.color = color

    def get_styles(self, s_color):
        s = '''
        QSlider#brightness_slider::groove:horizontal {{
            border: 1px solid #bbb;
            background: white;
            height: 20px;
            border-radius: 4px;
        }}

        QSlider#brightness_slider::sub-page:horizontal {{
            background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
            stop: 0 {0}, stop: 1 {0});
            background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
            stop: 0 {0}, stop: 1 {0});
            border: 1px solid #777;
            height: 10px;
            border-radius: 4px;
        }}

        QSlider#brightness_slider::add-page:horizontal {{
            background: #fff;
            border: 1px solid #777;
            height: 10px;
            border-radius: 4px;
        }}

        QSlider#brightness_slider::handle:horizontal {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #eee, stop:1 #ccc);
            border: 1px solid #777;
            width: 13px;
            margin-top: -2px;
            margin-bottom: -2px;
            border-radius: 4px;
        }}

        QSlider#brightness_slider::handle:horizontal:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #fff, stop:1 #ddd);
            border: 1px solid #444;
            border-radius: 4px;
        }}

        QSlider#brightness_slider::sub-page:horizontal:disabled {{
            background: #bbb;
            border-color: #999;
        }}

        QSlider#brightness_slider::add-page:horizontal:disabled {{
            background: #eee;
            border-color: #999;
        }}

        QSlider#brightness_slider::handle:horizontal:disabled {{
            background: #eee;
            border: 1px solid #aaa;
            border-radius: 4px;
        }}

        QSlider#speed_slider::groove:vertical {{
            border: 1px solid #bbb;
            background: white;
            width: 20px;
            border-radius: 4px;
        }}

        QSlider#speed_slider::sub-page:vertical {{
            background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
            stop: 0 white, stop: 1 white);
            background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
            stop: 0 white, stop: 1 white);
            border: 1px solid #777;
            width: 10px;
            border-radius: 4px;
        }}

        QSlider#speed_slider::add-page:vertical {{
            background: {0};
            border: 1px solid #777;
            width: 10px;
            border-radius: 4px;
        }}

        QSlider#speed_slider::handle:vertical {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #eee, stop:1 #ccc);
            border: 1px solid #777;
            height: 13px;
            margin-top: -2px;
            margin-bottom: -2px;
            border-radius: 4px;
        }}

        QSlider#speed_slider::handle:vertical:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 {0}, stop:1 #ddd);
            border: 1px solid #444;
            border-radius: 4px;
        }}

        QSlider#speed_slider::sub-page:vertical:disabled {{
            background: #bbb;
            border-color: #999;
        }}

        QSlider#speed_slider::add-page:vertical:disabled {{
            background: #eee;
            border-color: #999;
        }}

        QSlider#speed_slider::handle:vertical:disabled {{
            background: #eee;
            border: 1px solid #aaa;
            border-radius: 4px;
        }}'''.format(s_color)
        return s
