from django.urls import path
from .views import batch_delete_products
from .views import batch_delete_category
from .views import ProductListCreate, CategoryListCreate, AddToBasketView, confirm_basket
from djoser import views as djoser_views

urlpatterns = [
    path('products/', ProductListCreate.as_view(), name='product-list-create'),
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('products/delete', batch_delete_products, name='batch-delete-products'),
    path('categories/delete', batch_delete_category, name='batch-delete-category'),
    path('add_to_basket/', AddToBasketView.as_view(), name='add-to-basket'),
    path('confirm_basket/', confirm_basket, name='confirm-basket'),
    path('auth/register/', djoser_views.UserCreateView.as_view(), name='user-register'),
    path('auth/login/', djoser_views.TokenCreateView.as_view(), name='user-login'),
    path('auth/logout/', djoser_views.TokenDestroyView.as_view(), name='user-logout'),
    
]
