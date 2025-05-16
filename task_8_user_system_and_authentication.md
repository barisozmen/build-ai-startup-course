# Task 8: User System and Authentication

## Objective
Set up a user database in Django and implement an authentication system with registration, login, and user profile functionality for our AI application.

## Prerequisites
- Completed Task 5: Django Setup
- SSH access to your DigitalOcean Droplet
- Basic understanding of Django and web applications

## Steps

### 1. Configure Django's Built-in Authentication System

1. Connect to your Droplet via SSH
2. Navigate to your Django project:
   ```
   cd ~/django_project
   source venv/bin/activate
   ```

3. Ensure Django's authentication apps are in INSTALLED_APPS in ai_app/settings.py:
   ```python
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'core',
       'ghibli_converter',
   ]
   ```

4. Make sure the authentication middleware is enabled in ai_app/settings.py:
   ```python
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.middleware.common.CommonMiddleware',
       'django.middleware.csrf.CsrfViewMiddleware',
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       'django.contrib.messages.middleware.MessageMiddleware',
       'django.middleware.clickjacking.XFrameOptionsMiddleware',
   ]
   ```

### 2. Create a User App

1. Create a new Django app for user management:
   ```
   python manage.py startapp users
   ```

2. Add the new app to INSTALLED_APPS in ai_app/settings.py:
   ```python
   INSTALLED_APPS = [
       # Default apps...
       'core',
       'ghibli_converter',
       'users',
   ]
   ```

### 3. Create User Profile Model

1. Edit users/models.py to create a user profile model:
   ```python
   from django.db import models
   from django.contrib.auth.models import User
   from django.db.models.signals import post_save
   from django.dispatch import receiver

   class Profile(models.Model):
       user = models.OneToOneField(User, on_delete=models.CASCADE)
       bio = models.TextField(max_length=500, blank=True)
       profile_image = models.ImageField(upload_to='profile_pics', default='profile_pics/default.jpg')
       date_joined = models.DateTimeField(auto_now_add=True)
       
       def __str__(self):
           return f'{self.user.username} Profile'

   @receiver(post_save, sender=User)
   def create_user_profile(sender, instance, created, **kwargs):
       if created:
           Profile.objects.create(user=instance)

   @receiver(post_save, sender=User)
   def save_user_profile(sender, instance, **kwargs):
       instance.profile.save()
   ```

2. Create and apply migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Create a default profile image:
   ```
   mkdir -p ~/django_project/media/profile_pics
   # Download a default profile image
   wget -O ~/django_project/media/profile_pics/default.jpg https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y
   ```

### 4. Create Forms for User Registration and Profile

1. Create users/forms.py:
   ```python
   from django import forms
   from django.contrib.auth.models import User
   from django.contrib.auth.forms import UserCreationForm
   from .models import Profile

   class UserRegisterForm(UserCreationForm):
       email = forms.EmailField()
       
       class Meta:
           model = User
           fields = ['username', 'email', 'password1', 'password2']
   
   class UserUpdateForm(forms.ModelForm):
       email = forms.EmailField()
       
       class Meta:
           model = User
           fields = ['username', 'email']
   
   class ProfileUpdateForm(forms.ModelForm):
       class Meta:
           model = Profile
           fields = ['bio', 'profile_image']
   ```

### 5. Create Views for Authentication

1. Edit users/views.py:
   ```python
   from django.shortcuts import render, redirect
   from django.contrib import messages
   from django.contrib.auth.decorators import login_required
   from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

   def register(request):
       if request.method == 'POST':
           form = UserRegisterForm(request.POST)
           if form.is_valid():
               form.save()
               username = form.cleaned_data.get('username')
               messages.success(request, f'Account created for {username}! You can now log in.')
               return redirect('login')
       else:
           form = UserRegisterForm()
       return render(request, 'users/register.html', {'form': form})

   @login_required
   def profile(request):
       if request.method == 'POST':
           u_form = UserUpdateForm(request.POST, instance=request.user)
           p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
           
           if u_form.is_valid() and p_form.is_valid():
               u_form.save()
               p_form.save()
               messages.success(request, 'Your profile has been updated!')
               return redirect('profile')
       else:
           u_form = UserUpdateForm(instance=request.user)
           p_form = ProfileUpdateForm(instance=request.user.profile)
       
       context = {
           'u_form': u_form,
           'p_form': p_form
       }
       return render(request, 'users/profile.html', context)
   ```

