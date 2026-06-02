import math

import pytest

import easyunits
from easyunits.base import normalize_text
from easyunits import (
    Area,
    Length,
    LengthCategory,
    Mass,
    MassCategory,
    Speed,
    Temperature,
    Time,
    UnitError,
    UnitNotFoundError,
    UnitCategory,
    Volume,
    Weight,
)


def test_normalize_text_common_fuzzy_inputs():
    assert normalize_text("cm") == "cm"
    assert normalize_text("INCHES") == "inches"
    assert normalize_text("in.") == "in"
    assert normalize_text("square meter") == "squaremeter"
    assert normalize_text("sq ft") == "sqft"
    assert normalize_text("µm") == "um"
    assert normalize_text("μm") == "um"
    assert normalize_text("  Pounds  ") == "pounds"
    assert normalize_text("m/s") == "ms"
    assert normalize_text("m^2") == "m2"
    assert normalize_text("°F") == "f"
    assert normalize_text('"') == "inch"
    assert normalize_text("'") == "foot"


def test_fuzzy_length_ratio_aliases():
    assert Length.ratio("Inch", "cm") == pytest.approx(2.54)
    assert Length.ratio("INCHES", "feet") == pytest.approx(1 / 12)
    assert Length.resolve_unit("INCHES") == "inch"
    assert Length.convert(12, "INCHES", "ft") == pytest.approx(1)


def test_weight_category_alias_and_conversion():
    assert Weight is Mass
    assert isinstance(Mass, MassCategory)
    assert Weight.convert(10, "Pounds", "kg") == pytest.approx(4.5359237)
    assert Mass.convert(16, "oz", "lb") == pytest.approx(1)
    assert Weight.ratio("lb", "oz") == pytest.approx(16)
    assert Mass.ratio("oz", "lb") == pytest.approx(1 / 16)


def test_temperature_absolute_conversion():
    assert Temperature.convert(32, "fahrenheit", "celsius") == pytest.approx(0)
    assert Temperature.convert(100, "c", "f") == pytest.approx(212)
    assert Temperature.convert(0, "celsius", "kelvin") == pytest.approx(273.15)


def test_temperature_affine_path_matches_callable_maps():
    for source in Temperature.units():
        for target in Temperature.units():
            for value in (-40, 0, 32, 100, 273.15):
                base_value = Temperature.TO_BASE[source](float(value))
                expected = Temperature.FROM_BASE[target](base_value)
                assert Temperature.convert(value, source, target) == pytest.approx(expected)


def test_temperature_difference_ratio():
    assert Temperature.ratio("fahrenheit", "celsius") == pytest.approx(5 / 9)
    assert Temperature.ratio("celsius", "fahrenheit") == pytest.approx(9 / 5)


def test_common_categories():
    categories = {category.NAME for category in (Length, Mass, Temperature, Area, Volume, Time, Speed)}
    assert categories >= {"length", "mass", "temperature", "area", "volume", "time", "speed"}
    assert "meter" in Length.units()
    assert "pound" in Weight.units()


def test_area_volume_time_speed():
    assert Area.convert(1, "acre", "square meter") == pytest.approx(4046.8564224)
    assert Area.ratio("square foot", "square inch") == pytest.approx(144)
    assert Volume.convert(1, "gallon", "liter") == pytest.approx(3.785411784)
    assert Volume.ratio("cup", "ml") == pytest.approx(236.5882365)
    assert Time.convert(2, "hours", "minutes") == pytest.approx(120)
    assert Time.ratio("hour", "minute") == pytest.approx(60)
    assert Speed.convert(60, "mph", "km/h") == pytest.approx(96.56064)
    assert Speed.ratio("m/s", "km/h") == pytest.approx(3.6)


def test_function_wrapper_api_is_removed():
    removed_names = {
        "area_ratio",
        "categories",
        "convert",
        "convert_area",
        "convert_length",
        "convert_mass",
        "convert_speed",
        "convert_temperature",
        "convert_time",
        "convert_volume",
        "convert_weight",
        "length_ratio",
        "mass_ratio",
        "ratio",
        "rebuild_indexes",
        "resolve_unit",
        "speed_ratio",
        "temperature_ratio",
        "time_ratio",
        "units",
        "volume_ratio",
        "weight_ratio",
    }
    assert all(not hasattr(easyunits, name) for name in removed_names)


