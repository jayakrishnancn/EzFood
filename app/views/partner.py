from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from ezFood.utils import processData, toId, getRole
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import Restaurant, MenuItem

# Create your views here 
@login_required
def restaurantDetails(request):
    data = {'title': 'My Restaurant Details'}
    print("one")
    if request.method == "POST":
        name = request.POST.get('name')
        address1 = request.POST.get('address1','')
        address2 = request.POST.get('address2','')
        country = request.POST.get('country','India')
        state = request.POST.get('state','')
        zip = request.POST.get('zip','')
        location = request.POST.get('location','pala')
        tag = request.POST.get('tag','')
        if not name: 
            messages.error(request,'cant save restaurant details')
            return redirect('restaurant_details')
        rest = Restaurant()
        try:
            rest = Restaurant.objects.create(user=request.user,name = name,address1 = address1,address2 = address2,country = country,state = state,zip = zip,location = location,tag = tag)
            messages.info(request,'saved restaurant details')

        except IntegrityError:
            rest = Restaurant.objects.get(user=request.user)
            rest.name = name
            rest.address1 = address1
            rest.address2 = address2
            rest.country = country
            rest.state = state
            rest.zip = zip
            rest.location = location
            rest.tag = tag
            rest.save()
            messages.info(request,'updated restaurant details.')
        except:
            messages.info(request,'cant save restaurant details. try again')
            
        return redirect('restaurant_details')
 
    data['rest'] = Restaurant.objects.filter(user=request.user).order_by('id').first()
    print(data['rest'])
    return render(request,'partner/owner/restaurant_details.html',processData(request,data))

@login_required
def viewMenu(request):
    data = {'title': 'view Menu for my restaurant'}
    data['menuItems'] = MenuItem.objects.filter(user=request.user)
    return render(request,'partner/owner/view_menu.html',processData(request,data))


@login_required
def deleteMenu(request):
    data = {'title': 'Delete item from Menu'}
 
    if request.method == 'POST':
        confirmed = request.POST.get('confirm','no')
        id = request.POST.get('id')

        if not id:
            messages.error(request,'please select item from menu to delete')
            return redirect('view_menu')

        if confirmed and confirmed.lower() == 'yes':
            try:
                itemToDelete  = MenuItem.objects.filter(user=request.user,id=id).first()
                itemToDelete.delete()
                messages.error(request,itemToDelete.name + ' deleted from Menu')
                return redirect('view_menu')
            except Exception as e:
                print(e)
                messages.error(request,'cant delete item with id' + str(id))
                return redirect('view_menu')

        else:
            messages.error(request,'please click "yes" to confirm and delete')
            return redirect('view_menu')

    
    id = request.GET.get('id')

    if not id :
        messages.error(request,'please select id to delete ')
        return redirect('view_menu')

    if MenuItem.objects.filter(user=request.user,id=id).count() !=  1:
        messages.error(request,'Cant find item from menu to delete')
        return redirect('view_menu')

    data['item'] = MenuItem.objects.filter(user=request.user,id=id).first()
    return render(request,'partner/owner/confirm_delete_item.html',processData(request,data))

    
@login_required
def addMenu(request):
    data = {'title': 'Add Items to Menu for my restaurant'}
    if request.method == "POST":

        id = request.POST.get('id')
        name = request.POST.get('name')
        price = request.POST.get('price')
        image =request.FILES.get('image')
        if not (name  and price ):
            messages.error(request,'please specify name of dish')
            return redirect('add_menu')

        try:
            if id:
                print('updating menu item')
                menuItem = MenuItem.objects.filter(user=request.user,id=id).first()
                menuItem.price = price
                if image:
                    menuItem.image.save(image.name, image)
                menuItem.save()
                messages.info(request,'updated price for item ' + name)                
            else :
                menuItem = MenuItem.objects.create(user=request.user,name=name,price=price,image=image)
                messages.info(request,'crated new Menu item')

        except Exception as e:
            messages.error(request,'an error occured try again')
            print(e)
            return redirect('add_menu')

        return redirect('view_menu')

    itemId = request.GET.get('id')
    if itemId:
        data['menuItem'] = MenuItem.objects.filter(id=itemId).first()

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