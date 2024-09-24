from rest_framework import serializers
from .models import User, Product, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {"password" : {"write_only" : True}}
    
    def create(self, validated_data):   
        user = User.objects.create_user(**validated_data)
        return user

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', "price", 'available_stock', "category", 'image']

class OrderItemsListSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        order_item = [OrderItem(**items) for items in validated_data] 
        # print(order_item)
        return order_item
    
    def update(self, instance, validated_data):
        print(instance, "instance")
        print(validated_data, 'validated_data')
        return None

    
class OrderItemsSerializer(serializers.Serializer):

    # order = Order()
    # quantity = serializers.IntegerField()
    product = serializers.CharField()
    quantity = serializers.IntegerField()

    class Meta:
        list_serializer_class = OrderItemsListSerializer
    
