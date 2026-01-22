from django.shortcuts import render
from .models import Book
from .forms import BookSearchForm

def book_list(request):
    form = BookSearchForm(request.GET)
    books = Book.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get("query")

        if query:
            # SECURITY: ORM automatically parameterizes queries
            books = books.filter(title__icontains=query)

    return render(request, "bookshelf/book_list.html", {
        "books": books,
        "form": form
    })


from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from django.shortcuts import render

class DeleteBookView(PermissionRequiredMixin, View):
    permission_required = "bookshelf.can_delete"
    raise_exception = True  # 👈 written here

    def get(self, request):
        return render(request, "bookshelf/book_list.html")

