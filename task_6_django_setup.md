# Task 6: Django Setup

## Objective
Install and configure Django to create a web application framework for our AI project.

## Prerequisites
- SSH access to your DigitalOcean Droplet
- Nginx web server installed and configured
- Basic understanding of Python and web frameworks


## Before we start
In this step, we will create a Django project in our DigitalOcean Droplet, and then do development there.

For doing remote development, there are multiple options:
- [Recommended] Use a remote development tool like [Cursor](https://www.cursor.com/) or [VS Code Remote Development](https://code.visualstudio.com/docs/remote/remote-overview)
- Develop locally and push code to Github, and then pull to the Droplet
- Develop locally and push code to remote by rsync command
  - `rsync -avz -e "ssh -i ~/.ssh/id_rsa" . root@your_droplet_ip:~/<project address>`
  - [How does `rsync` work?](https://chatgpt.com/share/6826fd39-7220-8010-bf5c-35549c46490d)


## Steps

### 1. Install Python and Required Packages
1. Connect to your Droplet via SSH
2. Update package lists and install Python dependencies:
   ```
   sudo apt update
   sudo apt install python3-pip python3-dev python3-venv -y
   ```

### 2. Create a Virtual Environment
1. Create a directory for your Django project:
   ```
   mkdir -p ~/django_project
   cd ~/django_project
   ```
2. Create a Python virtual environment:
   ```
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

### 3. Install Django
1. With the virtual environment activated, install Django:
   ```
   pip install django gunicorn
   ```
2. Verify Django installation:
   ```
   python -m django --version
   ```

### 4. Create a Django Project
1. Create a new Django project:
   ```
   django-admin startproject my_project .
   ```

You should now see files in a `my_project` directory and `manage.py` file.

Content of `my_project` directory:
- __init__.py
- asgi.py
- settings.py
- urls.py
- wsgi.py


2. Create a basic app within your project:
   ```
   python manage.py startapp ai_app
   ```

You should now see files in a `ai_app` directory.
- __init__.py
- admin.py
- apps.py
- models.py
- tests.py
- views.py


### 5. Configure Django Settings
1. Open the settings file:
   ```
   nano my_project/settings.py
   ```
2. Update the ALLOWED_HOSTS setting to include your Droplet's IP address:
   ```python
   ALLOWED_HOSTS = ['your_droplet_ip', 'localhost', '127.0.0.1']
   ```
3. Add your app to INSTALLED_APPS:
   ```python
   INSTALLED_APPS = [
       # Default apps...
       'ai_app',
   ]
   ```
4. Save and close the file

### 6. Create a Simple View
1. Edit the views.py file in your app:
   ```
   nano ai_app/views.py
   ```
2. Add a simple view:
   ```python
   from django.http import HttpResponse

   def index(request):
       return HttpResponse("<h1>Hello from Django!</h1><p>Your AI application is running with Django, and served by nginx on your droplet!</p>")
   ```

[What is a view in Django?](https://chatgpt.com/share/6826cde3-3a40-8010-b9a8-e84c65c4799e)

3. Create a urls.py file in your app:
   ```
   nano ai_app/urls.py
   ```
4. Add URL patterns:
   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
       path('', views.index, name='index'),
   ]
   ```
[How URL patterns work in Django?](https://chatgpt.com/c/6826ce0f-a37c-8010-b7a0-d38e700fb37c)

   
5. Update the project's urls.py:
   ```
   nano my_project/urls.py
   ```

   
6. Include your app's URLs:
   ```python
   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('ai_app.urls')),
   ]
   ```

### 7. Run Django Development Server

[What is purpose of manage.py in Django?](https://chatgpt.com/share/6826ce96-ab28-8010-a611-a5e081b765a7)


1. Run migrations to set up the database:
   ```
   python manage.py migrate
   ```
2. Start the development server:
   ```
   python manage.py runserver 0.0.0.0:8000
   ```
3. Open a web browser and navigate to `http://your_droplet_ip:8000`
4. You should see your "Hello from Django!" message


### 8. Configure Nginx to Proxy to Django

For development purposes, we'll configure Nginx to proxy requests to Django's built-in development server:

1. Create an Nginx configuration file directly in sites-enabled:
   ```
   sudo nano /etc/nginx/sites-enabled/my_ai_app
   ```

2. Add the following configuration (replace your_droplet_ip with your actual IP):
   ```
   server {
       listen 80;
       server_name your_droplet_ip;

       location = /favicon.ico { 
           access_log off; 
           log_not_found off; 
       }
       
       location /static/ {
           root /root/django_project;
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

3. Test the Nginx configuration:
   ```
   sudo nginx -t
   ```
   If you made syntax errors, this command will show you the errors. This is for confirming that the Nginx configuration is correct.

4. If the test is successful, restart Nginx:
   ```
   sudo systemctl restart nginx
   ```

5. Configure your firewall to allow Nginx:
   ```
   sudo ufw allow 'Nginx Full'
   ```

6. Run the Django development server in the background (you can use a screen or tmux session for this):
   ```
   cd ~/django_project
   source venv/bin/activate
   python manage.py runserver 0.0.0.0:8000
   ```

7. Visit your site at http://your_droplet_ip

> **Note**: This setup is for development only. Django's runserver is not suitable for production environments. For production, you should use a proper WSGI server like Gunicorn. We will do this later!

## Expected Outcome
A functioning Django web application accessible through your browser at your Droplet's IP address.

## Troubleshooting
- **500 Internal Server Error**: Check Gunicorn and Django logs for errors
- **Connection refused**: Ensure Gunicorn is running and the socket file exists
- **Static files not loading**: Verify static file paths and permissions
- **Permission issues**: Check file permissions for the project directory and socket file
- **Nginx not serving Django**: Verify the Nginx configuration and ensure the symbolic link is created correctly

## Notes
- Django provides a robust framework for building web applications
- For production, you should configure proper security settings and a domain name
- Remember to replace 'your_droplet_ip' with your actual Droplet IP address in all configurations
- The Django admin interface is accessible at `http://your_droplet_ip/admin/` after creating a superuser