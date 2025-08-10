from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import Author, Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user and get token if using token auth (optional)
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')  # login to get authenticated session

        # Create an author
        self.author = Author.objects.create(name="Test Author")

        # Create some books
        self.book1 = Book.objects.create(
            title="Test Book 1",
            publication_year=2000,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title="Another Book",
            publication_year=2010,
            author=self.author
        )

    def test_list_books_unauthenticated(self):
        """
        Test that anyone (unauthenticated) can list books.
        """
        self.client.logout()
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 books exist

    def test_create_book_authenticated(self):
        """
        Test that authenticated users can create books.
        """
        url = reverse('book-create')
        data = {
            "title": "New Book",
            "publication_year": 2022,
            "author": self.author.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['title'], data['title'])

    def test_create_book_unauthenticated(self):
        """
        Test unauthenticated users cannot create books.
        """
        self.client.logout()
        url = reverse('book-create')
        data = {
            "title": "Unauthorized Book",
            "publication_year": 2022,
            "author": self.author.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        """
        Test that authenticated users can update books.
        """
        url = reverse('book-update', args=[self.book1.id])
        data = {
            "title": "Updated Title",
            "publication_year": 2001,
            "author": self.author.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_update_book_unauthenticated(self):
        """
        Test unauthenticated users cannot update books.
        """
        self.client.logout()
        url = reverse('book-update', args=[self.book1.id])
        data = {
            "title": "Hack Attempt",
            "publication_year": 2001,
            "author": self.author.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authenticated(self):
        """
        Test that authenticated users can delete books.
        """
        url = reverse('book-delete', args=[self.book2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    def test_delete_book_unauthenticated(self):
        """
        Test unauthenticated users cannot delete books.
        """
        self.client.logout()
        url = reverse('book-delete', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_books_by_title(self):
        """
        Test filtering books by title.
        """
        url = reverse('book-list') + '?title=Test Book 1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test Book 1")

    def test_search_books(self):
        """
        Test searching books by keyword in title.
        """
        url = reverse('book-list') + '?search=Another'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Another Book")

    def test_order_books(self):
        """
        Test ordering books by publication_year descending.
        """
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
