"""Area unit category.

The public ``Area`` object converts common metric, imperial, and land-area
units. Conversion factors are stored relative to square meters.
"""

from .base import UnitCategory


class AreaCategory(UnitCategory):
    """Area category implementation.

    The category base unit is ``square_meter``. Values in ``UNITS`` are factors
    that convert each unit to square meters.

    Examples:
        >>> Area.convert(1, "acre", "square meter")
        4046.8564224
        >>> Area.ratio("square foot", "square inch")
        144.0
    """

    NAME = "area"
    BASE_UNIT = "square_meter"

    SQUARE_METER = 1.0
    SQUARE_KILOMETER = 1_000_000.0
    SQUARE_CENTIMETER = 0.0001
    SQUARE_FOOT = 0.09290304
    SQUARE_INCH = 0.00064516
    ACRE = 4046.8564224
    HECTARE = 10000.0

    UNITS = {
        "square_meter": SQUARE_METER,
        "square_kilometer": SQUARE_KILOMETER,
        "square_centimeter": SQUARE_CENTIMETER,
        "square_foot": SQUARE_FOOT,
        "square_inch": SQUARE_INCH,
        "acre": ACRE,
        "hectare": HECTARE,
    }
    UNIT_ALIASES = {
        "square_meter": ("m2", "m^2", "sqm", "sq m", "square meter", "square meters", "square metre", "square metres"),
        "square_kilometer": ("km2", "km^2", "sq km", "square kilometer", "square kilometers", "square kilometre", "square kilometres"),
        "square_centimeter": ("cm2", "cm^2", "sq cm", "square centimeter", "square centimeters", "square centimetre", "square centimetres"),
        "square_foot": ("ft2", "ft^2", "sq ft", "square foot", "square feet"),
        "square_inch": ("in2", "in^2", "sq in", "square inch", "square inches"),
        "acre": ("ac", "acres"),
        "hectare": ("ha", "hectares"),
    }


Area = AreaCategory()

__all__ = ["Area", "AreaCategory"]
