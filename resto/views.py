from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from .serializers import UserSerializer, ProductSerializer, OrderItemsSerializer
from .models import Product, OrderItem, Order
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
import json

# Create your views here.
def Home(request):
    return HttpResponse("<h1>This is the home age</h1>")

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ProductView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        product = Product.objects.all()
        return product
    
# class OrderItemsViews(generics.ListCreateAPIView):
#     serializer_class = OrderItemsSerializer
#     permission_classes = [AllowAny]

#     def create(self, request, *args, **kwargs):
#         # try:
#             serializer = self.get_serializer(data = request.data['order'], many = True)
#             # print(serializer)
#             if serializer.is_valid():
#                 self.perform_create(serializer)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return HttpResponse('failed')
#         # except:
#         #     return Response({"msg" : "Expected a List/Array Item"}, status=status.HTTP_400_BAD_REQUEST)

#     def perform_create(self, serializer):
#         # print(serializer.data, "event")
#         for orders in serializer.data:
#             new_order = Order.objects.create()
#             product_id = orders['product']
#             quantity = orders['quantity']
#             product = Product.objects.filter(id = product_id).first()
#             order_item = OrderItem.objects.create(product = product, order = new_order, quantity = quantity)

#             serializer.save(product = product, quantity = quantity, order = new_order)

    # def perform_create(self, serializer):

    #     order_items_data = self.request.get('order', [])
    #     serializer = OrderItemsSerializer(data=order_items_data, many = True)

    #     if serializer.is_valid():
    #         new_order = Order.objects.create()
    #         product = serializer.validated_data.get('product')
    #         quantity = serializer.validated_data.get('quantity')
    #         # product = Product.objects.filter(name = "").first()
    #         # print(product, product_id.price)

    #     return serializer.save(product = product, order = new_order, quantity = quantity)

@csrf_exempt
@api_view(['POST', 'GET'])
@require_http_methods(['GET', 'POST'])
def order_item(request):
    if request.method == "POST":
        data = request.body
        data = json.loads(data)['order']

        new_order = Order.objects.create()
        
        for order in data:
            product_id = order['product']
            quantity = order['quantity']
            product = Product.objects.filter(id = product_id).first()
            print(product)
            new_order_items = OrderItem.objects.create(product = product, order = new_order, quantity = quantity)
        response = {
                    "msg" : "Created Order successsfully", 
                    "data" :
                        {
                            "order_id" : new_order.id, 
                        }
        }

        return Response(response, status=status.HTTP_201_CREATED)
    
    if request == 'GET':
        print('event')

        return Response({"sdf" : "sdf1"})
    return Response({"sdf" : "sdf"})
        