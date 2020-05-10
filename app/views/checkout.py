from django.db import transaction
from django.shortcuts import render, redirect
from ezFood.utils import processData, toId, getRole, getTotalFromOrder
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import Restaurant, MenuItem, Order, OrderedItem
import stripe # new
from django.conf import settings
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY # new
currency = "INR" 

# Create your views here 
@login_required
def checkout(request):
    if request.method != 'POST':
        messages.error(request,'Please checkout from cart')
        return redirect('cart')    
    
    

    items = request.session.get('items')
     
    if not items or len(items) <= 0: 
        messages.error(request,'please select atleast one item')
        return redirect('cart')
    
    placedOrdersCount = 0
    print("here")

    discount = 0.0
    try:
        if items and items[0] and items[0]['coupon'] :
            discount = Decimal(items[0]['coupon'])
    except Exception as e:
        print(e)
    try:
        with transaction.atomic():
            print("here 4")
            total_price = getTotalFromOrder(items)
            print("here 5")
            orderDetails = Order.objects.create(user=request.user,deliveredOn=None,total_price=total_price,offers=discount)

            for item in items:
                menuItem = MenuItem.objects.filter(id=item['id']).first()
                OrderedItem.objects.create(item=menuItem,quantity=item['quantity'],order=orderDetails)
                placedOrdersCount+=1
        print("here 3")
        tmp = float(request.POST.get('total_amount'))
        total_amount = round(tmp)
        print(total_amount)
        charge = stripe.Charge.create(
            amount=total_amount,
            currency="INR",
            description='A Django charge',
            source=request.POST['stripeToken']
        )
    except Exception as e:
        print(e)
        placedOrdersCount = 0
        messages.error(request,"cant place order please contact admin")
        return redirect('cart')
    
    request.session['items'] = []

    messages.info(request,'successfully placed '+str(placedOrdersCount)+' order(s)')
    return redirect('home')