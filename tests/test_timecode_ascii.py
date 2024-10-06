import unittest
from ccsds_timecode.ascii import CCSDS_TimeCode_ASCII


class TestCcsdsTimecodeAscii(unittest.TestCase):
    def test_1958_01_01_A(self):
        cds = CCSDS_TimeCode_ASCII(code_type="A")
        actual = cds.get_t_field("1958-01-1T00:00:00")
        expected = bytes(
            [
                0x31,  # 1
                0x39,  # 9
                0x35,  # 5
                0x38,  # 8
                0x2D,  # -
                0x30,  # 0
                0x31,  # 1
                0x2D,  # -
                0x30,  # 0
                0x31,  # 1
                0x54,  # T
                0x30,  # 0
                0x30,  # 0
                0x3A,  # :
                0x30,  # 0
                0x30,  # 0
                0x3A,  # :
                0x30,  # 0
                0x30,  # 0
            ]
        )
        self.assertEqual(actual, expected)

    def test_1958_01_01_B(self):
        cds = CCSDS_TimeCode_ASCII(code_type="B")
        actual = cds.get_t_field("1958-01-1T00:00:00")
        expected = bytes(
            [
                0x31,  # 1
                0x39,  # 9
                0x35,  # 5
                0x38,  # 8
                0x2D,  # -
                0x30,  # 0
                0x30,  # 0
                0x31,  # 1
                0x54,  # T
                0x30,  # 0
                0x30,  # 0
                0x3A,  # :
                0x30,  # 0
                0x30,  # 0
                0x3A,  # :
                0x30,  # 0
                0x30,  # 0
            ]
        )
        self.assertEqual(actual, expected)
