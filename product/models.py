from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.forms import ModelForm
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

from django.db.models import Avg, Count

class Category(models.Model):
    category = models.CharField(max_length=100, unique=True, blank=False)
    parent = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True, unique=True)
    timeStamp=models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        verbose_name_plural = '1. Categories'
    def __str__(self):
        return self.category

class SubCategory(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=100, unique=True, blank=False)
    timeStamp=models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        verbose_name_plural = '2. Sub-categories'
    def __str__(self):
        return self.sub_category

class ChildSubCategory(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    child_sub_category = models.CharField(max_length=100, unique=True, blank=False)
    timeStamp=models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        verbose_name_plural = '3. Child sub-categories'
    def __str__(self):
        return self.child_sub_category


class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="brand_images/")
    class Meta:
        verbose_name_plural = '4. Brands'
    def __str__(self):
        return self.brand_name

# Color

class Color(models.Model):
    color = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = '5. Colors'
    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))
    def __str__(self):
        return self.color

# Size


class Size(models.Model):
    size = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = '6. Sizes'
    def __str__(self):
        return self.size


# Product Model
class Product(models.Model):

    status_choice = (
        ("Published", "Published"),
        ("Unlisted", "Unlisted"),
        ("Private", "Private"),
    )

    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )
    id = models.AutoField(unique=True, primary_key=True)
    product_name = models.CharField(max_length=200, unique=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    product_details = RichTextUploadingField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    child_sub_category = models.ForeignKey(ChildSubCategory, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    color = models.ManyToManyField(Color, blank=True)
    size = models.ManyToManyField(Size, blank=True)
    slug = models.SlugField(null=False, unique=True)
    price = models.PositiveIntegerField(default=0)
    # price_2 = models.FloatField()
    variant=models.CharField(max_length=10,choices=VARIANTS, default='None')
    discount_price = models.PositiveIntegerField(default=0, blank=True)
    image = models.ImageField(upload_to='products_images/', blank=True)
    image_url = models.CharField(max_length=1000, blank=True)
    delivery_cost = models.PositiveIntegerField(default=0, blank=True)
    shipping_information = RichTextUploadingField(blank=True)
    return_policy = RichTextUploadingField(blank=True)
    total_sells = models.PositiveIntegerField(default=0, null=True, blank=True)
    status = models.CharField(choices=status_choice, max_length=30, default='Published')
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = '7. Products'

    def __str__(self):
        return self.product_name

    # image tag doesn't appear needs working
    def image_tag(self):
        if self.image is None:
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.image_url.url))
        elif self.image_url is None:
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def averagereview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(average=Avg('rate'))
        avg=0
        if reviews["average"] is not None:
            avg=float(reviews["average"])
        return avg

    def countreview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

class Multiple_Product_Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='products_images/', blank=True)
    image_url = models.CharField(max_length=1000, blank=True)

    class Meta:
        verbose_name_plural = '8. Multiple Product Images'

    def __str(self):
        return self.alt_text



class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    image_id = models.IntegerField(blank=True,null=True,default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)

    def __str__(self):
        return self.title

    def image(self):
        img = Multiple_Product_Images.objects.get(id=self.image_id)
        if img.id is not None:
            if img.image is not None:
                varimage = img.image.url
            elif img.image_url is not None:
                varimage = img.image_url.url            
        else:
            varimage=""
        return varimage

    # def image_tag(self):
    #     img = Multiple_Product_Images.objects.get(id=self.image_id)
    #     if img.id is not None:
    #         if img.image is not None:
    #             return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
    #         elif img.image_url is not None:
    #             return mark_safe('<img src="{}" height="50"/>'.format(img.image_url.url))     
    #     else:
    #         return ""
    
    class Meta:
        verbose_name_plural = '9. Product Variants'
    
    
class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.TextField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status=models.CharField(max_length=10,choices=STATUS, default='New')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '10. Reviews'
        
    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']
        
        

  

