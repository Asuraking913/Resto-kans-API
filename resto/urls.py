from django.urls import path
from .views import CreateJobView, Home, ProductView, order_item
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path("", Home, name="Home response"), 
    # path("create/user/", CreateUserView.as_view(), name="Register User"), 
    path("product/", ProductView.as_view(), name="Get/Create Products"),
    path("order/", order_item.as_view(), name="Get/Create Orders"),

    # new endpoints
    path("create-list-job/", CreateJobView.as_view(), name="Get/Create Jobs")
]