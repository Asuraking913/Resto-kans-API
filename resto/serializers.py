from .models import User, Product
from rest_framework import serializers
from django.http import HttpResponse

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", 'email', "password"]
        extra_kwargs = {"password" : {"write_only" : True}}

    def create(self, validated_data):
        
        user_exist = User.objects.filter(email = validated_data['email'])
        if user_exist:
            raise serializers.ValidationError({"email" : "This email address already exists"})

        user = User(
            email = validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

    # def create_user(self, validated_data):
    #     user = User.objects.create(**validated_data)
    #     return user
    
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'available_stock', 'category']
    