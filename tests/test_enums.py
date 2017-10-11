"""
Test Enums
"""

from prana.constants import MULTIPLIER_CORRIDOR_MAIN, LIGHT_WATTS
from prana.enums import CorridorCategory, ApplianceCategory


def test_has_choices():
    """
    Does the given enums have choices properly applied?
    """
    assert hasattr(CorridorCategory, "CHOICES")
    assert hasattr(ApplianceCategory, "CHOICES")


def test_CorridorCategory_multiplier():
    """
    Test if corridor category returns proper multiplier
    """
    assert MULTIPLIER_CORRIDOR_MAIN == \
        CorridorCategory.multiplier(CorridorCategory.MAIN)


def test_ApplianceCategory_watts():
    """
    Test if ApplianceCategory returns proper watts
    """
    assert LIGHT_WATTS == \
        ApplianceCategory.watts(ApplianceCategory.LIGHT)
