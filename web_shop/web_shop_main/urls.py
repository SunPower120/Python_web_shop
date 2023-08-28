from django.urls import path
from .views import LoginAPI, LogoutAPI, batch_delete_products, batch_delete_category, ProductListCreate, CategoryListCreate, AddToBasketView, confirm_basket
from djoser import views as djoser_views

urlpatterns = [
    path('products/', ProductListCreate.as_view(), name='product-list-create'),
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('products/delete', batch_delete_products, name='batch-delete-products'),
    path('categories/delete', batch_delete_category, name='batch-delete-category'),
    path('add_to_basket/', AddToBasketView.as_view(), name='add-to-basket'),
    path('confirm_basket/', confirm_basket, name='confirm-basket'),
    path('auth/register/', djoser_views.UserViewSet.as_view({'post': 'create'}), name='user-register'),
    path('auth/login/', LoginAPI.as_view(), name='knox_login'),
    path('auth/logout/', LogoutAPI.as_view(), name='knox_logout'),
    
    
]
