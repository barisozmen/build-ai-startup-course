# Task 7: AI Image Generation App

## Objective
Create a Django web application that allows users to generate images from text prompts using an AI API and view all generated images in a gallery.

## Prerequisites
- Completed Task 6: Django Setup
- API key for an AI image generation service

## Steps

### 1. Choose an API for Image Generation

Several AI services offer text-to-image generation capabilities. For this project, we'll use the OpenAI DALL-E API:

1. Visit [OpenAI Platform](https://platform.openai.com/) and create an account
2. Get your API key from the dashboard
3. Note: You'll need to add payment information to use the API, but costs are generally low for testing

Alternative: You can use [StabilityAI](https://stability.ai/), [DeepAI](https://deepai.org/), or other similar services that offer text-to-image capabilities.

### 2. Update Django Project Structure

1. Connect to your Droplet via SSH
2. Navigate to your Django project:
   ```
   cd ~/django_project
   source venv/bin/activate
   ```

3. Create a new app for the image generator:
   ```
   python manage.py startapp image_generator
   ```

4. Add the new app to INSTALLED_APPS in my_project/settings.py:
   ```python
   INSTALLED_APPS = [
       # Default apps...
       'image_generator',
   ]
   ```

5. Configure media settings in my_project/settings.py:
   ```python
   import os
   
   # Add to the bottom of the file
   MEDIA_URL = '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
   ```

### 3. Create Model for Image Storage

1. Edit image_generator/models.py:
   ```python
   from django.db import models
   
   class GeneratedImage(models.Model):
       prompt = models.TextField()
       image = models.ImageField(upload_to='generated_images/')
       created_at = models.DateTimeField(auto_now_add=True)
       
       def __str__(self):
           return f"Image from: {self.prompt[:50]}"
   ```

2. Create and apply migrations:
   ```
   pip install pillow  # Required for ImageField
   python manage.py makemigrations
   python manage.py migrate
   ```

### 4. Install Required Packages

1. Install the OpenAI Python library and python-dotenv:
   ```
   pip install openai
   pip install requests
   pip install python-dotenv
   ```

### 5. Handle environment variables
2. Create a .env file in your project root:
   ```
   touch path-to-your-project/.env
   ```

3. Add your OpenAI API key to the .env file:
   ```
   nano path-to-your-project/.env
   ```

4. Inside the .env file, add your API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

5. For security, make sure .env is added to your .gitignore file:
   ```
   echo ".env" >> path-to-your-project/.gitignore
   ```

### 6. Create Forms for Prompt Input

1. Create image_generator/forms.py:
   ```python
   from django import forms
   
   class ImagePromptForm(forms.Form):
       prompt = forms.CharField(
           widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the image you want to generate...'}),
           max_length=1000
       )
   ```

### 7. Create Views for the Application

1. Edit image_generator/views.py:
   ```python
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

   # Initialize the OpenAI client with API key from environment variable
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
   ```

### 8. Create URL Patterns

1. Create image_generator/urls.py:
   ```python
   from django.urls import path
   from . import views
   
   urlpatterns = [
       path('', views.home, name='home'),
       path('gallery/', views.gallery, name='gallery'),
   ]
   ```

2. Update my_project/urls.py:
   ```python
   from django.contrib import admin
   from django.urls import path, include
   from django.conf import settings
   from django.conf.urls.static import static
   
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('image_generator.urls')),
   ]
   
   # Add this to serve media files during development
   if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

### 9. Create Templates

1. Create template directories:
   ```
   mkdir -p image_generator/templates/image_generator
   ```

2. Create image_generator/templates/image_generator/base.html:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title>AI Image Generator</title>
       <meta name="viewport" content="width=device-width, initial-scale=1">
       <style>
           body {
               font-family: Arial, sans-serif;
               max-width: 1000px;
               margin: 0 auto;
               padding: 20px;
               line-height: 1.6;
           }
           .header {
               text-align: center;
               margin-bottom: 30px;
           }
           .nav {
               display: flex;
               justify-content: center;
               margin-bottom: 20px;
           }
           .nav a {
               margin: 0 10px;
               text-decoration: none;
               color: #0066cc;
           }
           .gallery {
               display: grid;
               grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
               gap: 20px;
           }
           .image-card {
               border: 1px solid #ddd;
               border-radius: 5px;
               padding: 10px;
               box-shadow: 0 2px 5px rgba(0,0,0,0.1);
           }
           .image-card img {
               width: 100%;
               height: auto;
               border-radius: 3px;
           }
           .prompt {
               font-size: 0.9em;
               color: #555;
               margin-top: 10px;
           }
           .timestamp {
               font-size: 0.8em;
               color: #888;
               text-align: right;
           }
           form {
               max-width: 500px;
               margin: 0 auto;
           }
           textarea, button {
               width: 100%;
               padding: 10px;
               margin-bottom: 15px;
               box-sizing: border-box;
           }
           button {
               background-color: #0066cc;
               color: white;
               border: none;
               cursor: pointer;
               font-size: 1.1em;
               border-radius: 5px;
           }
           button:hover {
               background-color: #0055aa;
           }
       </style>
   </head>
   <body>
       <div class="header">
           <h1>AI Image Generator</h1>
           <p>Create amazing images with artificial intelligence</p>
       </div>
       
       <div class="nav">
           <a href="{% url 'home' %}">Generate</a>
           <a href="{% url 'gallery' %}">Gallery</a>
       </div>
       
       <div class="content">
           {% block content %}{% endblock %}
       </div>
   </body>
   </html>
   ```

3. Create image_generator/templates/image_generator/home.html:
   ```html
   {% extends 'image_generator/base.html' %}
   
   {% block content %}
   <h2>Generate a New Image</h2>
   <form method="post">
       {% csrf_token %}
       <div>
           <label for="{{ form.prompt.id_for_label }}">Describe the image you want:</label>
           {{ form.prompt }}
       </div>
       <button type="submit">Generate Image</button>
   </form>
   
   <div style="margin-top: 30px;">
       <h3>Tips for better results:</h3>
       <ul>
           <li>Be specific about what you want to see</li>
           <li>Include details about style, lighting, and composition</li>
           <li>Try phrases like "digital art", "photorealistic", or "oil painting"</li>
           <li>The more detailed your prompt, the better the results</li>
       </ul>
   </div>
   {% endblock %}
   ```

4. Create image_generator/templates/image_generator/gallery.html:
   ```html
   {% extends 'image_generator/base.html' %}
   
   {% block content %}
   <h2>Image Gallery</h2>
   
   {% if images %}
       <div class="gallery">
           {% for image in images %}
           <div class="image-card">
               <img src="{{ image.image.url }}" alt="Generated image">
               <div class="prompt">"{{ image.prompt }}"</div>
               <div class="timestamp">{{ image.created_at|date:"F j, Y, g:i a" }}</div>
           </div>
           {% endfor %}
       </div>
   {% else %}
       <p>No images have been generated yet. <a href="{% url 'home' %}">Create your first image!</a></p>
   {% endif %}
   {% endblock %}
   ```

5. Create image_generator/templates/image_generator/error.html:
   ```html
   {% extends 'image_generator/base.html' %}
   
   {% block content %}
   <h2>Error</h2>
   <div style="color: red; text-align: center; margin: 30px 0;">
       <p>{{ error }}</p>
       <a href="{% url 'home' %}">Try Again</a>
   </div>
   {% endblock %}
   ```

### 10. Configure Media Files for Nginx

1. Create the media directory:
   ```
   mkdir -p ~/django_project/media/generated_images
   ```

2. Update Nginx configuration to serve media files:
   ```
   sudo nano /etc/nginx/sites-enabled/my_ai_app
   ```

3. Add a location block for media files:
   ```
   server {
       listen 80;
       server_name your_droplet_ip;

       # Add this line to increase the upload limit to 10MB
       client_max_body_size 10M;
       
       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
            alias path-to-your-project/media/;
       }
       
       location /media/ {
            alias path-to-your-project/media/;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

4. Test and reload Nginx:
   ```
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### 11. Run the Django Development Server

1. Make sure you're in the project directory with the virtual environment activated:
   ```
   cd ~/django_project
   source venv/bin/activate
   ```

2. Run the Django development server:
   ```
   python manage.py runserver 0.0.0.0:8000
   ```

3. For running the server in the background (so you can close your SSH session), you can use:
   ```
   nohup python manage.py runserver 0.0.0.0:8000 > django.log 2>&1 &
   ```

### 12. Test the Application

1. Open a web browser and navigate to your Droplet's IP address
2. Enter a text prompt and generate an image
3. Check the gallery to see all generated images

## Expected Outcome
A functional web application that allows users to generate images from text prompts using AI and view a gallery of all created images.

## Troubleshooting

- **API Key Issues**: Verify your OpenAI API key is correct and has billing set up
- **Image Generation Failures**: Check if your prompt violates content policies
- **Media Files Not Displaying**: Ensure Nginx is properly configured to serve media files. 
- **Server Errors**: Check Django development server logs for detailed error messages
- **Server Not Running**: If you can't access the site, make sure the Django development server is running

## Notes

- The OpenAI API is not free, but costs are typically low for testing (a few cents per image)
- Consider implementing user authentication for a production application
- The application stores generated images, so monitor disk space usage
- For a more advanced application, you could add options for image size, style, and more parameters
- Remember that the Django development server is not suitable for production environments
