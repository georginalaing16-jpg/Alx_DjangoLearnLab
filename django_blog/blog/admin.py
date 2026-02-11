from django.contrib import admin
from .models import Post, Comment

# Register Post model to make it available in the Django admin interface
admin.site.register(Post)
# Register Comment model to make it available in the Django admin interface
admin.site.register(Comment)



