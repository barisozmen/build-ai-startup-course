# Task 8: User System and Authentication

## Objective
Extend the AI Image Generation App by adding a user authentication system, user profile pages, and associating generated images with specific users.

## Prerequisites
- Completed Task 7: AI Image Generation App
- Basic understanding of Django's authentication system

## Steps

### 1. Update Model to Include User Relationship

1. Modify the GeneratedImage model in image_generator/models.py to associate images with users:

```python:image_generator/models.py
from django.db import models
from django.contrib.auth.models import User
   
class GeneratedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images', null=True)
    prompt = models.TextField()
    image = models.ImageField(upload_to='generated_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Image from: {self.prompt[:50]}"
```

2. Create and apply migrations:
```
python manage.py makemigrations
python manage.py migrate
```

### 2. Create User Profile Model

1. Create a UserProfile model in image_generator/models.py:

```python:image_generator/models.py
# Add to the existing models.py file
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
```

2. Apply migrations:
```
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Forms for User Authentication

1. Update image_generator/forms.py to include user registration and profile forms:

```python:image_generator/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
   
class ImagePromptForm(forms.Form):
    prompt = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the image you want to generate...'}),
        max_length=1000
    )
    is_public = forms.BooleanField(required=False, initial=True, label='Make this image public')

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create user profile
            UserProfile.objects.create(user=user)
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_picture')
```

### 4. Create Templates for User Authentication

1. Create login template at image_generator/templates/image_generator/login.html:

```html:image_generator/templates/image_generator/login.html
{% extends 'image_generator/base.html' %}

{% block content %}
<h2>Login</h2>
<form method="post" class="auth-form">
    {% csrf_token %}
    <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" name="username" id="username" required>
    </div>
    <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" name="password" id="password" required>
    </div>
    <button type="submit">Login</button>
</form>
<div class="auth-links">
    <p>Don't have an account? <a href="{% url 'register' %}">Register here</a></p>
</div>
{% endblock %}
```

2. Create registration template at image_generator/templates/image_generator/register.html:

```html:image_generator/templates/image_generator/register.html
{% extends 'image_generator/base.html' %}

{% block content %}
<h2>Register</h2>
<form method="post" class="auth-form">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Register</button>
</form>
<div class="auth-links">
    <p>Already have an account? <a href="{% url 'login' %}">Login here</a></p>
</div>
{% endblock %}
```

3. Create profile template at image_generator/templates/image_generator/profile.html:

```html:image_generator/templates/image_generator/profile.html
{% extends 'image_generator/base.html' %}

{% block content %}
<div class="profile">
    <h2>{{ user.username }}'s Profile</h2>
    
    <div class="profile-info">
        {% if user.profile.profile_picture %}
            <img src="{{ user.profile.profile_picture.url }}" alt="Profile picture" class="profile-picture">
        {% endif %}
        
        <div class="profile-details">
            <p><strong>Username:</strong> {{ user.username }}</p>
            <p><strong>Email:</strong> {{ user.email }}</p>
            <p><strong>Bio:</strong> {{ user.profile.bio|default:"No bio provided." }}</p>
            <p><strong>Member since:</strong> {{ user.date_joined|date:"F j, Y" }}</p>
            <p><strong>Images created:</strong> {{ user.images.count }}</p>
        </div>
    </div>
    
    <div class="profile-actions">
        <a href="{% url 'edit_profile' %}" class="button">Edit Profile</a>
    </div>
    
    <h3>Your Images</h3>
    {% if user.images.exists %}
        <div class="gallery">
            {% for image in user.images.all %}
            <div class="image-card">
                <img src="{{ image.image.url }}" alt="Generated image">
                <div class="prompt">"{{ image.prompt }}"</div>
                <div class="timestamp">{{ image.created_at|date:"F j, Y, g:i a" }}</div>
                <div class="visibility">{% if image.is_public %}Public{% else %}Private{% endif %}</div>
            </div>
            {% endfor %}
        </div>
    {% else %}
        <p>You haven't created any images yet. <a href="{% url 'home' %}">Create your first image!</a></p>
    {% endif %}
