"""Volume unit category.

The public ``Volume`` object converts common metric, US customary, and imperial
volume units. Conversion factors are stored relative to liters.
"""

from .base import UnitCategory


class VolumeCategory(UnitCategory):
    """Volume category implementation.

    The category base unit is ``liter``. Values in ``UNITS`` are factors that
    convert each unit to liters.

    Examples:
        >>> Volume.convert(1, "gallon", "liter")
        3.785411784
        >>> Volume.ratio("cup", "ml")
        236.5882365
    """

    NAME = "volume"
    BASE_UNIT = "liter"

    LITER = 1.0
    MILLILITER = 0.001
    CUBIC_METER = 1000.0
    CUBIC_CENTIMETER = 0.001
    TEASPOON = 0.00492892159375
    TABLESPOON = 0.01478676478125
    FLUID_OUNCE = 0.0295735295625
    CUP = 0.2365882365
    PINT = 0.473176473
    QUART = 0.946352946
    GALLON = 3.785411784
    IMPERIAL_GALLON = 4.54609

    UNITS = {
        "liter": LITER,
        "milliliter": MILLILITER,
        "cubic_meter": CUBIC_METER,
        "cubic_centimeter": CUBIC_CENTIMETER,
        "teaspoon": TEASPOON,
        "tablespoon": TABLESPOON,
        "fluid_ounce": FLUID_OUNCE,
        "cup": CUP,
        "pint": PINT,
        "quart": QUART,
        "gallon": GALLON,
        "imperial_gallon": IMPERIAL_GALLON,
    }
    UNIT_ALIASES = {
        "liter": ("l", "litre", "liters", "litres"),
        "milliliter": ("ml", "millilitre", "milliliters", "millilitres"),
        "cubic_meter": ("m3", "m^3", "cbm", "cubic meter", "cubic meters", "cubic metre", "cubic metres"),
        "cubic_centimeter": ("cm3", "cc", "cm^3", "cubic centimeter", "cubic centimeters", "cubic centimetre", "cubic centimetres"),
        "teaspoon": ("tsp", "teaspoons"),
        "tablespoon": ("tbsp", "tablespoons"),
        "fluid_ounce": ("fl oz", "floz", "fluid ounce", "fluid ounces"),
        "cup": ("cups",),
        "pint": ("pt", "pints"),
        "quart": ("qt", "quarts"),
        "gallon": ("gal", "gallons"),
        "imperial_gallon": ("imp gal", "uk gal", "imperial gallon", "imperial gallons"),
    }


Volume = VolumeCategory()

__all__ = ["Volume", "VolumeCategory"]
