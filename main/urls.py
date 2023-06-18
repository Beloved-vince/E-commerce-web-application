from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from cart.views import CartView



urlpatterns = [
    path('', views.home, name="home"),
    path('sign-up/', views.signup, name="sign-up"),
    path('subscribe', views.subscribe, name="news-letter"),
    path('shop/', views.shop, name='shop'),
    path('<str:product_id>.html', views.details, name='carting'),    
    path('add-to-cart/', CartView.as_view(), name='add_to_cart'),
    path('view-cart-items/', CartView.as_view(), name='view_items'),
    path("add-cart/", views.post, name='add_cart'),
    path("login/", views.login_view, name="login")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

