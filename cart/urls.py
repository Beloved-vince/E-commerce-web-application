from django.urls import path
from .views import CartView

urlpatterns = [
    path('add-to-cart/', CartView.as_view(), name='add_to_cart'),
]