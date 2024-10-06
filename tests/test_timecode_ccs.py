import unittest
from ccsds_timecode.ccs import CCSDS_TimeCode_CCS
from time_exceptions import (
    OctetSizeException,
    NotUsedException,
)


class TestCcsdsTimecodeCcs(unittest.TestCase):
    def test_octet_size(self):
        with self.assertRaises(OctetSizeException):
            cds = CCSDS_TimeCode_CCS()
            cds.unpack_time_code(bytes([0x50, 00]))

    def test_p_field_moy_dom(self):
        cds = CCSDS_TimeCode_CCS(calendar_variation_flag=0, resolution=0)
        actual = cds.get_p_field()
        expected = bytes([0x50])
        self.assertEqual(actual, expected)

    def test_p_field_doy(self):
        cds = CCSDS_TimeCode_CCS(calendar_variation_flag=1, resolution=0)
        actual = cds.get_p_field()
        expected = bytes([0x58])
        self.assertEqual(actual, expected)

    def test_1958_01_01_resolution_000(self):
        cds = CCSDS_TimeCode_CCS(calendar_variation_flag=0, resolution=0)
        actual = cds.get_t_field("1958-01-01T23:45:56.123456789012")
        expected = bytes([0x19, 0x58, 0x01, 0x01, 0x23, 0x45, 0x56])
        self.assertEqual(actual, expected)

    def test_1958_01_01_resolution_001(self):
        cds = CCSDS_TimeCode_CCS(calendar_variation_flag=0, resolution=1)
        actual = cds.get_t_field("1958-01-01T00:00:00.123456789012")
        expected = bytes([0x19, 0x58, 0x01, 0x01, 0x00, 0x00, 0x00, 0x12])
        self.assertEqual(actual, expected)

    def test_1958_01_01_resolution_010(self):
        cds = CCSDS_TimeCode_CCS(calendar_variation_flag=0, resolution=2)
        actual = cds.get_t_field("1958-01-01T00:00:00.123456789012")
        expected = bytes([0x19, 0x58, 0x01, 0x01, 0x00, 0x00, 0x00, 0x12, 0x34])
        self.assertEqual(actual, expected)

    def test_1958_01_01_resolution_011(self):
        cds = CCSDS_TimeCode_CCS(calendar_variation_flag=0, resolution=3)
        actual = cds.get_t_field("1958-01-01T00:00:00.123456789012")
        expected = bytes([0x19, 0x58, 0x01, 0x01, 0x00, 0x00, 0x00, 0x12, 0x34, 0x56])
        self.assertEqual(actual, expected)

    def test_1958_01_01_resolution_100(self):
        cds = CCSDS_TimeCode_CCS(calendar_variation_flag=0, resolution=4)
        actual = cds.get_t_field("1958-01-01T00:00:00.123456789012")
        expected = bytes([0x19, 0x58, 0x01, 0x01, 0x00, 0x00, 0x00, 0x12, 0x34, 0x56, 0x78])
        self.assertEqual(actual, expected)

    def test_1958_01_01_resolution_101(self):
        cds = CCSDS_TimeCode_CCS(calendar_variation_flag=0, resolution=5)
        actual = cds.get_t_field("1958-01-01T00:00:00.123456789012")
        expected = bytes([0x19, 0x58, 0x01, 0x01, 0x00, 0x00, 0x00, 0x12, 0x34, 0x56, 0x78, 0x90])
        self.assertEqual(actual, expected)

    def test_1958_01_01_resolution_110(self):
        cds = CCSDS_TimeCode_CCS(calendar_variation_flag=0, resolution=6)
        actual = cds.get_t_field("1958-01-01T00:00:00.123456789012")
        expected = bytes([0x19, 0x58, 0x01, 0x01, 0x00, 0x00, 0x00, 0x12, 0x34, 0x56, 0x78, 0x90, 0x12])
        self.assertEqual(actual, expected)

    def test_1958_01_01_resolution_111(self):
        with self.assertRaises(NotUsedException):
            CCSDS_TimeCode_CCS(calendar_variation_flag=0, resolution=7)
