from django.shortcuts import render, HttpResponse, redirect
from django.views import View, generic
from django.utils.translation import gettext as _
from cafe.models import Category, MenuItem, Table

# Create your views here.
class MenuView(generic.ListView):
    """
    Class based Generic List View for List of Menu Items
    """

    model = MenuItem
    template_name = "cafe/menu.html"
    context_object_name = "items"
    paginate_by = 10


class CategoryView(generic.ListView):
    """
    Class based Generic List View for Filter by Category
    """

    template_name = "cafe/menu.html"
    context_object_name = "items"
    paginate_by = 10

    def get_queryset(self):
        c = Category.objects.get(title_en=self.kwargs['title'])
        return c.items.all()


class TableView(generic.ListView):
    """
    Class based Generic List View for Empty Tables
    """

    template_name = "cafe/tables.html"
    context_object_name = "tables"
    paginate_by = 10

    def get_queryset(self):
        return Table.objects.filter(status="T")
