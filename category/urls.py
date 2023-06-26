from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('health/', HealthProductView.as_view(), name='health'),
    path('health/<str:subcategory>/', HealthProductView.as_view(), name='health_by_subcategory'),
    
    path('indoor/', IndoorProductView.as_view(), name='indoor'),
    path('indoor/<str:subcategory>/', HealthProductView.as_view(), name='indoor_by_subcategory'),
    
    path('grocery/', SupermarketProductView.as_view(), name='grocery'),
    path('grocery/<str:subcategory>/', HealthProductView.as_view(), name='grocery_by_subcategory'),
    
    path('appliances/', AppliancesProductView.as_view(), name='appliances'),
    path('appliances/<str:subcategory>/', HealthProductView.as_view(), name='appliances_by_subcategory'),
    
    path('electronics/', ElectronicsProductView.as_view(), name='electronics'),
    path('electronics/<str:subcategory>/', HealthProductView.as_view(), name='electronics_by_subcategory'),
    
    path('phones-tablets/', PhoneProductView.as_view(), name='mobile'),
    path('phones-tablets/<str:subcategory>/', HealthProductView.as_view(), name='phones_by_subcategory'),
    
    path('computing/', ComputingProductView.as_view(), name='computing'),
    path('computing/<str:subcategory>/', HealthProductView.as_view(), name='computing_by_subcategory'),
    
    path('fashion/', FashionProductView.as_view(), name='fashion'),
    path('fashion/<str:subcategory>/', HealthProductView.as_view(), name='fashion_by_subcategory'),
    
    path('baby-product/', BabyProductView.as_view(), name='baby-product'),
    path('baby-product/<str:subcategory>/', HealthProductView.as_view(), name='baby-product_by_subcategory'),
    
    path('sport-goods/', SportProductView.as_view(), name='sports'),
    path('sport-goods/<str:subcategory>/', HealthProductView.as_view(), name='sport_by_subcategory'),
    
    path('video-games/', GameProductView.as_view(), name='games'),
    path('video-games/<str:subcategory>/', HealthProductView.as_view(), name='video-games_by_subcategory'),
]
