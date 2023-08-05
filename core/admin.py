from django.contrib import admin
from .models import Product, Category, \
Vendor, CartOrder, CartOrderItems, ProductImage, \
ProductReview, Wishlish, Address;
# Register your models here.

class ProductImageAdmin(admin.TabularInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines =[ProductImageAdmin]
    list_display = ['pid', 'user', 'title', 'product_image', 'price', 'featured']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['cid', 'title', 'category_image']

class VendorAdmin(admin.ModelAdmin):
    list_display = ['vid', 'title', 'vendor_image']

class CarrOrderAdmin(admin.ModelAdmin):
    # list_editable = ['paid_status', 'product_status']
    list_display = ['user', 'price',  'order_date', ]

class CartOrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'order_image', 'quantity', 'price', 'total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_name', 'address', 'status']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CarrOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlish, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
