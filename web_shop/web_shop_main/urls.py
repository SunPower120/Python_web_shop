from django.urls import path
from .views import ProductListCreate, CategoryListCreate

urlpatterns = [
    path('products/', ProductListCreate.as_view(), name='product-list-create'),
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
]
