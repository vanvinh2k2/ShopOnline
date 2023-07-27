from django.contrib import admin
from .models import*

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_active', 'is_staff', 'date_joined']

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'full_name', 'bio', 'phone']

admin.site.register(User, UserAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Profile, ProfileAdmin)