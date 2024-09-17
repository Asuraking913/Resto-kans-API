from rest_framework import generics
from .models import User, Product
from .serializers import UserSerializer, ProductSerializer, ObtainAccessToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView

def home(response):
    return HttpResponse('<h1>Resto Kans</h1>')

class ObtainTokenView(TokenObtainPairView):
    serializer_class = ObtainAccessToken

class CreateUserView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    # def get_queryset(self, serializer):
    #     return Product.objects.filter(name = serializer)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)


def handleLogin(request):
    if request.method == 'POST': 
        print(request.json)




        