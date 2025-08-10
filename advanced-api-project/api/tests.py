from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Author, Book
User = get_user_model()
class TaskTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='tester', password='pass1234')
        self.author1 = Author.objects.create(name='Author One')
        self.author2 = Author.objects.create(name='Author Two')
        Book.objects.create(title='First Book', publication_year=2000, author=self.author1)
        Book.objects.create(title='Second Book', publication_year=2010, author=self.author2)
        self.books_url = reverse('book-list')
        self.authors_url = reverse('author-list')
    def test_list_books_returns_200(self):
        resp = self.client.get(self.books_url)
        self.assertEqual(resp.status_code, 200)
    def test_create_book_requires_auth_and_returns_201_on_success(self):
        data = {'title': 'New Book', 'publication_year': 2020, 'author': self.author1.id}
        resp = self.client.post(self.books_url, data, format='json')
        self.assertEqual(resp.status_code, 401)  # unauthorized for unauthenticated
        self.client.force_authenticate(user=self.user)
        resp2 = self.client.post(self.books_url, data, format='json')
        self.assertEqual(resp2.status_code, 201)
    def test_publication_year_validation_returns_400(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Future Book', 'publication_year': 3000, 'author': self.author1.id}
        resp = self.client.post(self.books_url, data, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('publication_year', resp.data)
    def test_filter_search_ordering_behaviour(self):
        # filter by author name (query param 'author' per BookFilter)
        resp = self.client.get(self.books_url + '?author=Author One')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)
        # search by title
        resp2 = self.client.get(self.books_url + '?search=Second')
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(len(resp2.data), 1)
        # ordering by publication_year desc
        resp3 = self.client.get(self.books_url + '?ordering=-publication_year')
        self.assertEqual(resp3.status_code, 200)
        years = [item['publication_year'] for item in resp3.data]
        self.assertEqual(years, sorted(years, reverse=True))
    def test_author_crud_and_permissions_status_codes(self):
        # unauthenticated create attempt
        resp = self.client.post(self.authors_url, {'name': 'New Author'}, format='json')
        self.assertEqual(resp.status_code, 401)
        # authenticated create
        self.client.force_authenticate(user=self.user)
        resp2 = self.client.post(self.authors_url, {'name': 'New Author'}, format='json')
        self.assertEqual(resp2.status_code, 201)
        author_detail = reverse('author-detail', args=[resp2.data['id']])
        # update author -> 200
        resp3 = self.client.put(author_detail, {'name': 'Updated Author'}, format='json')
        self.assertEqual(resp3.status_code, 200)
        # delete author -> 204
        resp4 = self.client.delete(author_detail)
        self.assertEqual(resp4.status_code, 204)
