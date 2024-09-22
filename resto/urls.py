from django.urls import path
from . import views
from django.urls import include
from .views import CreateUserView, ProductView, ObtainTokenView
from django.conf.urls.static import static
from django.conf import settings
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("", views.home, name="home"), 
    path("api/create/user/", CreateUserView.as_view(), name="Register View"), 
    path("api/token/", ObtainTokenView.as_view(), name = 'Generate token'), 
    path("api-auth/", include("rest_framework.urls")),


    path("api/product/", ProductView.as_view(), name="Product View"), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)