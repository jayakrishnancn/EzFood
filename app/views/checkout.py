from django.db import transaction
from django.shortcuts import render, redirect
from ezFood.utils import processData, toId, getRole, getTotalFromOrder
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import Restaurant, MenuItem, Order, OrderedItem

# Create your views here 
@login_required
def checkout(request):
    items = request.session.get('items')
    
    if request.method != 'POST':
        messages.error(request,'Please checkout from cart')
        return redirect('cart')    

    if not items or len(items) <= 0: 
        messages.error(request,'please select atleast one item')
        return redirect('cart')
    
    placedOrdersCount = 0
    
    try:
        with transaction.atomic():
            total_price = getTotalFromOrder(items)
            orderDetails = Order.objects.create(user=request.user,deliveredOn=None,total_price=total_price)

            for item in items:
                menuItem = MenuItem.objects.filter(id=item['id']).first()
                OrderedItem.objects.create(item=menuItem,quantity=item['quantity'],orderId=orderDetails)
                placedOrdersCount+=1
                
    except Exception as e:
        print(e)
        placedOrdersCount = 0
        messages.error(request,"cant place order please try again")
        return redirect('cart')
    
    request.session['items'] = []

    messages.info(request,'successfully placed '+str(placedOrdersCount)+' order(s)')
    return redirect('home')