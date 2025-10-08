from django.db import models
from django.utils import timezone

# Supplier model
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Product model
class Product(models.Model):
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True)  # Stock Keeping Unit
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=5)
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"


# Purchase model
class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Purchase of {self.product.name} on {self.purchase_date}"

    def save(self, *args, **kwargs):
        """Increase stock automatically on purchase."""
        super().save(*args, **kwargs)
        self.product.quantity_in_stock += self.quantity
        self.product.save()


# Stock Adjustment model
class StockAdjustment(models.Model):
    ADJUSTMENT_TYPES = [
        ('ADD', 'Addition'),
        ('SUB', 'Subtraction'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    adjustment_type = models.CharField(max_length=3, choices=ADJUSTMENT_TYPES)
    quantity = models.PositiveIntegerField()
    reason = models.TextField(blank=True, null=True)
    adjusted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.adjustment_type} - {self.product.name}"

    def save(self, *args, **kwargs):
        """Apply adjustment to stock on save."""
        if self.adjustment_type == 'ADD':
            self.product.quantity_in_stock += self.quantity
        elif self.adjustment_type == 'SUB':
            self.product.quantity_in_stock -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)


# Employee model
class Employee(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    date_joined = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.employee_id})"
