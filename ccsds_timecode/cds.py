import math
from struct import pack
from time_exceptions import EpochException, OctetSizeException, ReservedForFutureUse
from ccsds_timecode.timecode_base import CCSDS_TimeCode


def unpack_uint(data):
    value = 0
    for datum in data:
        value <<= 8
        value += datum
    return value


class CCSDS_TimeCode_CDS(CCSDS_TimeCode):
    """Implements CCSDS Time Code Format with T-Field and P-Field."""

    def __init__(
        self,
        epoch="1958-01-01T00:00:00Z",
        epoch_id=0b0,
        length_of_day_segment=0b0,
        length_of_subms_segment=0b01,
        library="my",
    ):
        super().__init__(epoch, library)

        if length_of_subms_segment == 0b11:
            raise ReservedForFutureUse("not implemented")

        self.epoch = epoch
        self.time_code_id = 0b100
        self.epoch_id = epoch_id
        self.length_of_day_segment = length_of_day_segment
        self.length_of_subms_segment = length_of_subms_segment

        if (epoch_id == 0b001) and (
            self.time_handler.total_seconds("1958-01-01T00:00:00Z") != 0
        ):
            raise EpochException(
                "The epoch must be 1958 January 1 when time code identification is 1. "
                f"The specified epoch is {epoch}."
            )

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
        Convert total seconds into days, milliseconds of the day,
        and remaining fractional seconds.

        Args:
            total_seconds (float): Duration in seconds.

        Returns:
            tuple: (days, ms_of_day, rem)
                - days (int): Number of full days.
                - ms_of_day (int): Milliseconds within the current day.
                - rem (float): Remaining fractional seconds.
        """
        days = int(math.floor(total_seconds // 86400))
        rem = total_seconds - (days * 86400)
        ms_of_day = int(math.floor(rem * 1e3))
        rem -= ms_of_day * 1e-3
        return {"days": days, "ms_of_day": ms_of_day, "subms_of_ms": rem}

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

        contents = self.get_contents(total_seconds)
        if self.length_of_day_segment == 0:
            day_octets = pack(">H", contents["days"])
        else:
            day_octets = pack(">I", contents["days"])[1:]

        ms_octets = pack(">I", contents["ms_of_day"])

        if self.length_of_subms_segment == 0b00:
            subms_octets = bytes([])
        else:
            if self.length_of_subms_segment == 0b01:
                subms = contents["subms_of_ms"] * 1e6
                subms_octets = pack(">H", int(subms))
            elif self.length_of_subms_segment == 0b10:
                subms = contents["subms_of_ms"] * 1e12
                subms_octets = pack(">I", int(subms))
        return day_octets + ms_octets + subms_octets

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
        p_field = {
            "extension_flag": time_code[0] >> 7,
            "time_code_id": (time_code[0] >> 4) & 0b111,
            "epoch_id": (time_code[0] >> 3) & 0b1,
            "length_of_day_segment": (time_code[0] >> 2) & 0b1,
            "length_of_subms_segment": time_code[0] & 0b11,
        }
        size_p_field = 1
        size_day = 2 if p_field["length_of_day_segment"] == 0 else 3
        size_ms = 4
        if p_field["length_of_subms_segment"] == 0b00:
            size_subms = 0
            subms_unit = 0
        elif p_field["length_of_subms_segment"] == 0b01:
            size_subms = 2
            subms_unit = 1e-6
        elif p_field["length_of_subms_segment"] == 0b10:
            size_subms = 4
            subms_unit = 1e-9
        else:
            raise ReservedForFutureUse("not implemented")

        length = size_p_field + size_day + size_ms + size_subms
        if len(time_code) != length:
            raise OctetSizeException(
                f"The length of time code must be {length}. "
                f"The length of day segment is {size_day}. "
                f"The length of ms_of_day segment is {size_ms}. "
                f"The length of subms_of_ms segment is {size_subms}. "
            )

        elapsed_seconds = 0
        days = unpack_uint(time_code[1 : 1 + size_day])
        ms = unpack_uint(time_code[1 + size_day : 1 + size_day + size_ms])
        subms = unpack_uint(time_code[1 + size_day + size_ms :]) if size_ms > 0 else 0
        elapsed_seconds = days * 86400 + ms * 1e-3 + subms * subms_unit
        return p_field, self.time_handler.utc_string(elapsed_seconds)