### 6. Create URL Patterns for User Authentication

1. Create users/urls.py:
   ```python
   from django.urls import path
   from . import views
   from django.contrib.auth import views as auth_views

   urlpatterns = [
       path('register/', views.register, name='register'),
       path('profile/', views.profile, name='profile'),
       path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
       path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
       path('password-reset/', 
            auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), 
            name='password_reset'),
       path('password-reset/done/', 
            auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
            name='password_reset_done'),
       path('password-reset-confirm/<uidb64>/<token>/', 
            auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
            name='password_reset_confirm'),
       path('password-reset-complete/', 
            auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
            name='password_reset_complete'),
   ]
   ```

2. Update the project's urls.py:
   ```python
   from django.contrib import admin
   from django.urls import path, include
   from django.conf import settings
   from django.conf.urls.static import static

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('ghibli_converter.urls')),
       path('users/', include('users.urls')),
   ]

   if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

### 7. Configure Login/Logout Redirects

1. Add these settings to ai_app/settings.py:
   ```python
   # Authentication settings
   LOGIN_REDIRECT_URL = 'home'
   LOGIN_URL = 'login'
   ```

### 8. Create Templates for User Authentication

1. Create template directories:
   ```
   mkdir -p users/templates/users
   ```

2. Create users/templates/users/register.html:
   ```html
   {% extends "ghibli_converter/base.html" %}
   {% block content %}
       <div class="form-container">
           <h2>Register</h2>
           <form method="POST">
               {% csrf_token %}
               <fieldset>
                   <legend>Join Today</legend>
                   {{ form.as_p }}
               </fieldset>
               <div>
                   <button type="submit">Sign Up</button>
               </div>
           </form>
           <div class="border-top pt-3">
               <small>
                   Already Have An Account? <a href="{% url 'login' %}">Sign In</a>
               </small>
           </div>
       </div>
   {% endblock content %}
   ```

3. Create users/templates/users/login.html:
   ```html
   {% extends "ghibli_converter/base.html" %}
   {% block content %}
       <div class="form-container">
           <h2>Login</h2>
           <form method="POST">
               {% csrf_token %}
               <fieldset>
                   <legend>Log In</legend>
                   {{ form.as_p }}
               </fieldset>
               <div>
                   <button type="submit">Login</button>
               </div>
               <div class="border-top pt-3">
                   <small>
                       <a href="{% url 'password_reset' %}">Forgot Password?</a>
                   </small>
               </div>
           </form>
           <div class="border-top pt-3">
               <small>
                   Need An Account? <a href="{% url 'register' %}">Sign Up Now</a>
               </small>
           </div>
       </div>
   {% endblock content %}
   ```

4. Create users/templates/users/logout.html:
   ```html
   {% extends "ghibli_converter/base.html" %}
   {% block content %}
       <div class="form-container">
           <h2>You have been logged out</h2>
           <div>
               <small>
                   <a href="{% url 'login' %}">Log In Again</a>
               </small>
           </div>
       </div>
   {% endblock content %}
   ```

5. Create users/templates/users/profile.html:
   ```html
   {% extends "ghibli_converter/base.html" %}
   {% block content %}
       <div class="profile-container">
           <div class="profile-header">
               <img class="profile-image" src="{{ user.profile.profile_image.url }}">
               <div class="profile-info">
                   <h2>{{ user.username }}</h2>
                   <p>{{ user.email }}</p>
                   <p>{{ user.profile.bio }}</p>
               </div>
           </div>
           
           <div class="form-container">
               <h3>Update Profile</h3>
               <form method="POST" enctype="multipart/form-data">
                   {% csrf_token %}
                   <fieldset>
                       <legend>Profile Info</legend>
                       {{ u_form.as_p }}
                       {{ p_form.as_p }}
                   </fieldset>
                   <div>
                       <button type="submit">Update</button>
                   </div>
               </form>
           </div>
       </div>
   {% endblock content %}
   ```

6. Create password reset templates:
   ```
   touch users/templates/users/password_reset.html
   touch users/templates/users/password_reset_done.html
   touch users/templates/users/password_reset_confirm.html
   touch users/templates/users/password_reset_complete.html
   ```

7. Add basic content to each password reset template (example for password_reset.html):
   ```html
   {% extends "ghibli_converter/base.html" %}
   {% block content %}
       <div class="form-container">
           <h2>Reset Password</h2>
           <form method="POST">
               {% csrf_token %}
               <fieldset>
                   <legend>Password Reset</legend>
                   {{ form.as_p }}
               </fieldset>
               <div>
                   <button type="submit">Request Password Reset</button>
               </div>
           </form>
       </div>
   {% endblock content %}
   ```

### 9. Update Base Template to Include Authentication Links

1. Update ghibli_converter/templates/ghibli_converter/base.html to include authentication links:
   ```html
   <div class="nav">
       <a href="{% url 'home' %}">Home</a>
       <a href="{% url 'gallery' %}">Gallery</a>
       {% if user.is_authenticated %}
           <a href="{% url 'profile' %}">Profile</a>
           <a href="{% url 'logout' %}">Logout</a>
       {% else %}
           <a href="{% url 'login' %}">Login</a>
           <a href="{% url 'register' %}">Register</a>
       {% endif %}
   </div>
   ```

2. Add CSS for user-related elements:
   ```html
   <style>
       /* Existing styles... */
       
       .form-container {
           max-width: 500px;
           margin: 0 auto;
           padding: 20px;
           border: 1px solid #ddd;
           border-radius: 5px;
       }
       
       .profile-container {
           max-width: 700px;
           margin: 0 auto;
       }
       
       .profile-header {
           display: flex;
           align-items: center;
           margin-bottom: 20px;
       }
       
       .profile-image {
           width: 100px;
           height: 100px;
           border-radius: 50%;
           object-fit: cover;
           margin-right: 20px;
       }
       
       .profile-info {
           flex: 1;
       }
       
       .messages {
           list-style: none;
           padding: 0;
           margin: 10px 0;
       }
       
       .messages li {
           padding: 10px;
           margin: 5px 0;
           border-radius: 5px;
       }
       
       .messages .success {
           background-color: #d4edda;
           color: #155724;
       }
       
       .messages .error {
           background-color: #f8d7da;
           color: #721c24;
       }
   </style>
   ```

3. Add message display to the base template:
   ```html
   <div class="content">
       {% if messages %}
           <ul class="messages">
               {% for message in messages %}
                   <li class="{{ message.tags }}">{{ message }}</li>
               {% endfor %}
           </ul>
       {% endif %}
       
       {% block content %}{% endblock %}
   </div>
   ```

### 10. Configure Email for Password Reset (Optional)

1. For development, add these settings to ai_app/settings.py:
   ```python
   # Email settings (for development)
   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   ```

2. For production, configure a real email backend:
   ```python
   # Email settings (for production)
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'  # Or your email provider
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'your-email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-app-password'  # Use app password for Gmail
   ```

### 11. Register Models in Admin

1. Edit users/admin.py:
   ```python
   from django.contrib import admin
   from .models import Profile

   admin.site.register(Profile)
   ```

### 12. Protect Views That Require Authentication

1. Update ghibli_converter/views.py to require login for certain views:
   ```python
   from django.contrib.auth.decorators import login_required

   # Add @login_required decorator to views that should require authentication
   @login_required
   def home(request):
       # Existing view code...
   ```

### 13. Restart Gunicorn to Apply Changes

1. Restart the Gunicorn service:
   ```
   sudo systemctl restart gunicorn
   ```

## Expected Outcome
A complete user authentication system with registration, login, profile management, and password reset functionality integrated into your Django application.

## Troubleshooting

- **Database migration errors**: Check migration files and database consistency
- **Template errors**: Verify template paths and inheritance structure
- **Static/Media file issues**: Ensure proper configuration of static and media file settings
- **Email configuration problems**: Test email settings with Django's send_test_email command
- **Permission issues**: Check file permissions for media uploads
- **Login redirect loops**: Verify LOGIN_REDIRECT_URL and LOGIN_URL settings

## Notes

- Django's built-in authentication system provides a robust foundation for user management
- For production, consider adding additional security measures like:
  - Email verification for new accounts
  - Two-factor authentication
  - Rate limiting for login attempts
  - HTTPS enforcement
- The user profile model can be extended with additional fields as needed
- Consider implementing social authentication (Google, Facebook, etc.) using django-allauth for a more complete solution
