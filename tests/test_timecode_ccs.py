import unittest
from ccsds_timecode.ccs import CCSDS_TimeCode_CCS
from time_exceptions import (
    OctetSizeException,
)


class TestCcsdsTimecodeCcs(unittest.TestCase):
    def test_octet_size(self):
        with self.assertRaises(OctetSizeException):
            cds = CCSDS_TimeCode_CCS()
            cds.unpack_time_code(bytes([0x50, 00]))
