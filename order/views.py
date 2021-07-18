from django.shortcuts import render, HttpResponse, redirect
from django.views import View, generic
from django.urls import reverse
from django.utils.translation import gettext as _
from order.models import Order, Recepite
from cafe.models import Category, MenuItem, Table

# Create your views here.
class NewRecepiteView(View):
    """
    Add New Recepite on a Table and Change Status of it from Empty to Full
    """

    def get(self, request, *args, **kwargs):
        """
        GET Request to this Page Handled in this Method for Add Recepite
        """
        
        try:
            tab = Table.objects.get(id=kwargs["table"])
        except Table.DoesNotExist:
            pass
        else:
            if tab.status != 'F':
                recp = Recepite.objects.create(table=tab)
                tab.change_status(_("Full"))
                return redirect(f"/recepite/{recp.id}")
        return redirect(reverse("tables"))


class AddOrderView(View):
    """

    """

    def get(self, request, *args, **kwargs):
        """
        
        """

        return HttpResponse("GET ADD_ORD")
    
    def post(self, request, *args, **kwargs):
        """
        
        """

        return HttpResponse("POST ADD_ORD")
