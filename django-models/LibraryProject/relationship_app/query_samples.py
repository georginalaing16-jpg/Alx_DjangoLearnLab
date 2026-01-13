import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


# Query 1: All books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)


# Query 2: List all books in a library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()


# Query 3: Retrieve the librarian for a library
def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian


if __name__ == "__main__":
    print("Books by Author:")
    for book in books_by_author("John Doe"):
        print(book.title)

    print("\nBooks in Library:")
    for book in books_in_library("Central Library"):
        print(book.title)

    print("\nLibrarian for Library:")
    librarian = librarian_for_library("Central Library")
    print(librarian.name)