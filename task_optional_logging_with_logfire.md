# Task: Optional Logging with Logfire

## Objective
Set up structured logging for your Django application using Logfire, a modern logging platform that provides powerful visualization and analysis tools for your application logs.

## Prerequisites
- Completed Task 5: Django Setup
- SSH access to your DigitalOcean Droplet
- Basic understanding of Python logging

## Steps

### 1. Install Logfire Python Package

1. Connect to your Droplet via SSH
2. Navigate to your Django project and activate the virtual environment:
   ```
   cd ~/django_project
   source venv/bin/activate
   ```
3. Install the Logfire Python package:
   ```
   pip install logfire
   ```

### 2. Create a Logfire Account and Project

1. Visit [Logfire Dashboard](https://logfire.pydantic.dev/) and create an account
2. Create a new project for your Django application
3. After creating the project, you'll receive a project token - save this for later use

### 3. Configure Environment Variables

1. Create or update your `.env` file to store the Logfire token:
   ```
   nano ~/django_project/.env
   ```
2. Add your Logfire token to the file:
   ```
   LOGFIRE_TOKEN=your_logfire_project_token
   ```
3. Install python-dotenv to load environment variables:
   ```
   pip install python-dotenv
   ```

### 4. Configure Django Settings for Logfire

1. Open your Django settings file:
   ```
   nano ~/django_project/ai_app/settings.py
   ```
2. Add the following imports at the top:
   ```python
   import os
   import logfire
   from dotenv import load_dotenv
   
   # Load environment variables
   load_dotenv()
   ```
3. Initialize Logfire in your settings file:
   ```python
   # Logfire configuration
   LOGFIRE_TOKEN = os.getenv('LOGFIRE_TOKEN')
   if LOGFIRE_TOKEN:
       logfire.init(token=LOGFIRE_TOKEN, service_name="django-ai-app")
   ```
4. Configure Django's logging to use Logfire:
   ```python
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'formatters': {
           'verbose': {
               'format': '{levelname} {asctime} {module} {message}',
               'style': '{',
           },
       },
       'handlers': {
           'console': {
               'level': 'INFO',
               'class': 'logging.StreamHandler',
               'formatter': 'verbose',
           },
           'logfire': {
               'level': 'INFO',
               'class': 'logfire.integrations.django.LogfireHandler',
           },
       },
       'loggers': {
           'django': {
               'handlers': ['console', 'logfire'],
               'level': 'INFO',
               'propagate': True,
           },
           'ghibli_converter': {
               'handlers': ['console', 'logfire'],
               'level': 'INFO',
               'propagate': True,
           },
           # Add other app loggers as needed
       },
   }
   ```

### 5. Create a Middleware for Request Logging

1. Create a new file for the logging middleware:
   ```
   nano ~/django_project/ai_app/middleware.py
   ```
2. Add the following code to the file:
   ```python
   import time
   import logging
   import logfire

   logger = logging.getLogger(__name__)

   class LogfireMiddleware:
       def __init__(self, get_response):
           self.get_response = get_response

       def __call__(self, request):
           start_time = time.time()
           
           # Process the request
           response = self.get_response(request)
           
           # Log request details
           duration = time.time() - start_time
           status_code = response.status_code
           
           logfire.info(
               "Request processed",
               method=request.method,
               path=request.path,
               status_code=status_code,
               duration_ms=round(duration * 1000, 2),
               user_id=request.user.id if request.user.is_authenticated else None,
               user_agent=request.META.get('HTTP_USER_AGENT', ''),
               ip_address=self.get_client_ip(request),
           )
           
           return response
       
       def get_client_ip(self, request):
           x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
           if x_forwarded_for:
               ip = x_forwarded_for.split(',')[0]
           else:
               ip = request.META.get('REMOTE_ADDR')
           return ip
   ```

3. Add the middleware to your Django settings:
   ```python
   MIDDLEWARE = [
       # Existing middleware...
       'ai_app.middleware.LogfireMiddleware',
   ]
   ```

### 6. Add Structured Logging to Your Views

1. Update your views to use structured logging. For example, in `ghibli_converter/views.py`:
   ```python
   import logging
   import logfire
   
   logger = logging.getLogger(__name__)
   
   def home(request):
       logger.info("Home page accessed")
       # Existing view code...
   
   def convert_to_ghibli(original_image):
       try:
           # Existing conversion code...
           logfire.info(
               "Image converted to Ghibli style",
               image_id=original_image.id,
               image_title=original_image.title,
               image_size=original_image.image.size,
           )
           return ghibli_image
       except Exception as e:
           logfire.error(
               "Failed to convert image",
               image_id=original_image.id,
               image_title=original_image.title,
               error=str(e),
               exception=e,
           )
           raise
   ```

### 7. Add Context to User Authentication Events

1. Update the user authentication views to include structured logging. For example, in `users/views.py`:
   ```python
   import logging
   import logfire
   
   logger = logging.getLogger(__name__)
   
   def register(request):
       if request.method == 'POST':
           form = UserRegisterForm(request.POST)
           if form.is_valid():
               user = form.save()
               username = form.cleaned_data.get('username')
               logfire.info(
                   "User registered",
                   username=username,
                   email=user.email,
               )
               messages.success(request, f'Account created for {username}! You can now log in.')
               return redirect('login')
       # Rest of the view...
   
   @login_required
   def profile(request):
       logfire.info(
           "User accessed profile page",
           user_id=request.user.id,
           username=request.user.username,
       )
       # Rest of the view...
   ```

### 8. Track API Calls with Logfire

If you're using external APIs (like the image conversion API), add structured logging:

```python
def call_external_api(data):
    try:
        start_time = time.time()
        response = requests.post(API_URL, data=data, headers=headers)
        duration = time.time() - start_time
        
        logfire.info(
            "External API call",
            api="DeepAI Style Transfer",
            status_code=response.status_code,
            duration_ms=round(duration * 1000, 2),
            success=response.status_code == 200,
        )
        
        return response.json()
    except Exception as e:
        logfire.error(
            "External API call failed",
            api="DeepAI Style Transfer",
            error=str(e),
            exception=e,
        )
        raise
```

### 9. Add Performance Monitoring

1. Create a decorator for monitoring function performance:
   ```python
   import time
   import functools
   import logfire
   
   def monitor_performance(func):
       @functools.wraps(func)
       def wrapper(*args, **kwargs):
           start_time = time.time()
           result = func(*args, **kwargs)
           duration = time.time() - start_time
           
           logfire.info(
               "Function performance",
               function=func.__name__,
               module=func.__module__,
               duration_ms=round(duration * 1000, 2),
           )
           
           return result
       return wrapper
   ```

2. Use the decorator on performance-critical functions:
   ```python
   @monitor_performance
   def convert_to_ghibli(original_image):
       # Existing code...
   ```

### 10. Restart Gunicorn to Apply Changes

1. Restart the Gunicorn service:
   ```
   sudo systemctl restart gunicorn
   ```

## Expected Outcome
Your Django application will now send structured logs to Logfire, allowing you to monitor application performance, track user behavior, and quickly identify and debug issues through the Logfire dashboard.

## Troubleshooting

- **No logs appearing in Logfire**: Verify your token is correct and that the application has internet access
- **Missing context in logs**: Ensure you're using structured logging with named parameters
- **Performance issues**: If logging is causing performance problems, adjust the log levels to reduce volume
- **Rate limiting**: Be mindful of log volume if you're on a free tier with limits

## Tips for Effective Logging

1. **Use structured logging**: Always include context as named parameters rather than string interpolation:
   ```python
   # Good
   logfire.info("User action", user_id=user.id, action="download")
   
   # Avoid
   logger.info(f"User {user.id} performed download action")
   ```

2. **Choose appropriate log levels**:
   - `DEBUG`: Detailed information, typically useful only for diagnosing problems
   - `INFO`: Confirmation that things are working as expected
   - `WARNING`: Indication that something unexpected happened, but the application is still working
   - `ERROR`: Due to a more serious problem, the application has not been able to perform a function
   - `CRITICAL`: A serious error indicating that the program itself may be unable to continue running

3. **Add request IDs**: Generate a unique ID for each request to trace it through your system:
   ```python
   import uuid
   
   class RequestIDMiddleware:
       def __init__(self, get_response):
           self.get_response = get_response
           
       def __call__(self, request):
           request.id = str(uuid.uuid4())
           response = self.get_response(request)
           return response
   ```

4. **Log exceptions with context**:
   ```python
   try:
       # Some code that might fail
   except Exception as e:
       logfire.exception(
           "Operation failed",
           operation="image_conversion",
           input_data=input_data,
           # The exception parameter automatically includes the traceback
           exception=e,
       )
   ```

5. **Create custom dimensions** for important business metrics:
   ```python
   logfire.info(
       "Image processed",
       image_type="ghibli",
       processing_time_ms=processing_time,
       image_size_kb=image_size / 1024,
       premium_user=user.is_premium,
   )
   ```

6. **Set up alerts** in the Logfire dashboard for critical errors or performance thresholds

7. **Use sampling** for high-volume events to reduce costs while maintaining visibility

8. **Add environment tags** to distinguish between development, staging, and production logs:
   ```python
   logfire.init(
       token=LOGFIRE_TOKEN,
       service_name="django-ai-app",
       environment=os.getenv("DJANGO_ENV", "development")
   )
   ```

By implementing these logging practices, you'll gain valuable insights into your application's behavior, making it easier to monitor performance, troubleshoot issues, and understand user patterns.
