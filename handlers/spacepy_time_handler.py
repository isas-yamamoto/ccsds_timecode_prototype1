import logging
import spacepy.time as spt
from .time_handler_base import TimeHandlerBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpacepyTimeHandler(TimeHandlerBase):
    """Time handler using SpacePy."""

    def total_seconds(self, utc):
        """Calculate the total seconds between the epoch and a given UTC time."""
        try:
            epoch_dt = spt.Ticktock(self.epoch_str, 'ISO').TAI[0]
            utc_dt = spt.Ticktock(utc, 'ISO').TAI[0]
            return utc_dt - epoch_dt
        except Exception as e:
            logger.error(f"Error in time conversion with SpacePy: {e}")
            return None
