from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Category, BasketItem
from knox.models import AuthToken

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'amount']

class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['id', 'product', 'quantity']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'is_staff']

    def create(self, validated_data):
        password = validated_data.pop('password')
        
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = User
        fields = ['user', 'is_staff']
        
class KnoxTokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='token_key')
    
    class Meta:
        model = AuthToken
        fields = ('auth_token',)