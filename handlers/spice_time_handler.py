import logging
import spiceypy as spice
from .time_handler_base import TimeHandlerBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpiceTimeHandler(TimeHandlerBase):
    """Time handler using SPICE."""

    def __init__(self, epoch_str):
        super().__init__(epoch_str)
        self._load_spice_kernels()
        self.boundary_et = spice.utc2et("1972-01-01T00:00:00")

    @staticmethod
    def _load_spice_kernels():
        """Load SPICE kernels required for time conversion."""
        try:
            spice.furnsh("naif0012.tls")
            logger.info("SPICE kernels loaded successfully.")
        except FileNotFoundError as e:
            logger.error(f"SPICE kernel file not found: {e}")
        except Exception as e:
            logger.error(f"Error loading SPICE kernels: {e}")

    def utc2et(self, utc_str):
        et = spice.utc2et(utc_str)
        if et < self.boundary_et:
            et -= 9.0
        return et

    def total_seconds(self, utc):
        """Calculate the total seconds between the epoch and a given UTC time."""
        try:
            epoch_et = self.utc2et(self.epoch_str)
            utc_et = self.utc2et(utc)
            return utc_et - epoch_et
        except Exception as e:
            logger.error(f"Error in time conversion with SPICE: {e}")
            return None
