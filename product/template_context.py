from .models import Product
from django.db.models import Min,Max
def get_filters(request):
	cats=Product.objects.distinct().values('category__category','category__id')
	brands=Product.objects.distinct().values('brand__brand_name','brand__id')
	colors=Product.objects.distinct().values('color__color','color__id','color__color_code')
	sizes=Product.objects.distinct().values('size__size','size__id')
	minMaxPrice=Product.objects.aggregate(Min('price'),Max('price'))
	data={
		'cats':cats,
		'brands':brands,
		'colors':colors,
		'sizes':sizes,
		'minMaxPrice':minMaxPrice,
	}
	return data