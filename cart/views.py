from typing import Any
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from main.models import Cart, CartItem
from .forms import AddToCartForm


# Create your views here.

class CartView(View):
    def __init__(self):
        self.cart_items = None
        
    def get(self, request, product_id=None):
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            self.cart_items = CartItem.objects.filter(cart=cart)
        else:
            # Retrieve cart data from the session or cookie for unauthenticated users
            self.cart_items = request.session.get('cart_id', None)
    
        total_price = sum(items.product.price * items.quantity for items in self.cart_items)
        context = {
            'cart_item': self.cart_items,
            'total_price': total_price
        }
        
        return render(request, 'cart.hmtl', context)
    
    def post(self, request):
        form = AddToCartForm(request.POST)
        if form.is_valid():
            item_id = form.cleaned_data('product_id')
            # quantity = form.cleaned_data('quantity')

            if request.user.is_authenticated:
                self.cart_items = CartItem.objects.create(id=item_id)
            else:
                self.cart_items = request.POST.get('cart_id')
                request.session['cart_id'] = self.cart_items
            return HttpResponse("Success")
        return render (request, 'cart.html')
                




















# from django.views import View
# from django.shortcuts import render
# from django.contrib.auth.mixins import LoginRequiredMixin

# class CartView(View):
#     def post(self, request):
#         if request.user.is_authenticated:
#             # Save cart data to the database for authenticated users
#             cart_data = request.POST.get('cart_data')
#             # Perform the necessary operations to save cart_data to the database
#             # ...
#             return render(request, 'success.html')
#         else:
#             # Save cart data to the browser for unauthenticated users
#             cart_data = request.POST.get('cart_data')
#             # Save the cart_data to the session or cookie
#             request.session['cart_data'] = cart_data
#             return render(request, 'success.html')

            
# from django.views import View
# from django.shortcuts import render
# from django.contrib.auth.mixins import LoginRequiredMixin

# class CartView(View):
#     def get(self, request):
#         if request.user.is_authenticated:
#             # Retrieve cart data from the database for authenticated users
#             # Perform the necessary operations to retrieve cart data from the database
#             # ...
#             cart_data = "Cart data from the database"
#         else:
#             # Retrieve cart data from the session or cookie for unauthenticated users
#             cart_data = request.session.get('cart_data', None)

#         return render(request, 'cart.html', {'cart_data': cart_data})
