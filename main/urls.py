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
    
    path('cart-items/', views.cart_view, name='cart_view'),    
    path('add-to-cart/', CartView.as_view(), name='add_to_cart'),
    path('update-items/', views.update_cart, name="update-items"),
    path('cart-items/<int:item_id>', views.delete_cart_item, name="delete-cart-items"),
    
    path('view-cart-items/', CartView.as_view(), name='view_items'),
    path("add-item-to-cart/<str:product_id>.html", views.add_to_cart, name='add_cart'),
    
    
    path("wish-list", views.create_wishlist, name="wish_list"),
    path("search/results/wish-list", views.create_wishlist, name="wish_list"),
    path("category/appliances/wish-list/", views.create_wishlist, name="wish_list"),
    path("category/grocery/wish-list/", views.create_wishlist, name="wish_list"),
    path("category/indoor/wish-list/", views.create_wishlist, name="wish_list"),
    path("category/health/wish-list/", views.create_wishlist, name="wish_list"),
    path("category/electronics/wish-list/", views.create_wishlist, name="wish_list"),
    path("category/phones-tablets/wish-list/", views.create_wishlist, name="wish_list"),
    path("category/computing/wish-list/", views.create_wishlist, name="wish_list"),
    path("category/fashion/wish-list/", views.create_wishlist, name="wish_list"),
    path("category/baby-product/wish-list/", views.create_wishlist, name="wish_list"),
    path("category/sport-goods/wish-list/", views.create_wishlist, name="wish_list"),
    
    path('wishlist/<int:wishlist_id>/delete/<int:product_id>/', views.delete_wishlist_item, name='delete_wishlist_item'),
    path("wishlist/", views.wishlist_view, name="wishlist"),
    
    path("feedback-form/", views.capture_user_feedback, name="capture_feedback"),
    path("login/", views.login_view, name="login"),
    
    path("edit-account/", views.update_profile, name="edit-account"),
    path("change-password/", views.change_password, name="change-password"),
    
    path("create-address/", views.create_address, name="address_list"),
    path("order-details/", views.order_details, name="order-details"),
    
    path('search/', views.SearchView.as_view(), name='search'),
    path('search/results/', views.SearchResultsView.as_view(), name='search_results'),
    
    path('checkout', views.checkout, name='checkout')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

