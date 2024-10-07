import logging
from astropy.time import Time
from .time_handler_base import TimeHandlerBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AstropyTimeHandler(TimeHandlerBase):
    """Time handler using Astropy."""

    def __init__(self, epoch_str):
        super().__init__(epoch_str)
        self.epoch_time = Time(self.epoch_str, scale="utc")

    def total_seconds(self, utc):
        """Calculate the total seconds between the epoch and a given UTC time."""
        try:
            utc_time = Time(utc, scale="utc")
            return (utc_time - self.epoch_time).sec
        except Exception as e:
            logger.error(f"Error in time conversion with Astropy: {e}")
            return None

    def utc_string(self, elapsed_seconds: float, precision: int = 6) -> str:
        """Convert elapsed seconds since the epoch to a UTC string in ISO format."""
        utc = self.epoch_time + elapsed_seconds / 86400
        utc.format = "isot"
        utc.precision = precision
        return str(utc)
    
    def cal_to_jd(self, year: int, month: int, day: int) -> float:
        """Convert a calendar date to Julian Day."""
        t = Time(f"{year:04d}-{month:02d}-{day:02d}")
        return t.jd
    
