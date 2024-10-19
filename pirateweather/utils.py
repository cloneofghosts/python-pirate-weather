"""Utilities for the Pirate Weather library."""


class UnicodeMixin:
    """Mixin class to handle defining the proper __str__/__unicode__ methods in Python 3."""

    def __str__(self):
        """Return the unicode representation of the object for Python 3 compatibility."""
        return self.__unicode__()
