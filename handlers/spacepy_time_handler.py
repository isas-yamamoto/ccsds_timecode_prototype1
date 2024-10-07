import logging
import spacepy.time as spt
from datetime import timedelta
from .time_handler_base import TimeHandlerBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpacepyTimeHandler(TimeHandlerBase):
    """Time handler using SpacePy."""

    def __init__(self, epoch_str):
        super().__init__(epoch_str)
        self.epoch_dt = spt.Ticktock(self.epoch_str, 'ISO')

    def total_seconds(self, utc):
        """Calculate the total seconds between the epoch and a given UTC time."""
        try:
            utc_dt = spt.Ticktock(utc, 'ISO').TAI[0]
            return utc_dt - self.epoch_dt.TAI[0]
        except Exception as e:
            logger.error(f"Error in time conversion with SpacePy: {e}")
            return None

    def utc_string(self, elapsed_seconds: float) -> str:
        """Convert elapsed seconds since the epoch to a UTC string in ISO format."""
        dt = self.epoch_dt + timedelta(seconds=elapsed_seconds)
        return dt.UTC.strftime("%Y-%m-%dT%H:%M:%S.%f")

    def cal_to_jd(self, year: int, month: int, day: int) -> float:
        """Convert a calendar date to Julian Day."""
        t = spt.Ticktock(f"{year:04d}-{month:02d}-{day:02d}T00:00:00", "ISO")
        return t.JD