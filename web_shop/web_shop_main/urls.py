from django.urls import path
from .views import LoginAPI, LogoutAPI, BatchDeleteProductsView, BatchDeleteCategoryView, ProductListCreate, CategoryListCreate, AddToBasketView, ConfirmBasketView
from djoser import views as djoser_views

urlpatterns = [
    path('auth/register/', djoser_views.UserViewSet.as_view({'post': 'create'}), name='user-register'),
    path('auth/login/', LoginAPI.as_view(), name='knox_login'),
    path('auth/logout/', LogoutAPI.as_view(), name='knox_logout'),
    path('products/', ProductListCreate.as_view(), name='product-list-create'),
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('products/delete', BatchDeleteProductsView.as_view(), name='batch-delete-products'),
    path('categories/delete', BatchDeleteCategoryView.as_view(), name='batch-delete-category'),
    path('add_to_basket/', AddToBasketView.as_view(), name='add-to-basket'),
    path('confirm_basket/', ConfirmBasketView.as_view(), name='confirm-basket'),

]
