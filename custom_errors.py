class UnauthorizedUserError(Exception):
    def __init__(self):
        self.message = 'Unauthorized user'
        super().__init__(self.message)


class LinkButtonNotPressedError(Exception):
    def __init__(self):
        self.message = 'Link button not pressed'
        super().__init__(self.message)


class DeviceIsOffError(Exception):
    def __init__(self):
        self.message = 'Device is set to off'
        super().__init__(self.message)


class GenericHueError(Exception):
    def __init__(self, error_details):
        self.message = 'Error ' + str(error_details['type']) + ': ' + str(error_details['description'])
        super().__init__(self.message)