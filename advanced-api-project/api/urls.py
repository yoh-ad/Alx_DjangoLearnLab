from django.urls import path
from . import views
urlpatterns = [
    path('books/', views.BookListCreateAPIView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookRetrieveUpdateDestroyAPIView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListCreateAPIView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorRetrieveUpdateDestroyAPIView.as_view(), name='author-detail'),
]
