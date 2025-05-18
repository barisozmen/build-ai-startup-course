# Task Optional: Email Notification System

## Overview
In this optional task, we'll implement an email notification system that sends users an email each time they generate an image. The notification will include details about the generated image, such as the prompt used and a link to view it. This feature enhances user engagement and provides a useful record of their generated content.

## Objectives
- Configure Django for sending emails
- Create an email notification function
- Integrate the notification system with our image generation process
- Test the email functionality

## Step 1: Configure Django Email Settings

First, we need to configure Django's email settings in `settings.py`:

```python:imagegeneration/settings.py
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Or your email service provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'  # Your email address
EMAIL_HOST_PASSWORD = 'your_app_password'  # App password for Gmail
DEFAULT_FROM_EMAIL = 'Image Generator <your_email@gmail.com>'
```

> **Note:** For Gmail, you'll need to create an "App Password" in your Google Account security settings, as Gmail no longer supports direct password authentication for third-party apps.

For development/testing purposes, you can use Django's console email backend:

```python:imagegeneration/settings.py
# For development - emails will be printed to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Step 2: Create an Email Notification Function

Create a new file for email utilities:

```python:generator/utils/email_utils.py
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_image_generation_notification(user, image_obj):
    """
    Send an email notification to user about their generated image
    
    Args:
        user: User object who generated the image
        image_obj: GeneratedImage object with image details
    """
    if not user.email:
        return False  # Skip if user has no email
        
    # Set email subject
    subject = 'Your AI Image Has Been Generated!'
    
    # Context for email template
    context = {
        'user': user,
        'prompt': image_obj.prompt,
        'created_at': image_obj.created_at,
        'image_url': image_obj.get_absolute_url(),
    }
    
    # Render email content from template
    html_message = render_to_string('emails/image_notification.html', context)
    plain_message = strip_tags(html_message)
    
    # Send email
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )
    
    return True
```

## Step 3: Create Email Template

Create a directory structure for email templates:

```
mkdir -p generator/templates/emails
```

Then create the HTML template for the email notification:

```html:generator/templates/emails/image_notification.html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #4a6ee0; color: white; padding: 15px; text-align: center; }
        .content { padding: 20px; background-color: #f9f9f9; }
        .footer { font-size: 12px; text-align: center; margin-top: 30px; color: #999; }
        .btn { display: inline-block; background-color: #4a6ee0; color: white; padding: 10px 20px; 
               text-decoration: none; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Your AI Image is Ready!</h1>
        </div>
        <div class="content">
            <p>Hello {{ user.username }},</p>
            <p>We're excited to let you know that your AI image has been successfully generated!</p>
            
            <h3>Image Details:</h3>
            <p><strong>Prompt:</strong> {{ prompt }}</p>
            <p><strong>Created:</strong> {{ created_at }}</p>
            
            <p style="text-align: center; margin: 30px 0;">
                <a href="{{ image_url }}" class="btn">View Your Image</a>
            </p>
            
            <p>Thank you for using our AI Image Generator!</p>
        </div>
        <div class="footer">
            <p>This is an automated notification. Please do not reply to this email.</p>
        </div>
    </div>
</body>
</html>
```

## Step 4: Integrate with Image Generation Process

Now, update the view where images are generated to send email notifications:

```python: image_generator/views.py:
   def home(request):
       if request.method == 'POST':
           form = ImagePromptForm(request.POST)
           if form.is_valid():
               prompt = form.cleaned_data['prompt']
               
               # Generate image using OpenAI API
               try:
                    generated_image = generate_image(prompt)

                    send_image_generation_notification(request.user, generated_image)

                   return redirect('gallery')
               except Exception as e:
                   return render(request, 'image_generator/error.html', {'error': str(e)})
       else:
           form = ImagePromptForm()
       
       return render(request, 'image_generator/home.html', {'form': form})
```

## Step 5: Add URL Method to GeneratedImage Model

Ensure your `GeneratedImage` model has a method to get the absolute URL for the image:

```python:generator/models.py
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class GeneratedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()
    image = models.ImageField(upload_to='generated_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Add this method
    def get_absolute_url(self):
        """Returns the full URL to view this image"""
        return reverse('view_image', kwargs={'image_id': self.id})
```

## Step 6: Test Email Functionality

To test your email notification system:

1. Configure your email settings in `settings.py` (use console backend during testing)
2. Generate an image as a logged-in user
3. Check the console output (if using console backend) or your inbox to see the email

## Step 7: Environment Variable Configuration (Optional but Recommended)

For security, it's best to store email credentials as environment variables:

```python:imagegeneration/settings.py
import os

# Email Configuration
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'Image Generator <noreply@example.com>')
```

Then set these in your environment or `.env` file.

## Troubleshooting

If emails aren't being sent:

1. Check email settings in `settings.py`
2. Verify the user has a valid email address in their profile
3. If using Gmail, ensure you're using an App Password, not your regular account password
4. Check your spam folder
5. Look for any error messages in the Django console

## Conclusion

You've successfully implemented an email notification system for your image generation application. This feature keeps users informed about their content creation activities and improves the overall user experience by providing convenient access to their generated images.
