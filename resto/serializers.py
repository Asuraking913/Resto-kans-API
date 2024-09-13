from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", 'username', "password"]
        extra_kwargs = {"password" : {"write_only" : True}}

    def validate_email(self, value):
        if User.objects.filter(useremail = value).exists():
            raise serializers.ValidationError("This email Already exists")


    def create_user(self, validated_data):
        user = User.objects.create(**validated_data)
        return user