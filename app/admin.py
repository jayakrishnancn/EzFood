from django.contrib import admin
from .models import Profile, Restaurant, MenuItem, Order, OrderedItem,Coupon
# Register your models here.

admin.site.register(Profile)
admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderedItem)
admin.site.register(Coupon)