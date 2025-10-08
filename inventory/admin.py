from django.contrib import admin
from .models import Product, Supplier, Purchase, StockAdjustment, Employee

admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(StockAdjustment)
admin.site.register(Employee)
