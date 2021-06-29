from django.contrib import admin
from .models import Kitchen, Food, Customer, Order, OrderItem
# Register your models here.

admin.site.register(Kitchen)
admin.site.register(Food)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)

