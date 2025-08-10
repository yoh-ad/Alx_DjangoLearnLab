import django_filters
from .models import Book
class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    author_name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    publication_year = django_filters.NumberFilter(field_name='publication_year')
    class Meta:
        model = Book
        fields = ['title','author_name','publication_year']
