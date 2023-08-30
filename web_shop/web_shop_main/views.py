from rest_framework import generics, status

from .policies import StaffAccessPolicy
from .models import Product, Category, Basket, BasketItem
from .serializers import ProductSerializer, CategorySerializer, BasketItemSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from knox.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist


class ProductListCreate(generics.ListCreateAPIView):
    permission_classes = [StaffAccessPolicy,]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryListCreate(generics.ListCreateAPIView):
    permission_classes = [StaffAccessPolicy,]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BatchDeleteProductsView(APIView):
    permission_classes = [StaffAccessPolicy,]

    def post(self, request):
        try:
            product_ids = request.data.get('product_ids', [])
            
            if not product_ids or not set(product_ids).issubset(set(Product.objects.values_list('id', flat=True))):
                return Response({"error": "Invalid or missing product_ids."}, status=status.HTTP_400_BAD_REQUEST)

            Product.objects.filter(id__in=product_ids).delete()

            return Response({"message": "Products deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class BatchDeleteCategoryView(APIView):
    permission_classes = [StaffAccessPolicy,]

    def post(self, request):
        try:
            category_ids = request.data.get('category_ids', [])
            
            if not category_ids or not set(category_ids).issubset(set(Category.objects.values_list('id', flat=True))):
                return Response({"error": "Invalid or missing category_ids."}, status=status.HTTP_400_BAD_REQUEST)

            Category.objects.filter(id__in=category_ids).delete()

            return Response({"message": "Categorie deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class AddToBasketView(generics.CreateAPIView):
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
          basket, _ = Basket.objects.get_or_create(user=self.request.user, confirmed=False)
          serializer.save(basket=basket)
        else:
          return Response({"error": "User needs to be authenticated to add to basket."}, status=status.HTTP_401_UNAUTHORIZED)


class ConfirmBasketView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            basket = Basket.objects.get(user=request.user, confirmed=False)
            for item in basket.items.all():
                product = item.product
                product.amount = str(int(product.amount) - item.quantity)
                product.save()
            basket.confirmed = True
            basket.save()
            return Response({"message": "Basket confirmed and products updated."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPI(LoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return super(LoginAPI, self).post(request, format=None)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPI(LogoutView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response({"message": "Logged out!"}, status=200)