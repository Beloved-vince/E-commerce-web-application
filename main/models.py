from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser,  BaseUserManager, User
from uuid import uuid4

class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



SUB_CATEGORY =(
    ('official', 'OFFICIAL STORES'),
    ('books', 'BOOKS, MOVIES AND MUSIC'),
    ('pet', 'PET SUPPLIES'),

)
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



# - - -------------------------------------------- BREAKAGE - ------------------------------------------------------#

from uuid import uuid4, uuid3, uuid5
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    manufacture_by = models.CharField(max_length=200)
    # color = models.CharField(max_length=10, choices=COLOR_CHOICES)
    discount_percentage = models.DecimalField(max_digits=7, decimal_places=2, null=True, default=0)
    
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
            pass

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
        return f"{self.quantity} * {self.product.price} in Cart #{self.cart.id}"
    

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid3, editable=False)
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
    

class UserFeedback(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    feedback_text = models.TextField()

    def __str__(self):
        return self.name
