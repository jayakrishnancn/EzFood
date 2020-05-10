# payments/views.py
import stripe # new
from ezFood.utils import processData
 
from django.conf import settings
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect # new
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY # new

def payments(request):

    if request.method != 'POST':
        messages.error(request,'Please checkout from cart')
        return redirect('cart')    
 
    tmp = float(request.POST.get('total_amount'))
    total_amount = round(tmp,2)
    context = {'title' : 'Payment portal'}
    context['amount_rs'] = total_amount
    context['amount'] = total_amount  * 100 
    context['currency'] = "INR" 
    context['key'] = settings.STRIPE_PUBLISHABLE_KEY
   
    return render(request,'payments/home.html',processData(request,context))
 