import math
from struct import pack
from time_handler import TimeHandler
from time_exceptions import ReservedForFutureUse


class CCSDS_TimeCode_CDS:
    """Implements CCSDS Time Code Format with T-Field and P-Field."""

    def __init__(
        self,
        epoch="1958-01-01T00:00:00Z",
        time_code_id=0b100,
        epoch_id=0b0,
        length_of_day_segment=0b0,
        length_of_subms_segment=0b01,
        library="my",
    ):
        if length_of_subms_segment == 0b11:
            raise ReservedForFutureUse("not implemented")

        self.epoch = epoch
        self.time_code_id = time_code_id
        self.epoch_id = epoch_id
        self.length_of_day_segment = length_of_day_segment
        self.length_of_subms_segment = length_of_subms_segment
        self.time_handler = TimeHandler.create_handler(epoch, library)

    def __str__(self) -> str:
        epoch_id_str = {
            0: "1958 January 1 epoch (Level 1 Time Code)",
            1: "Agency-defined epoch (Level 2 Time Code)",
        }
        items = [
            "Time Code: CDS",
            f"Epoch Identification: {self.epoch_id} ... {epoch_id_str[self.epoch_id]}",
            f"Time Code Identification: {self.time_code_id}",
            f"Length of day segment: {self.length_of_day_segment}",
            f"Length of submillisecond segment: {self.length_of_subms_segment}",
            f"Epoch: {self.epoch}",
        ]
        return "\n".join(items)

    def get_p_field(self):
        """
        Get the P-field according to CCSDS CDS specification.

        Returns:
            int: The P-field as an integer value.
        """
        # Calculate the bit values based on the CCSDS specification
        extension_bit = 0  # For now, assume no extension

        # Construct the P-field bit by bit
        p_field_bits = (
            (extension_bit << 7)
            | (self.time_code_id << 4)
            | (self.epoch_id << 3)
            | (self.length_of_day_segment << 2)
            | (self.length_of_subms_segment)
        )

        return bytes([p_field_bits])

    def get_contents(self, total_seconds):
        """
        Convert a time duration given in total seconds into three components:
        - days: The total number of full days (24-hour periods) within the given seconds.
        - ms_of_day: The remaining milliseconds within the current day (after accounting for full days).
        - rem: The remaining fractional seconds (sub-millisecond precision) after removing the full days and milliseconds.

        Parameters:
        - total_seconds (float): The total duration in seconds, potentially including fractional seconds.

        Returns:
        - tuple: A tuple containing:
            - days (int): The number of full days.
            - ms_of_day (int): The number of milliseconds that remain within the current day.
            - rem (float): The remaining fractional seconds (sub-millisecond part).
        """
        days = int(math.floor(total_seconds // 86400))
        rem = total_seconds - (days * 86400)
        ms_of_day = int(math.floor(rem * 1e3))
        rem -= ms_of_day * 1e-3
        return days, ms_of_day, rem

    def get_t_field(self, utc):
        """
        Get the T-field as a byte sequence from a given UTC time.

        Args:
            utc (str): The UTC time string in ISO 8601 format.

        Returns:
            bytes: A byte sequence representing the T-field.
        """
        total_seconds = self.time_handler.total_seconds(utc)
        if total_seconds is None:
            return bytes()

        days, ms_of_day, rem = self.get_contents(total_seconds)
        if self.length_of_day_segment == 0:
            day_octets = pack(">H", days)
        else:
            day_octets = pack(">I", days)[1:]

        ms_octets = pack(">I", ms_of_day)

        if self.length_of_subms_segment == 0b00:
            subms_octets = bytes([])
        else:
            if self.length_of_subms_segment == 0b01:
                rem *= 1e6
                subms_octets = pack(">H", int(rem))
            elif self.length_of_subms_segment == 0b10:
                rem *= 1e12
                subms_octets = pack(">I", int(rem))
        return day_octets + ms_octets + subms_octets

    def get_total_seconds(self, utc):
        """
        Return the total seconds between the epoch and a given UTC time.

        Args:
            utc (str): The UTC time string in ISO 8601 format.

        Returns:
            float: Total seconds between the epoch and the given UTC time.
        """
        return self.time_handler.total_seconds(utc)
