class TimeCodeIdentificationException(Exception):
    def __init__(self, message):
        self.message = message


class EpochException(Exception):
    def __init__(self, message):
        self.message = message
