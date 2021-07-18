from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from cafe.models import *

# Create your models here.
class Order(models.Model):
    recepite_number = models.ForeignKey("Recepite", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    status = models.BooleanField(default=False, blank=True)

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
