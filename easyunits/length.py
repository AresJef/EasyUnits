"""Length unit category.

The public ``Length`` object converts common metric, imperial, and nautical
length units. Conversion factors are stored relative to meters.
"""

from .base import UnitCategory


class LengthCategory(UnitCategory):
    """Length category implementation.

    The category base unit is ``meter``. Values in ``UNITS`` are factors that
    convert each unit to meters. Public callers normally use the module-level
    singleton ``Length`` rather than instantiating this class directly.

    Examples:
        >>> Length.convert(12, "inches", "ft")
        1.0
        >>> Length.ratio("inch", "cm")
        2.54
    """

    NAME = "length"
    BASE_UNIT = "meter"
    ALIASES = ("distance",)

    METER = 1.0
    KILOMETER = 1000.0
    CENTIMETER = 0.01
    MILLIMETER = 0.001
    MICROMETER = 1e-6
    NANOMETER = 1e-9
    INCH = 0.0254
    FOOT = 0.3048
    YARD = 0.9144
    MILE = 1609.344
    NAUTICAL_MILE = 1852.0

    UNITS = {
        "meter": METER,
        "kilometer": KILOMETER,
        "centimeter": CENTIMETER,
        "millimeter": MILLIMETER,
        "micrometer": MICROMETER,
        "nanometer": NANOMETER,
        "inch": INCH,
        "foot": FOOT,
        "yard": YARD,
        "mile": MILE,
        "nautical_mile": NAUTICAL_MILE,
    }
    UNIT_ALIASES = {
        "meter": ("m", "metre", "meters", "metres"),
        "kilometer": ("km", "kilometre", "kilometers", "kilometres"),
        "centimeter": ("cm", "centimetre", "centimeters", "centimetres"),
        "millimeter": ("mm", "millimetre", "millimeters", "millimetres"),
        "micrometer": ("um", "µm", "μm", "micron", "microns", "micrometre", "micrometers", "micrometres"),
        "nanometer": ("nm", "nanometre", "nanometers", "nanometres"),
        "inch": ("in", "in.", "inches", '"'),
        "foot": ("ft", "feet", "'"),
        "yard": ("yd", "yards"),
        "mile": ("mi", "miles"),
        "nautical_mile": ("nmi", "nautical mile", "nautical miles"),
    }


Length = LengthCategory()

__all__ = ["Length", "LengthCategory"]
