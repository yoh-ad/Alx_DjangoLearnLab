from rest_framework import serializers
from .models import Author, Book
import datetime

class BookSerializer(serializers.ModelSerializer):
    """Serializes Book model; includes validation to ensure publication_year is not in the future."""
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError('publication_year cannot be in the future.')
        return value

class NestedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year']

class AuthorSerializer(serializers.ModelSerializer):
    """Author serializer includes nested books dynamically using a nested BookSerializer."""
    books = NestedBookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
