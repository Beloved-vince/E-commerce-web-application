from django.shortcuts import render, redirect
from django.views import View
from main.models import Cart, CartItem
from .forms import AddToCartForm

# Create your views here.

class CartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
        else:
            cart_items = []
    
        total_price = sum(items)