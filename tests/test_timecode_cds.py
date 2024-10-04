import unittest
from struct import unpack
from ccsds_timecode.cds import CCSDS_TimeCode_CDS
from time_exceptions import (
    EpochException,
    OctetSizeException,
    ReservedForFutureUse,
)


class TestCcsdsTimecodeCds(unittest.TestCase):
    def test_p_field_identification_tai_epoch(self):
        cuc = CCSDS_TimeCode_CDS(epoch_id=0b0)
        epoch_id_mask = 0b0_000_1_0_00
        expected = 0b0_000_0_0_00
        actual = (unpack("B", cuc.get_p_field())[0]) & epoch_id_mask
        self.assertEqual(actual, expected)

    def test_p_field_identification_agency_defined_epoch(self):
        cuc = CCSDS_TimeCode_CDS(epoch_id=0b1)
        epoch_id_mask = 0b0_000_1_0_00
        expected = 0b0_000_1_0_00
        actual = (unpack("B", cuc.get_p_field())[0]) & epoch_id_mask
        self.assertEqual(actual, expected)

    def test_invalid_epoch(self):
        with self.assertRaises(EpochException):
            CCSDS_TimeCode_CDS(epoch="1958-01-01T00:00:01", epoch_id=0b1)

    def test_octet_size(self):
        with self.assertRaises(OctetSizeException):
            cds = CCSDS_TimeCode_CDS()
            cds.unpack_time_code(bytes([0x40, 00]))

    def test_1958_01_01(self):
        """
        total_seconds:  0
        DAY: 0
        ms_of_day: 0
        """
        cds = CCSDS_TimeCode_CDS(library="my")
        actual = cds.get_t_field("1958-01-01T00:00:00Z")
        day = bytes([0x00, 0x00])
        ms_of_day = bytes([0x00, 0x00, 0x00, 0x00])
        subms_of_ms = bytes([0x00, 0x00])
        expected = day + ms_of_day + subms_of_ms
        self.assertEqual(actual, expected)

    def test_1959_01_01(self):
        """
        total_seconds: 31536000
        DAY: 365 = 0x016d
        ms_of_day: 0
        """
        day = bytes([0x01, 0x6D])
        ms_of_day = bytes([0x00, 0x00, 0x00, 0x00])
        subms_of_ms = bytes([0x00, 0x00])
        data = day + ms_of_day + subms_of_ms

        cds = CCSDS_TimeCode_CDS(library="my")
        actual = cds.get_t_field("1959-01-01T00:00:00Z")
        expected = data
        self.assertEqual(actual, expected)

        """
        Extension: 0b0
        Time code identification: 0b100
        Epoch identification: 0 ... TAI Epoch (1958-01-01 00:00:00)
        length of day segment: 0b0 ... 16bits
        length of submillisecond segment: 0b01 ... 16bit(microsecond)
        => p-field: 0b0_100_0_0_01 = 0x41
        """
        p_field_data = bytes([0x41])
        _, actual = cds.unpack_time_code(p_field_data + data)
        expected = "1959-01-01T00:00:00.000000"
        self.assertEqual(actual, expected)

    def test_1961_01_01_subms_absent(self):
        """
        total_seconds:  94694401.422818
        DAY: total_seconds / 86400 = 1096 = 0x0448
        ms_of_day: 1.4228180 * 1e3 = 1422 = 0x0000058e
        subms_of_ms: None
        """
        day = bytes([0x04, 0x48])
        ms_of_day = bytes([0x00, 0x00, 0x05, 0x8E])
        subms_of_ms = bytes([])
        data = day + ms_of_day + subms_of_ms

        cds = CCSDS_TimeCode_CDS(length_of_subms_segment=0b00, library="my")
        actual = cds.get_t_field("1961-01-01T00:00:00Z")
        expected = data
        self.assertEqual(actual, expected)

        """
        Extension: 0b0
        Time code identification: 0b100
        Epoch identification: 0 ... TAI Epoch (1958-01-01 00:00:00)
        length of day segment: 0b0 ... 16bits
        length of submillisecond segment: 0b00 ... absent
        => p-field: 0b0_100_0_0_00 = 0x40
        total_seconds: 94694401.422 (not 94694401.422818)
        """
        p_field_data = bytes([0x40])
        _, actual = cds.unpack_time_code(p_field_data + data)
        expected = "1960-12-31T23:59:59.999182"
        self.assertEqual(actual, expected)

    def test_1961_01_01_microseconds(self):
        """
        total_seconds:  94694401.422818
        DAY: total_seconds / 86400 = 1096 = 0x0448
        ms_of_day: 1.4228180 * 1e3 = 1422 = 0x0000058e
        subms_of_ms: 0.0008180 * 1e6 = 818 = 0x0332
        """
        cds = CCSDS_TimeCode_CDS(length_of_subms_segment=0b01, library="my")
        actual = cds.get_t_field("1961-01-01T00:00:00Z")
        day = bytes([0x04, 0x48])
        ms_of_day = bytes([0x00, 0x00, 0x05, 0x8E])
        subms_of_ms = bytes([0x03, 0x32])
        expected = day + ms_of_day + subms_of_ms
        self.assertEqual(actual, expected)

    def test_1961_01_01_picoseconds(self):
        """
        total_seconds:  94694401.422818
        DAY: total_seconds / 86400 = 1096 = 0x0448
        ms_of_day: 1.4228180 * 1e3 = 1422 = 0x0000058e
        subms_of_ms: 0.0008180 * 1e12 = 818000000 = 0x30c1b080
        """
        cds = CCSDS_TimeCode_CDS(length_of_subms_segment=0b10, library="my")
        actual = cds.get_t_field("1961-01-01T00:00:00Z")
        day = bytes([0x04, 0x48])
        ms_of_day = bytes([0x00, 0x00, 0x05, 0x8E])
        subms_of_ms = bytes([0x30, 0xC1, 0xB0, 0x80])
        expected = day + ms_of_day + subms_of_ms
        self.assertEqual(actual, expected)

    def test_1961_01_01_reserved(self):
        """
        check reserved
        """
        with self.assertRaises(ReservedForFutureUse):
            CCSDS_TimeCode_CDS(length_of_subms_segment=0b11, library="my")

    def test_1961_01_01_day_segment_24bits(self):
        """
        total_seconds:  94694401.422818
        DAY: total_seconds / 86400 = 1096 = 0x000448
        ms_of_day: 1.4228180 * 1e3 = 1422 = 0x0000058e
        subms_of_ms: None
        """
        cds = CCSDS_TimeCode_CDS(
            length_of_day_segment=0b1,
            length_of_subms_segment=0b00,
            library="my",
        )
        actual = cds.get_t_field("1961-01-01T00:00:00Z")
        day = bytes([0x00, 0x04, 0x48])
        ms_of_day = bytes([0x00, 0x00, 0x05, 0x8E])
        subms_of_ms = bytes([])
        expected = day + ms_of_day + subms_of_ms
        self.assertEqual(actual, expected)

    def test_unpack_1958_01_01(self):
        """
        Extension: 0b0
        Time code identification: 0b100
        Epoch identification: 0 ... TAI Epoch (1958-01-01 00:00:00)
        length of day segment: 0b0 ... 16bits
        length of submillisecond segment: 0b00 ... absent
        => p-field: 0b0_100_0_0_00 = 0x40
        """
        cds = CCSDS_TimeCode_CDS()
        p_field = bytes([0x40])
        day = bytes([0x00, 0x00])
        ms = bytes([0x00, 0x00, 0x00, 0x00])
        subms = bytes([])
        _, actual = cds.unpack_time_code(p_field + day + ms + subms)
        expected = "1958-01-01T00:00:00.000000"
        self.assertEqual(actual, expected)
