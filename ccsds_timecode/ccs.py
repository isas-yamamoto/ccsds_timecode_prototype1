from datetime import datetime
from time_exceptions import NotUsedException, OctetSizeException
from ccsds_timecode.timecode_base import (
    CCSDS_TimeCode,
    pack_uint,
    int2bcd,
)


class CCSDS_TimeCode_CCS(CCSDS_TimeCode):
    """Implements CCSDS Time Code Format with T-Field and P-Field."""

    def __init__(
        self,
        calendar_variation_flag=0b0,
        resolution=0b000,
        library="my",
    ):
        if resolution == 0b111:
            raise NotUsedException("resolution {resolution} is not used.")

        self.time_code_id = 0b101
        self.calendar_variation_flag = calendar_variation_flag
        self.resolution = resolution

    def __str__(self) -> str:
        items = [
            "Time Code: CCS",
            f"calendar_variation_flag: {self.calendar_variation_flag}",
            f"resolution: {self.resolution}",
        ]
        return "\n".join(items)

    def get_p_field(self):
        """
        Get the P-field according to CCSDS CCS specification.

        Returns:
            int: The P-field as an integer value.
        """
        # Calculate the bit values based on the CCSDS specification
        extension_bit = 0  # For now, assume no extension

        # Construct the P-field bit by bit
        p_field_bits = (
            (extension_bit << 7)
            | (self.time_code_id << 4)
            | (self.calendar_variation_flag << 3)
            | (self.resolution)
        )

        return bytes([p_field_bits])

    def get_t_field(self, utc):
        """
        Get the T-field as a byte sequence from a given UTC time.

        Args:
            utc (str): The UTC time string in ISO 8601 format.

        Returns:
            bytes: A byte sequence representing the T-field.
        """

        cols = utc.split(".")
        dt = datetime.strptime(cols[0], "%Y-%m-%dT%H:%M:%S")

        year = pack_uint(int2bcd(dt.year))
        h = pack_uint(int2bcd(dt.hour))
        m = pack_uint(int2bcd(dt.minute))
        s = pack_uint(int2bcd(dt.second))

        if self.calendar_variation_flag == 0b0:
            mo = pack_uint(int2bcd(dt.month))
            dom = pack_uint(int2bcd(dt.day))
            data = year + mo + dom + h + m + s
        else:
            doy = pack_uint(int2bcd(dt.timetuple().tm_yday))
            data = year + doy + h + m + s

        optional = bytes([])
        size_optional = 2 * self.resolution

        if len(cols) == 2:
            frac_str = cols[1][:size_optional]
            frac_str += "0" * (size_optional - len(frac_str))
            optional = pack_uint(int2bcd(frac_str))
        else:
            optional = bytes([0x00] * self.resolution)
        return data + optional

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
            "calendar_variation_flag": (time_code[0] >> 3) & 0b1,
            "resolution": time_code[0] & 0b111,
        }

        size_p_field = 1
        size_base = 7
        size_optional = 2 * p_field["resolution"]

        length = size_p_field + 7 + size_optional
        if len(time_code) != length:
            raise OctetSizeException(
                f"The length of time code must be {length}. "
                f"The length of optional is {size_optional}. "
            )

        t_field = time_code[size_p_field : size_p_field + size_base + size_optional]
        s = ""
        for data in t_field:
            s += f"{data:02X}"

        if p_field["calendar_variation_flag"] == 0:
            format = "%y%m%dH%M%S"
        else:
            format = "%y0%jH%M%S"

        dt = datetime.strptime(s[:14], format)
        utc_string = dt.strftime("%Y-%m-%d %H:%M:%S")

        if size_optional > 0:
            utc_string += "." + s[14:]

        return p_field, utc_string
