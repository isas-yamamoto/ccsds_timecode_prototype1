from datetime import datetime
from time_exceptions import NotUsedException, OctetSizeException
from ccsds_timecode.timecode_base import CCSDS_TimeCode
from ccsds_timecode.utils import pack_uint, int2bcd


class CCSDS_TimeCode_ASCII(CCSDS_TimeCode):
    """Implements CCSDS Time Code Format with T-Field and P-Field."""

    def __init__(
        self,
        code_type="A",
        library="my",
    ):
        self.code_type = code_type

    def __str__(self) -> str:
        items = [
            f"Time Code: ASCII CODE {self.code_type}",
        ]
        return "\n".join(items)

    def get_p_field(self):
        """
        Get the P-field according to CCSDS CCS specification.

        Returns:
            int: The P-field as an integer value.
        """
        return None

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

        if self.code_type == "A":
            ascii = dt.strftime("%Y-%m-%dT%H:%M:%S")
        else:
            ascii = dt.strftime("%Y-%jT%H:%M:%S")
        if len(cols) == 2:
            ascii += f".{cols[1]}"
        return ascii.encode()

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
        s = time_code.decode()
        cols = s.split(".")

        if self.code_type == "A":
            utc_string = datetime.strptime(cols[0], "%Y-%m-%dT%H:%M:%S")
        else:
            utc_string = datetime.strptime(cols[0], "%Y-%jT%H:%M:%S")

        if len(cols) == 2:
            utc_string += f".{cols[1]}"

        return None, utc_string
