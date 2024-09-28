from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, CustomTokenSerializer
# from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework_simplejwt import views
from rest_framework.response import Response

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainView(views.TokenObtainPairView):
    serializer_class = CustomTokenSerializer

    def post(self, request: views.Request, *args, **kwargs) -> views.Response:

        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        response = Response({
            'is_admin' : data['is_admin'], 
            'is_staff' : data['is_staff'], 
            'access' : data['access']
        })

        response.set_cookie('access', data['access'], samesite='Lax', secure=True, httponly=True)

        return response


