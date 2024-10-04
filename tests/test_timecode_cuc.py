import unittest
from struct import unpack
from ccsds_timecode.cuc import CCSDS_TimeCode_CUC
from time_exceptions import (
    TimeCodeIdentificationException,
    EpochException,
    OctetSizeException,
)


class TestCcsdsTimecodeCuc(unittest.TestCase):
    def test_p_field_identification_tai_epoch(self):
        cuc = CCSDS_TimeCode_CUC(time_code_id=0b001)
        time_code_id_mask = 0b0_111_00_00
        expected = 0b0_001_00_00
        actual = (unpack("B", cuc.get_p_field())[0]) & time_code_id_mask
        self.assertEqual(actual, expected)

    def test_p_field_identification_agency_defined_epoch(self):
        cuc = CCSDS_TimeCode_CUC(time_code_id=0b010)
        time_code_id_mask = 0b0_111_00_00
        expected = 0b0_010_00_00
        actual = (unpack("B", cuc.get_p_field())[0]) & time_code_id_mask
        self.assertEqual(actual, expected)

    def test_invalid_p_field_identification(self):
        with self.assertRaises(TimeCodeIdentificationException):
            CCSDS_TimeCode_CUC(time_code_id=0b000)

        with self.assertRaises(TimeCodeIdentificationException):
            CCSDS_TimeCode_CUC(time_code_id=0b011)

        with self.assertRaises(TimeCodeIdentificationException):
            CCSDS_TimeCode_CUC(time_code_id=0b100)

        with self.assertRaises(TimeCodeIdentificationException):
            CCSDS_TimeCode_CUC(time_code_id=0b101)

        with self.assertRaises(TimeCodeIdentificationException):
            CCSDS_TimeCode_CUC(time_code_id=0b110)

        with self.assertRaises(TimeCodeIdentificationException):
            CCSDS_TimeCode_CUC(time_code_id=0b111)

    def test_invalid_epoch(self):
        with self.assertRaises(EpochException):
            CCSDS_TimeCode_CUC(epoch="1958-01-01T00:00:01", time_code_id=0b001)

    def test_octet_size(self):
        with self.assertRaises(OctetSizeException):
            cuc = CCSDS_TimeCode_CUC()
            cuc.unpack_time_code(bytes([0x10, 00, 00]))

    def test_unpack_1958_01_01(self):
        cuc = CCSDS_TimeCode_CUC(num_basic_octets=4, num_fractional_octets=0)
        p_field, utcstr = cuc.unpack_time_code(bytes([0x1C, 00, 00, 00, 00]))
        expected = "1958-01-01T00:00:00.000000"
        self.assertEqual(utcstr, expected)

    def test_unpack_1959_01_01(self):
        cuc = CCSDS_TimeCode_CUC(num_basic_octets=4, num_fractional_octets=0)
        p_field, utcstr = cuc.unpack_time_code(bytes([0x1C, 0x01, 0xE1, 0x33, 0x80]))
        expected = "1959-01-01T00:00:00.000000"
        self.assertEqual(utcstr, expected)

    def test_unpack_1961_01_01(self):
        cuc = CCSDS_TimeCode_CUC(num_basic_octets=4, num_fractional_octets=0)
        p_field, utcstr = cuc.unpack_time_code(bytes([0x1C, 0x05, 0xA4, 0xEC, 0x00]))
        expected = "1960-12-31T23:59:58.577182"
        self.assertEqual(utcstr, expected)

    def test_unpack_1962_01_01(self):
        """
        Epoch:  1958-01-01 00:00:00 TAI
        Target: 1962-01-01T00:00:00 UTC (old)
        total seconds: 126230401.845858
        HEX: 0x7861f81 + 0.845858
        """
        cuc = CCSDS_TimeCode_CUC(num_basic_octets=4, num_fractional_octets=0)
        p_field, utcstr = cuc.unpack_time_code(bytes([0x1C, 0x07, 0x86, 0x1F, 0x81]))
        expected = "1961-12-31T23:59:59.154142"
        self.assertEqual(utcstr, expected)

    def test_unpack_1972_01_01_utc(self):
        """
        Epoch:  1958-01-01 00:00:00 TAI
        Target: 1972-01-01T00:00:00 UTC
        total seconds: 441763210
        HEX: 0x1a54c58a
        """
        cuc = CCSDS_TimeCode_CUC(num_basic_octets=4, num_fractional_octets=0)
        p_field, utcstr = cuc.unpack_time_code(bytes([0x1C, 0x1A, 0x54, 0xC5, 0x8A]))
        expected = "1972-01-01T00:00:00.000000"
        self.assertEqual(utcstr, expected)

    def test_unpack_2000_01_01_utc(self):
        """
        Test unpacking a CCSDS time code for the target UTC date of 2000-01-01 00:00:00.

        Calculation details:
        - Epoch time: 1958-01-01 00:00:00 TAI
        - Target time: 2000-01-01 00:00:00 UTC

        1. Year difference calculation:
        - 2000 - 1958 = 42 years
        - Number of leap years between 1958 and 2000: 10
            (Leap years: 1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 1996)

        2. Total number of days calculation:
        - Total days = (42 years * 365 days/year) + 10 leap days = 15340 days

        3. Total seconds calculation:
        - Total seconds = (15340 days * 86400 seconds/day) + offset + total leap seconds
        - Offset: 10 seconds as of 1972-01-01
        - Total leap seconds: 22 seconds as of 2000-01-01

        4. Final total seconds:
        - 1325376000 + 10 + 22 = 1325376032 seconds
        - Hexadecimal representation: 0x4effa220
        """
        cuc = CCSDS_TimeCode_CUC(num_basic_octets=4, num_fractional_octets=0)
        p_field, utcstr = cuc.unpack_time_code(bytes([0x1C, 0x4E, 0xFF, 0xA2, 0x20]))
        expected = "2000-01-01T00:00:00.000000"
        self.assertEqual(utcstr, expected)


if __name__ == "__main__":
    unittest.main()
