from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from knox.models import AuthToken
from .models import Product, Category, Basket
from django.urls import reverse

class ViewTestCase(TestCase):
    
    def setUp(self):
        # Set up the APIClient
        self.client = APIClient()

        # Create a test user
        self.test_user = User.objects.create_user(username="testuser", password="testpassword", email="test@example.com", is_staff=False)
        
        # Create a test admin
        self.test_admin_user = User.objects.create_user(username="testadminuser", password="testadminpassword", email="testadmin@example.com", is_staff=True)
        
        # Create a token for the user
        self.token = AuthToken.objects.create(user=self.test_user)[1]  # Returns instance and token
        
        # Create a token for the test_admin
        self.admin_token = AuthToken.objects.create(user=self.test_admin_user)[1]  # Returns instance and token
        
        # Attach token to client headers for authentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Sample data for category
        self.category_data = {'name': 'Test Category'}
        self.category = Category.objects.create(**self.category_data)
        
        # Retrieving category
        retrieved_category = Category.objects.get(name='Test Category')
    
        # Sample data for product
        self.product_data = {
            'name': 'Test Product', 
            'description': 'Test Description', 
            'price': '100', 
            'category': retrieved_category,
            'amount': '10'
        }
        self.product = Product.objects.create(**self.product_data)

    def test_product_list_create(self):
        print(self.product_data)
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(reverse('product-list-create'), self.product_data)
    
        print("Response data:", response.data)
        print(self.category)
    
        self.assertEqual(response.status_code, 403)  
        
        self.client.force_authenticate(user=self.test_admin_user)
        response = self.client.post(reverse('product-list-create'), self.product_data)
    
        print("Response data:", response.data)
    
        self.assertEqual(response.status_code, 201)
        

    def tearDown(self):
        self.product.delete()
        self.category.delete()
        self.test_user.delete()
        self.test_admin_user.delete()