from django.shortcuts import redirect, render

from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from product import models
from product.models import Category, SubCategory, ChildSubCategory, Brand, Color, Size, Multiple_Product_Images, Product

from django.core.mail import EmailMessage
# from api.models import Favorites
# Create your views here.

def index(request):
    products = Product.objects.all().order_by('?')[:20]
    featured_products = Product.objects.filter(is_featured=True).order_by('-id')
    newest_products = Product.objects.all().order_by('-id')[:20]
    popular_products = Product.objects.all().order_by('-total_sells')[:20]
    
    context = {
        'products': products, 
        'newest_products': newest_products,
        'popular_products': popular_products,
    }
    return render(request, 'index.html', context)
