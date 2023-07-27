from django.urls import path, include
from .views import *
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
    path('delete-wishlist/', delete_wishlist, name="delete-wishlist")
]