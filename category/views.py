from django.shortcuts import render
from .models import *
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
class BaseProductView(View):
    """
    OOP class encapsulated for rendering endpoint for the model
    """
    model = None
    template_name = 'shop.html'
    per_page = 12

    def get_queryset(self, subcategory=None):
        queryset = self.model.objects.all()
        if subcategory:
            queryset = queryset.filter(sub_category=subcategory)
        return queryset

    def get_context_data(self, subcategory=None, **kwargs):
        context = {}
        from django.db.models import F
        
        sort_by = self.request.GET.get('sort_by', 'position')
        products = Product.objects.all()
        
        if sort_by == 'name':
            products = products.order_by('name')
        elif sort_by == 'price':
            products = products.order_by('price')
            
        else:
            products = products.annotate(position=F('id'))
        
        query_set = self.get_queryset(subcategory)
        
        paginator = Paginator(query_set, self.per_page)
        
        page_number = self.request.GET.get('page')
        
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)
            
        context['products'] = page_obj
        context['sort_by'] = sort_by
        
        return context

    def get(self, request, *args, **kwargs):
        subcategory = request.GET.get('subcategory')
        context = self.get_context_data(subcategory)
        return render(request, self.template_name, context)


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
    



def home(request):
    return render (request, "index.html") 