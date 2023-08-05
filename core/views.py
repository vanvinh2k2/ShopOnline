from django.shortcuts import render, get_object_or_404, redirect
from taggit.models import Tag
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string
from .models import Product, Category, \
Vendor, CartOrder, CartOrderItems, ProductImage, \
ProductReview, Wishlish, Address;
from userauths.models import Profile
from .forms import ProductReviewForm
import calendar
from django.db.models.functions import ExtractMonth

from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.

def index(request):
    productsHot = Product.objects.filter(product_status="published", featured=True)
    products = Product.objects.filter(product_status="published")

    content = {'productsHot' : productsHot, 'products' : products}
    return render(request, 'core/index.html', content)

def category_product_list(request, cid):
    vendors = Vendor.objects.all()
    category = Category.objects.get(cid=cid);
    products = Product.objects.filter(category=category, product_status="published");
    txt_search = category.title
    
    content = {'category' : category, 'products' : products,\
                'txt_search': txt_search, "vendors" : vendors}
    return render(request, 'core/category.html', content)

def vender_list(request):
    vendors = Vendor.objects.all()
    content = {"vendors" : vendors}
    return render(request, 'core/vendor.html', content)

def vender_detail_list(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor)

    content = {"vendor" : vendor, "products" : products}
    return render(request, 'core/detail-vendor.html', content)

def product_detail_list(request, pid):
    product = Product.objects.get(pid=pid)
    productImages = product.product_images.all()
    vendor = product.vendor
    products = Product.objects.filter(vendor=vendor)
    reviews = ProductReview.objects.filter(product=product)
    avg_rate = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    forms = ProductReviewForm()
    make_review = True

    if request.user.is_authenticated:
        user_review = ProductReview.objects.filter(user=request.user, product=product).count()
        if user_review > 0:
            make_review = False

    content = {"productdetail" : product, "productImages" : productImages,'avg_rate' : avg_rate,\
                'vendor' : vendor, "products" : products, 'reviews' : reviews, 'forms' : forms, \
                    'make_review':make_review}
    return render(request, 'core/detail-product.html', content)

def tag_list(request, tag_slug=None):
    vendors = Vendor.objects.all()
    products = Product.objects.filter(product_status="published").order_by("-pid")
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    txt_search = "#"+str(tag)

    content = {'txt_search' : txt_search, 'products' : products, "vendors" : vendors}
    return render(request, 'core/category.html', content)

def add_review(request, pid):
    product = Product.objects.get(pid=pid)
    user = request.user
    review = request.POST['review']
    rating = request.POST['rating']

    review_form = ProductReview.objects.create(user=user, product=product, review=review, rating=rating)

    context = {
        'user' : user.username,
        'review' : review,
        'rating' : rating,
        'date' : review_form.date,
    }
    avg_review = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    return JsonResponse({'bool':True, 'context':context, 'avg_review':avg_review})

def search_view(request):
    txt_search = request.GET['txt_search']
    products = Product.objects.filter(title__icontains=txt_search).order_by("-date")
    vendors = Vendor.objects.all()
    categorys = Category.objects.all()

    context = {'txt_search': txt_search, "products":products, 'categorys' : categorys, "vendors" : vendors}
    return render(request, 'core/category.html', context)

def filter_product(request):
    vendors = request.GET.getlist('vendor[]')
    min_max_price = request.GET.getlist('filter-price[]')
    evaluates = request.GET.getlist('evaluate[]')

    max_price = min_max_price[1]
    min_price = min_max_price[0]
    
    products = Product.objects.filter(product_status='published').order_by("-id").distinct()
    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)
    # avg_rating = products.aaggregate(product__rating=Avg('product__rating'))

    if len(vendors)>0:
        products = products.filter(vendor_id__in = vendors).distinct()

    if len(evaluates)>0:
        products = products.filter(product__rating__in = evaluates).distinct()

    context = {'products': products}
    data = render_to_string('core/async/detail-product.html', context)

    return JsonResponse({'data': data})

