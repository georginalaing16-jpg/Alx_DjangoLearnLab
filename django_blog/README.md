### TASK 2
#How the authentication flow works
# Registration
- User visits /register/
- RegisterForm (extends UserCreationForm) collects username, email, password1, password2
- On success, the user is created and immediately logged in via login(request, user)

# Login
- User visits /login/
- Django’s built-in LoginView authenticates and starts a session

# Profile
- User visits /profile/
- Protected by @login_required
- GET: show profile edit form prefilled with current username/email
- POST: validate + save changes, show success/error message

# Logout

- User posts to /logout/
- Django’s built-in LogoutView ends the session

# Files' functions
blog/forms.py
- RegisterForm: creates users + validates unique email
- UserUpdateForm: updates username/email safely

blog/views.py
- register_view: custom registration flow
- profile_view: view + edit profile details

blog/urls.py
- routes /login/ /logout/ /register/ /profile/

blog/templates/blog/*.html
- UI + CSRF protection + error display + success messages

# How to test each feature
- Registration: fill form → redirects to profile
- Login: use created credentials → redirects to profile
- Logout: click logout button → session ends
- Profile edit: change email → saved and visible after refresh
- Security: confirm profile requires login; confirm CSRF present in page source



### TASK 3
#Blog Post Management - Documentation
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



### TASK 4
#Comment System
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




### TASK 5
#Tagging and Search
# Tagging
Posts support multiple tags via a ManyToMany relationship between `Post` and `Tag`.
Tags are entered in the post form as a comma-separated list (e.g., `django, python, web`).

**Rules:**
- Tags are normalized to lowercase.
- New tags are created automatically if they don’t exist.
- Tags are optional.

# Viewing Tags
Tags are displayed on the post list and post detail pages.
Each tag links to a filtered list of posts:

- `/tags/<tag_name>/` shows all posts with that tag.

# Search
Users can search posts by:
- title
- content
- tag names

Search is handled through `/search/?q=<query>` using Django `Q` objects and `icontains`.
Results are displayed on the search results page.

# How to Use
1. Create or edit a post and add tags in the tags field (comma-separated).
2. Click a tag (e.g., `#django`) to view tagged posts.
3. Use the search bar to find posts by keywords or tag names.
