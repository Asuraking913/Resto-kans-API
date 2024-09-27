from django.urls import path
from .views import CreateUserView, CustomTokenObtainView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("create/user/", CreateUserView.as_view(), name="Register User"), 
    # path("login/user/", TokenObtainPairView.as_view(), name = "Login user"), 
    path("login/user/", CustomTokenObtainView.as_view(), name = "Login user"), 
]