"""Represents an employees shift at work."""

from datetime import datetime

class Shift:
    """An employees shift at work."""
    def __init__(self, start: datetime, end: datetime):
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.start} - {self.end}"


