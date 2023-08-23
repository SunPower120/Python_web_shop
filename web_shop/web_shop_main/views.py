from rest_framework import generics
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

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