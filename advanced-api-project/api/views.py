from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

# Handles GET requests for list of books (ListView)
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()  # Retrieves all Book instances
    serializer_class = BookSerializer  # Specifies the serializer to use for converting model instances to JSON

# Handles GET requests for retrieving a single Book instance by its primary key (id) (DetailView)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()   
    serializer_class = BookSerializer  

# Handles POST requests for creating a new Book instance (CreateView)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()  
    serializer_class = BookSerializer   

# Handles PUT and PATCH requests for updating an existing Book instance by its primary key (id) (UpdateView)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()   
    serializer_class = BookSerializer   

# Handles DELETE requests for deleting an existing Book instance by its primary key (id) (DeleteView)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer   



from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can create books

    def perform_create(self, request, *args, **kwargs):
        # Automatically set the owner of the book to the logged-in user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "Book created successfully", "book": serializer.data}, status=status.HTTP_201_CREATED)
    

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can update books

    def perform_update(self, request, *args, **kwargs):
        # Ensure that only the owner can update the book
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Book updated successfully", "book": serializer.data}, status=status.HTTP_200_OK)
    



from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

# List all books with filtering and search capabilities
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user to view the list

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author']  # Enable search by title and author
    ordering_fields = ['title', 'published_year']  # Enable ordering by published date and title

# Retrieve a single book by its primary key (id)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user to view book details

# Create a new book (only for authenticated users)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can create books

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "Book created successfully", "book": serializer.data}, status=status.HTTP_201_CREATED)
    
# Update an existing book by its primary key (id) (only for authenticated users)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can update books

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Book updated successfully", "book": serializer.data}, status=status.HTTP_200_OK)
    
# Delete an existing book by its primary key (id) (only for authenticated users)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can delete books

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)