from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework import generics
from .serializers import ProductSerializer, OrderItemsSerializer
from .models import Product, OrderItem, Order, User
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
import json
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


# Create your views here.
def Home(request):
    return HttpResponse("<h1>This is the home age</h1>")

class ProductView(generics.ListCreateAPIView):
    # permission_classes = [AllowAny, IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        product = Product.objects.all()
        return product
    
    def perform_create(self, serializer):

        return super().perform_create(serializer)
    
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
        try:
            data = json.loads(data)['order']

            if not isinstance(data, list):
                return Response({"error" : "value 'order' must be of array/list"}, status=status.HTTP_400_BAD_REQUEST)
            
            for order in data:
                product_id = order.get("product")
                quantity = order.get("quantity")
                if not product_id or not quantity:
                    return Response({"error" : "List objects has no product and quantity key"}, status=status.HTTP_400_BAD_REQUEST)
            
        except json.JSONDecodeError:
            return Response({"error" : "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"error" : "payload does not contain a key 'order'"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = request.user
            if not user.is_authenticated:
                raise ValueError("User is not authenticated")
            new_order = Order.objects.create(user = user)
        except ValueError:
            new_order = Order.objects.create()
 
        for order in data:
            product_id = order['product']
            quantity = order['quantity']
            product = Product.objects.filter(id = product_id).first()
            new_order_items = OrderItem.objects.create(product = product, order = new_order, quantity = quantity)
        response = {
                    "msg" : "Created Order successsfully", 
                    "data" :
                        {
                            "order_id" : new_order.id, 
                        }
        }

        return Response(response, status=status.HTTP_201_CREATED)
    
    elif request.method == 'GET':

        try:
            user = request.user
            token = request.COOKIES.get('access')

            if not token:
                return Response({"error" : "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            access =  AccessToken(token)
            user = User.objects.filter(id = access['user_id']).first()
            try:
                if not user.is_superuser:
                    # return Response({"error" : "Unathorized request"}, status=status.HTTP_401_UNAUTHORIZED)
                    raise ValueError("Unauthorized")
                order_list = Order.objects.all()
            except ValueError:
                order_list = user.order_set.all()

            response_list = []


            #pagination
            paginator = Paginator(order_list, 10)
            page = request.GET.get('page', 1)
            # print(page, 'event')

            try:
                orders = paginator.page(page)
            except PageNotAnInteger:
                orders = paginator.page(1)
            except EmptyPage:
                orders = []
                # orders = paginator.page(paginator.num_pages)

            for order in orders:

                response_list.append({
                    "total" : len(order.orderitem_set.all()),
                    "orderId" : order.id,
                    "date" : order.created_at, 
                    "products" : [ 
                                {
                                    "name" : order_item.product.name, 
                                    "quantity" : order_item.quantity, 
                                    "price" : order_item.product.price, 
                                    "img" : request.build_absolute_uri(order_item.product.image.url), 
                                } 
                                for order_item in order.orderitem_set.all()
                            ]
                })  
            print(len(response_list) , 'event', request.GET.get('page'))
            return Response({"data" : response_list}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"error" : "wer"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({"sdf" : "sdf"})
