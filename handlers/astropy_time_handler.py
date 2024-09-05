import logging
from astropy.time import Time
from .time_handler_base import TimeHandlerBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AstropyTimeHandler(TimeHandlerBase):
    """Time handler using Astropy."""

    def total_seconds(self, utc):
        """Calculate the total seconds between the epoch and a given UTC time."""
        try:
            epoch_time = Time(self.epoch_str, scale="utc")
            utc_time = Time(utc, scale="utc")
            return (utc_time - epoch_time).sec
        except Exception as e:
            logger.error(f"Error in time conversion with Astropy: {e}")
            return None
