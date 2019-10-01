from django.shortcuts import render, redirect
from ezFood.utils import processData, toId, getRole
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here 
@login_required
def restaurantDetails(request):
    data = {'title': 'My Restaurant Details'}
    return render(request,'partner/owner/restaurant_details.html',processData(request,data))
