from typing import Any
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from main.models import Cart, CartItem, User
from .forms import AddToCartForm
from django.contrib.auth.decorators import login_required
from main.models import User

# Create your views here.

class CartView(View):
    def __init__(self):
        self.cart_items = None
    
    def get(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            self.cart_items = CartItem.objects.filter(cart=cart)
  
        else:
            # Retrieve cart data from the session or cookie for unauthenticated users
            cart_id = request.session.get('cart_id')
            if cart_id:
                try:
                    cart = Cart.objects.get(id=cart_id)
                    self.cart_items = CartItem.objects.filter(cart=cart)
                except Cart.DoesNotExist:
                    pass

        if self.cart_items is None:
            return HttpResponse("cart.html")

        cart_data = []
        total_price = 0

        for item in self.cart_items:
            product = item.product
            image = product.image.url if product.image else ''
            name = product.name
            price = item.quantity * product.price
            quantity = item.quantity
            subtotal = item.quantity * product.price

            cart_data.append({
                'image': image,
                'name': name,
                'price': price,
                'quantity': quantity,
                'subtotal': subtotal
            })

            total_price += subtotal

        context = {
            'cart_data': cart_data,
            'total_price': total_price
        }

        return render(request, 'cart.html', context)
    
    def post(self, request):
        form = AddToCartForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                item_id = form.cleaned_data['product_id']
                quantity = form.cleaned_data['quantity']
                print(f"{quantity},  {item_id}")
            
                try:
                    cart = Cart.objects.get(user=request.user)
                    print(cart)
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(user=request.user)
                
                # Check if a CartItem with the same product_id already exists in the cart
                try:
                    cart_item = CartItem.objects.get(cart=cart, product_id=item_id)
                    cart_item.quantity += quantity
                    cart_item.save()
                except CartItem.DoesNotExist:
                    cart_item = CartItem.objects.create(cart=cart, product_id=item_id, quantity=quantity)# else:
                    cart_id = request.session.get('cart_id', None)
                    if not cart_id:
                        cart = Cart.objects.create()
                        cart_id = cart.id
                        request.session['cart_id'] = cart_id
                    else:
                        cart = Cart.objects.get(id=cart_id)
                    self.cart_item = CartItem.objects.create(cart=cart, product_id=item_id, quantity=quantity)
                
                    return HttpResponse("Success")
        
        return render(request, 'product-details.html', {'form': form})





















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
