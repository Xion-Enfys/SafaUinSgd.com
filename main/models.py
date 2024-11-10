from datetime import timezone
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import uuid
from django.contrib.auth.models import User


# Create your models here.
class TokoEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    category = models.TextField()

    def __str__(self):
        return self.name

class ProductEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField(validators=[MinValueValidator(1)])
    description = models.TextField()
    image = models.URLField(max_length=500, blank=True, null=True)
    toko = models.ForeignKey(TokoEntry, on_delete=models.CASCADE, related_name='products')

class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(ProductEntry, on_delete=models.CASCADE)
    
class Review(models.Model):
    product = models.ForeignKey(ProductEntry, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.product.name} ({self.rating}/5)'


class CartItem(models.Model):
    product = models.ForeignKey(ProductEntry, on_delete=models.CASCADE, related_name = "cart")
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, related_name='carts', blank=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def total_price(self):
        return sum(item.total_price for item in self.items.all())
