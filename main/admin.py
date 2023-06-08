from django.contrib import admin
from .models import User, UserManager, Subscription

# Register your models here.
admin.site.register(User)
admin.site.register(Subscription)