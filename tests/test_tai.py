import unittest
from datetime import datetime, timedelta
from ccsds_timecode.cuc import CCSDS_TimeCode_CUC
import gmpy2


class TestTai(unittest.TestCase):
    def setUp(self):
        self.cuc = CCSDS_TimeCode_CUC(library="astropy")
        self.delta = gmpy2.mpfr("1e-16")

    def test_zero_time(self):
        expected = 0
        actual = self.cuc.get_total_seconds("1958-01-01T00:00:00Z")
        self.assertEqual(actual, expected)

        elapsed_seconds = 0
        expected = "1958-01-01T00:00:00.000000"
        actual = self.cuc.utc_string(elapsed_seconds)
        self.assertEqual(actual, expected)

    def test_1960_12_31_utc(self):
        """
        Tests the total seconds from January 1, 1958, to December 31, 1960.

        Key points:
        - The difference between UTC and TAI was not defined on this date.
        - 1960 is a leap year, contributing an extra day.
        - Total days from Jan 1, 1958, to Dec 31, 1960:
        2 years (730 days) + 1 leap day + 364 days in 1960 = 1095 days.
        - Total seconds: 1095 days * 86400 seconds/day = 94608000 seconds.
        """
        expected = gmpy2.mpz("94608000")
        actual = self.cuc.get_total_seconds("1960-12-31T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1960-12-31T00:00:00.000000"
        actual = self.cuc.utc_string(94608000)
        self.assertEqual(actual, expected)

    def test_1961_01_01_utc(self):
        """
        Tests the total seconds from January 1, 1958, to January 1, 1961.

        Key points:
        - As of January 1, 1961, the UTC-TAI difference was defined as
        1.4228180 seconds.
        - 1960 was a leap year, contributing an extra day.
        - Total days from Jan 1, 1958, to Jan 1, 1961:
          (3 years * 365 days) + 1 leap day = 1096 days.
        - Total seconds:
          (1096 days * 86400 seconds/day) + 1.4228180 = 94694401.422818.
        """
        expected = gmpy2.mpfr("94694401.422818")
        actual = self.cuc.get_total_seconds("1961-01-01T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1961-01-01T00:00:00.000000"
        actual = self.cuc.utc_string(94694401.422818)
        self.assertEqual(actual, expected)

    def test_1961_01_02_utc(self):
        """
        Tests the total seconds from January 1, 1958, to Janulary 2, 1961.

        Key points:
        - As of January 1, 1961, the UTC-TAI difference was 1.4228180 seconds,
        with a daily increase of 0.001296 seconds from that date.
        - The total difference on Janulary 2, 1961 was 1.424114 seconds.
        - 1960 was a leap year, so total seconds from 1958 to Jan 2, 1961:
        (3 years * 365 days) + 1 day + 1 leap day = 1097 days.
        - Total seconds:
        (1097 days * 86400 seconds/day) + 1.424114 = 94780801.424114.
        """
        expected = gmpy2.mpfr("94780801.424114")
        actual = self.cuc.get_total_seconds("1961-01-02T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1961-01-02T00:00:00.000000"
        actual = self.cuc.utc_string(94780801.424114)
        self.assertEqual(actual, expected)

    def test_1961_07_31_utc(self):
        """
        Tests the total seconds from January 1, 1958, to July 31, 1961.

        Key points:
        - As of January 1, 1961, the UTC-TAI difference was 1.4228180 seconds,
        with a daily increase of 0.001296 seconds from that date.
        - The total difference on July 31, 1961 was 1.696274 seconds.
        - Calculation for days from Jan 1, 1961 to July 31, 1961:
        31 + 28 + 31 + 30 + 31 + 30 + 31 - 1 = 211 days.
        - Increment: 211 days * 0.001296 = 0.273456 seconds.
        - Total UTC-TAI difference: 1.4228180 + 0.273456 = 1.696274 seconds.
        - 1960 was a leap year, so total seconds from 1958 to July 31, 1961:
        (3 years * 365 days) + 211 days + 1 leap day = 1307 days.
        - Total seconds:
        (1307 days * 86400 seconds/day) + 1.696274 = 112924801.696274.
        """
        expected = gmpy2.mpfr("112924801.696274")
        actual = self.cuc.get_total_seconds("1961-07-31T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1961-07-31T00:00:00.000000"
        actual = self.cuc.utc_string(112924801.696274)
        self.assertEqual(actual, expected)

    def test_1961_08_01_utc(self):
        """
        Tests the total seconds from January 1, 1958, to August 1, 1961.

        As of Aug. 1, 1961, the UTC-TAI difference was calculated as follows:
        days: 31 + 28 + 31 + 30 + 31 + 30 + 31 = 212
        offset: 1.3728180 + 212 * 0.001296 = 1.3728180 + 0.274752 = 1.64757
        total: ((365 * (1961 - 1958)) + 212 + 1) * 86400 + 1.64757 = 113011201.64757 s
        """
        expected = gmpy2.mpfr("113011201.64757")
        actual = self.cuc.get_total_seconds("1961-08-01T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1961-08-01T00:00:00.000000"
        actual = self.cuc.utc_string(113011201.64757)
        self.assertEqual(actual, expected)

    def test_1961_08_02_utc(self):
        """
        Tests the total seconds from January 1, 1958, to August 2, 1961.

        As of Aug. 1, 1961, the UTC-TAI difference was calculated as follows:
        days: 31 + 28 + 31 + 30 + 31 + 30 + 31 + 1 = 213
        offset: 1.3728180 + 213 * 0.001296 = 1.3728180 + 0.276048 = 1.648866
        total: ((365 * (1961 - 1958)) + 213 + 1) * 86400 + 1.648866 = 113097601.648866 s
        """
        expected = gmpy2.mpfr("113097601.648866")
        actual = self.cuc.get_total_seconds("1961-08-02T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1961-08-02T00:00:00.000000"
        actual = self.cuc.utc_string(113097601.648866)
        self.assertEqual(actual, expected)

    def test_1961_12_31_utc(self):
        """
        Tests the total seconds from January 1, 1958, to December 31, 1961.

        As of Aug. 1, 1961, the UTC-TAI difference was calculated as follows:
        days: 364
        offset: 1.3728180 + 364 * 0.001296 = 1.844562
        total: ((365 * (1961 - 1958)) + 364 + 1) * 86400 + 1.844562 = 126144001.844562 s
        """
        expected = gmpy2.mpfr("126144001.844562")
        actual = self.cuc.get_total_seconds("1961-12-31T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1961-12-31T00:00:00.000000"
        actual = self.cuc.utc_string(126144001.844562)
        self.assertEqual(actual, expected)

    def test_1962_01_01_utc(self):
        """
        Tests the total seconds from January 1, 1958, to January 1, 1962.

        As of Jan. 1, 1962, the UTC-TAI difference was calculated as follows:
        days: 0
        offset: 1.8458580 + 0 * 0.0011232 = 1.8458580
        total: ((365 * (1962 - 1958)) + 0 + 1) * 86400 + 1.8458580 = 126230401.845858 s
        """
        expected = gmpy2.mpfr("126230401.845858")
        actual = self.cuc.get_total_seconds("1962-01-01T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1962-01-01T00:00:00.000000"
        actual = self.cuc.utc_string(126230401.845858)
        self.assertEqual(actual, expected)

    def test_1962_01_02_utc(self):
        """
        Tests the total seconds from January 1, 1958, to January 2, 1962.

        As of Jan. 2, 1962, the UTC-TAI difference was calculated as follows:
        days: 1
        offset: 1.8458580 + 1 * 0.0011232 = 1.8469812
        total: ((365 * (1962 - 1958)) + 1 + 1) * 86400 + 1.8469812 = 126316801.8469812 s
        """
        expected = gmpy2.mpfr("126316801.8469812")
        actual = self.cuc.get_total_seconds("1962-01-02T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1962-01-02T00:00:00.000000"
        actual = self.cuc.utc_string(126316801.8469812)
        self.assertEqual(actual, expected)

    def test_1963_10_31_utc(self):
        """
        Tests the total seconds from January 1, 1958, to October 31, 1963.

        As of Oct. 31, 1963, the UTC-TAI difference was calculated as follows:
        days: 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 - 1 = 303
        offset: 1.8458580 + (365 + 303) * 0.0011232 = 2.5961556
        total: ((365 * (1963 - 1958)) + 303 + 1) * 86400 + 2.5961556 = 183945602.5961556 s
        """
        expected = gmpy2.mpfr("183945602.5961556")
        actual = self.cuc.get_total_seconds("1963-10-31T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1963-10-31T00:00:00.000000"
        actual = self.cuc.utc_string(183945602.5961556)
        self.assertEqual(actual, expected)

    def test_1963_11_01_utc(self):
        """
        Tests the total seconds from January 1, 1958, to November 1, 1963.

        As of Nov. 1, 1963, the UTC-TAI difference was calculated as follows:
        days: 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 = 304
        offset: 1.9458580 + (365 + 304) * 0.0011232 = 2.6972788
        total: ((365 * (1963 - 1958)) + 304 + 1) * 86400 + 2.6972788 = 184032002.6972788 s
        """
        expected = gmpy2.mpfr("184032002.6972788")
        actual = self.cuc.get_total_seconds("1963-11-01T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1963-11-01T00:00:00.000000"
        actual = self.cuc.utc_string(184032002.6972788)
        self.assertEqual(actual, expected)

    def test_1963_11_02_utc(self):
        """
        Tests the total seconds from January 1, 1958, to November 2, 1963.

        As of Nov. 2, 1963, the UTC-TAI difference was calculated as follows:
        days: 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 1= 305
        offset: 1.9458580 + (365 + 305) * 0.0011232 = 2.698402
        total: ((365 * (1963 - 1958)) + 305 + 1) * 86400 + 2.698402 = 184118402.698402 s
        """
        expected = gmpy2.mpfr("184118402.698402")
        actual = self.cuc.get_total_seconds("1963-11-02T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1963-11-02T00:00:00.000000"
        actual = self.cuc.utc_string(184118402.698402)
        self.assertEqual(actual, expected)

    def test_1963_12_31_utc(self):
        """
        Tests the total seconds from January 1, 1958, to December 31, 1963.

        As of Dec. 31, 1963, the UTC-TAI difference was calculated as follows:
        days: 364
        offset: 1.9458580 + (365 + 364) * 0.0011232 = 2.7646708
        total: ((365 * (1963 - 1958)) + 364 + 1) * 86400 + 2.7646708 = 189216002.7646708 s
        """
        expected = gmpy2.mpfr("189216002.7646708")
        actual = self.cuc.get_total_seconds("1963-12-31T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1963-12-31T00:00:00.000000"
        actual = self.cuc.utc_string(189216002.7646708)
        self.assertEqual(actual, expected)

    def test_1964_01_01_utc(self):
        """
        Tests the total seconds from January 1, 1958, to Jan 1, 1964.

        As of Jan. 1, 1964, the UTC-TAI difference was calculated as follows:
        days: 0
        offset: 3.2401300 + (-366 + 0) * 0.001296 = 2.765794
        total: ((365 * (1964 - 1958)) + 0 + 1) * 86400 + 2.765794 = 189302402.765794 s
        """
        expected = gmpy2.mpfr("189302402.765794")
        actual = self.cuc.get_total_seconds("1964-01-01T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1964-01-01T00:00:00.000000"
        actual = self.cuc.utc_string(189302402.765794)
        self.assertEqual(actual, expected)

    def test_1964_01_02_utc(self):
        """
        Tests the total seconds from January 1, 1958, to Jan 2, 1964.

        As of Jan. 2, 1964, the UTC-TAI difference was calculated as follows:
        days: 1
        offset: 3.2401300 + (-366 + 1) * 0.001296 = 2.76709
        total: ((365 * (1964 - 1958)) + 1 + 1) * 86400 + 2.76709 = 189388802.76709 s
        """
        expected = gmpy2.mpfr("189388802.76709")
        actual = self.cuc.get_total_seconds("1964-01-02T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1964-01-02T00:00:00.000000"
        actual = self.cuc.utc_string(189388802.76709)
        self.assertEqual(actual, expected)

    def test_1964_03_31_utc(self):
        """
        Tests the total seconds from January 1, 1958, to March 31, 1964.

        As of Mar. 31, 1964, the UTC-TAI difference was calculated as follows:
        days: 31 + 29 + 30 = 90
        offset: 3.2401300 + (-366 + 90) * 0.001296 = 2.882434
        total: ((365 * (1964 - 1958)) + 90 + 1) * 86400 + 2.882434 = 197078402.882434 s
        """
        expected = gmpy2.mpfr("197078402.882434")
        actual = self.cuc.get_total_seconds("1964-03-31T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1964-03-31T00:00:00.000000"
        actual = self.cuc.utc_string(197078402.882434)
        self.assertEqual(actual, expected)

    def test_1964_04_01_utc(self):
        """
        Tests the total seconds from January 1, 1958, to April 1, 1964.

        As of Apr. 1, 1964, the UTC-TAI difference was calculated as follows:
        days: 31 + 29 + 31 = 91
        offset: 3.3401300 + (-366 + 91) * 0.001296 = 2.98373
        total: ((365 * (1964 - 1958)) + 91 + 1) * 86400 + 2.98373 = 197164802.98373 s
        """
        expected = gmpy2.mpfr("197164802.98373")
        actual = self.cuc.get_total_seconds("1964-04-01T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1964-04-01T00:00:00.000000"
        actual = self.cuc.utc_string(197164802.98373)
        self.assertEqual(actual, expected)

    def test_1964_04_02_utc(self):
        """
        Tests the total seconds from January 1, 1958, to April 2, 1964.

        As of Apr. 2, 1964, the UTC-TAI difference was calculated as follows:
        days: 31 + 29 + 31 + 1 = 92
        offset: 3.3401300 + (-366 + 92) * 0.001296 = 2.985026
        total: ((365 * (1964 - 1958)) + 92 + 1) * 86400 + 2.985026 = 197251202.985026 s
        """
        expected = gmpy2.mpfr("197251202.985026")
        actual = self.cuc.get_total_seconds("1964-04-02T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1964-04-02T00:00:00.000000"
        actual = self.cuc.utc_string(197251202.985026)
        self.assertEqual(actual, expected)

    def test_1964_08_31_utc(self):
        """
        Tests the total seconds from January 1, 1958, to August 31, 1964.

        As of Aug. 31, 1964, the UTC-TAI difference was calculated as follows:
        days: 31 + 29 + 31 + 30 + 31 + 30 + 31 + 30 = 243
        offset: 3.3401300 + (-366 + 243) * 0.001296 = 3.180722
        total: ((365 * (1964 - 1958)) + 243 + 1) * 86400 + 3.180722 = 210297603.180722 s
        """
        expected = gmpy2.mpfr("210297603.180722")
        actual = self.cuc.get_total_seconds("1964-08-31T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1964-08-31T00:00:00.000000"
        actual = self.cuc.utc_string(210297603.180722)
        self.assertEqual(actual, expected)

    def test_1964_09_01_utc(self):
        """
        Tests the total seconds from January 1, 1958, to September 1, 1964.

        As of Sep. 31, 1964, the UTC-TAI difference was calculated as follows:
        days: 31 + 29 + 31 + 30 + 31 + 30 + 31 + 31 = 244
        offset: 3.4401300 + (-366 + 244) * 0.001296 = 3.282018
        total: ((365 * (1964 - 1958)) + 244 + 1) * 86400 + 3.282018 = 210384003.282018 s
        """
        expected = gmpy2.mpfr("210384003.282018")
        actual = self.cuc.get_total_seconds("1964-09-01T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1964-09-01T00:00:00.000000"
        actual = self.cuc.utc_string(210384003.282018)
        self.assertEqual(actual, expected)

    def test_1964_09_02_utc(self):
        """
        Tests the total seconds from January 1, 1958, to September 2, 1964.

        As of Sep. 31, 1964, the UTC-TAI difference was calculated as follows:
        days: 31 + 29 + 31 + 30 + 31 + 30 + 31 + 31 + 1= 245
        offset: 3.4401300 + (-366 + 245) * 0.001296 = 3.283314
        total: ((365 * (1964 - 1958)) + 245 + 1) * 86400 + 3.283314 = 210470403.283314 s
        """
        expected = gmpy2.mpfr("210470403.283314")
        actual = self.cuc.get_total_seconds("1964-09-02T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1964-09-02T00:00:00.000000"
        actual = self.cuc.utc_string(210470403.283314)
        self.assertEqual(actual, expected)

    def test_1964_12_31_utc(self):
        """
        Tests the total seconds from January 1, 1958, to December 31, 1964.

        As of Dec. 31, 1964, the UTC-TAI difference was calculated as follows:
        days: 365
        offset: 3.4401300 + (-366 + 365) * 0.001296 = 3.438834
        total: ((365 * (1964 - 1958)) + 365 + 1) * 86400 + 3.438834 = 220838403.438834 s
        """
        expected = gmpy2.mpfr("220838403.438834")
        actual = self.cuc.get_total_seconds("1964-12-31T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1964-12-31T00:00:00.000000"
        actual = self.cuc.utc_string(220838403.438834)
        self.assertEqual(actual, expected)

    def test_1965_01_01_utc(self):
        """
        Tests the total seconds from January 1, 1958, to January 1, 1965.

        As of Jan. 1, 1965, the UTC-TAI difference was calculated as follows:
        days: 0
        offset: 3.5401300 + 0 * 0.001296 = 3.54013
        total: ((365 * (1965 - 1958)) + 0 + 2) * 86400 + 3.54013 = 220924803.54013 s
        """
        expected = gmpy2.mpfr("220924803.54013")
        actual = self.cuc.get_total_seconds("1965-01-01T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1965-01-01T00:00:00.000000"
        actual = self.cuc.utc_string(220924803.54013)
        self.assertEqual(actual, expected)

    def test_1965_01_02_utc(self):
        """
        Tests the total seconds from January 1, 1958, to January 2, 1965.

        As of Jan. 2, 1965, the UTC-TAI difference was calculated as follows:
        days: 1
        offset: 3.5401300 + 1 * 0.001296 = 3.541426
        total: ((365 * (1965 - 1958)) + 1 + 2) * 86400 + 3.541426 = 221011203.541426 s
        """
        expected = gmpy2.mpfr("221011203.541426")
        actual = self.cuc.get_total_seconds("1965-01-02T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1965-01-02T00:00:00.000000"
        actual = self.cuc.utc_string(221011203.541426)
        self.assertEqual(actual, expected)

    def test_1965_02_28_utc(self):
        """
        Tests the total seconds from January 1, 1958, to February 28, 1965.

        As of Feb. 28, 1965, the UTC-TAI difference was calculated as follows:
        days: 31 + 27 = 58
        offset: 3.5401300 + 58 * 0.001296 = 3.615298
        total: ((365 * (1965 - 1958)) + 58 + 2) * 86400 + 3.615298 = 225936003.615298 s
        """
        expected = gmpy2.mpfr("225936003.615298")
        actual = self.cuc.get_total_seconds("1965-02-28T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1965-02-28T00:00:00.000000"
        actual = self.cuc.utc_string(225936003.615298)
        self.assertEqual(actual, expected)

    def test_1965_03_01_utc(self):
        """
        Tests the total seconds from January 1, 1958, to March 1, 1965.

        As of Mar. 1, 1965, the UTC-TAI difference was calculated as follows:
        days: 31 + 28 = 59
        offset: 3.6401300 + 59 * 0.001296 = 3.716594
        total: ((365 * (1965 - 1958)) + 59 + 2) * 86400 + 3.716594 = 226022403.716594 s
        """
        expected = gmpy2.mpfr("226022403.716594")
        actual = self.cuc.get_total_seconds("1965-03-01T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1965-03-01T00:00:00.000000"
        actual = self.cuc.utc_string(226022403.716594)
        self.assertEqual(actual, expected)

    def test_1965_03_02_utc(self):
        """
        Tests the total seconds from January 1, 1958, to March 2, 1965.

        As of Mar. 2, 1965, the UTC-TAI difference was calculated as follows:
        days: 31 + 28 + 1 = 60
        offset: 3.6401300 + 60 * 0.001296 = 3.71789
        total: ((365 * (1965 - 1958)) + 60 + 2) * 86400 + 3.71789 = 226108803.71789 s
        """
        expected = gmpy2.mpfr("226108803.71789")
        actual = self.cuc.get_total_seconds("1965-03-02T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1965-03-02T00:00:00.000000"
        actual = self.cuc.utc_string(226108803.71789)
        self.assertEqual(actual, expected)

    def test_1965_06_30_utc(self):
        """
        Tests the total seconds from January 1, 1958, to June 30, 1965.

        As of Jun. 30, 1965, the UTC-TAI difference was calculated as follows:
        days: 31 + 28 + 31 + 30 + 31 + 29 = 180
        offset: 3.6401300 + 180 * 0.001296 = 3.87341
        total: ((365 * (1965 - 1958)) + 180 + 2) * 86400 + 3.87341 = 236476803.87341 s
        """
        expected = gmpy2.mpfr("236476803.87341")
        actual = self.cuc.get_total_seconds("1965-06-30T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1965-06-30T00:00:00.000000"
        actual = self.cuc.utc_string(236476803.87341)
        self.assertEqual(actual, expected)

    def test_1965_07_01_utc(self):
        """
        Tests the total seconds from January 1, 1958, to July 1, 1965.

        As of Jul. 1, 1965, the UTC-TAI difference was calculated as follows:
        days: 31 + 28 + 31 + 30 + 31 + 30 = 181
        offset: 3.7401300 + 181 * 0.001296 = 3.974706
        total: ((365 * (1965 - 1958)) + 181 + 2) * 86400 + 3.974706 = 236563203.974706 s
        """
        expected = gmpy2.mpfr("236563203.974706")
        actual = self.cuc.get_total_seconds("1965-07-01T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1965-07-01T00:00:00.000000"
        actual = self.cuc.utc_string(236563203.974706)
        self.assertEqual(actual, expected)

    def test_1965_07_02_utc(self):
        """
        Tests the total seconds from January 1, 1958, to July 21, 1965.

        As of Jul. 1, 1965, the UTC-TAI difference was calculated as follows:
        days: 31 + 28 + 31 + 30 + 31 + 30 + 1 = 182
        offset: 3.7401300 + 182 * 0.001296 = 3.976002
        total: ((365 * (1965 - 1958)) + 182 + 2) * 86400 + 3.976002 = 236649603.976002 s
        """
        expected = gmpy2.mpfr("236649603.976002")
        actual = self.cuc.get_total_seconds("1965-07-02T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1965-07-02T00:00:00.000000"
        actual = self.cuc.utc_string(236649603.976002)
        self.assertEqual(actual, expected)

    def test_1965_08_31_utc(self):
        """
        Tests the total seconds from January 1, 1958, to August 31, 1965.

        As of Aug. 31, 1965, the UTC-TAI difference was calculated as follows:
        days: 31 + 28 + 31 + 30 + 31 + 30 + 31 + 30 = 242
        offset: 3.7401300 + 242 * 0.001296 = 4.053762
        total: ((365 * (1965 - 1958)) + 242 + 2) * 86400 + 4.053762 = 241833604.053762 s
        """
        expected = gmpy2.mpfr("241833604.053762")
        actual = self.cuc.get_total_seconds("1965-08-31T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1965-08-31T00:00:00.000000"
        actual = self.cuc.utc_string(241833604.053762)
        self.assertEqual(actual, expected)

    def test_1965_09_01_utc(self):
        """
        Tests the total seconds from January 1, 1958, to September 1, 1965.

        As of Sep. 1, 1965, the UTC-TAI difference was calculated as follows:
        days: 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 = 243
        offset: 3.8401300 + 243 * 0.001296 = 4.155058
        total: ((365 * (1965 - 1958)) + 243 + 2) * 86400 + 4.155058 = 241920004.155058 s
        """
        expected = gmpy2.mpfr("241920004.155058")
        actual = self.cuc.get_total_seconds("1965-09-01T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1965-09-01T00:00:00.000000"
        actual = self.cuc.utc_string(241920004.155058)
        self.assertEqual(actual, expected)

    def test_1965_09_02_utc(self):
        """
        Tests the total seconds from January 1, 1958, to September 1, 1965.

        As of Sep. 1, 1965, the UTC-TAI difference was calculated as follows:
        days: 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 1 = 244
        offset: 3.8401300 + 244 * 0.001296 = 4.156354
        total: ((365 * (1965 - 1958)) + 244 + 2) * 86400 + 4.156354 = 242006404.156354 s
        """
        expected = gmpy2.mpfr("242006404.156354")
        actual = self.cuc.get_total_seconds("1965-09-02T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1965-09-02T00:00:00.000000"
        actual = self.cuc.utc_string(242006404.156354)
        self.assertEqual(actual, expected)

    def test_1965_12_31_utc(self):
        """
        Tests the total seconds from January 1, 1958, to December 31, 1965.

        As of Dec. 31, 1965, the UTC-TAI difference was calculated as follows:
        days: 364
        offset: 3.8401300 + 364 * 0.001296 = 4.311874
        total: ((365 * (1965 - 1958)) + 364 + 2) * 86400 + 4.311874 = 252374404.311874 s
        """
        expected = gmpy2.mpfr("252374404.311874")
        actual = self.cuc.get_total_seconds("1965-12-31T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1965-12-31T00:00:00.000000"
        actual = self.cuc.utc_string(252374404.311874)
        self.assertEqual(actual, expected)

    def test_1966_01_01_utc(self):
        """
        Tests the total seconds from January 1, 1958, to January 1, 1966.

        As of Jan. 1, 1966, the UTC-TAI difference was calculated as follows:
        days: 0
        offset: 4.3131700 + 0 * 0.002592 = 4.3131700
        total: ((365 * (1966 - 1958)) + 0 + 2) * 86400 + 4.3131700 = 252460804.31317 s
        """
        expected = gmpy2.mpfr("252460804.31317")
        actual = self.cuc.get_total_seconds("1966-01-01T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1966-01-01T00:00:00.000000"
        actual = self.cuc.utc_string(252460804.31317)
        self.assertEqual(actual, expected)

    def test_1966_01_02_utc(self):
        """
        Tests the total seconds from January 1, 1958, to January 2, 1966.

        As of Jan. 2, 1966, the UTC-TAI difference was calculated as follows:
        days: 1
        offset: 4.3131700 + 1 * 0.002592 = 4.315762
        total: ((365 * (1966 - 1958)) + 1 + 2) * 86400 + 4.315762 = 252547204.315762 s
        """
        expected = gmpy2.mpfr("252547204.315762")
        actual = self.cuc.get_total_seconds("1966-01-02T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1966-01-02T00:00:00.000000"
        actual = self.cuc.utc_string(252547204.315762)
        self.assertEqual(actual, expected)

    def test_1968_01_31_utc(self):
        """
        Tests the total seconds from January 1, 1958, to January 31, 1968.

        As of Jan. 31, 1966, the UTC-TAI difference was calculated as follows:
        days: 30
        offset: 4.3131700 + (365 + 365 + 30) * 0.002592 = 6.28309
        total: ((365 * (1968 - 1958)) + 30 + 2) * 86400 + 6.28309 = 318124806.28309 s
        """
        expected = gmpy2.mpfr("318124806.28309")
        actual = self.cuc.get_total_seconds("1968-01-31T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1968-01-31T00:00:00.000000"
        actual = self.cuc.utc_string(318124806.28309)
        self.assertEqual(actual, expected)

    def test_1968_02_01_utc(self):
        """
        Tests the total seconds from January 1, 1958, to February 1, 1968.

        As of Feb. 1, 1968, the UTC-TAI difference was calculated as follows:
        days: 31
        offset: 4.2131700 + (365 + 365 + 31) * 0.002592 = 6.185682
        total: ((365 * (1968 - 1958)) + 31 + 2) * 86400 + 6.185682 = 318211206.185682 s
        """
        expected = gmpy2.mpfr("318211206.185682")
        actual = self.cuc.get_total_seconds("1968-02-01T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1968-02-01T00:00:00.000000"
        actual = self.cuc.utc_string(318211206.185682)
        self.assertEqual(actual, expected)

    def test_1968_02_02_utc(self):
        """
        Tests the total seconds from January 1, 1958, to February 1, 1968.

        As of Feb. 2, 1968, the UTC-TAI difference was calculated as follows:
        days: 31 + 1 = 32
        offset: 4.2131700 + (365 + 365 + 32) * 0.002592 = 6.188274
        total: ((365 * (1968 - 1958)) + 32 + 2) * 86400 + 6.188274 = 318297606.188274 s
        """
        expected = gmpy2.mpfr("318297606.188274")
        actual = self.cuc.get_total_seconds("1968-02-02T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1968-02-02T00:00:00.000000"
        actual = self.cuc.utc_string(318297606.188274)
        self.assertEqual(actual, expected)

    def test_1971_12_31_utc(self):
        """
        Tests the total seconds from January 1, 1958, to December 31, 1971.

        As of Dec. 31, 1971, the UTC-TAI difference was calculated as follows:
        days: 364
        offset: 4.2131700 + ((1971 - 1966) * 365 + 1 + 364) * 0.002592 = 9.88965
        total: (((1971 - 1958) * 365) + 364 + 3) * 86400 + 9.88965 = 441676809.88965 s
        """
        expected = gmpy2.mpfr("441676809.88965")
        actual = self.cuc.get_total_seconds("1971-12-31T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1971-12-31T00:00:00.000000"
        actual = self.cuc.utc_string(441676809.88965)
        self.assertEqual(actual, expected)

    def test_1972_01_01_utc(self):
        """
        As of Jan. 1, 1972, the differences between UTC and TAI was defined as
        10 seconds. Considering leap years, 1960, 1964, and 1968 are included
        between 1958 and 1972. The total number of days between 1958 and 1972
        is calculated by multiplying the number of years by 365 and adding
        3 days for the leap years.
        The total elapsed time is calculated as follows:
        (((1972 - 1958) * 365) + 3) * 86400 + 10 = 441763210 seconds
        """
        expected = gmpy2.mpfr("441763210")
        actual = self.cuc.get_total_seconds("1972-01-01T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1972-01-01T00:00:00.000000"
        actual = self.cuc.utc_string(441763210)
        self.assertEqual(actual, expected)

    def test_1972_01_02_utc(self):
        """
        Tests the total seconds from January 1, 1958, to January 2, 1972.

        As of Jan. 2, 1972, the UTC-TAI difference was calculated as follows:
        days: 1
        offset: 10
        total: (((1972 - 1958) * 365) + 1 + 3) * 86400 + 10 = 441676809.88965 s
        """
        expected = gmpy2.mpz("441849610")
        actual = self.cuc.get_total_seconds("1972-01-02T00:00:00Z")
        self.assertAlmostEqual(actual, expected, delta=self.delta)

        expected = "1972-01-02T00:00:00.000000"
        actual = self.cuc.utc_string(441849610)
        self.assertEqual(actual, expected)

    def test_leap_seconds(self):
        """
        Function to test if there is a 2-second difference before and after
        a leap second insertion
        """
        targets = [
            "1972-07-01",
            "1973-01-01",
            "1974-01-01",
            "1975-01-01",
            "1976-01-01",
            "1977-01-01",
            "1978-01-01",
            "1979-01-01",
            "1980-01-01",
            "1981-07-01",
            "1982-07-01",
            "1983-07-01",
            "1985-07-01",
            "1988-01-01",
            "1990-01-01",
            "1991-01-01",
            "1992-07-01",
            "1993-07-01",
            "1994-07-01",
            "1996-01-01",
            "1997-07-01",
            "1999-01-01",
            "2006-01-01",
            "2009-01-01",
            "2012-07-01",
            "2015-07-01",
            "2017-01-01",
        ]
        expected = 2
        for target in targets:
            utc = datetime.strptime(target, "%Y-%m-%d")
            utc -= timedelta(seconds=1)
            utcstr1 = utc.strftime("%Y-%m-%dT%H:%M:%SZ")
            utcstr2 = f"{target}T00:00:00Z"
            tai1 = self.cuc.get_total_seconds(utcstr1)
            tai2 = self.cuc.get_total_seconds(utcstr2)
            actual = tai2 - tai1
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
