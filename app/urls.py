from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home' ),
    path('login', views.loginUser, name='login' ),
    path('logout', views.logoutUser, name='logout' ),
    path('signup', views.signup, name='signup' ),
    path('specials', views.specials, name='specials' ),
    path('offers', views.offers, name='offers' ),
    path('support', views.support, name='support' ),
    path('cart', views.cart, name='cart' ),
    path('addItemToCart', views.addItemToCart, name='addItemToCart' ),
    path('profile', views.profile, name='profile' ),
    path('dashboard', views.dashboard, name='dashboard' ),
]
