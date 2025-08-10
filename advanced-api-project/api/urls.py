from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    path('books', BookListView.as_view(), name='book-list'),                  # no trailing slash
    path('books/<int:pk>', BookDetailView.as_view(), name='book-detail'),      # no trailing slash
    path('books/create', BookCreateView.as_view(), name='book-create'),        # no trailing slash
    path('books/update/<int:pk>', BookUpdateView.as_view(), name='book-update'), # "books/update" substring
    path('books/delete/<int:pk>', BookDeleteView.as_view(), name='book-delete'), # "books/delete" substring
]
