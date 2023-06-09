from django.contrib import admin
from .models import  Subscription, User, CartItem, Cart, Category, Payment,  Product, Address, Wishlist, Order, OrderItem, Coupon


# Register your models here.
app_models = [ Subscription, User, CartItem, Cart, Category, Payment,  Product, Address, Wishlist, Order, OrderItem, Coupon]

for all in app_models:
    admin.site.register(all)
    