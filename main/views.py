from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from rest_framework.decorators import api_view
from .forms import SignUpForm, SubscriptionForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Subscription,  Product, Cart, CartItem
from django import forms
from cart.forms import AddToCartForm


User = get_user_model()

def home(request):
    return render(request, "index.html")


def signup(request):
    """
    Get user account data
    """
    form = SignUpForm()
    
    if request.method == 'POST':
        # try:
            print(request.POST)
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.email
                password = form.cleaned_data['password']
                confirm_password = form.cleaned_data['confirm_password']

                if password != confirm_password:
                    print("Password Error")
                    messages.error(request, "Password do not match")
                else:
                    user.set_password(password)
                    form.save()
                    return redirect("shop")
            else:
                print(form.errors)
                return HttpResponse(form.errors)
        # except Exception as e:
        #     return HttpResponse(f"The error message is {e}")
    return render(request, 'register.html')


def subscribe(request):
    """News letter for subscribers only"""
    
    if request.method == 'POST':
            form = SubscriptionForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'shop.html')

    return render(request, 'register.html')



def shop(request):
    product = Product.objects.all()
    
    context = {
        'products': product,
    }
    return render(request, 'shop.html', context)


@api_view(["GET", "POST"])
def details(request, product_id):
    if request.method == "GET":
        product = get_object_or_404(Product, id=product_id)
        image_url = product.image.url
        return render(request, 'product-details.html', {'image_url': image_url})

    if request.method == "POST":
        return redirect('add_cart')


def post(request):
    """
    Adding cart items to the browser session for un-authenticated user
    Or storing it to the database for authenticated user
    """
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
                cart_id = request.session.get('cart_id')
                if not cart_id:
                    cart = Cart.objects.create()
                    cart_id = cart.id
                    request.session['cart_id'] = cart_id
                else:
                    cart = Cart.objects.get(id=cart_id)
                cart_item = CartItem.objects.create(cart=cart, product_id=item_id, quantity=quantity)
            
                return HttpResponse("Success")
    
    return render(request, 'product-details.html', {'form': form})
