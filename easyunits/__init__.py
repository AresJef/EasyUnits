"""Easy fuzzy unit ratios and conversions.

The public API is category-first. Import a singleton category object, then call
``ratio()``, ``convert()``, ``resolve_unit()``, or ``units()`` on that object:

    Length.convert(12, "inches", "ft")
    Temperature.convert(32, "fahrenheit", "celsius")
"""

from .area import Area, AreaCategory
from .base import UnitCategory
from .errors import CategoryNotFoundError, UnitError, UnitNotFoundError
from .length import Length, LengthCategory
from .mass import Mass, MassCategory, Weight
from .speed import Speed, SpeedCategory
from .temperature import Temperature, TemperatureCategory
from .time import Time, TimeCategory
from .volume import Volume, VolumeCategory

__all__ = [
    "Area",
    "AreaCategory",
    "CategoryNotFoundError",
    "Length",
    "LengthCategory",
    "Mass",
    "MassCategory",
    "Speed",
    "SpeedCategory",
    "Temperature",
    "TemperatureCategory",
    "Time",
    "TimeCategory",
    "UnitError",
    "UnitNotFoundError",
    "UnitCategory",
    "Volume",
    "VolumeCategory",
    "Weight",
]
