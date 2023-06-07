from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.signup, name="sign-up"),
    path('subscribe', views.Subscriber, name="news-letter")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)