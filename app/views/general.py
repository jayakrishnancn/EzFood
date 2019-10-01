from django.shortcuts import render, redirect
from ezFood.utils import processData, toId, getRole
from app.cart import addItemToCart
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here 

def home(request):
    data = {'title': 'Welcome to ezFood'}
    return render(request,'index.html',processData(request,data))

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
                return redirect('dashboard')

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
    
    return render(request,'cart.html',processData(request,data))

def addToCart(request):
    if request.method == 'POST':
        items = request.session.get('items',[])
        data = {'title' : 'add Item To Cart'}

        items = addItemToCart(items,{
                'id' : 1,
                'name':'Burger',
                'description':'Veg Burger',
                'restaurantName':'McDonald\'s',
                'price':233,
                'quantity':2,

                })
        request.session['items'] = items
        return render(request,'cart.html',processData(request,data))
    else:
        return redirect('cart')


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