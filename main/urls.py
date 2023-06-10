from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.signup, name="sign-up"),
    path('subscribe', views.subscribe, name="news-letter"),
    path('shop/', views.shop, name='shop'),
    path('home/', views.home, name="home")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