</div>
{% endblock %}
```

4. Create edit profile template at image_generator/templates/image_generator/edit_profile.html:

```html:image_generator/templates/image_generator/edit_profile.html
{% extends 'image_generator/base.html' %}

{% block content %}
<h2>Edit Profile</h2>
<form method="post" enctype="multipart/form-data" class="profile-form">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save Changes</button>
</form>
<div class="profile-actions">
    <a href="{% url 'profile' %}" class="button secondary">Back to Profile</a>
</div>
{% endblock %}
```

### 5. Update the Base Template to Include Authentication Links

1. Update image_generator/templates/image_generator/base.html:

```html:image_generator/templates/image_generator/base.html
<!DOCTYPE html>
<html>
<head>
    <title>AI Image Generator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        /* Existing styles */
        body {
            font-family: Arial, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        /* Add styles for auth components */
        .auth-section {
            position: absolute;
            top: 20px;
            right: 20px;
            font-size: 0.9em;
        }
        .auth-links a {
            margin-left: 10px;
            color: #0066cc;
            text-decoration: none;
        }
        .auth-form {
            max-width: 400px;
            margin: 0 auto;
        }
        .auth-form .form-group {
            margin-bottom: 15px;
        }
        .auth-form label {
            display: block;
            margin-bottom: 5px;
        }
        .auth-form input {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
        }
        .profile-picture {
            max-width: 150px;
            border-radius: 50%;
            margin-right: 20px;
        }
        .profile-info {
            display: flex;
            margin-bottom: 30px;
        }
        .profile-actions {
            margin: 20px 0;
        }
        .button {
            display: inline-block;
            padding: 8px 15px;
            background-color: #0066cc;
            color: white;
            text-decoration: none;
            border-radius: 4px;
        }
        .button.secondary {
            background-color: #666;
        }
        .visibility {
            font-size: 0.8em;
            color: #555;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="auth-section">
        {% if user.is_authenticated %}
            Welcome, <a href="{% url 'profile' %}">{{ user.username }}</a> | 
            <a href="{% url 'logout' %}">Logout</a>
        {% else %}
            <a href="{% url 'login' %}">Login</a> | 
            <a href="{% url 'register' %}">Register</a>
        {% endif %}
    </div>

    <div class="header">
        <h1>AI Image Generator</h1>
        <p>Create amazing images with artificial intelligence</p>
    </div>
    
    <div class="nav">
        <a href="{% url 'home' %}">Generate</a>
        <a href="{% url 'gallery' %}">Gallery</a>
        {% if user.is_authenticated %}
            <a href="{% url 'profile' %}">My Profile</a>
        {% endif %}
    </div>
    
    {% if messages %}
    <div class="messages">
        {% for message in messages %}
            <div class="message {% if message.tags %}{{ message.tags }}{% endif %}">
                {{ message }}
            </div>
        {% endfor %}
    </div>
    {% endif %}
    
    <div class="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

### 6. Update Views to Handle Authentication and Profiles

1. Update image_generator/views.py:

```python:image_generator/views.py
import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImagePromptForm, UserRegistrationForm, UserProfileForm
from .models import GeneratedImage, UserProfile
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@login_required
def home(request):
    if request.method == 'POST':
        form = ImagePromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            is_public = form.cleaned_data['is_public']
            
            # Generate image using OpenAI API
            try:
                generated_image = generate_image(prompt, request.user, is_public)
                return redirect('gallery')
            except Exception as e:
                return render(request, 'image_generator/error.html', {'error': str(e)})
    else:
        form = ImagePromptForm()
    
    return render(request, 'image_generator/home.html', {'form': form})

def generate_image(prompt, user, is_public=True):
    # Call OpenAI API to generate an image using the new syntax
    try:
        response = client.images.generate(
            model="dall-e-2",  # or "dall-e-3" for the newer model
            prompt=prompt,
            n=1,
            size="512x512"
        )
        
        # Get the image URL from the new response format
        image_url = response.data[0].url
        
        # Download the generated image
        image_response = requests.get(image_url)
        
        # Create a new GeneratedImage instance
        generated_image = GeneratedImage(prompt=prompt, user=user, is_public=is_public)
        generated_image.image.save(
            f"generated_{generated_image.id}.png",
            ContentFile(image_response.content)
        )
        generated_image.save()
        
        return generated_image
    except Exception as e:
        raise Exception(f"API Error: {str(e)}")

def gallery(request):
    # If user is authenticated, show public images and user's private images
    if request.user.is_authenticated:
        images = GeneratedImage.objects.filter(
            is_public=True
        ).order_by('-created_at') | GeneratedImage.objects.filter(
            user=request.user
        ).order_by('-created_at')
    else:
        # If not authenticated, only show public images
        images = GeneratedImage.objects.filter(is_public=True).order_by('-created_at')
    
    return render(request, 'image_generator/gallery.html', {'images': images})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            
    return render(request, 'image_generator/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
        
    return render(request, 'image_generator/register.html', {'form': form})

@login_required
def profile(request):
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'image_generator/profile.html')

@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
        
    return render(request, 'image_generator/edit_profile.html', {'form': form})
```

### 7. Update URLs to Include Authentication Routes

1. Update image_generator/urls.py:

```python:image_generator/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
```

### 8. Register Models in Admin

1. Update image_generator/admin.py:

```python:image_generator/admin.py
from django.contrib import admin
from .models import GeneratedImage, UserProfile

admin.site.register(GeneratedImage)
admin.site.register(UserProfile)
```

### 9. Add Messages Template

1. Update image_generator/templates/image_generator/base.html to style the messages:

```html:image_generator/templates/image_generator/base.html
<!-- Add this CSS to the style section -->
<style>
    /* ... existing styles ... */
    
    .messages {
        margin: 10px 0;
        padding: 0;
        list-style: none;
    }
    
    .message {
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 4px;
    }
    
    .success {
        background-color: #d4edda;
        color: #155724;
    }
    
    .error {
        background-color: #f8d7da;
        color: #721c24;
    }
    
    .warning {
        background-color: #fff3cd;
        color: #856404;
    }
    
    .info {
        background-color: #d1ecf1;
        color: #0c5460;
    }
</style>
```

### 10. Update Settings to Configure Login URLs

1. Add the following to my_project/settings.py:

```python:my_project/settings.py
# Add these lines to the end of the file
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```

3. Apply the migrations:
```
python manage.py makemigrations
python manage.py migrate
```

### 12. Test the Authentication System

1. Start the Django development server:
```
python manage.py runserver 0.0.0.0:8000
```

2. Test the registration, login, and profile functionality:
   - Register a new user
   - Login with the new user
   - Generate images
   - View and edit your profile
   - Verify that public/private images work correctly

## Expected Outcome

A complete Django web application with:
- User registration and login functionality
- User profile pages with customizable information
- Image generation capability that associates images with the creating user
- A gallery that respects image privacy settings (public vs. private)
- Proper authentication for protected routes

## Troubleshooting

- **Migration Errors**: If you encounter issues with migrations, you might need to reset them or create them from scratch
- **Login Issues**: Check that your authentication views are correctly configured
- **Image Visibility Issues**: Verify that your query in the gallery view correctly filters for public vs. private images
- **Profile Picture Problems**: Ensure media files are properly configured in settings and URLs

## Notes

- For production environments, consider implementing password reset functionality
- You can enhance security by implementing email verification for new accounts
- Consider adding social authentication (Google, Facebook, etc.) for a more seamless experience
- The current implementation is basic; you might want to add additional features like:
  - Following other users
  - Liking/favoriting images
  - Commenting on images
  - Settings for default image visibility
  - User roles (admin, moderator, regular user)
