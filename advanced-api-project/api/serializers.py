from rest_framework import serializers
from .models import Author, Book
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model, serializes all fields of Book.
    Includes validation to ensure publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Validates that the publication year is not in the future.
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model.
    Includes the 'name' field and a nested list of related books serialized using BookSerializer.
    """
    books = BookSerializer(many=True, read_only=True)
    # 'books' corresponds to related_name in Book.author ForeignKey

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
