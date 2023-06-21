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
    
    path('cart/', views.cart_view, name='cart_view'),    
    path('add-to-cart/', CartView.as_view(), name='add_to_cart'),
    
    path('view-cart-items/', CartView.as_view(), name='view_items'),
    path("add-item-to-cart/<str:product_id>.html", views.post, name='add_cart'),
    
    path("category/appliances/wish-list/", views.create_wishlist, name="wish_list"),
    path("wishlist/", views.wishlist_view, name="wishlist"),
    
    path("feedback-form/", views.capture_user_feedback, name="capture_feedback"),
    path("login/", views.login_view, name="login"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

