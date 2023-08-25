from rest_framework import generics
from .models import Product, Category, Basket, BasketItem, ShopOwnerAccessPolicy
from .serializers import ProductSerializer, CategorySerializer, BasketItemSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@api_view(['POST'])
def batch_delete_products(request):
    try:
        # Get the ids of the products from the JSON body
        product_ids = request.data.get('product_ids', [])
        
        # Check if all category_ids exist
        if not set(product_ids).issubset(set(Product.objects.values_list('id', flat=True))):
            return Response({"error": "Category ID are invalid."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the products that match the provided ids
        Product.objects.filter(id__in=product_ids).delete()

        return Response({"message": "Products deleted successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def batch_delete_category(request):
    try:
        # Get the ids of the products from the JSON body
        category_ids = request.data.get('category_ids', [])
        
        # Check if all category_ids exist
        if not set(category_ids).issubset(set(Category.objects.values_list('id', flat=True))):
            return Response({"error": "Category ID are invalid."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the products that match the provided ids
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
        # Return a 401 Unauthorized response or another appropriate response
          return Response({"error": "User needs to be authenticated to add to basket."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def confirm_basket(request):
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

class SomeShopOwnerView(generics.ListCreateAPIView):
    permission_classes = [ShopOwnerAccessPolicy]