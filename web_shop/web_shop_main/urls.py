from django.urls import path
from .views import batch_delete_products
from .views import batch_delete_category
from .views import ProductListCreate, CategoryListCreate

urlpatterns = [
    path('products/', ProductListCreate.as_view(), name='product-list-create'),
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('products/delete', batch_delete_products, name='batch-delete-products'),
    path('categories/delete', batch_delete_category, name='batch-delete-category'),
]
