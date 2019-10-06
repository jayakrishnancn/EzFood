from django.shortcuts import render, redirect
from ezFood.utils import processData, toId, getRole
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import Restaurant, MenuItem, Orders

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

    for item in items:
        pass

    messages.info(request,'successfully placed order')
    return redirect('home')
    