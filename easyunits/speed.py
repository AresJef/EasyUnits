"""Speed unit category.

The public ``Speed`` object converts common speed and velocity units.
Conversion factors are stored relative to meters per second.
"""

from .base import UnitCategory


class SpeedCategory(UnitCategory):
    """Speed category implementation.

    The category base unit is ``meter_per_second``. Values in ``UNITS`` are
    factors that convert each unit to meters per second.

    Examples:
        >>> Speed.convert(60, "mph", "km/h")
        96.56064
        >>> Speed.ratio("m/s", "km/h")
        3.6
    """

    NAME = "speed"
    BASE_UNIT = "meter_per_second"
    ALIASES = ("velocity",)

    METER_PER_SECOND = 1.0
    KILOMETER_PER_HOUR = 1.0 / 3.6
    MILE_PER_HOUR = 0.44704
    FOOT_PER_SECOND = 0.3048
    KNOT = 0.5144444444444445

    UNITS = {
        "meter_per_second": METER_PER_SECOND,
        "kilometer_per_hour": KILOMETER_PER_HOUR,
        "mile_per_hour": MILE_PER_HOUR,
        "foot_per_second": FOOT_PER_SECOND,
        "knot": KNOT,
    }
    UNIT_ALIASES = {
        "meter_per_second": ("m/s", "mps", "meter per second", "meters per second", "metre per second", "metres per second"),
        "kilometer_per_hour": ("km/h", "kph", "kmh", "kilometer per hour", "kilometers per hour", "kilometre per hour", "kilometres per hour"),
        "mile_per_hour": ("mph", "mi/h", "mile per hour", "miles per hour"),
        "foot_per_second": ("ft/s", "fps", "foot per second", "feet per second"),
        "knot": ("kn", "kt", "kts", "knots"),
    }


Speed = SpeedCategory()

__all__ = ["Speed", "SpeedCategory"]
