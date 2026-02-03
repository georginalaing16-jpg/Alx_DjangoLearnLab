#Add models to api_app
from django.db import models

# Writer can have many books in this Author representation
# One-to-Many relationship between Author and Book (the 'one' side is Author)
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

# This book model represents published books associated with a particular author
# One-to-many relationship between Author and Book (the 'many' side is Book)
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title

# Create your models here.
