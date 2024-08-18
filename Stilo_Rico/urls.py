# urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('home/', home, name='home'),
    path('store/<str:store_name>/', store_products, name='store_products'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('register/', register_view, name='register'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('profile/', user_profile_view, name='user_profile'),
    path('checkout/', checkout_view, name='checkout'),
    path('payment/success/', payment_success, name='payment_success'),
]
