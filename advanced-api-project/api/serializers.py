# Add serializers to api_app
from rest_framework import serializers
from datetime import date
from .models import Author, Book

# BookSerializer with validation for publication_year
class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

# Validates that publication_year is not in the future
        def validate_publication_year(self, value):
            current_year = date.today().year
            if value > current_year:
                raise serializers.ValidationError("Publication year cannot be in the future.")
            return value
        
# AuthorSerializer with nested BookSerializer
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']