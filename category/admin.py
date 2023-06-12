from django.contrib import admin
from .models import *


# Register your models here.
category_models = [HealthBeautyProduct, IndoorProduct, SupermarketProduct,
                   AppliancesProduct, ElectronicsProduct, PhoneProduct, ComputingProduct,
                   FashionProduct, BabyProduct, SportProduct, GameProduct]

for all in category_models:
    admin.site.register(all)

# admin.site.register(Product)

