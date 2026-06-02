"""Time unit category.

The public ``Time`` object converts common duration units. Conversion factors
are stored relative to seconds.
"""

from .base import UnitCategory


class TimeCategory(UnitCategory):
    """Time category implementation.

    The category base unit is ``second``. Values in ``UNITS`` are factors that
    convert each unit to seconds.

    Examples:
        >>> Time.convert(2, "hours", "minutes")
        120.0
        >>> Time.ratio("hour", "minute")
        60.0
    """

    NAME = "time"
    BASE_UNIT = "second"
    ALIASES = ("duration",)

    NANOSECOND = 1e-9
    MICROSECOND = 1e-6
    MILLISECOND = 0.001
    SECOND = 1.0
    MINUTE = 60.0
    HOUR = 3600.0
    DAY = 86400.0
    WEEK = 604800.0
    YEAR = 31557600.0

    UNITS = {
        "nanosecond": NANOSECOND,
        "microsecond": MICROSECOND,
        "millisecond": MILLISECOND,
        "second": SECOND,
        "minute": MINUTE,
        "hour": HOUR,
        "day": DAY,
        "week": WEEK,
        "year": YEAR,
    }
    UNIT_ALIASES = {
        "nanosecond": ("ns", "nanoseconds"),
        "microsecond": ("us", "µs", "μs", "microseconds"),
        "millisecond": ("ms", "milliseconds"),
        "second": ("s", "sec", "secs", "seconds"),
        "minute": ("min", "mins", "minutes"),
        "hour": ("h", "hr", "hrs", "hours"),
        "day": ("d", "days"),
        "week": ("wk", "wks", "weeks"),
        "year": ("yr", "yrs", "years"),
    }


Time = TimeCategory()

__all__ = ["Time", "TimeCategory"]
