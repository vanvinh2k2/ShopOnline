from django.contrib.auth import authenticate, login, logout
from .models import User, Profile
from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms.models import model_to_dict
from rest_framework import status, permissions, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.backends import ModelBackend
from allauth.socialaccount.models import SocialAccount
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
base_url = "http://127.0.0.1:8000"

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh' : str(refresh),
        'access' : str(refresh.access_token),
    }

class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all();
    serializer_class = RegisterUserSeriallize
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serialize = self.get_serializer(data=request.data)
        if serialize.is_valid():
            user = serialize.save()
            user.set_password(request.data['password'])
            user.save()
            profile = Profile.objects.create(user=user)
            token = get_tokens_for_user(user)
            return Response({'success' : True, 
                             'message' : 'Login is successful.', 
                             "data" : {
                                    'id' : user.id,
                                    'username' : user.username,
                                    'email' : user.email,
                                    'is_active' : user.is_active,
                                    'date_joined' : user.date_joined,
                                    'avatar' : base_url + profile.image.url,
                                    'token' : token
                                },
                            }, status=status.HTTP_200_OK)
        return Response({'success' : False,
                            'message' : 'Register is fail!'}, 
                            status=status.HTTP_400_BAD_REQUEST)

class LoginAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginUserSeriallize
    permission_classes = [permissions.AllowAny]
    # raise_exception=True
    def create(self, request):
        serialize = self.get_serializer(data=request.data)
        if serialize.is_valid(raise_exception=True):
            user = authenticate(request, 
                                email=serialize.data['email'], 
                                password=request.data['password'])
            if user is None:
                return Response({'success' : False,
                            'message' : 'User is not exists!'}, 
                            status=status.HTTP_404_NOT_FOUND)
            else: 
                token = get_tokens_for_user(user)
                profile = Profile.objects.get(user=user)
                return Response({'success' : True, 
                             'message' : 'Login is successful.', 
                             "data" : {
                                    'id' : user.id,
                                    'username' : user.username,
                                    'email' : user.email,
                                    'is_active' : user.is_active,
                                    'date_joined' : user.date_joined,
                                    'avatar' : base_url+profile.image.url,
                                    'token' : token
                                },
                            }, status=status.HTTP_200_OK)
        return Response({'success' : False,
                            'message' : 'Login is fail!'}, 
                            status=status.HTTP_400_BAD_REQUEST)
    
class GoogleLogin(APIView):
    def post(self, request):
        id_google = request.data.get('id_google')
        email = request.data.get('email')
        name = request.data.get('name')
        profile = None
        if request.data.get('avatar') : avatar = request.data.get('avatar')
        else : avatar = ""
        try:
            social_account = SocialAccount.objects.get(uid=id_google, provider='google')
            user = social_account.user
            profile = Profile.objects.get(user=user)
            
        except SocialAccount.DoesNotExist:
            user = User.objects.create_user(username=name, email=email)
            user.save()
            social_account = SocialAccount.objects.create(user=user, uid=id_google, provider='google')
            if avatar == "": Profile.objects.create(user=user, full_name=name)
            else: profile = Profile.objects.create(user=user, full_name=name, image=avatar)

        user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'
        token=get_tokens_for_user(user)
        return Response({'success' : True, 
                             'message' : 'Login is successful.', 
                             "data" : {
                                    'id' : user.id,
                                    'username' : user.username,
                                    'email' : user.email,
                                    'is_active' : user.is_active,
                                    'date_joined' : user.date_joined,
                                    'avatar' : base_url+profile.image.url,
                                    'token' : token
                                },
                            }, status=status.HTTP_200_OK
                        )
    
class FacebookLogin(APIView):
    def post(self, request):
        id_facebook = request.data.get('id_facebook')
        email = request.data.get('email')
        name = request.data.get('name')
        profile = None
        if request.data.get('avatar') : avatar = request.data.get('avatar')
        else : avatar = ""
        try:
            social_account = SocialAccount.objects.get(uid=id_facebook, provider='facebook')
            user = social_account.user
            profile = Profile.objects.get(user=user)
            
        except SocialAccount.DoesNotExist:
            user = User.objects.create_user(username=name, email=email)
            user.save()
            social_account = SocialAccount.objects.create(user=user, uid=id_facebook, provider='facebook')
            if avatar == "": Profile.objects.create(user=user, full_name=name)
            else: profile = Profile.objects.create(user=user, full_name=name, image=avatar)

        user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'
        token=get_tokens_for_user(user)
        return Response({'success' : True, 
                             'message' : 'Login is successful.', 
                             "data" : {
                                    'id' : user.id,
                                    'username' : user.username,
                                    'email' : user.email,
                                    'is_active' : user.is_active,
                                    'date_joined' : user.date_joined,
                                    'avatar' : base_url+profile.image.url,
                                    'token' : token
                                },
                            }, status=status.HTTP_200_OK
                        )
    
class Logout(APIView):
    def post(self, request):
        refresh_token = request.data['refresh']
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)  # Tạo đối tượng RefreshToken từ chuỗi refresh_token
                token.check_blacklist()  # Kiểm tra xem token đã tồn tại trong đen danh chưa
            except (TokenError, InvalidToken) as e:
                return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            token.blacklist()
            return Response({'success': True, 
                             'message': 'Logout successful.'}, 
                             status=status.HTTP_200_OK)
        else: return Response({'success': False, 
                             'message': 'Refresh token is required.'}, 
                             status=status.HTTP_400_BAD_REQUEST)