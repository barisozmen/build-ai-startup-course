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