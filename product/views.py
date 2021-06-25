from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from product.models import Category, SubCategory, ChildSubCategory, Brand, Color, Size, Multiple_Product_Images, Product, CommentForm, Comment, Variants
from django.contrib import messages

import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q, F
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request

from django.template.loader import render_to_string
from django.urls import reverse

from home.forms import SearchForm
from home.models import ContactForm, ContactMessage
from src import settings
from user.models import UserProfile


def index(request):
    products_slider = Product.objects.all().order_by('id')[:4]  #first 4 products
    products_picked = Product.objects.all().order_by('?')[:4]   #Random selected 4 products
    page="home"
    context={
             'page':page,
             'products_slider': products_slider,
             'products_latest': products_latest,
             'products_picked': products_picked,
             #'category':category
             }
    return render(request,'index.html',context)


def aboutus(request):
    return render(request, 'about.html', context)

def contactus(request):
    if request.method == 'POST': # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage() #create relation with model
            data.name = form.cleaned_data['name'] # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  #save data to table
            messages.success(request,"Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')
    form = ContactForm
    context={'form':form  }
    return render(request, 'contactus.html', context)


def category_products(request,id,slug):
    catdata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id) #default language
    context={'products': products,
             #'category':category,
             'catdata':catdata }
    return render(request,'category_products.html',context)


def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query,category_id=catid)

            category = Category.objects.all()
            context = {'products': products, 'query':query,
                       'category': category }
            return render(request, 'home/products.html', context)
    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)
        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title +" > " + rs.category.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def product_detail(request,id,slug):
    query = request.GET.get('q')
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    more_from_shop = Product.objects.filter(brand=product.brand).exclude(id=id)
    top_picks = Product.objects.all().order_by('?')
    images = Multiple_Product_Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id,status='True')
    context = {'product': product,'category': category,
               'images': images, 'comments': comments,
               'more_from_shop': more_from_shop, 'top_picks': top_picks
               }
    if product.variant !="None": # Product have variants
        if request.method == 'POST': #if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id) #selected product by click color radio
            colors = Variants.objects.filter(product_id=id,size_id=variant.size_id )
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
            query += variant.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
            variant =Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant,'query': query
                        })
    return render(request,'home/single_product.html',context)


def addcomment(request,id):
   url = request.META.get('HTTP_REFERER')  # get last url
   #return HttpResponse(url)
   if request.method == 'POST':  # check post
      form = CommentForm(request.POST)
      if form.is_valid():
        data = Comment()  # create relation with model
        data.subject = form.cleaned_data['subject']
        data.comment= form.cleaned_data['comment']
        data.rate = form.cleaned_data['rate']
        data.ip = request.META.get('REMOTE_ADDR')
        data.product_id=id
        current_user= request.user
        data.user_id=current_user.id
        data.save()  # save data to table
        messages.success(request, "Your review has ben sent. Thank you for your interest.")
        return HttpResponseRedirect(url)
   return HttpResponseRedirect(url)

def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)

def colors(request):
    return render(request,'product_color.html')


def filter_data(request):
	colors=request.GET.getlist('color[]')
	categories=request.GET.getlist('category[]')
	brands=request.GET.getlist('brand[]')
	sizes=request.GET.getlist('size[]')
	# minPrice=request.GET['minPrice']
	# maxPrice=request.GET['maxPrice']
	allProducts=Product.objects.all().order_by('-id').distinct()
	# allProducts=allProducts.filter(productattribute__price__gte=minPrice)
	# allProducts=allProducts.filter(productattribute__price__lte=maxPrice)
    
	if len(colors)>0:
		allProducts=allProducts.filter(color__id__in=colors).distinct()
	if len(categories)>0:
		allProducts=allProducts.filter(category__id__in=categories).distinct()
	if len(brands)>0:
		allProducts=allProducts.filter(brand__id__in=brands).distinct()
	if len(sizes)>0:
		allProducts=allProducts.filter(size__id__in=sizes).distinct()
	t=render_to_string('home/products.html',{'data':allProducts})
    
	return render (request, 'home/products.html',{'data':allProducts})
