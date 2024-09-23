from rest_framework import generics
from .models import User, Product, Order
from .serializers import UserSerializer, ProductSerializer, ObtainAccessToken, OrderSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.exceptions import AuthenticationFailed

def home(response):
    return HttpResponse('<h1>Resto Kans</h1>')


# obtain token/Login
class ObtainTokenView(TokenObtainPairView):
    serializer_class = ObtainAccessToken

    # def post(self, request, *args, **kwargs):
    #     query = self.get_queryset()
    #     serializer = self.get_serializer(data = request.data)

    #     try:
    #         serializer.is_valid(raise_exception = True)
    #     except:
    #         return Response({"msg" : "Invalid Credentials 2"}, status=400)
        
    #     access_token = serializer.validated_data.get('access')

    #     response = Response({
    #         "msg" : "Logged in successfully", 
    #     })

    #     response.set_cookie('access',  value=access_token, samesite='Lax', httponly=True, secure=True)

    #     return response
    
    def get_queryset(self):

        user = get_user_model()

        
        return user.objects.all()


            
#Register user
class CreateUserView(generics.CreateAPIView):


    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    

class ProductView(generics.ListCreateAPIView):

    parser_classes = [MultiPartParser, FormParser, JSONParser]
    


    queryset = Product.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer

    # def get_queryset(self, serializer):
    #     return Product.objects.filter(name = serializer)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

class OrderView(generics.ListCreateAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes= [AllowAny]

    def perform_create(self, serializer):
        if serializer.is_valid(): 
            user = self.request.user

            if not user or not user.is_authenticated:
                raise AuthenticationFailed("Please log in to your account")

            product_id = self.request.data.get('product')
            product = Product.objects.filter(id = product_id).first()
            serializer.save(user = user, product = product)
        return super().perform_create(serializer)





        