from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from home import views

from product import views
from order import views as OrderViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('product/', include('product.urls')),
    path('order/', include('order.urls')),
    path('user/', include('user.urls')),
    path('shopcart/', OrderViews.shopcart, name='shopcart'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/', views.filter_data, name='filter_data'),

    path('ckeditor/', include('ckeditor_uploader.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
