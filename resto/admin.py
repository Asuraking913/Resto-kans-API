from django.contrib import admin
from .models import User, Product, PaymentMethod, Order

admin.site.register([User, PaymentMethod, Order, Product])

# Register your models here.
