from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from rest_framework.decorators import api_view
from .forms import SignUpForm, SubscriptionForm, AddressForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Subscription,  Product, Cart, CartItem, Wishlist, Address, UserFeedback
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.urls import reverse
from urllib.parse import urlencode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.sessions.backends.db import SessionStore


User = get_user_model()

def home(request):
    """
    Return the first and last 10 product to the home page
    Also get product id if user is adding to wishlist
    """
    if request.method == 'GET':
        first_ten_product = Product.objects.order_by('created_at')[:10]
        last_ten_product = Product.objects.order_by('created_at')[11:]
        # sale_product = Product.objects.order_by("")
        
        context =  {
            'products': first_ten_product,
            'featured': last_ten_product
            }
        return render(request, "index.html", context)
    elif request.method == 'POST':
        try:
            if request.method == 'POST':
                print('Received POST data:', request.POST)
                product_id = request.POST.get('product_id')
                print('Received product_id:', product_id)  
                if product_id is not None:
                    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
                    product = Product.objects.get(id=product_id)

                    if product not in wishlist.product.all():
                        wishlist.product.add(product)
                wishlist.save()
            return JsonResponse({'message': 'Success'}, status=200)
        except Exception as e:
            print(e)
            return HttpResponse(e)
    return JsonResponse({'message': 'Invalid request method'}, status=405)


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
    """
    Sorting and pagination to product list
    order by: name, price and position
    """
    from django.db.models import F
    
    sort_by = request.GET.get('sort_by', 'position')
    products = Product.objects.all()
    
    if sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == 'price':
        products = products.order_by('price')
        
    else:
        products = products.annotate(position=F('id'))
    # results = sorted(results, key=lambda x: x.price, reverse=True)
    paginator = Paginator(products, per_page=10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {
        'products': page_obj,
        'sort_by': sort_by
    }
    return render(request, 'shop.html', context)






@login_required
@api_view(['POST'])
def create_wishlist(request):
    """
    Wish list function
    Get product id if not already added to the wishislist else
        do nothin
    """
    try:
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            print(product_id)
            if product_id is not None:
                wishlist, created = Wishlist.objects.get_or_create(user=request.user)
                product = Product.objects.get(id=product_id)

                if product not in wishlist.product.all():
                    wishlist.product.add(product)
                    return JsonResponse({'message': 'Success'}, status=200)
            return JsonResponse({"message": "Product added to wishlist"})
    except Exception as e:
        print(e)
        return HttpResponse(e)



def delete_wishlist_item(request, wishlist_id, product_id):
    """
    Delete a wishlist item
    Get wishlist id and product id
    """
    try:
        if request.method == 'DELETE':
            wishlist = Wishlist.objects.get(id=wishlist_id, user=request.user)
            product = Product.objects.get(id=product_id)
            
            if product in wishlist.product.all():
                wishlist.product.remove(product)
                return JsonResponse({'message': 'Success'}, status=200)
            else:
                return JsonResponse({'message': 'Product not found in wishlist'}, status=404)
        
    except Wishlist.DoesNotExist:
        return JsonResponse({'message': 'Wishlist does not exist'}, status=404)
    
    except Exception as e:
        return JsonResponse({'message': 'Error deleting wishlist item', 'error': str(e)}, status=500)


def cart_view(request):
    """
    Return all cart item of requested user and prices
    """
    total_price = 0
    
    user_cart = Cart.objects.filter(user=request.user).first()  
    if user_cart:
        cart_items = CartItem.objects.filter(cart=user_cart)  # 
    else:
        cart_items = []

    for item in cart_items:
        item.subtotal = item.quantity * item.product.price
        total_price += item.subtotal
        
   
    context = {
        "cart_data": cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)



def wishlist_view(request):
    """Return user wishlist"""
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {
        "wishlist": wishlist
    }
    
    
    return render(request, 'wishlist.html', context)

def add_to_cart(request, product_id):
    import random
    """
    Saving cart items to the database if request is POST
    Rendering related product base on category they belong to
    random six
    """
    product = get_object_or_404(Product, id=product_id)
    image_url = product.image.url
    price = product.price
    name = product.name
    category = product.category
    related_products = Product.objects.filter(category=category).exclude(id=product_id)[:6]
    related_products = random.sample(list(related_products), min(len(related_products), 6))
    context = {
        'image_url': image_url,
        'product_id': product_id,
        'name': name,
        'price': price,
        'related_products': related_products 
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
            return JsonResponse({'message': 'Quantity is missing.'})

    return render(request, "product-details.html", context)

def update_cart(request):
    """
    Updating cart item
    """
    if request.method == 'POST':
        cart_data = request.POST.getlist('quantity') 
        cart_item_ids = request.POST.getlist('cart_item_id')  
        for item_id, quantity in zip(cart_item_ids, cart_data):
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.quantity = int(quantity)
            cart_item.save()
        
        
    return redirect('cart_view')


def delete_cart_item(request, item_id):
    """
    Deleting cart items from the database 
    """
    cart_item = get_object_or_404(CartItem, id=item_id)

    # Check if the user has permission to delete the cart item
    if cart_item.cart.user != request.user:
        return JsonResponse({'error': 'You do not have permission to delete this item.'}, status=403)

    # Delete the cart item
    cart_item.delete()

    return JsonResponse({'message': 'Cart item deleted successfully.'})

def capture_user_feedback(request):
    """
    Getting user feedback on a product
        name of the user
        email of the user
        phone_number of the user
        feedback_text of the user
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        feedback_text = request.POST.get('feedback_text')
        
        feedback = UserFeedback(email=email, name=name, phone_number=phone_number, feedback_text=feedback_text)
        feedback.save()
        messages.success(request, "Thank you for your feedback")
    return render(request, 'contact.html')
    

def login_view(request):
    """
    Login user if email and password is in the database
    """
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
    """
    Logout user function
    """
    logout(request)
    return redirect('login-in')


@login_required
def update_profile(request):
    """
    Update user profile account if authenticated
        first_name, last_name, email
        username is then set as email
    """
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
    """
    Change password function 
    """
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
    """
    Address of the user to deliver product to
    """
    if request.method == 'POST':
        form = AddressForm(request.POST)
        print(form.errors)
        if request.user.is_authenticated:
            form.instance.user = request.user
        if form.is_valid():
            address = form.save()
            return redirect('addresses')
    else:
        form = AddressForm()

    return render(request, 'user_accountpage.html', {'form': form})

@login_required
def order_details(request):
    """Ordered products details of the user"""
    if request.user.is_authenticated:
        user_addresses = Address.objects.filter(user=request.user)[:4]
        return render(request, 'user_accountpage.html', {'user_addresses': user_addresses})
    return render(request, 'user_accountpage.html')



class SearchView(View):
    """Searching view """    
    def post(self, request):
        """
            Get query paramters and return related object
            saving it in the browser session
        """
        search_query = request.POST.get('search_query', '')

        session = SessionStore(session_key=request.session.session_key)
        session['search_query'] = search_query
        session.save()
    
        return redirect('search_results')
    


class SearchResultsView(View):
    def get(self, request):
        try:
            session = SessionStore(session_key=request.session.session_key)
            search_query = session.get('search_query')

            # Get the page number from the request GET parameters
            page_number = request.GET.get('page')
    
            # Perform the search
            results = self.perform_search(search_query)

            # Get the sorting option from the request GET parameters
            sort_by = request.GET.get('sort_by')

            # Sort the results based on the sorting option
            if sort_by == 'price':
                results = sorted(results, key=lambda x: x.discounted_price, reverse=True)
            elif sort_by == 'name':
                results = sorted(results, key=lambda x: x.name)
            else:
                results = sorted(results, key=lambda x: x.id)  # Default sort by ID

            # Create a paginator object with the results and set the desired number of items per page
            paginator = Paginator(results, per_page=5)

            # Get the requested page from the paginator based on the page number
            try:
                page_obj = paginator.get_page(page_number)
            except PageNotAnInteger:
                page_obj = paginator.get_page(1)
            except EmptyPage:
                page_obj = paginator.get_page(paginator.num_pages)

            # Build the query parameters for the URL
            query_params = {'q': search_query}

            # Add the page number to the query parameters if it exists
            if page_number:
                query_params['page'] = page_number

            # Encoding the query parameters into a URL-encoded string
            encoded_query_params = urlencode(query_params)

            # Constructing the redirect URL with the query parameters
            redirect_url = f"{reverse('search_results')}?{encoded_query_params}"

            # Redirecting to the URL if search query exists and 'q' parameter is not present
            if search_query and not request.GET.get('q'):
                return redirect(redirect_url, permanent=True)

            context = {
                'search_query': search_query,
                'results': page_obj,
                'sort_by': sort_by
            }

            return render(request, 'search.html', context)
        except Exception as e:
            print(e)
            return HttpResponse(e)


    def perform_search(self, query):
        """
        Perform the search using the Query object
        to search across multiple fields
        """
        context = Product.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(description__icontains=query) |
            Q(manufacture_by__icontains=query) |
            Q(slug__icontains=query)
        )
        return context

        

def checkout(request):

    return render(request, 'checkout.html')