from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser,  BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    """"
        Create user model params for signing up
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Define user data arguements
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(max_length=200, unique=False)
    last_name = models.CharField(max_length=200, unique=False)
    email = models.EmailField(unique=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'password', 'confirm_password']

    objects = UserManager()

    # Add related_name arguments to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.email


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


CATEGORY_CHOICE = (
    ('supermarket', 'SUPERMARKET'),
    ('health&beauty', 'HEALTH & BEAUTY'),
    ('home&office', 'HOME & OFFICE'),
    ('appliances', 'APPLIANCES'),
    ('phones&tablets', 'PHONE & TABLETS'),
    ('computing', 'COMPUTING'),
    ('eletronics', 'ELECTRONICS'),
    ('fashion', 'FASHION'),
    ('Baby product', 'BABY PRODUCTS'),
    ('gaming', 'GAMING'),
    ('sporting goods', 'SPORTING GOODS'),
    ('other categories', 'OTHER CATEGORIES'),
)

SUB_CATEGORY =(
    ('food cupboard', 'FOOD'),
    ('beverages', 'BEVERAGES'),
    ('beer', 'BEER, WINE & SPIRITS'),
    ('baby product', 'BABY PRODUCT'),
    ('make up', 'MAKE UP'),
    ('personal care', 'PERSONAL CARE'),
    ('fragrances', 'FRAGRANCES'),
    ('hair care', 'HAIR CARE'),
    ('oral care', 'ORAL CARE'),
    ('health care', 'HEALTH CARE'),
    ('home & kitchen', 'HOME& KITCHEN'),
    ('office', 'OFFICE PRODUCTS'),
    ('home & office furniture', 'HOME & OFFICE FURNITURE'),
    ('small appliances', 'SMALL APPLIANCES'),
    ('large appliances', 'LARGE APPLIANCES'),
    ('mobile', 'MOBILE PHONES'),
    ('mobile accessories', 'MOBILE ACCESSOORIES'),
    ('tablets', 'TABLETS'),
    ('computers', 'COMPUTER'),
    ('data storage', 'DATA STORAGE'),
    ('printers', 'PRINTERS'),
    ('televisions & video', 'TELEVISION & VIDEO'),
    ('home audio', 'HOME AUDIO'),
    ('Generator', 'GENERATOR & PORTABLE POWER'),
    ('women', "WOMEN'S FASHION"),
    ('men', "MEN'S FASHION"),
    ('kid', "KID'S FASHION"),
    ('all', 'ALL FASHION'),
    ('watch', 'WATCHES'),
    ('glass', 'GLASSES'),
    ('diapering', 'DIAPERING'),
    ('feeding', 'FEEDING'),
    ('toys', 'TOYS'),
    ('bathing', 'BATHING & SKIN CARE'),
    ('gear', 'GEAR'),

    
)

class Category(models.Model):
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICE)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name


COLOR_CHOICES = (
    ('red', 'Red'),
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('yellow', 'Yellow'),
    ('orange', 'Orange'),
    ('purple', 'Purple'),
    ('pink', 'Pink'),
)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    manufacture_by = models.CharField(max_length=200)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    def __str__(self) -> str:
        return self.name

    @property
    def discounted_price(self):
        if self.discount_percentage is not None:
            discounted_amount = round(self.price * (1 - self.discount_percentage / 100), 2)
            return discounted_amount
        return self.price
    
    @property
    def discount(self):
        if self.discount_percentage:
            self.discount_percentage = round((self.discount_percentage * 100) / self.price, 2)
            return f"{self.discount_percentage}%"
        else:
            return ""

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"Cart #{self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} * {self.product.name} in Cart #{self.cart.id}"
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment #{self.id}"
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    
    def __str__(self):
        return f"Wishlist for {self.user.username}"


class Coupon(models.Model):
    code = models.CharField(max_length=50)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return self.code