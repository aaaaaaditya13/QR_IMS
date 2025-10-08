from django import forms
from .models import Product, Supplier, Purchase, StockAdjustment, Employee

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'supplier', 'category', 'price', 'quantity_in_stock', 'reorder_level']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input w-full'}),
            'price': forms.NumberInput(attrs={'class': 'form-input w-full'}),
        }


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'


class StockAdjustmentForm(forms.ModelForm):
    class Meta:
        model = StockAdjustment
        fields = '__all__'


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
