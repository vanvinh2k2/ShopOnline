from django.urls import path, include
from .views import *
from .backend import *

app_name='userauths'

urlpatterns = [
    path('sign-up/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),

    # API
    path('api/sign-up/', RegisterAPI.as_view(), name="api-register"),
    path('api/login/', LoginAPI.as_view(), name="api-login"),
    path('api/login/google', GoogleLogin.as_view(), name="api-google"),
    path('api/login/facebook', FacebookLogin.as_view(), name="api-facebook"),
    path('api/logout/', Logout.as_view(), name="api-logout"),
]