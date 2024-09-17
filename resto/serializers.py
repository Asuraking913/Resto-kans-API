from typing import Any, Dict
from .models import User, Product
from rest_framework import serializers
from django.http import HttpResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

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

class ObtainAccessToken(TokenObtainPairSerializer):
    # username_field = 'email'
    email = serializers.EmailField(required = True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'] = serializers.EmailField(required = True)
        self.fields.pop('username', None)

    def validate(self, attrs):
        
        credentials = {
            'email' : attrs.get('email'),
            "password" : attrs.get('password')
        }
        print(credentials)

        user = authenticate(**credentials)

        if user is None:
            raise serializers.ValidationError({"msg" :"Invalid credentials"})
        
        data = super().validate(attrs)

        return data
    