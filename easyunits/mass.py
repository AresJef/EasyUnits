"""Mass and weight unit category.

The public ``Mass`` object converts common metric, imperial, and US customary
mass units. ``Weight`` is an alias for ``Mass`` because everyday unit
conversion usually treats weight-unit names as mass conversions.
"""

from .base import UnitCategory


class MassCategory(UnitCategory):
    """Mass category implementation.

    The category base unit is ``kilogram``. Values in ``UNITS`` are factors
    that convert each unit to kilograms. Public callers normally use the
    module-level singletons ``Mass`` or ``Weight``.

    Examples:
        >>> Weight.convert(10, "pounds", "kg")
        4.5359237
        >>> Mass.ratio("lb", "oz")
        16.0
    """

    NAME = "mass"
    BASE_UNIT = "kilogram"
    ALIASES = ("weight",)

    KILOGRAM = 1.0
    GRAM = 0.001
    MILLIGRAM = 1e-6
    METRIC_TON = 1000.0
    POUND = 0.45359237
    OUNCE = 0.028349523125
    STONE = 6.35029318
    SHORT_TON = 907.18474
    LONG_TON = 1016.0469088

    UNITS = {
        "kilogram": KILOGRAM,
        "gram": GRAM,
        "milligram": MILLIGRAM,
        "metric_ton": METRIC_TON,
        "pound": POUND,
        "ounce": OUNCE,
        "stone": STONE,
        "short_ton": SHORT_TON,
        "long_ton": LONG_TON,
    }
    UNIT_ALIASES = {
        "kilogram": ("kg", "kilograms", "kilo", "kilos"),
        "gram": ("g", "grams"),
        "milligram": ("mg", "milligrams"),
        "metric_ton": ("tonne", "tonnes", "metric ton", "metric tons", "t"),
        "pound": ("lb", "lbs", "pounds"),
        "ounce": ("oz", "ounces"),
        "stone": ("st", "stones"),
        "short_ton": ("us ton", "us tons", "short ton", "short tons"),
        "long_ton": ("imperial ton", "imperial tons", "long ton", "long tons"),
    }


Mass = MassCategory()
Weight = Mass

__all__ = ["Mass", "MassCategory", "Weight"]
