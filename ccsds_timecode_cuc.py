from time_handler import TimeHandler


class CCSDS_TimeCode_CUC:
    """Implements CCSDS Time Code Format with T-Field and P-Field."""

    def __init__(
        self,
        epoch="1958-01-01T00:00:00Z",
        time_code_id=0b001,
        basic_time_unit=1,
        num_basic_octets=4,
        num_fractional_octets=2,
        library="astropy",
    ):
        self.epoch = epoch
        self.time_code_id = time_code_id
        self.basic_time_unit = basic_time_unit
        self.num_basic_octets = num_basic_octets
        self.num_fractional_octets = num_fractional_octets
        self.time_handler = TimeHandler.create_handler(epoch, library)

    def get_p_field(self):
        """
        Get the P-field according to CCSDS CUC specification.

        Returns:
            int: The P-field as an integer value.
        """
        # Calculate the bit values based on the CCSDS specification
        extension_bit = 0  # For now, assume no extension
        time_code_id = self.time_code_id
        basic_time_octets_minus_one = self.num_basic_octets - 1
        fractional_time_octets = self.num_fractional_octets

        # Construct the P-field bit by bit
        p_field_bits = (
            (extension_bit << 7)
            | (time_code_id << 4)
            | (basic_time_octets_minus_one << 2)
            | (fractional_time_octets)
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
        total_seconds = self.time_handler.total_seconds(utc)
        if total_seconds is None:
            return bytes()

        # Calculate basic time octets
        basic_time_octets = [
            int(total_seconds // (256**i)) % 256
            for i in reversed(range(self.num_basic_octets))
        ]

        # Calculate fractional time octets
        fractional_seconds = total_seconds - int(total_seconds)
        fractional_time_octets = [
            int(fractional_seconds * (256 ** (i + 1))) % 256
            for i in range(self.num_fractional_octets)
        ]

        return bytes(basic_time_octets + fractional_time_octets)

    def get_total_seconds(self, utc):
        """
        Return the total seconds between the epoch and a given UTC time.

        Args:
            utc (str): The UTC time string in ISO 8601 format.

        Returns:
            float: Total seconds between the epoch and the given UTC time.
        """
        return self.time_handler.total_seconds(utc)
