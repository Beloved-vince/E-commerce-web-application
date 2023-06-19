from django.contrib import admin
from .models import  Subscription, CartItem, Cart, Category, Payment,Address, Wishlist, Order, OrderItem, Coupon


# Register your models here.
app_models = [ Subscription, CartItem, Cart, Category, Payment, Address, Wishlist, Order, OrderItem, Coupon]

for all in app_models:
    admin.site.register(all)
    