from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from cafe.models import *
from .validators import *

# Create your models here.
class Order(models.Model):
    """
    Model of Order for Collect of Menu Items to One Recepite on Table
    """

    STATUSES = {
        'N': _("New"),
        'C': _("Cooking"),
        'S': _("Serving"),
        'D': _("Deleted"),
    }

    recepite_number = models.ForeignKey("Recepite", on_delete=models.CASCADE, related_name="orders",
        verbose_name=_("Recepite Number"), help_text=_("Please Enter Your Recepite Number"))
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, verbose_name=_("Menu Item"),
        help_text=_("Please Select Item to Add this Order to Your Recepite"))
    count = models.IntegerField(default=1, verbose_name=_("Count of Order"),
        help_text=_("Please Enter Count of Order(Minimum = 1)"), validators=[count_validator])
    status = models.CharField(max_length=1, default='N', verbose_name=_("Status"),
                                choices=[(key, value) for key, value in STATUSES.items()],
                                help_text=_("Status of Order New or Serving or ..."))
    create_timestamp = models.DateTimeField(auto_now_add=True)
    modify_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.recepite_number.id}: {_(self.menu_item.title_fa)} - {self.count}"

class Recepite(models.Model):
    """
    Model of Recepite for Collect Orders with Foreign Key to Table
    """

    STATUSES = {
        'P': _("Paid"),
        'U': _("Unpaid"),
        'D': _("Deleted"),
    }

    table = models.ForeignKey(Table, on_delete=models.CASCADE,
        verbose_name=_("Table"), help_text=_("Please Choose Table Number to Sit on it"))
    total_price = models.IntegerField(default=0, verbose_name=_("Total Price"),
        help_text=_("Please Enter Total of Price without Apply Discounts"))
    final_price = models.IntegerField(default=0, verbose_name=_("Final Price"),
        help_text=_("Please Enter Final of Price with Apply Discounts"))
    status = models.CharField(max_length=1, default='U', verbose_name=_("Status"),
                                choices=[(key, value) for key, value in STATUSES.items()],
                                help_text=_("Status of Recepite Paid or Unpaid or ..."))
    create_timestamp = models.DateTimeField(auto_now_add=True)
    modify_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id}) Table{self.table_number.id}: {self.total_price}$ - {self.time_stamp}"
