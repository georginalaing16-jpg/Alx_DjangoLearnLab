from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import RegisterForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("blog:profile")
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile_view(request):
    return render(request, "blog/profile.html")



from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserUpdateForm

@login_required
def profile_view(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("blog:profile")
        messages.error(request, "Please correct the errors below.")
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "blog/profile.html", {"form": form})


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post
from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["-published_date"]
    paginate_by = 10  # optional


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        # Set author automatically from logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)


class AuthorRequiredMixin(UserPassesTestMixin):
    """Only allow the author of a post to edit/delete it."""
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        # Prevent changing author via crafted POST requests
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")




from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView

from .models import Post, Comment
from .forms import CommentForm


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def dispatch(self, request, *args, **kwargs):
        # Ensure the post exists
        self.post = get_object_or_404(Post, pk=kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.post = self.post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["post"] = self.post
        ctx["mode"] = "create"
        return ctx


class CommentAuthorRequiredMixin(UserPassesTestMixin):
    raise_exception = True  # return 403 instead of redirect loops

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user


class CommentUpdateView(LoginRequiredMixin, CommentAuthorRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["post"] = self.object.post
        ctx["mode"] = "update"
        return ctx


class CommentDeleteView(LoginRequiredMixin, CommentAuthorRequiredMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        # after delete, go back to the post detail page
        return self.object.post.get_absolute_url()


from django.db.models import Q
from django.views.generic import ListView
from .models import Post, Tag

class PostSearchView(ListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        qs = Post.objects.all().order_by("-published_date")
        if not q:
            return qs.none()

        return qs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["query"] = self.request.GET.get("q", "").strip()
        return ctx


class PostsByTagView(ListView):
    model = Post
    template_name = "blog/posts_by_tag.html"
    context_object_name = "posts"

    def get_queryset(self):
        tag_name = self.kwargs["tag_name"].strip().lower()
        return Post.objects.filter(tags__name=tag_name).order_by("-published_date")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tag_name"] = self.kwargs["tag_name"]
        return ctx
