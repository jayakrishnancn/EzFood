from django.core.exceptions import ObjectDoesNotExist
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
        name = request.POST.get('name')
        address1 = request.POST.get('address1','')
        address2 = request.POST.get('address2','')
        country = request.POST.get('country','India')
        state = request.POST.get('state','')
        zip = request.POST.get('zip','')
        location = request.POST.get('location','India')
        tag = request.POST.get('tag','')
        ## ah  
        if name:
            rest  = Restaurant(user=request.user,name = name,address1 = address1,address2 = address2,country = country,state = state,zip = zip,location = location,tag = tag)
            rest.save()
            print(rest.user)
            print(rest.name)
            print(rest.location)
            print('saved')
            messages.info(request,'saved restaurant details')
        else:
            messages.error(request,'cant save restaurant details')

        return redirect('restaurant_details')
        
        messages.error(request,"cant save. please try again or conact admin")
        return redirect('restaurant_details')

    data['rest'] = Restaurant.objects.filter(user=request.user).order_by('id').first()
    print(data['rest'])
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