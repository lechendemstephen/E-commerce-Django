from django.shortcuts import render # type: ignore
from .models import Category

def menu_links(request): 
    links = Category.objects.all()
    return {
        'links': links
    }