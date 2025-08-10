from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Author, Book
User = get_user_model()
class BookAuthorAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='tester', password='pass1234')
        self.author1 = Author.objects.create(name='Author One')
        self.author2 = Author.objects.create(name='Author Two')
        Book.objects.create(title='First Book', publication_year=2000, author=self.author1)
        Book.objects.create(title='Second Book', publication_year=2010, author=self.author2)
        self.books_url = reverse('book-list')
        self.authors_url = reverse('author-list')
    def test_list_books(self):
        resp = self.client.get(self.books_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 2)
    def test_author_list_and_retrieve_includes_books(self):
        resp = self.client.get(self.authors_url)
        self.assertEqual(resp.status_code, 200)
        # authors have nested books in retrieve
        detail = reverse('author-detail', args=[self.author1.id])
        r = self.client.get(detail)
        self.assertEqual(r.status_code, 200)
        self.assertIn('books', r.data)
    def test_create_book_requires_auth(self):
        data = {'title': 'New Book', 'publication_year': 2020, 'author': self.author1.id}
        resp = self.client.post(self.books_url, data, format='json')
        self.assertEqual(resp.status_code, 401)
        self.client.force_authenticate(user=self.user)
        resp2 = self.client.post(self.books_url, data, format='json')
        self.assertEqual(resp2.status_code, 201)
        self.assertEqual(Book.objects.filter(title='New Book').count(), 1)
    def test_publication_year_validation(self):
        self.client.force_authenticate(user=self.user)
        future_year = 3000
        data = {'title': 'Future Book', 'publication_year': future_year, 'author': self.author1.id}
        resp = self.client.post(self.books_url, data, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('publication_year', resp.data)
    def test_filtering_search_ordering(self):
        # filter by author name via author_name param
        resp = self.client.get(self.books_url + '?author_name=Author One')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)
        # search
        resp2 = self.client.get(self.books_url + '?search=Second')
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(len(resp2.data), 1)
        # ordering
        resp3 = self.client.get(self.books_url + '?ordering=-publication_year')
        self.assertEqual(resp3.status_code, 200)
        years = [item['publication_year'] for item in resp3.data]
        self.assertEqual(years, sorted(years, reverse=True))
    def test_author_crud_permissions(self):
        # unauthenticated cannot create author
        resp = self.client.post(self.authors_url, {'name': 'New Author'}, format='json')
        self.assertEqual(resp.status_code, 401)
        self.client.force_authenticate(user=self.user)
        resp2 = self.client.post(self.authors_url, {'name': 'New Author'}, format='json')
        self.assertEqual(resp2.status_code, 201)
        # update author
        detail = reverse('author-detail', args=[resp2.data['id']])
        resp3 = self.client.put(detail, {'name': 'Updated'}, format='json')
        self.assertEqual(resp3.status_code, 200)
        # delete author
        resp4 = self.client.delete(detail)
        self.assertEqual(resp4.status_code, 204)
