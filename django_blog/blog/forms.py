from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(" This email is already in use.")
        return email
    

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "input"}) 



from django import forms
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        qs = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email is already in use.")
        return email


from django import forms
from .models import Post
from taggit.forms import TagWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "tags"]

        widgets = {
            "tags": TagWidget(),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        return title




from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)

    def clean_content(self):
        content = self.cleaned_data["content"].strip()
        if len(content) < 2:
            raise forms.ValidationError("Comment is too short.")
        return content


from django import forms
from .models import Post, Tag

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas (e.g., django, python, web)."
    )

    class Meta:
        model = Post
        fields = ("title", "content", "tags")

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        return title

    def clean_tags(self):
        raw = self.cleaned_data.get("tags", "")
        # Split by comma, strip spaces, remove empties, make lowercase
        tags = [t.strip().lower() for t in raw.split(",") if t.strip()]
        # Optional: prevent too many tags
        if len(tags) > 10:
            raise forms.ValidationError("Please use 10 tags or fewer.")
        return tags

    def save(self, commit=True):
        post = super().save(commit=commit)
        # tags cleaned as list
        tag_names = self.cleaned_data.get("tags", [])

        # Attach tags (create if needed)
        tag_objs = []
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tag_objs.append(tag)

        post.tags.set(tag_objs)
        return post
