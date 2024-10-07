import unittest
from ccsds_timecode.pb5j import TimeCode_PB5J


class TestCcsdsTimecodePb5j(unittest.TestCase):
    def setUp(self):
        self.library = "my"

    def test_1968_05_24(self):
        """
        TJD: 0
        """
        pb5j = TimeCode_PB5J(library=self.library)
        actual = pb5j.get_t_field("1968-05-24T00:00:00")
        expected = bytes([0x00, 0x00, 0x00, 0x00])
        self.assertEqual(actual, expected)

    def test_1968_05_24_00_00_01(self):
        """
        TJD: 0
        """
        pb5j = TimeCode_PB5J(library=self.library)
        actual = pb5j.get_t_field("1968-05-24T00:00:01")
        expected = bytes([0x00, 0x00, 0x00, 0x02])
        self.assertEqual(actual, expected)

    def test_1968_05_24_23_59_59(self):
        """
        TJD: 0
        """
        pb5j = TimeCode_PB5J(library=self.library)
        actual = pb5j.get_t_field("1968-05-24T23:59:59")
        expected = bytes([0x00, 0x02, 0xa2, 0xfe])
        self.assertEqual(actual, expected)
