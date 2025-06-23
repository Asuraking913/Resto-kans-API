from random import choices
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
    role_choices = (
            ('hire', 'hire'),
            ('freelance', 'freelance'),
        )

    id = models.CharField(max_length=255, primary_key= True, default = generate_id, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    address_default = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length = 255, blank=True)
    last_name = models.CharField(max_length = 255, blank=True)
    phone_number = models.CharField(max_length = 255, blank=True)
    location = models.TextField(blank=True)
    role  = models.CharField(choices = role_choices, max_length = 255, null=False)

    REQUIRED_FIELDS = []
    objects = UserManager()

class Profile(models.Model):
    job_title = models.CharField(max_length = 255)
    experience = models.IntegerField(default = 1)
    hourly_rate = models.FloatField()
    languages = models.CharField(max_length = 255)
    Bio = models.TextField()
    skills = models.TextField()
    education = models.TextField()
    website_link = models.CharField(max_length = 255)
    linkdeln_link = models.CharField(max_length = 255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Product(models.Model):
    id = models.CharField(max_length=255, primary_key= True, default = generate_id, null = False)
    name  = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    available_stock = models.PositiveIntegerField(null=False)
    category = models.CharField(max_length=50, null = False)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class Order(models.Model):
    id = models.CharField(max_length=255, default=generate_id, primary_key=True, unique=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    id = models.CharField(max_length=255, unique=True, primary_key=True, default=generate_id, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
