from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    """"
        Create user model params for signing up
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
        first_name = models.CharField(max_length=200)
        last_name = models.CharField(max_length=200)
        email =models.EmailField(unique=True)
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=False)
        
        USERNAME_FIELDS = 'email'
        REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'password']
        
        
        objects = UserManager()

        def __str__(self):
            return self.email