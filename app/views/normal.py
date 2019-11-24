import copy
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from ezFood.utils import processData, toId, getRole
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import Restaurant, MenuItem, Order,OrderedItem

@login_required
def orderHistory(request):
    data = {'title': 'Previous orders '}

    if request.method == "POST":
        messages.error(request,"cant save. please try again or conact admin")
        return redirect('order_history')

    ordersFromDb = Order.objects.filter(user=request.user).order_by('-id')

    newOrders = []
    for order in ordersFromDb:
        tmp_order = {}
        tmp_order['id'] = order.id
        tmp_order['delivered'] = order.delivered
        tmp_order['rider'] = order.rider
        tmp_order['deliveredOn'] = order.deliveredOn
        tmp_order['total'] = order.total_price 
        tmp_order['items'] = OrderedItem.objects.filter(order=order).order_by('-id')
        newOrders.append(tmp_order)

    print(newOrders)

    data['orders'] = newOrders

    return render(request,'partner/owner/order_history.html',processData(request,data))