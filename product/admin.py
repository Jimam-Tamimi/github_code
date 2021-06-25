from django.contrib import admin
from product import models
from product.models import Category, SubCategory, ChildSubCategory, Brand, Color, Size, Multiple_Product_Images, Product, CommentForm, Comment, Variants
# Register your models here.

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'timeStamp')

@admin.register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'sub_category', 'timeStamp')

@admin.register(models.ChildSubCategory)
class ChildSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('sub_category', 'child_sub_category', 'timeStamp')

@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'image')

@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('color', 'color_code')

# @admin.register(models.Size)
# class SizeAdmin(admin.ModelAdmin):
#     list_display = ('size')


admin.site.register(Size)

class productImageInline(admin.TabularInline):
    model = Multiple_Product_Images
    extra = 1

class ProductVariantsInline(admin.TabularInline):
    model = Variants
    # readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title']
admin.site.register(Multiple_Product_Images,ImagesAdmin)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'brand', 'category', 'sub_category', 'child_sub_category',
                    'status', 'is_featured')
    list_editable = ('status', 'is_featured')
    list_filter = ['brand']
    inlines = [productImageInline, ProductVariantsInline]
    prepopulated_fields = {'slug': ('product_name',)}
     

class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title','product','color','size','price','quantity']
admin.site.register(Variants,VariantsAdmin)

    
@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment', 'status','create_at']
    list_filter = ['status']
    readonly_fields = ('subject','comment','user','product','rate','id')
