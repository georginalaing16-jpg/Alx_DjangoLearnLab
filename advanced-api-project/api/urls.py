"""
URL configuration for advanced_api_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import (BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView)

urlpatterns = [
    path("books/", BookListView.as_view(), name="book-list"),  # URL for listing all books
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),  # URL for retrieving a single book by its primary key (id)
    path("books/create/", BookCreateView.as_view(), name="book-create"),  # URL for creating a new book
    path("books/<int:pk>/update/", BookUpdateView.as_view(), name="book-update"),  # URL for updating an existing book by its primary key (id)
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),  # URL for deleting an existing book by its primary key (id)
]
