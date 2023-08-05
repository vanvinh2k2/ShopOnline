from django.urls import path, include
from .views import *
from .backend import *
app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('category/<cid>/', category_product_list, name='category'),
    path('vendor/', vender_list, name='vendor'),
    path('vendor/<vid>/', vender_detail_list, name='vendor-detail'),
    path('product/<pid>/', product_detail_list, name='product-detail'),
    path('product/tag/<slug:tag_slug>/', tag_list, name='tag'),
    path('add-review/<pid>/', add_review, name='add-review'),
    path('search/', search_view, name='search'),
    path('product-filter/', filter_product, name="product-filter"),
    path('add-cart/', add_cart, name='add-cart'),
    path('cart/', cart_view, name='cart'),
    path('delete-cart/', delete_cart, name='delete-cart'),
    path('update-cart/', update_cart, name='update-cart'),
    path('checkout/', checkout, name='checkout'),
    path('payment-completed/', payment_completed, name='payment-completed'),
    path('payment-failed/', payment_failed, name='payment-failed'),
    path('dashboard/', customer_dashboard, name="dashboard"),
    path('dashboard/order/<int:id>', order_detail, name="order-detail"),
    path('add-address/', add_address, name="add-address"),
    path('update-address/', update_address, name="update-address"),
    path('add-wishlist/', add_wishlist, name="add-wishlist"),
    path('address-default/', address_default, name="address-default"),
    path('display-data-update/', display_data_update, name="display-data-update"),
    path('wishlist/', wishlist_view, name="wishlist"),
    path('save-profile/', save_profile, name="save-profile"),
    path('contact-us/', contact_us, name="contact"),
    path('delete-wishlist/', delete_wishlist, name="delete-wishlist"),
# --------------------------------------------------------------------------------------------------
    # API
    path('api/category/', CategoryAPI.as_view(), name='api-category-list'),
    path('api/category/<cid>/', CategoryAPI.as_view(), name='api-category'),
    path('api/vendor/', VendorAPI.as_view(), name='api-vendor-list'),
    path('api/vendor/<vid>/', VendorAPI.as_view(), name='api-vendor'),
    path('api/product/', ProductAPI.as_view(), name='api-product-list'),
    path('api/product/<pid>/', ProductAPI.as_view(), name='api-product'),
    path('api/add-review/<id>/<pid>/', add_product_review, name='api-add-review'),
    path('api/get-review/<pid>/', get_product_review, name='api-get-review'),
    path('api/search/', search, name='api-search'),
    path('api/filter-category/<cid>/', filter_category, name='api-filter-category'),
    path('api/cart/<id>/', cart, name='api-cart'),
    path('api/detail-cart/<oid>/', cart_detail, name='api-detail-cart'),
]