from rest_framework.serializers import ModelSerializer
from .models import User, Product

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['email']
