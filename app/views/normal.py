
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

    data['orders'] = OrderedItem.objects.filter(order__user=request.user)

    print(data)
    return render(request,'partner/owner/order_history.html',processData(request,data))