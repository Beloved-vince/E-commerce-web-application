from django.urls import path
from .views import *


urlpatterns = [
    path('health/', HealthProductView.as_view(), name='health'),
    path('indoor/', IndoorProductView.as_view(), name='indoor'),
    path('grocery/', SupermarketProductView.as_view(), name='grocery'),
    path('appliances/', AppliancesProductView.as_view(), name='appliances'),
    path('electronics/', ElectronicsProductView.as_view(), name='electronics'),
    path('phones-tablets/', PhoneProductView.as_view(), name='mobile'),
    path('computing/', ComputingProductView.as_view(), name='computing'),
    path('fashion/', FashionProductView.as_view(), name='fashion'),
    path('baby-product/', BabyProductView.as_view(), name='baby-product'),
    path('sport-goods/', SportProductView.as_view(), name='sports'),
    path('video-games/', GameProductView.as_view(), name='games'),
]
