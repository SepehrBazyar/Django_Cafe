from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views import View, generic
from django.urls import reverse
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
    paginate_by = 5


class CategoryView(generic.ListView):
    """
    Class based Generic List View for Filter by Category
    """

    template_name = "cafe/menu.html"
    context_object_name = "items"
    paginate_by = 10

    def get_queryset(self):
        cat = get_object_or_404(Category, title_en=self.kwargs['title'])
        return cat.items.all()


class TableView(generic.ListView):
    """
    Class based Generic List View for Empty Tables
    """

    template_name = "cafe/tables.html"
    context_object_name = "tables"

    def get_queryset(self):
        return Table.objects.filter(status="T")
