from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from .serializers import UserSerializer

# Create your views here.
def Home(request):
    return HttpResponse("<h1>This is the home age</h1>")

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]