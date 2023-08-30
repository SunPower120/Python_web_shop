from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from knox.models import AuthToken
from .models import Product, Category, Basket
from django.urls import reverse

class ViewTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()

        self.test_user = User.objects.create_user(username="testuser", password="testpassword", email="test@example.com", is_staff=False)
        
        self.test_admin_user = User.objects.create_user(username="testadminuser", password="testadminpassword", email="testadmin@example.com", is_staff=True)
        
        self.token = AuthToken.objects.create(user=self.test_user)[1]  # Returns instance and token
        
        self.admin_token = AuthToken.objects.create(user=self.test_admin_user)[1]  # Returns instance and token
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.category_data = {'name': 'Test Category'}
        self.category = Category.objects.create(**self.category_data)
        
        retrieved_category = Category.objects.get(name='Test Category')
    
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
        self.client.force_authenticate(user=self.test_admin_user)
        response = self.client.post(reverse('product-list-create'), self.product_data)
        self.assertEqual(response.status_code, 201)
    
        product_id = response.data.get('id')
    
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(reverse('batch-delete-products'), {'product_ids': [product_id]}, format='json')
        self.assertEqual(response.status_code, 403) 

        self.client.force_authenticate(user=self.test_admin_user)
        response = self.client.post(reverse('batch-delete-products'), {'product_ids': [product_id]}, format='json')
        self.assertEqual(response.status_code, 200) 

    def test_batch_delete_categories(self):
        
        self.client.force_authenticate(user=self.test_admin_user)
        response = self.client.post(reverse('category-list-create'), self.category_data)
        self.assertEqual(response.status_code, 201)
    
        category_id = response.data.get('id')
    
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(reverse('batch-delete-category'), {'category_ids': [category_id]}, format='json')
        self.assertEqual(response.status_code, 403) 
        
        self.client.force_authenticate(user=self.test_admin_user)
        response = self.client.post(reverse('batch-delete-category'), {'category_ids': [category_id]}, format='json')
        self.assertEqual(response.status_code, 200) 

    def tearDown(self):
        self.category.delete()
        self.test_user.delete()
        self.test_admin_user.delete()