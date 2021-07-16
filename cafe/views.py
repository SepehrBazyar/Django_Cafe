from django.shortcuts import render, HttpResponse, redirect
from django.views import View, generic
from django.utils.translation import gettext as _
from cafe.models import MenuItem

# Create your views here.
class MenuView(generic.ListView):
    model = MenuItem
    template_name = "cafe/menu.html"
    context_object_name = "items"
    paginate_by = 10
