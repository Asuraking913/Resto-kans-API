from django.urls import path
from . import views
from django.urls import include
from .views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("", views.home, name="home"), 
    path("api/create/user/", CreateUserView.as_view(), name="Register View"), 
    path("api/token/", TokenObtainPairView.as_view(), name = 'Generate token'), 
    path("api-auth/", include("rest_framework.urls"))
]