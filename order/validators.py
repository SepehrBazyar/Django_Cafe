from django.core.exceptions import *
from django.utils.translation import gettext as _

def count_validator(value: int):
    """
    Validator Function for Count of Orders to Check not Zero or Negative Numbers
    """

    if value < 1:
        raise ValidationError(_("Order Count Can't be Zero pr Negative Number"))
