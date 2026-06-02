# easyunits

Created to be used in a project, this package is published to github for ease of management and installation across different modules.

`easyunits` is a tiny performance-focused Python library for fuzzy unit ratios and conversions.

It provides category objects with inherited ratio and conversion methods:

- `{Category}.ratio(from_unit, to_unit)`: returns the multiplicative ratio between compatible units.
- `{Category}.convert(value, from_unit, to_unit)`: converts a value from one unit to another.

Temperature uses affine conversion, so `Temperature.ratio()` supports temperature differences and `Temperature.convert()` supports normal temperature values.

## Installation

From PyPI:

```bash
pip install easyunits
```

For local development from this repository:

```bash
python -m pip install -e ".[test]"
```

Run tests:

```bash
python -m pytest
```

## Examples

```python
from easyunits import Length, Temperature, Weight

Length.ratio("inch", "cm")
# 2.54

Weight.convert(10, "Pounds", "kg")
# 4.5359237

Temperature.convert(32, "fahrenheit", "celsius")
# 0.0

Length.convert(12, "INCHES", "ft")
# 1.0
```

## Categories

- `length`
- `mass` / `weight`
- `temperature`
- `area`
- `volume`
- `time`
- `speed`

Unit names are fuzzy: plural forms, case differences, punctuation, spaces, and common abbreviations are accepted. For example, `Inch`, `inch`, `INCH`, `inches`, `in.`, and `"` all resolve to inches.

## Category Objects

Each public category, such as `Length`, is a singleton object backed by a normal class, such as `LengthCategory`, that inherits from `UnitCategory`. This keeps the preferred API compact while letting shared behavior use regular instance methods instead of classmethods.

```python
from easyunits import Length, LengthCategory, UnitCategory

isinstance(Length, LengthCategory)
# True

isinstance(Length, UnitCategory)
# True

Length.INCH
# 0.0254

Length.UNITS["inch"]
# 0.0254

Length.UNIT_ALIASES["inch"]
# ("in", "in.", "inches", '"')

Length.resolve_unit("INCHES")
# "inch"

Length.ratio("inch", "cm")
# 2.54

Length.convert(12, "INCHES", "ft")
# 1.0
```

To add a unit in the library source, add a constant, a `UNITS` entry, and optional `UNIT_ALIASES` entries to the matching category class. If you add units dynamically at runtime, update the category object and call that object's `rebuild_index()` afterward so fuzzy lookup sees the new aliases and clears cached resolutions.

```python
from easyunits import Length

Length.FURLONG = 201.168
Length.UNITS = {**Length.UNITS, "furlong": Length.FURLONG}
Length.UNIT_ALIASES = {**Length.UNIT_ALIASES, "furlong": ("fur", "furlongs")}
Length.rebuild_index()

Length.convert(2, "fur", "m")
# 402.336
```

To create a new category, subclass `UnitCategory`, define `NAME`, `BASE_UNIT`, `UNITS`, and `UNIT_ALIASES`, instantiate it, then call `your_category.rebuild_index()` before using fuzzy lookup if you changed its maps after construction.

Each built-in category lives in its own module: `length.py`, `mass.py`, `temperature.py`, `area.py`, `volume.py`, `time.py`, and `speed.py`. Shared behavior lives in `base.py`, while errors live in `errors.py`.

`rebuild_index()` also checks for fuzzy alias collisions. If two units in the same category normalize to the same alias, it raises `UnitError` instead of silently overwriting one unit with another.

## Public API

Use category objects directly:

- `Length.ratio()`, `Length.convert()`
- `Mass.ratio()`, `Mass.convert()`
- `Weight.ratio()`, `Weight.convert()`
- `Temperature.ratio()`, `Temperature.convert()`
- `Area.ratio()`, `Area.convert()`
- `Volume.ratio()`, `Volume.convert()`
- `Time.ratio()`, `Time.convert()`
- `Speed.ratio()`, `Speed.convert()`
