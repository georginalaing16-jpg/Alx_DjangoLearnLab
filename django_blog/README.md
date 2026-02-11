Blog Post Management - Documentation

This project extends the django_blog application with full blog post management using Django class-based views and authentication.
 

# Features

View all posts – /posts/ (public)

View post details – /posts/<pk>/ (public)

Create posts – /posts/new/ (login required)

Edit posts – /posts/<pk>/edit/ (author only)

Delete posts – /posts/<pk>/delete/ (author only)


# Permissions

Only authenticated users can create posts (LoginRequiredMixin)

Only the post author can edit or delete their posts (UserPassesTestMixin)

List and detail views are accessible to everyone


# Forms and Data Handling

Uses a ModelForm for creating and updating posts

The author field is set automatically from the logged-in user

published_date is created automatically

CSRF protection is enabled for all forms

Passwords are securely handled by Django’s built-in authentication system


# Templates

Templates include:

Post list

Post detail

Create/Edit form

Delete confirmation
All templates extend base.html and use the project’s CSS.


# Testing

Logged-out users cannot access create/edit/delete pages

Users cannot modify or delete posts they do not own

Forms validate and save data correctly