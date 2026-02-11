## Blog Post Management - Documentation
This project extends the django_blog application with full blog post management using Django class-based views and authentication.
 
# Features
- View all post – /post/ (public)
- View post details – /post/<pk>/ (public)
- Create post – /post/new/ (login required)
- Edit post – /post/<pk>/edit/ (author only)
- Delete post – /post/<pk>/delete/ (author only)

# Permissions
- Only authenticated users can create posts (LoginRequiredMixin)
- Only the post author can edit or delete their posts (UserPassesTestMixin)
- List and detail views are accessible to everyone

# Forms and Data Handling
- Uses a ModelForm for creating and updating posts
- The author field is set automatically from the logged-in user
- Published_date is created automatically
- CSRF protection is enabled for all forms
- Passwords are securely handled by Django’s built-in authentication system

# Templates
- Templates include:
- Post list
- Post detail
- Create/Edit form
- Delete confirmation
All templates extend base.html and use the project’s CSS.

# Testing
- Logged-out users cannot access create/edit/delete pages
- Users cannot modify or delete posts they do not own
- Forms validate and save data correctly




## Comment System
Each blog post supports a list of comments. All users can read comments, but only authenticated users can create comments. Only the comment author can edit or delete their own comments.

# Model
Comment fields:
- post (ForeignKey → Post)
- author (ForeignKey → User)
- content (TextField)
- created_at (auto_now_add)
- updated_at (auto_now)

# URLs
- Create comment: /post/<post_id>/comments/new/
- Edit comment: /comments/<comment_id>/edit/
- Delete comment: /comments/<comment_id>/delete/

# Permissions
- Creating a comment requires login (LoginRequiredMixin).
- Editing/deleting a comment requires login and ownership (UserPassesTestMixin).
- Unauthorized edit/delete returns HTTP 403.

# Data Handling Notes
- Comment.author is set automatically from the logged-in user in the CreateView.
- Comment.post is set from the URL post_id in the CreateView.
- content is validated to prevent empty/too-short comments.

# Testing
1. Visit a post detail page and confirm comments display for logged-out users.
2. Login and add a comment; confirm it appears under the post.
3. Edit your comment and confirm updated_at changes.
4. Delete your comment and confirm it is removed.
5. Login as another user and verify you cannot edit/delete someone else’s comment (403).
