import logging
import gmpy2
from collections import namedtuple
from datetime import datetime, timezone
from .time_handler_base import TimeHandlerBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MyTimeHandler(TimeHandlerBase):
    """
    This class is independently implemented to provide time handling features
    using gmpy2.
    """

    def __init__(self, epoch_str, prec=100):
        self.epoch_str = epoch_str
        gmpy2.get_context().precision = prec

    def leap_second_correction(self, dt):
        # Leap second correction
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
        offset = 0
        for target in targets:
            leap = datetime.strptime(target, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            if dt < leap:
                break
            offset += 1
        return gmpy2.mpz(offset)

    def old_utc_correction(self, dt):
        """
        Reference:
        - https://hpiers.obspm.fr/eop-pc/index.php?index=TAI-UTC_tab&lang=en
        - https://eco.mtk.nao.ac.jp/koyomi/wiki/B6A8C4EAC0A4B3A6BBFE2F1963.html
        """
        P = namedtuple("Param", "start epoch fixed coeff")
        params = [
            P("1961-01-01", "1961-01-01", "1.4228180", "0.001296"),
            P("1961-08-01", "1961-01-01", "1.3728180", "0.001296"),
            P("1962-01-01", "1962-01-01", "1.8458580", "0.0011232"),
            P("1963-11-01", "1962-01-01", "1.9458580", "0.0011232"),
            P("1964-01-01", "1965-01-01", "3.2401300", "0.001296"),
            P("1964-04-01", "1965-01-01", "3.3401300", "0.001296"),
            P("1964-09-01", "1965-01-01", "3.4401300", "0.001296"),
            P("1965-01-01", "1965-01-01", "3.5401300", "0.001296"),
            P("1965-03-01", "1965-01-01", "3.6401300", "0.001296"),
            P("1965-07-01", "1965-01-01", "3.7401300", "0.001296"),
            P("1965-09-01", "1965-01-01", "3.8401300", "0.001296"),
            P("1966-01-01", "1966-01-01", "4.3131700", "0.002592"),
            P("1968-02-01", "1966-01-01", "4.2131700", "0.002592"),
        ]
        offset = gmpy2.mpz(0)
        if dt < datetime(1972, 1, 1).replace(tzinfo=timezone.utc):
            for param in params[::-1]:
                start = datetime.strptime(param.start, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                if start <= dt:
                    epoch = datetime.strptime(param.epoch, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                    seconds = gmpy2.mpz((dt - epoch).total_seconds())
                    days = seconds / gmpy2.mpz(86400)
                    offset = gmpy2.mpfr(param.fixed) + days * gmpy2.mpfr(param.coeff)
                    break
        elif dt < datetime(1972, 7, 1).replace(tzinfo=timezone.utc):
            offset = gmpy2.mpz(10)
        return offset

    def timestamp(self, utc):
        """Calculate the elapsed seconds from 1970-01-01"""
        if utc.endswith("Z"):
            utc = utc[:-1]
        cols = utc.split(".")
        dt = datetime.strptime(f"{cols[0]}", "%Y-%m-%dT%H:%M:%S").replace(
            tzinfo=timezone.utc
        )
        timestamp = gmpy2.mpz(dt.timestamp())
        frac_seconds = gmpy2.mpfr("0." + cols[1]) if len(cols) == 2 else gmpy2.mpfr(0.0)

        timestamp += self.old_utc_correction(dt)
        timestamp += self.leap_second_correction(dt)
        return gmpy2.mpfr(timestamp) + frac_seconds

    def total_seconds(self, utc):
        """Calculate the total seconds between the epoch and a given UTC time."""
        es_epoch = self.timestamp(self.epoch_str)
        es_utc = self.timestamp(utc)
        return es_utc - es_epoch
