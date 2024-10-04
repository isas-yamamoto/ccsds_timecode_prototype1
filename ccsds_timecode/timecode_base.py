from abc import ABC, abstractmethod
from time_handler import TimeHandler


class CCSDS_TimeCode(ABC):
    """Abstract base class for time handling."""

    def __init__(self, epoch, library="my"):
        self.time_handler = TimeHandler.create_handler(epoch, library)

    def get_total_seconds(self, utc):
        """
        Return the total seconds between the epoch and a given UTC time.

        Args:
            utc (str): The UTC time string in ISO 8601 format.

        Returns:
            float: Total seconds between the epoch and the given UTC time.
        """
        return self.time_handler.total_seconds(utc)

    def utc_string(self, elapsed_seconds: float) -> str:
        """
        Convert elapsed seconds to a formatted UTC time string.

        Args:
            elapsed_seconds (float): The elapsed time in seconds since the epoch.

        Returns:
            str: The corresponding UTC time in string format.
        """
        return self.time_handler.utc_string(elapsed_seconds)

    def get_contents(self, elapsed_seconds: float) -> dict:
        return {}

    @abstractmethod
    def get_p_field(self):
        """
        Get the P-field.

        Returns:
            int: The P-field as an integer value.
        """
        pass

    @abstractmethod
    def get_t_field(self, utc):
        """
        Get the T-field as a byte sequence from a given UTC time.

        Args:
            utc (str): The UTC time string in ISO 8601 format.

        Returns:
            bytes: A byte sequence representing the T-field.
        """
        pass

    @abstractmethod
    def unpack_time_code(self, time_code: bytes) -> tuple:
        """
        Unpacks a time code from bytes into a dictionary of fields and elapsed time.

        Args:
            time_code (bytes): The time code as a byte sequence.

        Returns:
            tuple: A tuple containing a dictionary of parsed fields and the UTC time string.

        Raises:
            OctetSizeException: If the time code length is invalid.
        """
        pass
