from django.shortcuts import render, redirect
from ezFood.utils import processData, toId, getRole
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here 
@login_required
def restaurantDetails(request):
    data = {'title': 'My Restaurant Details'}
    if request.method == "POST":
        messages.error(request,"cant save. please try again or conact admin")
        return redirect('restaurant_details')
    return render(request,'partner/owner/restaurant_details.html',processData(request,data))
