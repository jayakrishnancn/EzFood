from django.shortcuts import render, redirect
from ezFood.utils import processData, toId, getRole
from app.cart import addItemToCart
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from app.models import Restaurant, MenuItem , Coupon
import logging

logger = logging.getLogger(__name__)
# Create your views here 

def home(request):
    data = {'title': 'Welcome to ezFood'}
    items = MenuItem.objects.filter(active=True)
    if items and items.count() > 0 :
        data['menuItems'] = items
    
    data  = processData(request,data)

    for  mItem in items:
        print(mItem.id)
        for cItem in data['cartItems']:
            if(mItem.id == cItem['id']):
                mItem.quantity = cItem['quantity'] 
                
        
    return render(request,'index.html',data)

def logoutUser(request):
    auth.logout(request)
    messages.info(request,'User loggedout')
    return redirect('login')

def loginUser(request):
    data = {'title':'Login to your account'}

    if request.method == 'POST':

        username = request.POST.get('username') 
        password = request.POST.get('password')

        if not (username and password):
            messages.error(request,'All fields are mandatory')
            return redirect('login')

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print('user logged in') 
                nextUrl = request.POST.get('next')
                print(nextUrl)
                if not nextUrl:
                    nextUrl = 'dashboard'

                return redirect(nextUrl)

        messages.error(request,'Invalid credentials')
        return redirect('login')

    else: 
        # check account type, 3 types normal, rider and restaurent owner
        
        data['role'] = getRole(request)
        return render(request,'login.html',processData(request,data))

def signup(request):
    data = {'title' : 'Create an account'}
    if(request.method == 'POST'):  
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if not(first_name and last_name and username and email and password1 and password2):
            messages.info(request,'All fields are mandatory')
            return redirect('signup')

        if password1 != password2:
            messages.info(request, 'passwords not matching')
            return redirect('signup')
            
        else:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken. please select another username')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already registered.Please login to continue')
            else:
                user = User.objects.create_user(username=username,email=email,password=password1,first_name=first_name,last_name=last_name)
                user.profile.role = getRole(request)
                user.save()

                print('user crated')
                messages.info(request, 'Account created successfully. Please login to continue')
        return redirect('login')
    else:
        # check account type, 3 types normal, rider and restaurent owner
        role = request.GET.get('type','normal').lower()
         
        if role != 'rider' and role != 'owner' :
            role = 'normal'
        
        data['role'] = role
        return render(request,'signup.html',processData(request,data))

def specials(request):
    data = {'title' : 'Special deals'}
    return render(request,'specials.html',processData(request,data))

def offers(request):
    data = {'title' : 'New offers'}
    return render(request,'offers.html',processData(request,data))

def support(request):
    data = {'title' : 'Customer support page'}
    return render(request,'support.html',processData(request,data))

def cart(request):
    data = {'title' : 'Shopping Cart'}
    
    # logger.warning("Your log message is here")
    # logger.warning(processData(request,data))
    # logger.info("pppppppppppppppppppp")
    return render(request,'cart.html',processData(request,data))


@login_required
def addToCart(request):
    id = request.GET.get('id',None);
    count = request.GET.get('count',1)
    
    if id:
        try:
            items = request.session.get('items',[])
            itemToAdd = MenuItem.objects.filter(active=True,id=id)

            
            if itemToAdd and itemToAdd.values() and itemToAdd.values()[0]:
                items = addItemToCart(items,itemToAdd.values()[0],count)
                request.session['items'] = items
                newItem = itemToAdd.values()[0]
                messages.error(request, newItem['name'] + " added to cart please 'proceed to checkout' from your cart to finish your order")

            else:
                messages.error(request,"cant find item you have selected")

        except Exception as e:
            print(e)
            messages.error(request,"an error occured. please try again")

    else:
        messages.error(request,"Please select item to add to cart")

    return redirect(request.META.get('HTTP_REFERER', 'cart'))

@login_required
def removeFromCart(request):
    data = {'title' : 'Remove Item From Cart'}

    id = toId(request.GET.get('id',-1))
    if not id:
        messages.error(request,'Please select an item to remove from cart')
        return redirect(request.META.get('HTTP_REFERER', 'home'))


    items = request.session.get('items',[])
    itemToRemove = None

    for item in items:
        if item["id"] == id:
            itemToRemove = item
            break

    if not itemToRemove:
        messages.info(request,'cant find item in cart')

    else:
        newItems = [i for i in items if not (i['id'] == itemToRemove["id"])]
        request.session['items'] = newItems   
        messages.info(request,'removed ' + itemToRemove["name"] + ' from cart')

    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def profile(request):
    data = {'title' : 'Profile'}
    return render(request,'user/profile.html',processData(request,data))

@login_required
def dashboard(request):
     
    data = {'title' : 'Dashboard'}
    return render(request,'user/profile.html',processData(request,data))
    

def partnerWithUs(request):
    data = {'title' : 'Partner with us'}
    return render(request,'partner/select.html',processData(request,data))

@login_required
def applyCoupon(request):

    id = request.POST.get('id',None)
    if not id:
        messages.error(request,'Invalid Coupon')
        redirect('cart')
    logger.warning("Your log message is here")
    
    logger.warning(id)
    coupon = Coupon.objects.filter(couponKey=id)
    if not coupon.exists():
        return redirect('cart')
    couponItem = Coupon.objects.filter(couponKey=id).first()    

    logger.warning(couponItem)    
    if not couponItem  : 
        messages.error(request,'Invalid Coupon')
        redirect('cart')

    couponId = couponItem.price

    items = request.session.get('items',[])
    for item in items:
        item['coupon'] = couponId
    
    request.session['items'] = items
    return redirect('cart')

@login_required
def removeCoupon(request):

    items = request.session.get('items',[])
    for item in items:
        item['coupon'] = 0
    
    request.session['items'] = items
    return redirect('cart')