from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from uuid import uuid4
from django.contrib import admin

def generate_id():
    return uuid4().hex

class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("The email field is not provided")
        if not password:
            raise ValueError("The password field should be provided@")
        email = self.normalize_email(email)
        user = self.model(email = email, **kwargs)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('is_staff attribute must be set to true')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('is_superuser must be set to True')
        
        return self.create_user(email, password, **kwargs)

# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD = 'email'
    username = None
    id = models.CharField(max_length=255, primary_key= True, default = generate_id, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    address_default = models.CharField(max_length=255)

    REQUIRED_FIELDS = []
    objects = UserManager()

class Product(models.Model):
    id = models.CharField(max_length=255, primary_key= True, default = generate_id, null = False)
    name  = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    available_stock = models.PositiveIntegerField(null=False)
    category = models.CharField(max_length=50, null = False)
    image = models.ImageField()

    




