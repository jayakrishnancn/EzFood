from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home' ),
    path('login', views.loginUser, name='login' ),
    path('logout', views.logoutUser, name='logout' ),
    path('signup', views.signup, name='signup' ),
    path('specials', views.specials, name='specials' ),
    path('offers', views.offers, name='offers' ),
    path('support', views.support, name='support' ),
    path('cart', views.cart, name='cart' ),
    path('add-item-to-cart', views.addToCart, name='addItemToCart' ),
    path('remove-item-from-cart', views.removeFromCart, name='remove_item_from_cart' ),
    path('profile', views.profile, name='profile' ),
    path('dashboard', views.dashboard, name='dashboard' ),
    path('partner-with-us', views.partnerWithUs, name='partner_with_us' ),
    path('apply-coupon', views.applyCoupon, name='applycoupon' ),
    path('remove-coupon', views.removeCoupon, name='removecoupon' ),

    path('restaurant-details', views.restaurantDetails, name='restaurant_details' ),
    path('add-menu', views.addMenu, name='add_menu' ),
    path('view-menu', views.viewMenu, name='view_menu' ),
    path('delete-menu', views.deleteMenu, name='delete_menu' ),
    path('revenue', views.revenue, name='revenue' ),
    path('order-history', views.orderHistory, name='order_history' ),
    path('owner-history', views.ownerHistory, name='owner_history' ),
    
    path('get-order', views.getOrder, name='get_order' ),
    path('take-for-delivery', views.takeForDelivery, name='take_for_delivery' ),
    path('complete-delivery', views.completeDelivery, name='complete_delivery' ),
    path('delivery-history', views.deliveryHistory, name='delivery_history' ),

    path('checkout', views.checkout, name='checkout' ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)