@login_required
def add_cart(request):
    cart_product = {}
    cart_product[str(request.GET['product_id'])] = {
        'title' : request.GET['product_title'],
        'qty' : request.GET['quantity'],
        'price' : request.GET['product_price'],
        'image' : request.GET['product_image'],
        'pid' : request.GET['product_pid']
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['product_id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['product_id'])]['qty'] = int(cart_product[str(request.GET['product_id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else: 
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({'data' : request.session['cart_data_obj'], 'totalcartitems' : len(request.session['cart_data_obj'])})

def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, 'core/cart.html', {'cart_data' : request.session['cart_data_obj'], \
            'totalCartItems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request, 'Your cart is empty!')
        return redirect('core:index')
    
def delete_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del cart_data[product_id]
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string('core/async/cart-product.html', {'cart_data' : request.session['cart_data_obj'], \
             'cart_total_amount':cart_total_amount, 'totalCartItems':len(request.session['cart_data_obj'])})
    return JsonResponse({'data_cart' : context, 'totalCartItems':len(request.session['cart_data_obj'])})

def update_cart(request):
    product_id = str(request.GET['id'])
    quantity = str(request.GET['qty'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[product_id]['qty'] = quantity
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string('core/async/cart-product.html', {'cart_data' : request.session['cart_data_obj'], \
             'cart_total_amount':cart_total_amount, 'totalCartItems':len(request.session['cart_data_obj'])})
    return JsonResponse({'data_cart' : context, 'totalCartItems':len(request.session['cart_data_obj'])})

@login_required
def checkout(request):
    cart_total_amount = 0
    total_amount = 0;
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])

        order = CartOrder.objects.create(user=request.user, price=total_amount)

        for pid, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            cart_order_products = CartOrderItems.objects.create(
                order = order,
                invoice_no = "INVOICE_NO-"+ str(order.id),
                item = item['title'],
                image = item['image'],
                quantity = item['qty'],
                price = item['price'],
                total = float(item['qty']) * float(item['price'])
            )

    host = request.get_host()
    paypal_dict = {
        'business' : settings.PAYPAL_RECEIVER_EMAIL,
        'amount' : cart_total_amount,
        'item_name' : 'Order-Item-No-'+str(order.id),
        'invoice' : "INVOICE_NO-"+ str(order.id),
        'currency_code' : "USD",
        'notify_url' : f'http://{host}{reverse("paypal-ipn")}',
        'return_url' : f'http://{host}{reverse("core:payment-completed")}',
        'cancel_return' : f'http://{host}{reverse("core:payment-failed")}',
    }
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'core/checkout.html', {'cart_data' : request.session['cart_data_obj'],'cart_total_amount' : total_amount, \
             'totalCartItems':len(request.session['cart_data_obj']), 'paypal_payment_button' : paypal_payment_button})

@login_required
def payment_completed(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    return render(request, 'core/payment-completed.html', {'cart_data' : request.session['cart_data_obj'], \
            'cart_total_amount' : cart_total_amount, 'totalCartItems':len(request.session['cart_data_obj'])})

@login_required
def payment_failed(request):
    return render(request, 'core/payment-failed.html')

@login_required
def customer_dashboard(request):
    orders = CartOrder.objects.filter(user=request.user).order_by("-id")
    addresses = Address.objects.filter(user=request.user)
    profile = Profile.objects.get(user= request.user)
    orders_chart = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values('month', 'count')
    month = []
    total_orders = []

    for i in orders_chart :
        month.append(calendar.month_name[i['month']])
        total_orders.append(i['count'])

    context = {"orders" : orders, 'addresses': addresses, 'month' : month, 'total_orders' : total_orders, 'profile' : profile}
    return render(request, 'core/dashboard.html', context)

@login_required
def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderItems.objects.filter(order=order)
    productsHot = Product.objects.filter(product_status="published", featured=True)

    context = {"order_items" : order_items, 'products' : productsHot}
    return render(request, 'core/order-detail.html', context)

@login_required
def add_address(request):
    display_name = request.GET['display-name']
    mobile = request.GET['mobile']
    address = request.GET['address']
    addresses = Address.objects.filter(user=request.user)
    if len(addresses) > 0:
        Address.objects.create(
                    user = request.user,
                    address=address,
                    mobile = mobile,
                    display_name = display_name,
                    status=True
                )
    else : Address.objects.create(
                    user = request.user,
                    address=address,
                    mobile = mobile,
                    display_name = display_name,
                    status=True,
                    is_default=True
                )
    addresses = Address.objects.filter(user=request.user)
    context = render_to_string('core/async/address.html', {'addresses': addresses})
    return JsonResponse({'data' : context})

@login_required
def add_wishlist(request):
    product_id = request.GET['product_id']
    product = Product.objects.get(id=product_id)
    wishlish_count = Wishlish.objects.filter(user=request.user, product=product).count()

    if wishlish_count > 0 :
        data = False
    else :
        Wishlish.objects.create(
            user=request.user,
            product=product
        )
        data = True

    return JsonResponse({'data': data})

def delete_wishlist(request):
    wishlist_id = request.GET['wishlist-id']
    wishlist = Wishlish.objects.get(id=wishlist_id)
    wishlist.delete()
    wishlists = Wishlish.objects.filter(user=request.user)
    wishlists_count = len(wishlists)
    context = render_to_string("core/async/wishlist.html", {'wishlists': wishlists, 'wishlists_count' : wishlists_count})
    return JsonResponse({'data': context})

def update_address(request):
    address_id = request.GET['address_id']
    display_name = request.GET['display-name']
    mobile = request.GET['mobile']
    address = request.GET['address']
    addresses = Address.objects.filter(user=request.user)

    address_update = Address.objects.get(user=request.user, id=address_id)
    address_update.address = address
    address_update.mobile = mobile
    address_update.display_name = display_name
    address_update.save()

    context = render_to_string('core/async/address.html', {'addresses': addresses})
    return JsonResponse({'data' : context})

def address_default(request):
    address_id = request.GET['address_id'];
    addresses = Address.objects.filter(user=request.user)
    address_default = Address.objects.get(user=request.user, is_default = True)
    address_default.is_default = False
    address_default.save()

    address_new = Address.objects.get(user=request.user, id=address_id)
    address_new.is_default = True
    address_new.save()
    context = render_to_string('core/async/address.html', {'addresses': addresses})
    return JsonResponse({'data' : context})

def display_data_update(request):
    address_id = request.GET['address_id'];
    print(address_id)
    address = Address.objects.get(user=request.user, id=address_id)

    context = render_to_string("core/async/dialog-update.html", {'address' : address})
    return JsonResponse({"data" : context})

@login_required
def wishlist_view(request):
    products = Product.objects.filter(product_status="published", featured=True)
    wishlists = Wishlish.objects.filter(user=request.user)
    wishlists_count = Wishlish.objects.filter(user=request.user).count()

    return render(request, 'core/wishlish.html', {'products' : products, 'wishlists' : wishlists, 'wishlists_count' : wishlists_count})

def save_profile(request):
    full_name = request.GET['full_name']
    bio = request.GET['bio']
    email = request.GET['email']
    phone = request.GET['phone']
    image = request.GET['image']
    profile = Profile.objects.get(user=request.user)
    profile.full_name = full_name
    profile.bio = bio
    profile.user.email = email
    profile.phone = phone
    profile.image = image
    profile.save()
    context = render_to_string('core/async/profile.html', {'profile' : profile})

    return JsonResponse({'data' : context})

def contact_us(request):
    context = {}
    return render(request, 'core/contact-us.html')