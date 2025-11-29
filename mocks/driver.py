"""Mock driver for E-Ink display."""


class MockEPD:
    """Mock E-Paper Display driver."""

    def __init__(self, width=800, height=480):
        self.width = width
        self.height = height

    def init(self, fast=False):
        pass

    def clear(self):
        pass

    def sleep(self):
        pass

    def display(self, image):
        pass

    def display_partial(self, image):
        pass
