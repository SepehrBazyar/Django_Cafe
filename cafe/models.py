from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from myproject.settings import LANGUAGE_CODE, MEDIA_ROOT
from .validators import *

# Create your models here.
class Category(models.Model):
    """
    Model of Category for Menu Items with Self Relations\n
    For Example Drinks is Sub Category for Hot Drinks.
    """

    title_fa = models.CharField(max_length=25, unique=True, verbose_name=_("Persian Title"),
                                help_text=_("Enter Title of Category to Persian Language"))
    title_en = models.CharField(max_length=25, unique=True, verbose_name=_("English Title"),
                                help_text=_("Enter Title of Category to English Language"))
    root = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_("Sub Category"), help_text=_("Select Sub Category"))  # self relation
    create_timestamp = models.DateTimeField(auto_now_add=True)
    modify_timestamp = models.DateTimeField(auto_now=True)

    @property
    def title(self) -> str:
        """
        Property Method to Translate Dynamic Text String by LANGUAGE_CODE
        """

        return self.title_fa if LANGUAGE_CODE == 'fa' else self.title_en

    def __str__(self) -> str:
        return f"{self.title}"


class MenuItem(models.Model):
    """
    Model of Menu Items in Cafe Some Fields & Foreign Key to Category
    """

    category = models.ForeignKey(Category, on_delete=models.CASCADE,
        verbose_name=_("Category"), help_text=_("Please Select Category of Item"))
    title_fa = models.CharField(max_length=50, unique=True, verbose_name=_("Persian Title"),
                                help_text=_("Enter Title of Item to Persian Language"))
    title_en = models.CharField(max_length=50, unique=True, verbose_name=_("English Title"),
                                help_text=_("Enter Title of Item to English Language"))
    price = models.IntegerField(verbose_name=_("Price"), help_text=_("Please Enter Price"),
                                validators=[price_validator])
    discount = models.IntegerField(default=0, verbose_name=_("Discount Percent"),
        help_text=_("Enter Discount Percent Between 0 & 100"), validators=[discount_validator])
    image = models.FileField(upload_to="cafe/menu_items/", verbose_name=_("Picture"),
        default=f"{MEDIA_ROOT}/cafe/menu_items/default.jpg",
        help_text=_("Please Upload Picture of Item for Show in Detail Page"))
    status = models.CharField(max_length=1, default='T', verbose_name=_("Status"),
                                choices=[('T', _('Available')), ('F', _('Unavailable'))],
                                help_text=_("Status of Item Available or Unavailable"))
    create_timestamp = models.DateTimeField(auto_now_add=True)
    modify_timestamp = models.DateTimeField(auto_now=True)

    @property
    def title(self) -> str:
        """
        Property Method to Translate Dynamic Text String by LANGUAGE_CODE
        """

        return self.title_fa if LANGUAGE_CODE == 'fa' else self.title_en
    
    @property
    def final_price(self) -> int:
        """
        Property Method to Calculate Final Price by Discount Percent
        """

        return int(self.price * (1 - (self.discount / 100)))

    def __str__(self) -> str:
        return f"{self.title}: {self.final_price}$"


class Table(models.Model):
    """
    Model of Tables in Cafe Some Fields for Foreign Key from Recepites
    """

    capacity = models.IntegerField(verbose_name=_("Capacity"), validators=[price_validator],
                                    help_text=_("Please Enter Capacity of Table by Person"))
    table_name = models.CharField(max_length=2, unique=True, verbose_name=_("Name of Table"),
                                    help_text=_("Please Enter Name for Table Unique Code"))
    status = models.CharField(max_length=1, default='T', verbose_name=_("Status"),
                                choices=[('T', _('Empty')), ('F', _('Full'))],
                                help_text=_("Status of Table Empty or Full Capacity"))
    create_timestamp = models.DateTimeField(auto_now_add=True)
    modify_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id}) {self.table_name}({self.capacity} Person) - {self.status}"
