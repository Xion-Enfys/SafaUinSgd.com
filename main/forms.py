from django.forms import ModelForm
from .models import TokoEntry, ProductEntry, Review
from django import forms

class TokoEntryForm(ModelForm):
    class Meta:
        model = TokoEntry
        fields = ['name', "category"]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if TokoEntry.objects.filter(name=name).exists():
            raise forms.ValidationError("Nama toko sudah digunakan, silahkan gunakan nama lain")
        return name

class ProductEntryForm(ModelForm):
    class Meta:
        model = ProductEntry

        fields = ["name", "price", "description", "image", "toko"]

    def clean(self):
        cleaned_data = super().clean()
        toko = TokoEntry.objects.all()

        # Cek apakah ada toko yang sudah terdaftar
        if not TokoEntry.objects.exists():
            raise forms.ValidationError("Tidak ada toko yang tersedia. Anda harus menambahkan toko sebelum menambahkan produk.")
        
        return cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

from .models import CartItem

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']