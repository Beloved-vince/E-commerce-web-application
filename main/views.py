from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from rest_framework.decorators import api_view
from .forms import SignUpForm, SubscriptionForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Subscription,  Product
from django import forms

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
    
    product = get_object_or_404(Product, id=product_id)
    image_url = product.image.url
    return render(request, 'product-details.html', {'image_url': image_url})