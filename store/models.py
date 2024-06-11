from django.db import models # type: ignore
from category.models import Category
from django.urls import reverse # type: ignore
from accounts.models import Account
from django.db.models import Avg, Count # type: ignore
# Create your models here.
class Product(models.Model): 
    product_name   = models.CharField(max_length=200, unique=True)
    slug           = models.SlugField(max_length=200, unique=True)
    description    = models.TextField(max_length=500, blank=True)
    price          = models.IntegerField()
    images         = models.ImageField(upload_to='photos/products',)
    stock          = models.IntegerField()
    is_available   = models.BooleanField(default=True)
    category       = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date   = models.DateTimeField(auto_now_add=True)
    modified_date  = models.DateTimeField(auto_now_add=True)

    def get_url(self): 
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def averageReview(self): 
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0 
        if reviews['average'] is not None: 
            avg = float(reviews['average'])
        return avg
    def countReview(self): 
         reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('rating'))
         count = 0 
         if reviews['count'] is not None: 
            count = int(reviews['count'])
         return count

    def __str__(self): 
        return self.product_name

class VariationManager(models.Manager): 
    def colors(self): 
        return super(VariationManager, self).filter(varation_category='color', is_active=True)
    def sizes(self): 
        return super(VariationManager, self).filter(varation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variations(models.Model): 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    varation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta: 
        verbose_name = 'Variations'
        verbose_name_plural = 'Variations'
    
    objects = VariationManager()
    
    def __str__(self): 
        return self.variation_value


class ReviewRating(models.Model): 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_add = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.subject
    