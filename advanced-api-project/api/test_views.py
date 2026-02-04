from rest_framework.test import from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Author, Book

# Unit tests for book API endpoints
class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        # Create author
        self.author = Author.objects.create(name="Test Author")

        # Create books
        self.book1 = Book.objects.create(
            title="Test Book 1",
            publication_year=2025,
            author=self.author
        )

        # API endpoints
        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", args=[self.book1.id])


    def test_create_book_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        data = {
            "title": "New Book",
            "publication_year": 2023,
            "author": self.author.id
        }
        response = self.client.post(reverse("book-create"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["book"]["title"], "Test Book")

    
    def test_create_book_unauthenticated(self):
        data = {
            "title": "Unauthenticated Book",
            "publication_year": 2023,
            "author": self.author.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        
    def test_update_book_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        data = {
            "title": "Updated Book Title"
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["book"]["title"], "Updated Book Title")


        def test_delete_book_unauthenticated(self):
            response = self.client.delete(self.detail_url)

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(Book.objects.count(), 1)