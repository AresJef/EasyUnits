"""Shared primitives for category objects and fuzzy unit lookup.

This module contains the reusable machinery behind all public category objects
such as ``Length`` and ``Weight``. A category stores conversion factors in
``UNITS`` and fuzzy aliases in ``UNIT_ALIASES``; :class:`UnitCategory` builds
fast lookup indexes and bounded caches from those maps.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Mapping, SupportsFloat, Tuple

from .errors import UnitError, UnitNotFoundError

Number = SupportsFloat

_CLEAN_RE = re.compile(r"[^a-z0-9]+")
_DELETE_NON_ALNUM_ASCII = {
    codepoint: None
    for codepoint in range(128)
    if not (48 <= codepoint <= 57 or 65 <= codepoint <= 90 or 97 <= codepoint <= 122)
}
_DEFAULT_SYMBOL_UNITS = {
    '"': "inch",
    "'": "foot",
}


def normalize_text(value: str, symbol_units: Mapping[str, str] = _DEFAULT_SYMBOL_UNITS) -> str:
    """Normalize user-facing unit or category text for dictionary lookup.

    The normalization is intentionally simple and performance-oriented:
    whitespace around the value is stripped, ASCII text is lowercased,
    punctuation is removed, and both common micro symbols are mapped to
    ``"u"`` so ``"µm"`` and ``"μm"`` resolve like ``"um"``.

    Args:
        value: Unit or category text supplied by a caller.
        symbol_units: Exact symbol aliases to resolve before general cleanup.

    Returns:
        A compact lowercase lookup key containing only letters and digits,
        or a canonical name for exact symbol aliases such as ``"`` and ``'``.

    Raises:
        TypeError: If ``value`` is not a string.
    """

    if not isinstance(value, str):
        raise TypeError("unit and category names must be strings")

    stripped = value.strip()
    if stripped in symbol_units:
        return symbol_units[stripped]

    if stripped.isascii():
        cleaned = stripped.lower()
        if cleaned.isalnum():
            return cleaned
        if " " in cleaned:
            no_space = cleaned.replace(" ", "")
            if no_space.isalnum():
                return no_space
        return cleaned.translate(_DELETE_NON_ALNUM_ASCII)

    cleaned = stripped.casefold()
    if "µ" in cleaned or "μ" in cleaned:
        cleaned = cleaned.replace("µ", "u").replace("μ", "u")
    if cleaned.isalnum():
        return cleaned
    return _CLEAN_RE.sub("", cleaned)


class UnitCategory:
    """Base class for unit category singleton objects.

    Subclasses define category metadata, unit constants, conversion factors,
    and fuzzy aliases. Instances inherit fast ratio, conversion, resolution,
    cache, and index-rebuild behavior.

    Attributes:
        NAME: Canonical category name, such as ``"length"``.
        BASE_UNIT: Canonical base unit name for the category.
        ALIASES: Alternative category names for registry lookup.
        UNITS: Mapping of canonical unit names to factors relative to the base
            unit. Linear categories use these factors for all conversions.
        UNIT_ALIASES: Mapping of canonical unit names to accepted fuzzy aliases.
        SYMBOL_UNITS: Exact symbol aliases resolved before normalization.
        RESOLVE_CACHE_LIMIT: Maximum cached raw unit strings.
        RATIO_CACHE_LIMIT: Maximum cached unit-pair ratios.
        CONVERSION_CACHE_LIMIT: Maximum cached category-specific conversion
            payloads used by subclasses such as temperature.
    """

    __slots__ = (
        "_index",
        "_resolve_cache",
        "_ratio_cache",
        "_ratio_cache_size",
        "_conversion_cache",
        "_conversion_cache_size",
        "_units_tuple",
    )

    NAME = ""
    BASE_UNIT = ""
    ALIASES: Tuple[str, ...] = ()
    UNITS: Mapping[str, float] = {}
    UNIT_ALIASES: Mapping[str, Tuple[str, ...]] = {}
    SYMBOL_UNITS = _DEFAULT_SYMBOL_UNITS
    RESOLVE_CACHE_LIMIT = 1024
    RATIO_CACHE_LIMIT = 2048
    CONVERSION_CACHE_LIMIT = 2048

    def __init__(self) -> None:
        """Initialize lookup indexes and bounded hot-path caches."""

        self._index: Dict[str, str] = {}
        self._resolve_cache: Dict[str, str] = {}
        self._ratio_cache: Dict[str, Dict[str, float]] = {}
        self._ratio_cache_size = 0
        self._conversion_cache: Dict[str, Dict[str, Any]] = {}
        self._conversion_cache_size = 0
        self._units_tuple: Tuple[str, ...] = ()
        self.rebuild_index()

    def normalize(self, value: str) -> str:
        """Normalize text using this category's symbol aliases.

        Args:
            value: Unit text to normalize.

        Returns:
            A normalized lookup key suitable for this category's index.

        Raises:
            TypeError: If ``value`` is not a string.
        """

        return normalize_text(value, self.SYMBOL_UNITS)

    def rebuild_index(self) -> None:
        """Rebuild fuzzy lookup indexes and clear conversion caches.

        Call this after mutating ``UNITS`` or ``UNIT_ALIASES`` at runtime.
        Rebuilding also validates that every alias key points to a known unit
        and that no two units normalize to the same alias.

        Raises:
            UnitError: If aliases reference unknown units or if two units share
                the same normalized alias.
        """

        units = self.UNITS
        unknown_alias_units = set(self.UNIT_ALIASES) - set(units)
        if unknown_alias_units:
            unknown = ", ".join(sorted(unknown_alias_units))
            raise UnitError(f"{self.NAME} aliases defined for unknown units: {unknown}")

        index: Dict[str, str] = {}
        for unit_name in units:
            self._register_alias(index, unit_name, unit_name)
            for alias in self.UNIT_ALIASES.get(unit_name, ()):
                self._register_alias(index, alias, unit_name)
        self._index = index
        self._units_tuple = tuple(units)
        self._resolve_cache.clear()
        self._ratio_cache.clear()
        self._ratio_cache_size = 0
        self._conversion_cache.clear()
        self._conversion_cache_size = 0

    def resolve_unit(self, unit: str) -> str:
        """Resolve a fuzzy unit string to its canonical unit name.

        Args:
            unit: User-provided unit string, abbreviation, symbol, or alias.

        Returns:
            The canonical unit name stored in ``UNITS``.

        Raises:
            TypeError: If ``unit`` is not a string.
            UnitNotFoundError: If ``unit`` cannot be resolved in this category.
        """

        cacheable = True
        cache = self._resolve_cache
        try:
            return cache[unit]
        except KeyError:
            pass
        except TypeError:
            cacheable = False

        index = self._index
        if cacheable:
            try:
                resolved = index[unit]
            except KeyError:
                normalized = self.normalize(unit)
                try:
                    resolved = index[normalized]
                except KeyError as exc:
                    available = ", ".join(sorted(self.UNITS))
                    raise UnitNotFoundError(
                        f"unknown {self.NAME} unit {unit!r}; available: {available}"
                    ) from exc
            if len(cache) >= self.RESOLVE_CACHE_LIMIT:
                cache.clear()
            cache[unit] = resolved
            return resolved

        normalized = self.normalize(unit)
        try:
            return index[normalized]
        except KeyError as exc:
            available = ", ".join(sorted(self.UNITS))
            raise UnitNotFoundError(
                f"unknown {self.NAME} unit {unit!r}; available: {available}"
            ) from exc

    def ratio(self, from_unit: str, to_unit: str) -> float:
        """Return the multiplicative ratio between two units.

        Args:
            from_unit: Source unit name or alias.
            to_unit: Target unit name or alias.

        Returns:
            Factor that converts a value in ``from_unit`` to ``to_unit``.

        Raises:
            TypeError: If either unit is not a string.
            UnitNotFoundError: If either unit is unknown.
        """

        try:
            return self._ratio_cache[from_unit][to_unit]
        except KeyError:
            cacheable = True
        except TypeError:
            cacheable = False

        units = self.UNITS
        source_name = self.resolve_unit(from_unit)
        target_name = self.resolve_unit(to_unit)
        factor = units[source_name] / units[target_name]
        if cacheable:
            self._cache_ratio(from_unit, to_unit, factor)
        return factor

    def convert(self, value: Number, from_unit: str, to_unit: str) -> float:
        """Convert a numeric value between two linear units.

        Args:
            value: Numeric value to convert. Any object accepted by ``float()``
                is supported.
            from_unit: Source unit name or alias.
            to_unit: Target unit name or alias.

        Returns:
            Converted value as ``float``.

        Raises:
            TypeError: If a unit is not a string or ``value`` is not float-like.
            ValueError: If ``value`` cannot be converted to ``float``.
            UnitNotFoundError: If either unit is unknown.
        """

        try:
            factor = self._ratio_cache[from_unit][to_unit]
        except KeyError:
            cacheable = True
        except TypeError:
            cacheable = False
        else:
            return float(value) * factor

        if cacheable:
            units = self.UNITS
            source_name = self.resolve_unit(from_unit)
            target_name = self.resolve_unit(to_unit)
            factor = units[source_name] / units[target_name]
            self._cache_ratio(from_unit, to_unit, factor)
            return float(value) * factor

        units = self.UNITS
        source_name = self.resolve_unit(from_unit)
        target_name = self.resolve_unit(to_unit)
        return float(value) * (units[source_name] / units[target_name])

    def units(self) -> Tuple[str, ...]:
        """Return this category's supported canonical unit names.

        Returns:
            Tuple of canonical names in insertion order from ``UNITS``.
        """

        return self._units_tuple

    def _register_alias(self, index: Dict[str, str], alias: str, canonical_name: str) -> None:
        """Register a single normalized alias in an index.

        Args:
            index: Mutable alias index being built.
            alias: Raw alias text to normalize and register.
            canonical_name: Canonical unit name that ``alias`` should resolve to.

        Raises:
            UnitError: If the normalized alias already maps to another unit.
            TypeError: If ``alias`` is not a string.
        """

        normalized = self.normalize(alias)
        if normalized:
            existing = index.get(normalized)
            if existing is not None and existing != canonical_name:
                raise UnitError(
                    f"alias {alias!r} in {self.NAME} resolves to both "
                    f"{existing!r} and {canonical_name!r}"
                )
            index[normalized] = canonical_name

    def _cache_ratio(self, from_unit: str, to_unit: str, factor: float) -> None:
        """Store a multiplicative conversion factor in the bounded ratio cache.

        Args:
            from_unit: Raw source unit string used as the first cache key.
            to_unit: Raw target unit string used as the nested cache key.
            factor: Multiplicative conversion factor.
        """

        if self._ratio_cache_size >= self.RATIO_CACHE_LIMIT:
            self._ratio_cache.clear()
            self._ratio_cache_size = 0

        targets = self._ratio_cache.get(from_unit)
        if targets is None:
            self._ratio_cache[from_unit] = {to_unit: factor}
            self._ratio_cache_size += 1
            return

        if to_unit not in targets:
            self._ratio_cache_size += 1
        targets[to_unit] = factor

    def _cache_conversion(self, from_unit: str, to_unit: str, conversion: Any) -> None:
        """Store subclass-specific conversion data in a bounded cache.

        Args:
            from_unit: Raw source unit string used as the first cache key.
            to_unit: Raw target unit string used as the nested cache key.
            conversion: Cached conversion payload. The base class does not
                inspect this value; subclasses decide its structure.
        """

        if self._conversion_cache_size >= self.CONVERSION_CACHE_LIMIT:
            self._conversion_cache.clear()
            self._conversion_cache_size = 0

        targets = self._conversion_cache.get(from_unit)
        if targets is None:
            self._conversion_cache[from_unit] = {to_unit: conversion}
            self._conversion_cache_size += 1
            return

        if to_unit not in targets:
            self._conversion_cache_size += 1
        targets[to_unit] = conversion

    def __repr__(self) -> str:
        """Return a concise debug representation for the category object."""

        return f"<{self.__class__.__name__} name={self.NAME!r}>"
