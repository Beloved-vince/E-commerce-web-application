from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from rest_framework.decorators import api_view
from .forms import SignUpForm, SubscriptionForm, AddressForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Subscription,  Product, Cart, CartItem
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render, redirect
from .models import Wishlist, Address
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import View

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
    """Return user wishlist"""
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {
        "wishlist": wishlist
    }
    
    return render(request, 'wishlist.html', context)

from .models import UserFeedback

def capture_user_feedback(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        feedback_text = request.POST.get('feedback_text')
        
        feedback = UserFeedback(email=email, name=name, phone_number=phone_number, feedback_text=feedback_text)
        feedback.save()
        messages.success(request, "Thank you for your feedback")
    # Render the feedback form template for the user to provide feedback
    return render(request, 'contact.html')
    

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email + password)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            print("success")
            login(request, user)
            return redirect('cart_view')  # Replace 'home' with the name of your home page URL
        else:
            print("error")
            messages.error(request, 'Invalid email or password')
            return JsonResponse({"message": "Invalid email or password"})

    return render(request, 'customer-login.html')


def logout_view(request):
    logout(request)
    return redirect('login-in')


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def update_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Retrieve the authenticated user
        user = request.user

        # Update the user's profile
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = email
        user.save()

        messages.success(request, 'Profile updated successfully!')
        return JsonResponse({"message": "Profile update completed"})

    # Render the profile update form
    return render(request, 'user_accountpage.html')

def change_password(request):
    user = request.user
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        
        if new_password != confirm_password:
            messages.error(request, "Password do not match")
        else:
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password change successfully")

    return render(request, "user_accountpage.html")



@login_required
def create_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        print(form.errors)
        if request.user.is_authenticated:
            form.instance.user = request.user
        if form.is_valid():
            address = form.save()
            return redirect('addresses')  # Redirect to a success page or another view
    else:
        form = AddressForm()

    return render(request, 'user_accountpage.html', {'form': form})

@login_required
def order_details(request):
    if request.user.is_authenticated:
        user_addresses = Address.objects.filter(user=request.user)[:4]
        return render(request, 'user_accountpage.html', {'user_addresses': user_addresses})
    return render(request, 'user_accountpage.html')


from django.db.models import QuerySet

class SearchView(View):
    def get(self, request):
        query = request.GET.get('query', '')
        results = self.perform_search(query)
        context = {'query': query, 'result': results}
        return render(request, 'shop.html', context)
    
    def perform_search(self, query):
        """
        Perform the search using the Query object
        to search across multiple fields
        """
        results = Product.objects.filter(
            QuerySet(name__icontains=query) |
            QuerySet(category__icontains=query) |
            QuerySet(subcategory__icontains = query)
        )
        
        return results