from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)

    #người dùng sẽ đăng nhập bằng địa chỉ email của họ thay vì tên người dùng.
    USERNAME_FIELD = "email"
    #khi đăng ký người dùng mới, cả trường email và tên người dùng đều được yêu cầu.
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    image = models.ImageField(upload_to="image", default="image/default.png")
    full_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    user = models.OneToOneField(User, models.CASCADE)

    def __str__(self):
        return self.user.username

class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    class Meta:
        verbose_name="Contact Us"
        verbose_name_plural="Contact Us"

    def __str__(self):
        return self.full_name