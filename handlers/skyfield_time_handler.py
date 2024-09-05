import logging
from skyfield.api import load, utc
from .time_handler_base import TimeHandlerBase
from datetime import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SkyfieldTimeHandler(TimeHandlerBase):
    """Time handler using Skyfield."""

    def __init__(self, epoch_str):
        super().__init__(epoch_str)
        try:
            self.ts = load.timescale()
            logger.info("Skyfield timescale loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading Skyfield timescale: {e}")

    def utc2time(self, utc_str):
        dt = datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%S%z")
        return self.ts.from_datetime(dt.replace(tzinfo=utc))

    def total_seconds(self, utc_str):
        """Calculate the total seconds between the epoch and a given UTC time."""
        try:
            epoch_time = self.utc2time(self.epoch_str)
            utc_time = self.utc2time(utc_str)
            total_seconds = (utc_time - epoch_time) * 86400
            # total_seconds += 10  # Skyfield BUG?
            return total_seconds
        except Exception as e:
            logger.error(f"Error in time conversion with SkyField: {e}")
            return None
