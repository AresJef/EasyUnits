"""Exception types raised by easyunits."""


class UnitError(ValueError):
    """Base exception for unit conversion failures.

    All easyunits-specific conversion errors inherit from this class, making it
    convenient to catch library errors without catching unrelated ``ValueError``
    exceptions.
    """


class CategoryNotFoundError(UnitError):
    """Raised when a category name or alias cannot be resolved.

    This error is retained for applications that build their own category
    registries on top of ``UnitCategory``.
    """


class UnitNotFoundError(UnitError):
    """Raised when a unit name or alias cannot be resolved.

    The error is category-specific: a unit may be valid in one category but
    invalid in another, such as ``"m"`` in length versus time.
    """
