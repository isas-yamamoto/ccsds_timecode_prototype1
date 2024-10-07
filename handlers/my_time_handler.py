import logging
import gmpy2
from collections import namedtuple
from datetime import datetime, timedelta, timezone
from .time_handler_base import TimeHandlerBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def strptime_utc(date_string: str, format_string: str) -> datetime:
    """
    Parse a date string into a UTC datetime object.

    :param date_string: The date string to parse.
    :param format_string: The format of the date string.
    :return: A datetime object in UTC.
    :raises ValueError: If the date string cannot be parsed.
    """
    try:
        dt = datetime.strptime(date_string, format_string)
    except ValueError as e:
        logger.error("Invalid date format: %s", e)
        raise
    return dt.replace(tzinfo=timezone.utc)


class MyTimeHandler(TimeHandlerBase):
    """
    This class provides time handling features using gmpy2 for high precision calculations.
    """

    P = namedtuple("Param", "start base fixed coeff")
    params = [
        P("1961-01-01", "1961-01-01", "1.422 818 0", "0.001 296"),
        P("1961-08-01", "1961-01-01", "1.372 818 0", "0.001 296"),
        P("1962-01-01", "1962-01-01", "1.845 858 0", "0.001 123 2"),
        P("1963-11-01", "1962-01-01", "1.945 858 0", "0.001 123 2"),
        P("1964-01-01", "1965-01-01", "3.240 130 0", "0.001 296"),
        P("1964-04-01", "1965-01-01", "3.340 130 0", "0.001 296"),
        P("1964-09-01", "1965-01-01", "3.440 130 0", "0.001 296"),
        P("1965-01-01", "1965-01-01", "3.540 130 0", "0.001 296"),
        P("1965-03-01", "1965-01-01", "3.640 130 0", "0.001 296"),
        P("1965-07-01", "1965-01-01", "3.740 130 0", "0.001 296"),
        P("1965-09-01", "1965-01-01", "3.840 130 0", "0.001 296"),
        P("1966-01-01", "1966-01-01", "4.313 170 0", "0.002 592"),
        P("1968-02-01", "1966-01-01", "4.213 170 0", "0.002 592"),
        P("1972-01-01", "1972-01-01", "10.0", "0.0"),
        P("1972-07-01", "1972-01-01", "11.0", "0.0"),
        P("1973-01-01", "1972-01-01", "12.0", "0.0"),
        P("1974-01-01", "1972-01-01", "13.0", "0.0"),
        P("1975-01-01", "1972-01-01", "14.0", "0.0"),
        P("1976-01-01", "1972-01-01", "15.0", "0.0"),
        P("1977-01-01", "1972-01-01", "16.0", "0.0"),
        P("1978-01-01", "1972-01-01", "17.0", "0.0"),
        P("1979-01-01", "1972-01-01", "18.0", "0.0"),
        P("1980-01-01", "1972-01-01", "19.0", "0.0"),
        P("1981-07-01", "1972-01-01", "20.0", "0.0"),
        P("1982-07-01", "1972-01-01", "21.0", "0.0"),
        P("1983-07-01", "1972-01-01", "22.0", "0.0"),
        P("1985-07-01", "1972-01-01", "23.0", "0.0"),
        P("1988-01-01", "1972-01-01", "24.0", "0.0"),
        P("1990-01-01", "1972-01-01", "25.0", "0.0"),
        P("1991-01-01", "1972-01-01", "26.0", "0.0"),
        P("1992-07-01", "1972-01-01", "27.0", "0.0"),
        P("1993-07-01", "1972-01-01", "28.0", "0.0"),
        P("1994-07-01", "1972-01-01", "29.0", "0.0"),
        P("1996-01-01", "1972-01-01", "30.0", "0.0"),
        P("1997-07-01", "1972-01-01", "31.0", "0.0"),
        P("1999-01-01", "1972-01-01", "32.0", "0.0"),
        P("2006-01-01", "1972-01-01", "33.0", "0.0"),
        P("2009-01-01", "1972-01-01", "34.0", "0.0"),
        P("2012-07-01", "1972-01-01", "35.0", "0.0"),
        P("2015-07-01", "1972-01-01", "36.0", "0.0"),
        P("2017-01-01", "1972-01-01", "37.0", "0.0"),
    ]

    def __init__(self, epoch_str: str, precision: int = 256):
        super().__init__(epoch_str)
        self.set_precision(precision)
        self.ts_epoch = self._timestamp(self.epoch_str)
        self.ts_tai_epoch = self._timestamp("1958-01-01T00:00:00Z")

    def set_precision(self, precision: int) -> None:
        gmpy2.get_context().precision = precision

    def _tai_to_utc_offset(self, dt: datetime) -> gmpy2.mpfr:
        """
        Calculate TAI-UTC for a given datetime.

        :param dt: The datetime object to correct.
        :return: The calculated offset in seconds as a gmpy2.mpz object.

        References:
            - `RELATIONSHIP BETWEEN TAI AND UTC <https://hpiers.obspm.fr/eop-pc/index.php?index=TAI-UTC_tab&lang=en>`
            - `暦Wiki/協定世界時/1963 - 国立天文台暦計算室 <https://eco.mtk.nao.ac.jp/koyomi/wiki/B6A8C4EAC0A4B3A6BBFE2F1963.html>`
        """
        offset = gmpy2.mpz(0)
        for param in MyTimeHandler.params[::-1]:
            start = strptime_utc(param.start, "%Y-%m-%d")
            if start <= dt:
                base = strptime_utc(param.base, "%Y-%m-%d")
                seconds = gmpy2.mpz((dt - base).total_seconds())
                days = seconds / gmpy2.mpz(86400)
                offset = gmpy2.mpfr(param.fixed) + days * gmpy2.mpfr(param.coeff)
                break
        return offset

    def _timestamp(self, utc: str) -> gmpy2.mpfr:
        """
        Calculate the elapsed seconds since the epoch (1970-01-01 TAI) for the given UTC time.

        :param utc: The UTC time as a string in ISO 8601 format.
        :return: The calculated timestamp as a gmpy2.mpfr object.
        """
        if len(utc) == 10:
            utc += "T00:00:00"
        if utc.endswith("Z"):
            utc = utc[:-1]
        cols = utc.split(".")
        if len(cols) > 2:
            raise ValueError(f"Invalid UTC string format: {utc}")

        dt = strptime_utc(f"{cols[0]}", "%Y-%m-%dT%H:%M:%S")
        timestamp = gmpy2.mpz(dt.timestamp())
        frac_seconds = gmpy2.mpfr("0." + cols[1]) if len(cols) == 2 else gmpy2.mpfr(0.0)

        timestamp += self._tai_to_utc_offset(dt)
        return gmpy2.mpfr(timestamp) + frac_seconds

    def total_seconds(self, utc: str) -> gmpy2.mpfr:
        """
        Calculate the total seconds between the epoch and a given UTC time.

        :param utc: The UTC time as a string in ISO 8601 format.
        :return: The total seconds as a gmpy2.mpfr object.
        """
        return self._timestamp(utc) - self.ts_epoch

    def utc_string(self, elapsed_seconds: float) -> str:
        """
        Return a UTC string from the given elapsed seconds from the epoch.

        :param elapsed_seconds: The elapsed seconds from the epoch.
        :return: UTC string.
        """
        ts = self.ts_epoch + elapsed_seconds
        ts_utc = ts
        for param in MyTimeHandler.params[::-1]:
            if self._timestamp(param.start) - gmpy2.mpfr(param.fixed) <= ts:
                coeff = gmpy2.mpfr(param.coeff) / gmpy2.mpz("86400")
                base = self._timestamp(param.base)
                ts_utc = (ts - gmpy2.mpfr(param.fixed) + coeff * base) / (1 + coeff)
                break
        dt = datetime(1970, 1, 1) + timedelta(seconds=float(ts_utc))
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")


    def cal_to_jd(self, year: int, month: int, day: int) -> float:
        """
        Convert a calendar date to Julian Day.

        Reference:
        - SOFA iauCal2jd() function
        <http://www.iausofa.org/current_C.html>
        """
        # Earliest year allowed (4800BC)
        YEAR_MIN = -4799

        # Month lengths in days
        month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        # Preset status.
        ret = 0

        # Validate year and month.
        if year < YEAR_MIN:
            raise ValueError(f"Invalid year: {year}")

        if month < 1 or month > month:
            raise ValueError(f"Invalid month: {month}")

        # If February in a leap year, 1, otherwise 0.
        is_leap_year = (month == 2) and (
            (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        )

        # Validate day
        max_day = month_lengths[month - 1] + (1 if is_leap_year else 0)
        if day < 1 or day > max_day:
            raise ValueError(f"Invalid day: {day}")

        # Julian Day calculation
        my = int((month - 14) / 12)
        adjusted_year = year + my

        a = int((1461 * (adjusted_year + 4800)) / 4)
        b = int((367 * (month - 2 - 12 * my)) / 12)
        c = (3 * ((adjusted_year + 4900) // 100)) // 4
        modified_julian_day = a + b - c + day - 2432076

        return 2400000.5 + modified_julian_day
