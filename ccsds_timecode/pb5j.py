from datetime import datetime
from ccsds_timecode.timecode_base import CCSDS_TimeCode
from time_handler import TimeHandler

"""
Truncated Julian Day Count System (TJD)

Reference:
- NASA Technical Memorandum 80606
  A groupd Binary Time Code for Telemetry and Space Applications
  A. R. Chi
  December 1979
  <https://ntrs.nasa.gov/api/citations/19800007830/downloads/19800007830.pdf>


Table 1 NASA Parallel Grouped Binary Time Codes

      |  TJD   |  s/D   |  ms/s  |  us/ms | ns/us  |
PB-5  |  (14)  |  (17)  |  (10)  |  (10)  |  (10)  |


Table 2 Truncated Juliday Day Count System
 
TJD. TJD*1 is a day count system which is truncated from Julian
Day Number (JDN)*2 giving year and day information in four digits.
TJD has an ambiguity period of 27.379 years*3.

| Date   | TJD  | JDN     |
|--------|------|---------|
| 680524 | 0    | 2440000 |
| 691006 | 500  | 2440500 |
| 710218 | 1000 | 2441000 |
| 720702 | 1500 | 2441500 |
| 731114 | 2000 | 2442000 |
| 750329 | 2500 | 2442500 |
| 760810 | 3000 | 2443000 |
| 771223 | 3500 | 2443500 |
| 790507 | 4000 | 2444000 |
| 800918 | 4500 | 2444500 |
| 820131 | 5000 | 2445000 |
| 830615 | 5500 | 2445500 |
| 841027 | 6000 | 2446000 |
| 860311 | 6500 | 2446500 |
| 870724 | 7000 | 2447000 |
| 881205 | 7500 | 2447500 |
| 900419 | 8000 | 2448000 |
| 910901 | 8500 | 2448500 |
| 930113 | 9000 | 2449000 |
| 940528 | 9500 | 2449500 |
| 951010 |    0 | 2450000 |

*1 To convert JDN to TJD, the truncation number is 2,440,000.5.
The 0.5 day is due to the change of the epoch of a calendar day
from mid-day to midnight at Greenwich Meridian on Janualy 1, 1925.
The epoch of a Julian Day always begins mid-day.

*2 The epoch of Julian Day Number began on January 1,4713 B.C.,
which predates recorded history. It is derived from the least common
multiple of the Roman cycle of indication (15 years), the metonic
cycle (19 years), and the solar cycle
(28 years). When the these cycles all begin together in 4713 B.C.
they will not come together agin until 3267 A.D.

*3. The ambiguity period is calculated based on 1 year = 365.2422 days.
"""


class TimeCode_PB5J(CCSDS_TimeCode):
    """Implements CCSDS Time Code Format with T-Field and P-Field."""

    def __init__(
        self,
        library="my",
    ):
        super().__init__("1968-05-24T00:00:00", library)
        self.time_code_id = 0b110

    def get_p_field(self):
        """
        Get the P-field according to CCSDS CCS specification.

        Returns:
            int: The P-field as an integer value.
        """
        return None

    def get_t_field(self, utc):
        """
        Get the T-field as a byte sequence from a given UTC time.

        Args:
            utc (str): The UTC time string in ISO 8601 format.

        Returns:
            bytes: A byte sequence representing the T-field.
        """

        # JD 2449444 at noon on 1994 April 1.
        # http://www.iausofa.org/sofa_ts_c.pdf
        dt_base = datetime(1994, 4, 1, 12, 0, 0)
        jd_base = 2449444

        cols = utc.split(".")
        if cols[0][-1] == "Z":
            cols[0] = cols[0][:-1]

        dt = datetime.strptime(cols[0], "%Y-%m-%dT%H:%M:%S")
        jd = self.time_handler.cal_to_jd(dt.year, dt.month, dt.day)

        tjd = (int(jd) - 2440000) % 10000

        seconds = int((
            dt - dt.replace(hour=0, minute=0, second=0)
        ).total_seconds())

        optional = []
        if len(cols) == 2:
            for i in range(0, len(cols[1]), 3):
                c = cols[1][i:i+3]
                if len(c) != 3:
                    c += "0" * 3 - (len(c))
                optional.append(int(c, 10))
        
        data = [
            tjd >> 6,
            ((tjd << 2) & 0xFF) | (seconds >> 15),
            (seconds >> 7) & 0xFF,
            ((seconds & 0xFF) << 1),
        ]

        if len(optional) > 0:
            data[3] |= optional[1] >> 9
            data.append((optional[1] >> 1) & 0xFF)
            data.append((optional[1] & 0x01) << 7)
        
        if len(optional) > 1:
            data[5] |= optional[2] >> 3
            data.append((optional[2] & 0x07) << 5)

        if len(optional) > 2:
            data[6] |= optional[3] >> 5
            data.append(optional[3] << 3)
        
        return bytes(data)

    def unpack_time_code(self, time_code: bytes) -> tuple:
        return super().unpack_time_code(time_code)