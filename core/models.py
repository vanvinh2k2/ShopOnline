from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
#Create your models here.

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered")
)

STATUS = (
    ("draf", "Draf"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In review"),
    ("published", "Published")
)

RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★")
)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category")

    class Meta:
        # dat lai hien name
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' %(self.image.url))
    
    def __str__(self):
        return self.title
    

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Nestify")
    image = models.ImageField(upload_to=user_directory_path, default="vender.png")
    image_cover = models.ImageField(upload_to=user_directory_path, default="vender.png")
    description = RichTextUploadingField(null=True, blank=True)
    address = models.CharField(max_length=100, default="490 Truong Chinh Street.")
    contact = models.CharField(max_length=100, default="+(84) 344 342 295")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        # dat lai hien name
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' %(self.image.url))
    
    def __str__(self):
        return self.title
    

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Fresh Pear")
    image = models.ImageField(upload_to=user_directory_path, default="product.png")
    description = RichTextUploadingField(null=True, blank=True, default="This is product")
    price = models.DecimalField(decimal_places=2, max_digits=50, default=2)
    old_price = models.DecimalField(decimal_places=2, max_digits=50, default=2)
    specifications = RichTextUploadingField(null=True, blank=True)
    product_status = models.CharField(choices=STATUS, default="in_review", max_length=50)
    type = models.CharField(max_length=100, default="Organic", null=True, blank=True)
    stock = models.CharField(max_length=100, default="10", null=True, blank=True)
    life = models.CharField(max_length=100, default="100 days", null=True, blank=True)
    mfd = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='category')
    tags = TaggableManager(blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, related_name='vendor')

    class Meta:
        # dat lai hien name
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' %(self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_precentage(self):
        new_price = (self.price / self.old_price)*100
        return round(100 - new_price)

class ProductImage(models.Model):
    images = models.ImageField(upload_to="product-images", default="image.png")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="product_images")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # dat lai hien name
        verbose_name_plural = "Product Images"

class CartOrder(models.Model):
    oid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(decimal_places=2, max_digits=50, default=2)
    paid_status = models.BooleanField(default=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=18, default="process")
    
    class Meta:
        # dat lai hien name
        verbose_name_plural = "Cart Order"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, null = True)
    invoice_no = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.ImageField(upload_to=user_directory_path, default="product.png")
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=50, default=2)
    total = models.DecimalField(decimal_places=2, max_digits=50, default=2)

    class Meta:
        # dat lai hien name
        verbose_name_plural = "Cart Order Items"

    def order_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' %(self.image))
    

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="product")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # dat lai hien name
        verbose_name_plural = "Product Reviews"
    
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    

class Wishlish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # dat lai hien name
        verbose_name_plural = "Wishlishs"
    
    def __str__(self):
        return self.product.title
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=15, null=True)
    display_name = models.CharField(max_length=150, null=True)
    is_default = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

    class Meta:
        # dat lai hien name
        verbose_name_plural = "Address"
