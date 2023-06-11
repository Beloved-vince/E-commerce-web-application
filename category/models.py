from django.db import models
from main.models import COLOR_CHOICES


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

SUPERMARKET_CHOICE = (
    ('food cupboard', 'FOOD'),
    ('beverages', 'BEVERAGES'),
    ('beer', 'BEER, WINE & SPIRITS'),
    ('baby product', 'BABY PRODUCT'),
)

HEALTH_BEAUTY = (
    ('make up', 'MAKE UP'),
    ('personal care', 'PERSONAL CARE'),
    ('fragrances', 'FRAGRANCES'),
    ('hair care', 'HAIR CARE'),
    ('oral care', 'ORAL CARE'),
    ('health care', 'HEALTH CARE'),    
)

INDOOR_CHOICE = (
    ('home & kitchen', 'HOME& KITCHEN'),
    ('office', 'OFFICE PRODUCTS'),
    ('home & office furniture', 'HOME & OFFICE FURNITURE'),    
)

APPLIANCES_CHOICE = (
    ('small appliances', 'SMALL APPLIANCES'),
    ('large appliances', 'LARGE APPLIANCES'),
    
)

ELECTRONICS_CHOICE = (
    ('televisions & video', 'TELEVISION & VIDEO'),
    ('home audio', 'HOME AUDIO'),
    ('Generator', 'GENERATOR & PORTABLE POWER'),
)

PHONE_CHOICE = (
    ('mobile', 'MOBILE PHONES'),
    ('mobile accessories', 'MOBILE ACCESSOORIES'),
    ('tablets', 'TABLETS'),
)

COMPUTING_CHOICE = (
    ('computers', 'COMPUTER'),
    ('data storage', 'DATA STORAGE'),
    ('printers', 'PRINTERS')
)

FASHION_CHOICE = (
    ('women', "WOMEN'S FASHION"),
    ('men', "MEN'S FASHION"),
    ('kid', "KID'S FASHION"),
    ('all', 'ALL FASHION'),
    ('watch', 'WATCHES'),
    ('glass', 'GLASSES'),
)
GAME_CHOICE = (
    ('accessories', 'ACCESSORIES'),
)

SPORT_CHOICE = (
    ('gear', 'GEAR'),
    ('cardio training', 'CARDIO TRAINING'),
    ('team sport', 'TEAM SPORT'),
    ('training', 'STRENGTH TRAINING EQUIPMENT'),
)
BABY_CHOICE = (
    ('diapering', 'DIAPERING'),
    ('feeding', 'FEEDING'),
    ('toys', 'TOYS'),
    ('bathing', 'BATHING & SKIN CARE'),
)


class Category(models.Model):
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICE)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

# Create your models here.
class HealthBeautyProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=20, choices=HEALTH_BEAUTY, default=None)
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
    
class IndoorProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=30, choices=INDOOR_CHOICE, default=None)
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

class SupermarketProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=20, choices=SUPERMARKET_CHOICE, default=None)
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
class AppliancesProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=20, choices=APPLIANCES_CHOICE, default=None)
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
class ElectronicsProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=20, choices=ELECTRONICS_CHOICE, default=None)
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
    

class PhoneProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=20, choices=PHONE_CHOICE, default=None)
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
class ComputingProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=20, choices=COMPUTING_CHOICE, default=None)
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


class FashionProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=20, choices=FASHION_CHOICE, default=None)
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

class BabyProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=20, choices=BABY_CHOICE, default=None)
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

class SportProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=20, choices=SPORT_CHOICE, default=None)
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

class GameProduct(models.Model):
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
