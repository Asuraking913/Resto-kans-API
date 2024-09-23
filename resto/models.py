from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


def generate_id():
    return uuid4().hex

# Create your models here.
class User(AbstractUser):
    id = models.CharField(max_length=255, default=generate_id, primary_key=True, unique=True)
    email = models.EmailField(unique=True)
    default_address = models.TextField(max_length=400, null=False)



    def __str__(self):
        return f"user: {self.username}"
    

class Product(models.Model):
    id = models.CharField(max_length=255, default=generate_id, primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available_stock = models.IntegerField()
    category = models.CharField(max_length=40)
    image = models.ImageField(null=True, blank=True)

class PaymentMethod(models.Model):
    id = models.CharField(max_length=255, default=generate_id, primary_key=True, unique=True)

    card_number = models.CharField(max_length=255)
    card_type = models.CharField(max_length=255)
    is_default = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Order(models.Model):
    id = models.CharField(max_length=255, default=generate_id, primary_key=True, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # payment_method = models.ForeignKey(PaymentMethod, on_delete= models.CASCADE)


class Receipt(models.Model):
    id = models.CharField(max_length=255, default=generate_id, primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)