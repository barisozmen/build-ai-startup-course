import os
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.base import ContentFile
from .forms import ImagePromptForm
from .models import GeneratedImage
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def home(request):
    if request.method == 'POST':
        form = ImagePromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            
            # Generate image using OpenAI API
            try:
                generated_image = generate_image(prompt)
                return redirect('gallery')
            except Exception as e:
                return render(request, 'image_generator/error.html', {'error': str(e)})
    else:
        form = ImagePromptForm()
    
    return render(request, 'image_generator/home.html', {'form': form})

def generate_image(prompt):
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
        generated_image = GeneratedImage(prompt=prompt)
        generated_image.image.save(
            f"generated_{generated_image.id}.png",
            ContentFile(image_response.content)
        )
        generated_image.save()
        
        return generated_image
    except Exception as e:
        raise Exception(f"API Error: {str(e)}")

def gallery(request):
    images = GeneratedImage.objects.all().order_by('-created_at')
    return render(request, 'image_generator/gallery.html', {'images': images})