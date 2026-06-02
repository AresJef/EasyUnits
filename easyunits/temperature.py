"""Temperature unit category.

The public ``Temperature`` object converts absolute temperature values and
temperature differences. Absolute conversion uses affine formulas; difference
ratios use linear scale factors stored in ``UNITS``.
"""

from __future__ import annotations

from typing import Callable, Mapping

from .base import Number, UnitCategory


class TemperatureCategory(UnitCategory):
    """Temperature category implementation.

    The category base unit is ``kelvin``. ``UNITS`` stores scale factors for
    temperature differences, while ``TO_BASE_AFFINE`` and ``FROM_BASE_AFFINE``
    store optimized absolute-temperature conversion coefficients.

    Examples:
        >>> Temperature.convert(32, "fahrenheit", "celsius")
        0.0
        >>> Temperature.ratio("fahrenheit", "celsius")
        0.5555555555555556
    """

    NAME = "temperature"
    BASE_UNIT = "kelvin"
    ALIASES = ("temp",)

    KELVIN = 1.0
    CELSIUS = 1.0
    FAHRENHEIT = 5.0 / 9.0
    RANKINE = 5.0 / 9.0

    UNITS = {
        "kelvin": KELVIN,
        "celsius": CELSIUS,
        "fahrenheit": FAHRENHEIT,
        "rankine": RANKINE,
    }
    UNIT_ALIASES = {
        "kelvin": ("k", "kelvins"),
        "celsius": ("c", "centigrade", "°c", "deg c", "degree celsius", "degrees celsius"),
        "fahrenheit": ("f", "°f", "deg f", "degree fahrenheit", "degrees fahrenheit"),
        "rankine": ("r", "°r", "deg r", "degree rankine", "degrees rankine"),
    }
    TO_BASE: Mapping[str, Callable[[float], float]] = {
        "kelvin": lambda x: x,
        "celsius": lambda x: x + 273.15,
        "fahrenheit": lambda x: (x + 459.67) * 5.0 / 9.0,
        "rankine": lambda x: x * 5.0 / 9.0,
    }
    FROM_BASE: Mapping[str, Callable[[float], float]] = {
        "kelvin": lambda x: x,
        "celsius": lambda x: x - 273.15,
        "fahrenheit": lambda x: x * 9.0 / 5.0 - 459.67,
        "rankine": lambda x: x * 9.0 / 5.0,
    }
    TO_BASE_AFFINE = {
        "kelvin": (1.0, 0.0),
        "celsius": (1.0, 273.15),
        "fahrenheit": (5.0 / 9.0, 459.67 * 5.0 / 9.0),
        "rankine": (5.0 / 9.0, 0.0),
    }
    FROM_BASE_AFFINE = {
        "kelvin": (1.0, 0.0),
        "celsius": (1.0, -273.15),
        "fahrenheit": (9.0 / 5.0, -459.67),
        "rankine": (9.0 / 5.0, 0.0),
    }

    def convert(self, value: Number, from_unit: str, to_unit: str) -> float:
        """Convert an absolute temperature value.

        Args:
            value: Absolute temperature value to convert.
            from_unit: Source temperature unit name or alias.
            to_unit: Target temperature unit name or alias.

        Returns:
            Converted absolute temperature as ``float``.

        Raises:
            TypeError: If unit arguments are not strings or ``value`` is not
                float-like.
            ValueError: If ``value`` cannot be converted to ``float``.
            UnitNotFoundError: If either unit is unknown.
        """

        try:
            to_scale, to_offset, from_scale, from_offset = self._conversion_cache[from_unit][to_unit]
        except KeyError:
            cacheable = True
        except TypeError:
            cacheable = False
        else:
            return (float(value) * to_scale + to_offset) * from_scale + from_offset

        source_name = self.resolve_unit(from_unit)
        target_name = self.resolve_unit(to_unit)
        to_scale, to_offset = self.TO_BASE_AFFINE[source_name]
        from_scale, from_offset = self.FROM_BASE_AFFINE[target_name]
        if cacheable:
            self._cache_conversion(from_unit, to_unit, (to_scale, to_offset, from_scale, from_offset))

        return (float(value) * to_scale + to_offset) * from_scale + from_offset


Temperature = TemperatureCategory()

__all__ = ["Temperature", "TemperatureCategory"]
