import logging
from datetime import datetime, timedelta
from skyfield.api import load, utc
from .time_handler_base import TimeHandlerBase


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SkyfieldTimeHandler(TimeHandlerBase):
    """Time handler using Skyfield."""

    def __init__(self, epoch_str):
        super().__init__(epoch_str)
        try:
            self.ts = load.timescale()
            logger.info("Skyfield timescale loaded successfully.")
            self.boundary_time = self.ts.utc(1972, 1, 1)
        except Exception as e:
            logger.error(f"Error loading Skyfield timescale: {e}")
        self.epoch_time = self._utc2time(self.epoch_str)

    def _utc2time(self, utc_str):
        if utc_str[-1] == "Z":
            utc_str = utc_str[:-1]
        dt = datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%S")
        utc_time = self.ts.from_datetime(dt.replace(tzinfo=utc))
        if utc_time < self.boundary_time:
            utc_time -= 10.0 / 86400
        return utc_time

    def total_seconds(self, utc_str):
        """Calculate the total seconds between the epoch and a given UTC time."""
        try:
            utc_time = self._utc2time(utc_str)
            total_seconds = (utc_time - self.epoch_time) * 86400
            return total_seconds
        except Exception as e:
            logger.error(f"Error in time conversion with SkyField: {e}")
            return None

    def utc_string(self, elapsed_seconds: float) -> str:
        """Convert elapsed seconds since the epoch to a UTC string in ISO format."""
        utc_time = self.epoch_time + timedelta(seconds=elapsed_seconds)
        return utc_time.utc_strftime("%Y-%m-%dT%H:%M:%S.%f")

    def cal_to_jd(self, year: int, month: int, day: int) -> float:
        """Convert a calendar date to Julian Day."""
        t = self.ts.utc(year, month, day)
        return t.tt