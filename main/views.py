from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from rest_framework.decorators import api_view
from .forms import SignUpForm, SubscriptionForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Subscription,  Product, Cart, CartItem
from cart.forms import CartItemForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render, redirect
from .models import Wishlist

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
    pass

    # if request.method == "POST":
    #     return redirect('add_cart')


from django.http import JsonResponse


from django.shortcuts import get_object_or_404

def post(request, product_id):
    """
    Saving cart items to the database
    """
    product = get_object_or_404(Product, id=product_id)
    image_url = product.image.url

    context = {
        'image_url': image_url,
        'product_id': product_id
    }

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        print(quantity)
        if quantity is not None:
            if request.user.is_authenticated:
                try:
                    cart = Cart.objects.get(user=request.user)
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(user=request.user)
                
                product = get_object_or_404(Product, id=product_id)
                
                # Check if a CartItem with the same product already exists in the cart
                try:
                    cart_item = CartItem.objects.get(cart=cart, product=product)
                    cart_item.quantity += int(quantity)
                    cart_item.save()
                except CartItem.DoesNotExist:
                    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=int(quantity))
                
                return JsonResponse({'message': 'Quantity increased and sent to the database.'})
            else:
                # For unauthenticated users, store the cart items in the session
                cart_items = request.session.get('cart_items', [])
                cart_items.append({
                    'product_id': product_id,
                    'quantity': quantity,
                })
                request.session['cart_items'] = cart_items

                return JsonResponse({'message': 'Cart item stored in session.'})

        else:
            return JsonResponse({'message': 'Quantity is missing.'})

    return render(request, "product-details.html", context)



def create_wishlist(request):
    """Wish list function"""

    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        if product_id is not None:
            wishlist, created = Wishlist.objects.get_or_create(user=request.user)
            product = Product.objects.get(id=product_id)

            if product not in wishlist.product.all():
                wishlist.product.add(product)
                return JsonResponse({'message': 'Product added to wishlist successfully'})
            else:
                return JsonResponse({'message': 'Product already exists in the wishlist'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_view(request):
    user_cart = Cart.objects.filter(user=request.user).first()  # Get the user's cart
    if user_cart:
        cart_items = CartItem.objects.filter(cart=user_cart)  # Get the cart items associated with the cart
    else:
        cart_items = []  # Empty list if the user does not have a cart

    for item in cart_items:
        item.subtotal = item.quantity * item.product.price  # Calculate the subtotal for each item

    context = {
        "cart_data": cart_items
    }
    return render(request, 'cart.html', context)



def wishlist_view(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    
    return render(request, 'wishlist.html')
    pass
    
    
def login_view(request):
    """
    Login view checks if input data is authenticated,
    allows login if true, else does nothing.
    """

    if request.method == 'POST':
        try:
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.get(email=email)

            # Authenticate the user explicitly
            authenticated_user = authenticate(request, username=email, password=password)

            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('add_cart')
            else:
                print("Anonymous login failed")
                messages.error(request, 'Username or password is incorrect')
        except User.DoesNotExist:
            print("User does not exist")
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'customer-login.html')


def logout_view(request):
    logout(request)
    return redirect('login-in')


