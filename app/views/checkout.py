from django.db import transaction
from django.shortcuts import render, redirect
from ezFood.utils import processData, toId, getRole, getTotalFromOrder
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import Restaurant, MenuItem, Order

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
    
    placedOrders = []
    
    try:
        with transaction.atomic():
            orderId  = Order.objects.all().count() + 1
            total_price = getTotalFromOrder(items)
            for item in items:
                menuItem = MenuItem.objects.filter(id=item['id']).first()
                orderDetails = Order.objects.create(user=request.user,item=menuItem,quantity=item['quantity'],orderId=orderId,deliveredOn=None,total_price=total_price)
                placedOrders.append(orderDetails)
                
    except Exception as e:
        print(e)
        placedOrders = []
        messages.error(request,"cant place order please try again")
        return redirect('cart')
    
    request.session['items'] = []

    messages.info(request,'successfully placed '+str(len(placedOrders))+' order(s)')
    return redirect('home')