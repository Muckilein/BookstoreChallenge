from django.test import TestCase
import json
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Book, CustomUser
from .serializers import BookSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.
class BookCRUDViewTest(APITestCase):
    def setUp(self):
        # Set up initial data for the test
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(
            title='Test Book',
            description='Test Description',
            author=self.user,
            cover_image='http://example.com/cover.jpg',
            price=10.0
        )
        self.url = reverse('bookCrud')
        self.client.force_authenticate(user=self.user)
        self.jwt_token = str(RefreshToken.for_user(self.user).access_token)

    def test_create_book(self):
        data = {
            'title': 'New Book',
            'description': 'New Description',
            'author_id': self.user.id,
            'cover_image': 'http://example.com/cover.jpg',
            'price': 15.0
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {self.jwt_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])

    def test_get_books(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.jwt_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_update_book(self):
        data = {
            'id': self.book.id,
            'title': 'Updated Book',
            'description': 'Updated Description',
            'author_id': self.user.id,
            'cover_image': 'http://example.com/updated_cover.jpg',
            'price': 20.0
        }
        response = self.client.put(self.url, json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {self.jwt_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, data['title'])

    def test_create_book_invalid_data(self):
        data = {
            'title': '',  # Title is required, so this should fail
            'description': 'Description',
            'author_id': self.user.id,
            'cover_image': 'http://example.com/cover.jpg',
            'price': 15.0
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {self.jwt_token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)