def test_errors_are_specific():
    with pytest.raises(UnitNotFoundError):
        Length.ratio("banana", "meter")


def test_returns_floats():
    assert isinstance(Length.convert(1, "m", "cm"), float)
    assert Length.convert(1, "m", "cm") == pytest.approx(100)
    assert math.isfinite(Volume.ratio("cup", "ml"))


def test_category_classes_inherit_behavior_and_can_be_extended():
    assert isinstance(Length, LengthCategory)
    assert isinstance(Length, UnitCategory)
    assert not isinstance(UnitCategory.__dict__["convert"], classmethod)
    assert "convert" not in Length.__dict__
    assert "ratio" not in Length.__dict__
    assert "resolve_unit" not in Length.__dict__
    assert Length.INCH == pytest.approx(0.0254)
    assert Length.UNITS["inch"] == Length.INCH
    assert not hasattr(Length, "__dataclass_fields__")

    original_units = Length.UNITS
    original_aliases = Length.UNIT_ALIASES
    try:
        Length.FURLONG = 201.168
        Length.UNITS = {**Length.UNITS, "furlong": Length.FURLONG}
        Length.UNIT_ALIASES = {**Length.UNIT_ALIASES, "furlong": ("fur", "furlongs")}
        Length.rebuild_index()

        assert Length.ratio("furlong", "m") == pytest.approx(201.168)
        assert Length.convert(2, "fur", "m") == pytest.approx(402.336)
    finally:
        Length.UNITS = original_units
        Length.UNIT_ALIASES = original_aliases
        if hasattr(Length, "FURLONG"):
            delattr(Length, "FURLONG")
        Length.rebuild_index()

    with pytest.raises(UnitNotFoundError):
        Length.resolve_unit("fur")
    assert Length._ratio_cache_size == 0


def test_new_category_can_subclass_unit_category():
    class PressureCategory(UnitCategory):
        NAME = "pressure"
        BASE_UNIT = "pascal"

        PASCAL = 1.0
        BAR = 100000.0

        UNITS = {
            "pascal": PASCAL,
            "bar": BAR,
        }
        UNIT_ALIASES = {
            "pascal": ("pa", "pascals"),
            "bar": ("bars",),
        }

    Pressure = PressureCategory()

    assert "convert" not in Pressure.__dict__
    assert Pressure.resolve_unit("PA") == "pascal"
    assert Pressure.ratio("bar", "pa") == pytest.approx(100000)
    assert Pressure.convert(2, "bar", "pa") == pytest.approx(200000)


def test_alias_collisions_fail_fast():
    class BadCategory(UnitCategory):
        NAME = "bad"
        BASE_UNIT = "a"
        UNITS = {
            "a": 1.0,
            "b": 2.0,
        }
        UNIT_ALIASES = {
            "a": ("same",),
            "b": ("same",),
        }

    with pytest.raises(UnitError):
        BadCategory()


def test_unknown_alias_keys_fail_fast():
    class BadAliasKeyCategory(UnitCategory):
        NAME = "bad_alias_key"
        BASE_UNIT = "a"
        UNITS = {
            "a": 1.0,
        }
        UNIT_ALIASES = {
            "missing": ("m",),
        }

    with pytest.raises(UnitError):
        BadAliasKeyCategory()


def test_hot_path_caches_are_bounded():
    for i in range(1100):
        try:
            Length.resolve_unit(f"unknown-{i}")
        except UnitNotFoundError:
            pass
    assert len(Length._resolve_cache) <= Length.RESOLVE_CACHE_LIMIT

    for i in range(2200):
        try:
            Length.ratio("m", f"unknown-{i}")
        except UnitNotFoundError:
            pass
    assert Length._ratio_cache_size <= Length.RATIO_CACHE_LIMIT

    Length.rebuild_index()
