# Task 5: Django Setup

## Objective
Install and configure Django to create a web application framework for our AI project.

## Prerequisites
- SSH access to your DigitalOcean Droplet
- Nginx web server installed and configured
- Basic understanding of Python and web frameworks

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
   django-admin startproject ai_app .
   ```
2. Create a basic app within your project:
   ```
   python manage.py startapp core
   ```

### 5. Configure Django Settings
1. Open the settings file:
   ```
   nano ai_app/settings.py
   ```
2. Update the ALLOWED_HOSTS setting to include your Droplet's IP address:
   ```python
   ALLOWED_HOSTS = ['your_droplet_ip', 'localhost', '127.0.0.1']
   ```
3. Add your app to INSTALLED_APPS:
   ```python
   INSTALLED_APPS = [
       # Default apps...
       'core',
   ]
   ```
4. Save and close the file

### 6. Create a Simple View
1. Edit the views.py file in your app:
   ```
   nano core/views.py
   ```
2. Add a simple view:
   ```python
   from django.http import HttpResponse

   def index(request):
       return HttpResponse("<h1>Hello from Django!</h1><p>Your AI application is running with Django.</p>")
   ```
3. Create a urls.py file in your app:
   ```
   nano core/urls.py
   ```
4. Add URL patterns:
   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
       path('', views.index, name='index'),
   ]
   ```
5. Update the project's urls.py:
   ```
   nano ai_app/urls.py
   ```
6. Include your app's URLs:
   ```python
   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('core.urls')),
   ]
   ```

### 7. Run Django Development Server
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

### 8. Configure Gunicorn
1. Test Gunicorn with your Django project:
   ```
   gunicorn --bind 0.0.0.0:8000 ai_app.wsgi
   ```
2. Create a systemd service file for Gunicorn:
   ```
   sudo nano /etc/systemd/system/gunicorn.service
   ```
3. Add the following configuration:
   ```
   [Unit]
   Description=gunicorn daemon
   After=network.target

   [Service]
   User=root
   Group=www-data
   WorkingDirectory=/root/django_project
   ExecStart=/root/django_project/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/root/django_project/ai_app.sock ai_app.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```
4. Start and enable the Gunicorn service:
   ```
   sudo systemctl start gunicorn
   sudo systemctl enable gunicorn
   ```

### 9. Configure Nginx to Proxy to Django
1. Update your Nginx configuration:
   ```
   sudo nano /etc/nginx/sites-available/ai-app
   ```
2. Modify the configuration to proxy to Gunicorn:
   ```
   server {
       listen 80;
       server_name your_droplet_ip;

       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
           root /root/django_project;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/root/django_project/ai_app.sock;
       }
   }
   ```
3. Create the proxy_params file if it doesn't exist:
   ```
   sudo nano /etc/nginx/proxy_params
   ```
4. Add the following content:
   ```
   proxy_set_header Host $http_host;
   proxy_set_header X-Real-IP $remote_addr;
   proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
   proxy_set_header X-Forwarded-Proto $scheme;
   ```
5. Enable the site by creating a symbolic link:
   ```
   sudo ln -s /etc/nginx/sites-available/ai-app /etc/nginx/sites-enabled/
   ```
6. Test Nginx configuration:
   ```
   sudo nginx -t
   ```
7. Reload Nginx:
   ```
   sudo systemctl reload nginx
   ```

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
- This setup uses Gunicorn as the WSGI server and Nginx as a reverse proxy
- For production, you should configure proper security settings and a domain name
- Remember to replace 'your_droplet_ip' with your actual Droplet IP address in all configurations
- The Django admin interface is accessible at `http://your_droplet_ip/admin/` after creating a superuser
