from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from requests import request

from .models import Book

def list_books(request):
    books = Book.objects.all()

    return render(request, 'relationship_app/list_books.html', {
        'books': books
    })

from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import Library

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView 

class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after registration
            return redirect('list_books')
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})