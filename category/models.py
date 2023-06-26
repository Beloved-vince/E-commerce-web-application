from django.db import models
from main.models import Category, Product



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
)
BABY_CHOICE = (
    ('diapering', 'DIAPERING'),
    ('feeding', 'FEEDING'),
    ('toys', 'TOYS'),
)

class HealthBeautyProduct(Product):
    sub_category = models.CharField(max_length=20, choices=HEALTH_BEAUTY, default=None, null=True)
# Create your models here.

    
class IndoorProduct(Product):
    sub_category = models.CharField(max_length=30, choices=INDOOR_CHOICE, default=None, null=True)

class SupermarketProduct(Product):
    sub_category = models.CharField(max_length=20, choices=SUPERMARKET_CHOICE, default=None, null=True)

class AppliancesProduct(Product):
    sub_category = models.CharField(max_length=20, choices=APPLIANCES_CHOICE, default=1,  null=True)
    

class ElectronicsProduct(Product):
    sub_category = models.CharField(max_length=20, choices=ELECTRONICS_CHOICE, default=None, null=True)


class PhoneProduct(Product):

    sub_category = models.CharField(max_length=20, choices=PHONE_CHOICE, default=None, null=True)

class ComputingProduct(Product):
    sub_category = models.CharField(max_length=20, choices=COMPUTING_CHOICE, default=None, null=True)
        

class FashionProduct(Product):
    sub_category = models.CharField(max_length=20, choices=FASHION_CHOICE, default=None, null=True)
    
class BabyProduct(Product):
    sub_category = models.CharField(max_length=20, choices=BABY_CHOICE, default=None, null=True)
    

class SportProduct(Product):
    sub_category = models.CharField(max_length=20, choices=SPORT_CHOICE, default=None, null=True)


class GameProduct(Product):
    sub_category = models.CharField(max_length=20, choices=GAME_CHOICE, default=None, null=True)
