from django.db import models
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission
from drf_access_policy import AccessPolicy

class Category(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.CharField(max_length=7, null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_shop_owner = models.BooleanField(default=False)
    
class IsShopOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.userprofile.is_shop_owner

class ShopOwnerAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve", "create", "update", "partial_update", "delete"],
            "principal": "user",
            "effect": "allow",
            "condition": "is_shop_owner"
        }
    ]

    def is_shop_owner(self, request, view, action) -> bool:
        return request.user.userprofile.is_shop_owner

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

class BasketItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, related_name="items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
