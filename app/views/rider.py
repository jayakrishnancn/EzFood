from django.db.models import Q
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from ezFood.utils import processData, toId, getRole
from django.contrib.auth.decorators import login_required
from app.models import Restaurant, MenuItem ,Order

@login_required
def getOrder(request):
    data = {'title': 'Previous orders '}

    data['pendingOrders'] = Order.objects.filter(Q(delivered=False) , Q(rider=None) | Q(rider=request.user) )
    
    return render(request,'partner/rider/get_order.html',processData(request,data))

@login_required
def takeForDelivery(request):
    data = {'title': 'Take delivery'}
    id = request.GET.get('id')

    if not id:
        messages.error(request,"select order for delivery")
        return redirect('get_order')

    try:
        orders = Order.objects.filter(id=id)

        for item in orders:
            item.rider = request.user
            item.delivered = False
            item.save()

    except Exception as e:
        print(e)
    messages.info(request,"order taken")
    return redirect('get_order')    

@login_required
def completeDelivery(request):
    data = {'title': 'complete delivery'}
    id = request.GET.get('id')

    if not id :
        messages.error(request,'select order to complete')
  
    orders = Order.objects.filter(id=id,rider=request.user)

    if not orders:
        messages.error(request,'cant find order to complete')
    else:
        for item in orders:
            item.delivered = True
            item.deliveredOn = datetime.now()
            item.save()
        messages.info(request,"Order delivered.please visit order history for details" )
    return redirect('get_order')    

@login_required
def deliveryHistory(request):
    data = {'title': 'Delivery history'}
    data['pendingOrders'] = Order.objects.filter(rider=request.user,delivered=True)
    return render(request,'partner/rider/delivery_history.html',processData(request,data))