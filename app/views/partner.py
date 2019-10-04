from django.shortcuts import render, redirect
from ezFood.utils import processData, toId, getRole
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import Restaurant

# Create your views here 
@login_required
def restaurantDetails(request):
    data = {'title': 'My Restaurant Details'}
    if request.method == "POST":
        messages.error(request,"cant save. please try again or conact admin")
        return redirect('restaurant_details')
    data['restautant'] = Restaurant(request.user)
    return render(request,'partner/owner/restaurant_details.html',processData(request,data))

@login_required
def addMenu(request):
    data = {'title': 'Add Items to Menu for my restaurant'}
    if request.method == "POST":
        messages.error(request,"cant save. please try again or conact admin")
        return redirect('add_menu')
    return render(request,'partner/owner/add_menu.html',processData(request,data))

@login_required
def revenue(request):
    data = {'title': 'Total revenue for my Restaurant'}
    if request.method == "POST":
        messages.error(request,"cant save. please try again or conact admin")
        return redirect('revenue')
    return render(request,'partner/owner/revenue.html',processData(request,data))

@login_required
def orderHistory(request):
    data = {'title': 'Orders for my Restaurant'}
    if request.method == "POST":
        messages.error(request,"cant save. please try again or conact admin")
        return redirect('order_history')
    return render(request,'partner/owner/order_history.html',processData(request,data))