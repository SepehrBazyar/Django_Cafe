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

    recepite = models.ForeignKey("Recepite", on_delete=models.CASCADE, related_name="orders",
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

    def change_status(self, new_status: str):
        """
        Change Status of Order from Cooking to Serving after Deliver to Cotumers
        """

        REVERSE = {value: key for key, value in self.STATUSES}
        self.status = REVERSE.get(new_status, self.status)
        self.save()

    @property
    def status_name(self) -> str:
        """
        Get Human Readable Status Name
        """

        return self.__class__.STATUSES[self.status]

    def __str__(self) -> str:
        return f"{self.recepite.id}: {self.item.title} - {self.count} - {self.status_name}"

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
    status = models.CharField(max_length=1, default='U', verbose_name=_("Status"),
                                choices=[(key, value) for key, value in STATUSES.items()],
                                help_text=_("Status of Recepite Paid or Unpaid or ..."))
    create_timestamp = models.DateTimeField(auto_now_add=True)
    modify_timestamp = models.DateTimeField(auto_now=True)

    @property
    def total_price(self) -> int:
        """
        Total Price of Recepite by Sum Order Price withou Apply Discounts
        """
        
        total = 0
        for order in self.orders.all():
            total += order.count * order.item.price
        return total

    @property
    def final_price(self) -> int:
        """
        Final Price of Recepite by Sum Order Price After Apply Discounts
        """

        final = 0
        for order in self.orders.all():
            final += order.count * order.item.final_price
        return final

    @property
    def status_name(self) -> str:
        """
        Get Human Readable Status Name
        """

        return self.__class__.STATUSES[self.status]
    
    def change_status(self, new_status: str):
        """
        Change Status of Recepite after Paid Price and Empty Tables for Next Recepites
        """

        REVERSE = {value: key for key, value in self.STATUSES}
        self.status = REVERSE.get(new_status, self.status)
        self.save()

    def __str__(self) -> str:
        tab = _("Table")
        return f"{self.id}) {tab} {self.table.id} - {self.final_price} - {self.status_name}"
