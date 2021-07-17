from django.core.exceptions import *
from django.utils.translation import gettext as _

def price_validator(value: int):
    """
    Validator Function for Price of Menu Items to Check not Negative Numbers
    """

    if value < 0:
        raise ValidationError(_("Price Value Can't be Negative Number"))

def discount_validator(value: int):
    """
    Validators Function for Discount of Menu Items to Check Between 0 and 100 Numbers
    """

    if not 0 <= value <= 100:
        raise ValidationError(_("Discount Value Must Number Between 0 & 100"))

def capacity_validator(value: int):
    """
    Validator Function for Capacity of Table to Check not Zero or Negative Numbers
    """

    if value < 1:
        raise ValidationError(_("Table Capacity Can't be Zero Negative Number"))
