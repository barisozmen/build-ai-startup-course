# Task 6: Ghibli Style Image Conversion App

## Objective
Create a Django web application that allows users to upload images and convert them to Studio Ghibli art style using an AI API.

## Prerequisites
- Completed Task 5: Django Setup
- SSH access to your DigitalOcean Droplet
- Basic understanding of Django and web applications
- API key for an image style transfer service

## Steps

### 1. Choose an API for Ghibli Style Transfer

Several AI services offer style transfer capabilities. For this project, we'll use the DeepAI Style Transfer API which supports Ghibli-style transformations:

1. Visit [DeepAI](https://deepai.org/) and create an account
2. Get your API key from the dashboard
3. Review the [Style Transfer API documentation](https://deepai.org/machine-learning-model/fast-style-transfer)

### 2. Update Django Project Structure

1. Connect to your Droplet via SSH
2. Navigate to your Django project:
   ```
   cd ~/django_project
   source venv/bin/activate
   ```

3. Create a new app for the image converter:
   ```
   python manage.py startapp ghibli_converter
   ```

4. Add the new app to INSTALLED_APPS in settings.py:
   ```python
   INSTALLED_APPS = [
       # Default apps...
       'core',
       'ghibli_converter',
   ]
   ```

5. Configure media settings in settings.py:
   ```python
   import os
   
   # Add to the bottom of the file
   MEDIA_URL = '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
   ```

### 3. Create Models for Image Storage

1. Edit ghibli_converter/models.py:
   ```python
   from django.db import models
   
   class OriginalImage(models.Model):
       title = models.CharField(max_length=200)
       image = models.ImageField(upload_to='original/')
       uploaded_at = models.DateTimeField(auto_now_add=True)
       
       def __str__(self):
           return self.title
   
   class GhibliImage(models.Model):
       original = models.ForeignKey(OriginalImage, on_delete=models.CASCADE, related_name='ghibli_versions')
       image = models.ImageField(upload_to='ghibli/')
       created_at = models.DateTimeField(auto_now_add=True)
       
       def __str__(self):
           return f"Ghibli version of {self.original.title}"
   ```

2. Create and apply migrations:
   ```
   pip install pillow  # Required for ImageField
   python manage.py makemigrations
   python manage.py migrate
   ```

### 4. Create Forms for Image Upload

1. Create ghibli_converter/forms.py:
   ```python
   from django import forms
   from .models import OriginalImage
   
   class ImageUploadForm(forms.ModelForm):
       class Meta:
           model = OriginalImage
           fields = ['title', 'image']
   ```

### 5. Create Views for the Application

1. Edit ghibli_converter/views.py:
   ```python
   import os
   import requests
   from django.shortcuts import render, redirect
   from django.conf import settings
   from django.core.files.base import ContentFile
   from .forms import ImageUploadForm
   from .models import OriginalImage, GhibliImage
   
   # Replace with your actual API key
   DEEPAI_API_KEY = "your-deepai-api-key"
   
   def home(request):
       if request.method == 'POST':
           form = ImageUploadForm(request.POST, request.FILES)
           if form.is_valid():
               original_image = form.save()
               
               # Call the DeepAI API to convert the image
               try:
                   ghibli_image = convert_to_ghibli(original_image)
                   return redirect('result', image_id=original_image.id)
               except Exception as e:
                   # Handle API errors
                   original_image.delete()
                   return render(request, 'ghibli_converter/error.html', {'error': str(e)})
       else:
           form = ImageUploadForm()
       
       return render(request, 'ghibli_converter/home.html', {'form': form})
   
   def convert_to_ghibli(original_image):
       # API call to DeepAI
       r = requests.post(
           "https://api.deepai.org/api/fast-style-transfer",
           files={
               'content': open(original_image.image.path, 'rb'),
               'style': 'ghibli',  # Use 'ghibli' as the style
           },
           headers={'api-key': DEEPAI_API_KEY}
       )
       
       response = r.json()
       
       if 'output_url' in response:
           # Download the converted image
           image_response = requests.get(response['output_url'])
           
           # Create a new GhibliImage instance
           ghibli_image = GhibliImage(original=original_image)
           ghibli_image.image.save(
               f"ghibli_{os.path.basename(original_image.image.name)}",
               ContentFile(image_response.content)
           )
           ghibli_image.save()
           
           return ghibli_image
       else:
           raise Exception("API Error: " + str(response))
   
   def result(request, image_id):
       try:
           original_image = OriginalImage.objects.get(id=image_id)
           ghibli_image = original_image.ghibli_versions.first()
           return render(request, 'ghibli_converter/result.html', {
               'original_image': original_image,
               'ghibli_image': ghibli_image
           })
       except OriginalImage.DoesNotExist:
           return redirect('home')
   
   def gallery(request):
       images = GhibliImage.objects.all().order_by('-created_at')
       return render(request, 'ghibli_converter/gallery.html', {'images': images})
   ```

### 6. Create URL Patterns

1. Create ghibli_converter/urls.py:
   ```python
   from django.urls import path
   from . import views
   
   urlpatterns = [
       path('', views.home, name='home'),
       path('result/<int:image_id>/', views.result, name='result'),
       path('gallery/', views.gallery, name='gallery'),
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
   ]
   
   # Add this to serve media files during development
   if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

### 7. Create Templates

1. Create template directories:
   ```
   mkdir -p ghibli_converter/templates/ghibli_converter
   ```

2. Create ghibli_converter/templates/ghibli_converter/base.html:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title>Ghibli Style Image Converter</title>
       <meta name="viewport" content="width=device-width, initial-scale=1">
       <style>
           body {
               font-family: Arial, sans-serif;
               max-width: 800px;
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
           .image-container {
               display: flex;
               flex-wrap: wrap;
               justify-content: space-around;
           }
           .image-card {
               margin: 10px;
               padding: 10px;
               border: 1px solid #ddd;
               border-radius: 5px;
               max-width: 300px;
           }
           .image-card img {
               max-width: 100%;
               height: auto;
           }
           form {
               max-width: 500px;
               margin: 0 auto;
           }
           input, button {
               margin: 10px 0;
               padding: 8px;
               width: 100%;
           }
           button {
               background-color: #0066cc;
               color: white;
               border: none;
               cursor: pointer;
           }
       </style>
   </head>
   <body>
       <div class="header">
           <h1>Ghibli Style Image Converter</h1>
           <p>Transform your photos into Studio Ghibli art style</p>
       </div>
       
       <div class="nav">
           <a href="{% url 'home' %}">Home</a>
           <a href="{% url 'gallery' %}">Gallery</a>
       </div>
       
       <div class="content">
           {% block content %}{% endblock %}
       </div>
   </body>
   </html>
   ```

3. Create ghibli_converter/templates/ghibli_converter/home.html:
   ```html
   {% extends 'ghibli_converter/base.html' %}
   
   {% block content %}
   <h2>Upload an Image</h2>
   <form method="post" enctype="multipart/form-data">
       {% csrf_token %}
       <div>
           <label for="{{ form.title.id_for_label }}">Title:</label>
           {{ form.title }}
       </div>
       <div>
           <label for="{{ form.image.id_for_label }}">Image:</label>
           {{ form.image }}
       </div>
       <button type="submit">Convert to Ghibli Style</button>
   </form>
   {% endblock %}
   ```

4. Create ghibli_converter/templates/ghibli_converter/result.html:
   ```html
   {% extends 'ghibli_converter/base.html' %}
   
   {% block content %}
   <h2>Conversion Result</h2>
   
   <div class="image-container">
       <div class="image-card">
           <h3>Original Image</h3>
           <img src="{{ original_image.image.url }}" alt="{{ original_image.title }}">
           <p>{{ original_image.title }}</p>
       </div>
       
       <div class="image-card">
           <h3>Ghibli Style</h3>
           <img src="{{ ghibli_image.image.url }}" alt="Ghibli version">
           <p>Created at: {{ ghibli_image.created_at }}</p>
       </div>
   </div>
   
   <div style="text-align: center; margin-top: 20px;">
       <a href="{% url 'home' %}">Convert Another Image</a>
   </div>
   {% endblock %}
   ```

5. Create ghibli_converter/templates/ghibli_converter/gallery.html:
   ```html
   {% extends 'ghibli_converter/base.html' %}
   
   {% block content %}
   <h2>Gallery of Converted Images</h2>
   
   {% if images %}
       <div class="image-container">
           {% for ghibli_image in images %}
           <div class="image-card">
               <img src="{{ ghibli_image.image.url }}" alt="Ghibli style image">
               <p>{{ ghibli_image.original.title }}</p>
               <p>Created: {{ ghibli_image.created_at }}</p>
           </div>
           {% endfor %}
       </div>
   {% else %}
       <p>No images have been converted yet.</p>
   {% endif %}
   {% endblock %}
   ```

6. Create ghibli_converter/templates/ghibli_converter/error.html:
   ```html
   {% extends 'ghibli_converter/base.html' %}
   
   {% block content %}
   <h2>Error</h2>
   <div style="color: red; text-align: center;">
       <p>{{ error }}</p>
       <a href="{% url 'home' %}">Try Again</a>
   </div>
   {% endblock %}
   ```

### 8. Configure Media Files for Nginx

1. Create the media directory:
   ```
   mkdir -p ~/django_project/media/original ~/django_project/media/ghibli
   ```

2. Update Nginx configuration to serve media files:
   ```
   sudo nano /etc/nginx/sites-available/ai-app
   ```

3. Add a location block for media files:
   ```
   server {
       listen 80;
       server_name your_droplet_ip;
       
       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
           root /root/django_project;
       }
       
       location /media/ {
           root /root/django_project;
       }
       
       location / {
           include proxy_params;
           proxy_pass http://unix:/root/django_project/ai_app.sock;
       }
   }
   ```

4. Test and reload Nginx:
   ```
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### 9. Restart Gunicorn to Apply Changes

1. Restart the Gunicorn service:
   ```
   sudo systemctl restart gunicorn
   ```

### 10. Test the Application

1. Open a web browser and navigate to your Droplet's IP address
2. Upload an image and test the conversion functionality
3. Check the gallery to see all converted images

## Expected Outcome
A functional web application that allows users to upload images and convert them to Studio Ghibli art style using AI.

## Troubleshooting

- **API Key Issues**: Verify your DeepAI API key is correct and has sufficient credits
- **Image Upload Errors**: Check file permissions on the media directories
- **Conversion Failures**: Review API response for error messages
- **Media Files Not Displaying**: Ensure Nginx is properly configured to serve media files
- **Server Errors**: Check Gunicorn and Django logs for detailed error messages:
  ```
  sudo journalctl -u gunicorn
  ```

## Notes

- The DeepAI API offers a free tier with limited requests, which is sufficient for testing
- For production use, consider implementing rate limiting or user authentication
- The application stores both original and converted images, so monitor disk space usage
- Consider implementing image size validation to prevent large uploads
- For a more advanced application, you could add multiple style options beyond just Ghibli
