from django.urls import path, include
from .views import*
from rest_framework.routers import DefaultRouter

app_name='userauths'
router = DefaultRouter()
router.register('login', login_api)
router.register('sign-up', register_api)

# router.register('logout/', )

urlpatterns = [
    path('sign-up/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('v1/', include(router.urls)),
]