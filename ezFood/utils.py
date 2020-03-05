import random 
from decimal import Decimal
from django.shortcuts import render, redirect as re

def processData(request=None,data=None):
    img = {
        'logo' : 'logo.svg'
    }  
     
    cartItemsFromSession = request.session.get('items', {})
    appliedCoupon = False,
    for item in cartItemsFromSession:
        print(item)
    appData = {'appliedCoupon':appliedCoupon,'companyName':'Ez Food','errorQuote':randomErrorQuotes(),'img':img,'cartItems':cartItemsFromSession }

    if(data is None):
        data = {}    
    appData.update(data)

    return appData 

def randomErrorQuotes():
    return random.choice([
        'looks like something went wrong on out end. please check after sometime or contact admin ',
        'something went wrong',
    ])
 
def toId(id,default=-1):
    try:
        return int(id)
    except:
        return -1

def getRole(request,method=None):
    if not method:
        method = request.method

    if type(request) == str:
        value = request
    elif method.upper() == 'POST':
        value = request.POST.get('role','normal')
    elif method.upper() == 'GET':
        value = request.GET.get('role','normal')
    else:
        return 'normal'

    role = value.lower()
    if role in  ('rider', 'owner' ) :
        return role
    return 'normal'
 
def getTotalFromOrder(items):

    total = 0
    for item in items:
        try:
            total += item['price'] * item['quantity']
        except Exception as e:
            pass

    return Decimal(total)