from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

def generate_id():
    return uuid4().hex


# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD = 'email'

    id = models.CharField(max_length=255, primary_key= True, default = generate_id, null=False)
    email = models.EmailField(max_length=255, unique=True, blank=True)
    address_default = models.CharField(max_length=255)

class Product(models.Model):
    id = models.CharField(max_length=255, primary_key= True, default = generate_id, null = False)
    name  = models.CharField(max_length=50)
    price = models.DecimalField()
    available_stock = models.PositiveIntegerField(null=False)
    category = models.CharField(max_length=50, null = False)
    image = models.ImageField()

    


