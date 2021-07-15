from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

# Create your models here.
class Category(models.Model):
    title_fa = models.CharField(max_length=25)
    title_en = models.CharField(max_length=25)
    image_name = models.CharField(max_length=100, blank=True, null=True, default=None)
    root = models.ForeignKey("self", on_delete=models.CASCADE,
                                blank=True, null=True, default=None)  # self relation

    def __str__(self) -> str:
        return f"{_(self.title_fa)}"


class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    title_fa = models.CharField(max_length=50)
    title_en = models.CharField(max_length=50)
    image_name = models.CharField(max_length=100, blank=True, null=True, default=None)
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{_(self.title_fa)}: {int(self.price * (1 - (self.discount / 100)))}$"


class Table(models.Model):
    capacity = models.IntegerField()
    table_name = models.CharField(max_length=2)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.id}){self.table_name}({self.capacity}Person) - {self.status}"
