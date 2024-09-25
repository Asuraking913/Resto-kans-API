from django.urls import path
from .views import Home, ProductView, order_item
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path("", Home, name="Home response"), 
    # path("create/user/", CreateUserView.as_view(), name="Register User"), 
    path("product/", ProductView.as_view(), name="Get/Create Products"),
    path("order/", order_item, name="Get/Create Orders")
]