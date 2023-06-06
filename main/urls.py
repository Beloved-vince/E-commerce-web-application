from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.login)
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)