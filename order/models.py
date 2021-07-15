from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from cafe.models import *

# Create your models here.
class Recepite(models.Model):
    table_number = models.ForeignKey(Table, on_delete=models.CASCADE)
    total_price = models.IntegerField(default=0, blank=True)
    final_price = models.IntegerField(default=0, blank=True)
    status = models.BooleanField(default=False, blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self) -> str:
        return f"{self.id}) Table{self.table_number.id}: {self.total_price}$ - {self.time_stamp}"


class Order(models.Model):
    recepite_number = models.ForeignKey(Recepite, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    status = models.BooleanField(default=False, blank=True)

    def __str__(self) -> str:
        return f"{self.recepite_number.id}: {_(self.menu_item.title_fa)} - {self.count}"
