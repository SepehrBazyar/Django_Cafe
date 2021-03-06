from django.shortcuts import render, HttpResponse, redirect
from django.views import View, generic
from django.urls import reverse
from django.utils.translation import gettext as _
from order.models import Order, Recepite
from cafe.models import Category, MenuItem, Table
from time import sleep

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
    View for See Orders of a Recepite and Edit it Add or Delete or ...
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET Request for See Details of Orders of Recepite in a Table
        """

        try:
            recp = Recepite.objects.get(id=kwargs["id"])
        except Recepite.DoesNotExist:
            return render(request, "404.html", status=404)
        else:
            orders = recp.orders.all()
            items = MenuItem.objects.all()
            return render(request, "order/details.html", {
                "orders": orders,
                "recepite": recp,
                "items": items,
            })
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST Request for Add New Order in this Recepite
        """

        posts = request.POST
        recp = Recepite.objects.get(id=kwargs["id"])
        item = MenuItem.objects.get(title_en=posts["item"])
        order = Order.objects.create(recepite=recp, item=item, count=posts["count"])
        return redirect(f"/recepite/{recp.id}")


class PaymentView(View):
    """
    View for Payment Price of Recepite and Change Status it to Paid
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET Request for See Details of Orders of Recepite in a Table
        """

        try:
            recp = Recepite.objects.get(id=kwargs["id"])
        except Recepite.DoesNotExist:
            return redirect(reverse("menu"))
        else:
            recp.change_status(_("Paid"))
            sleep(2)
            return redirect(f"/recepite/{recp.id}")
