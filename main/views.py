from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from rest_framework.decorators import api_view
from .forms import SignUpForm, SubscriptionForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Subscription,  Product, Cart, CartItem
from cart.forms import AddToCartForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.backends import ModelBackend


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


from django.http import JsonResponse

def post(request):
    """
    Adding cart items to the browser session for unauthenticated user
    Or storing it to the database for authenticated user
    """
    try:
        if request.method == 'POST':
            form = AddToCartForm(request.POST)
            print(form.errors)
            if form.is_valid():
                product_id = form.cleaned_data['product_id']
                quantity = form.cleaned_data['quantity']
                if request.user.is_authenticated:
                    try:
                        cart = Cart.objects.get(user=request.user)
                    except Cart.DoesNotExist:
                        cart = Cart.objects.create(user=request.user)
                    
                    # Check if a CartItem with the same product_id already exists in the cart
                    try:
                        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
                        cart_item.quantity += quantity
                        cart_item.save()
                    except CartItem.DoesNotExist:
                        cart_item = CartItem.objects.create(cart=cart, product_id=product_id, quantity=quantity)
                    
                    return JsonResponse({'message': 'Quantity is it true increased and sent to the database.'})
                else:
                    return JsonResponse
                #     # For unauthenticated users, store the cart items in the session
                #     cart_id = request.session.get('cart_id')
                #     if not cart_id:
                #         cart = Cart.objects.create()
                #         cart_id = cart.id
                #         request.session['cart_id'] = cart_id
                #     else:
                #         cart = Cart.objects.get(id=cart_id)
                    
                #     cart_item = CartItem.objects.create(cart=cart, product_id=product_id, quantity=quantity)
                    
                #     return JsonResponse({'message': 'Success'})
    
    except Exception as e:
        return(e)
        # return JsonResponse({'message': 'Error occurred'}, status=500)
    
    return JsonResponse({'message': 'Invalid request'}, status=400)





def login_view(request):
    """Login view checks if input data is authenticated,
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
