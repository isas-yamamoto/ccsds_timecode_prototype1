from abc import ABC, abstractmethod


class TimeHandlerBase(ABC):
    """Abstract base class for time handling."""

    def __init__(self, epoch_str):
        self.epoch_str = epoch_str

    @abstractmethod
    def total_seconds(self, utc):
        """Calculate the total seconds between the epoch and a given UTC time."""
        pass
