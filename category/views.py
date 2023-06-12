from django.shortcuts import render
from .models import *

# Create your views here.
class BaseProductView:
    """
        OOP class encapsulated for rendering endpoint for the model
    """
    model = None
    template_name = 'shop.html'

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_queryset()
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())


class HealthProductView(BaseProductView):
    model = HealthBeautyProduct

class IndoorProductView(BaseProductView):
    model = IndoorProduct

class SupermarketProductView(BaseProductView):
    model = SupermarketProduct

class AppliancesProductView(BaseProductView):
    model = AppliancesProduct

class ElectronicsProductView(BaseProductView):
    model = ElectronicsProduct
    
class PhoneProductView(BaseProductView):
    model = PhoneProduct

class ComputingProductView(BaseProductView):
    model = ComputingProduct

class FashionProductView(BaseProductView):
    model = FashionProduct

class BabyProductView(BaseProductView):
    model = BabyProduct

class SportProductView(BaseProductView):
    model = SportProduct

class GameProductView(BaseProductView):
    model = GameProduct
