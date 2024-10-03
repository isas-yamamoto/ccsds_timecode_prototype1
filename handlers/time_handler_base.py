from abc import ABC, abstractmethod


class TimeHandlerBase(ABC):
    """Abstract base class for time handling."""

    def __init__(self, epoch_str):
        self.epoch_str = epoch_str

    @abstractmethod
    def total_seconds(self, utc):
        """Calculate the total seconds between the epoch and a given UTC time."""
        pass

    @abstractmethod
    def utc_string(self, elapsed_seconds: float) -> str:
        """Convert elapsed seconds since the epoch to a UTC string in ISO format."""
        pass
