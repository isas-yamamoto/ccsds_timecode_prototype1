import unittest
from struct import unpack
from ccsds_timecode.cuc import CCSDS_TimeCode_CUC, TimeCodeIdentificationException


class TestCcsdsTimecodeCuc(unittest.TestCase):
    def setUp(self):
        self.cuc = CCSDS_TimeCode_CUC(library="my")

    def test_p_field_identification_tai_epoch(self):
        cuc = CCSDS_TimeCode_CUC(time_code_id=0b001)
        time_code_id_mask = 0b0_111_00_00
        expected = 0b0_001_00_00
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

    def test_p_field_identification_agency_defined_epoch(self):
        cuc = CCSDS_TimeCode_CUC(time_code_id=0b010)
        time_code_id_mask = 0b0_111_00_00
        expected = 0b0_010_00_00
        actual = (unpack("B", cuc.get_p_field())[0]) & time_code_id_mask
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
