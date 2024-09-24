from django.urls import path
from .views import Home, CreateUserView, ProductView
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path("", Home, name="Home response"), 
    path("create/user/", CreateUserView.as_view(), name="Register User"), 
    path("login/", TokenObtainPairView.as_view(), name = "Login user"), 
    path("product/", ProductView.as_view(), name="Get/Create Products")
]