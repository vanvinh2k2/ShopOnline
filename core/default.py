from .models import Product, Category, \
Vendor, CartOrder, CartOrderItems, ProductImage, \
ProductReview, Wishlish, Address;
from django.db.models import Min, Max, Count

def default(request):
    categorys = Category.objects.all()
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))
    try:
        count_wishlist = Wishlish.objects.filter(user=request.user).count()
    except: count_wishlist = 0;

    return {
        'min_max_price' : min_max_price,
        'categorys' : categorys,
        'count_wishlist' : count_wishlist
    }
