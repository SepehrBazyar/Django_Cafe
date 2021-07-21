from django.db import models, connection
from django.utils import timezone
from django.utils.translation import gettext as _
from typing import List
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

    STATUSES = {
        'T': _("Available"),
        'F': _("Unavailable"),
    }

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items",
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
        default="cafe/menu_items/default.jpg",
        help_text=_("Please Upload Picture of Item for Show in Detail Page"))
    status = models.CharField(max_length=1, default='T', verbose_name=_("Status"),
                                choices=[(key, value) for key, value in STATUSES.items()],
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

    def change_price(self, new_price:int):
        """
        Change Price of Item to New Price
        """

        self.price = new_price
        self.save()

    def change_discount(self, new_discount: int):
        """
        Change Discount of Item to New Discount by Percent Between 0 & 100
        """

        self.discount = new_discount
        self.save()
    
    def change_status(self, new_status: str):
        """
        Change Status of Item by Available or Unavailable in Archive Product Menu
        """

        REVERSE = {value: key for key, value in self.STATUSES.items()}
        self.status = REVERSE.get(new_status, self.status)
        self.save()

    @classmethod
    def filter_by_category(cls, category: str):
        """
        Filter Menu Items by Category name Method Get Name String and Return Query Set
        """

        return cls.objects.filter(category__title_en=category)
    
    @classmethod
    def maximum_price(cls):
        """
        Method for Get Item with Maximum Price in All Menu Item without Apply Discount
        """

        return cls.objects.aggregate(models.Max('price'))["price__max"]

    @classmethod
    def best_sellers(cls, count: int) -> List[tuple]:
        """
        Class Method Run Raw SQL Query for Find Best Sellers Menu Items
        """

        cursor = connection.cursor()
        cursor.execute("""SELECT cafe_menuitem.id, SUM(order_order.count) AS Sellers
FROM order_order INNER JOIN cafe_menuitem ON order_order.item_id = cafe_menuitem.id
GROUP BY cafe_menuitem.id ORDER BY Sellers DESC;""")

        bests = cursor.fetchall()[: count]
        result = []
        for item in bests:
            result.append((cls.objects.get(id=item[0]), item[1]))
        return result

    def __str__(self) -> str:
        return f"{self.title}: {self.final_price}$"


class Table(models.Model):
    """
    Model of Tables in Cafe Some Fields for Foreign Key from Recepites
    """

    STATUSES = {
        'T': _("Empty"),
        'F': _("Full"),
    }

    capacity = models.IntegerField(verbose_name=_("Capacity"), validators=[capacity_validator],
                                    help_text=_("Please Enter Capacity of Table by Person"))
    table_name = models.CharField(max_length=2, unique=True, verbose_name=_("Name of Table"),
                                    help_text=_("Please Enter Name for Table Unique Code"))
    status = models.CharField(max_length=1, default='T', verbose_name=_("Status"),
                                choices=[(key, value) for key, value in STATUSES.items()],
                                help_text=_("Status of Table Empty or Full Capacity"))
    create_timestamp = models.DateTimeField(auto_now_add=True)
    modify_timestamp = models.DateTimeField(auto_now=True)

    def change_status(self, new_status: str):
        """
        Change Status of Table with Recepite is Full and without it is Empty
        """

        REVERSE = {value: key for key, value in self.STATUSES.items()}
        self.status = REVERSE.get(new_status, self.status)
        self.save()

    @property
    def status_name(self) -> str:
        """
        Get Human Readable Status Name
        """

        return self.__class__.STATUSES[self.status]

    def __str__(self) -> str:
        person = _("Person")
        return f"{self.id}) {self.table_name}({self.capacity} {person}) - {self.status_name}"
