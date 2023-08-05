from rest_framework import serializers
from .models import *
from userauths.models import *

class UserSerialize(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CategorySerialize(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class VendorSerialize(serializers.ModelSerializer):
    user = UserSerialize(read_only=True)
    class Meta:
        model = Vendor
        fields = '__all__'

class ProductSerialize(serializers.ModelSerializer):
    category = CategorySerialize(read_only=True)
    vendor = VendorSerialize(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'pid', 'title', 'image', 'description', 'price',\
                   'old_price', 'product_status', 'type', 'stock', 'life',\
                      'mfd', 'status', 'in_stock', 'featured', 'digital',\
                          'sku', 'category', 'vendor', 'date', 'updated']
        
class ProductReviewSerialize(serializers.ModelSerializer):
    user = UserSerialize(read_only=True)
    product = ProductSerialize(read_only=True)
    class Meta:
        model = ProductReview
        fields = '__all__'

class CartOrderSerialize(serializers.ModelSerializer):
    user = UserSerialize(read_only=True)
    class Meta:
        model = CartOrder
        fields = '__all__'

class CartOrderItemsSerialize(serializers.ModelSerializer):
    class Meta:
        model = CartOrderItems
        fields = '__all__'