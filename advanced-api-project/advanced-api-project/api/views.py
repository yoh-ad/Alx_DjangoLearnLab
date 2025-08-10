from rest_framework import generics, permissions
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'publication_year', 'author__id', 'author__name']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
