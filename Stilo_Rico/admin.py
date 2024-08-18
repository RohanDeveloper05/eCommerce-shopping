from django.contrib import admin
from .models import Product, Store, Cart, CartItem

admin.site.register(Store)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)