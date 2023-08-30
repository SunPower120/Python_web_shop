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
            'category': retrieved_category.pk,
            'amount': '10'
        }
       

    def test_product_list_create(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(reverse('product-list-create'), self.product_data)
    
        print("Response data:", response.data)
        self.assertEqual(response.status_code, 403)  
        
        self.client.force_authenticate(user=self.test_admin_user)
        response = self.client.post(reverse('product-list-create'), self.product_data)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, 201)
        
    def test_category_list_create(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(reverse('category-list-create'), self.category_data)
        self.assertEqual(response.status_code, 403) 

        self.client.force_authenticate(user=self.test_admin_user)
        response = self.client.post(reverse('category-list-create'), self.category_data)
        self.assertEqual(response.status_code, 201)  

    def test_batch_delete_products(self):
        # First, use the admin user to create a product through a POST request.
        self.client.force_authenticate(user=self.test_admin_user)
        response = self.client.post(reverse('product-list-create'), self.product_data)
        self.assertEqual(response.status_code, 201)
    
        # Extract the created product's id from the response
        product_id = response.data.get('id')
    
        # Test the batch delete with a non-admin user
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(reverse('batch-delete-products'), {'product_ids': [product_id]}, format='json')
        self.assertEqual(response.status_code, 403)  # Expecting forbidden for non-admin users
        all_product_ids = Product.objects.values_list('id', flat=True)

        # Test the batch delete with an admin user
        self.client.force_authenticate(user=self.test_admin_user)
        response = self.client.post(reverse('batch-delete-products'), {'product_ids': [product_id]}, format='json')
        self.assertEqual(response.status_code, 200)  # Expecting successful deletion for admin users


    def tearDown(self):
        self.category.delete()
        self.test_user.delete()
        self.test_admin_user.delete()