from django.shortcuts import render, get_object_or_404 # type: ignore
from store.models import Product 
from category.models import Category
# Create your views here.

# Home url
def home(request): 
     products = Product.objects.all().filter(is_available=True)

     context = {
          'products': products
     }
     return render(request, 'BestStore/home.html', context)

def store(request, category_slug=None): 
     categories = None 
     products = None 
     if category_slug != None: 
          categories = get_object_or_404(Category, slug=category_slug)
          products = Product.objects.filter(category=categories, is_available=True)
          product_count = products.count()
     else: 
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

     context = {
          'categories': Category.objects.all(),
          'products': products,
          'product_count': product_count
     }
     return render(request, 'BestStore/store/store.html', context)
def product_detail(request, category_slug, product_slug): 
     try: 
          product = Product.objects.get(category__slug=category_slug, slug=product_slug)
     except Exception as e: 
          raise e 
     
     context = {
          'single_product': product
     }

     return render(request, 'BestStore/store/product_detail.html', context)