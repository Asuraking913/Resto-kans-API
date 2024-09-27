from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, CustomTokenSerializer
# from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework_simplejwt import views

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainView(views.TokenObtainPairView):
    serializer_class = CustomTokenSerializer


