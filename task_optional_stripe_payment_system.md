# Task: Optional Stripe Payment System for AI Image Generator

## Objective
Add a subscription payment system to your AI Image Generator application using Stripe, allowing users to pay for premium features.

## Prerequisites
- Completed Django setup with AI Image Generator app (Task 7)
- User authentication system (Task 8)
- Basic understanding of payment processing
- Credit/debit card for Stripe account verification

## Steps

### 1. Create a Stripe Account

1. Visit [Stripe's website](https://stripe.com) and sign up for an account
2. Complete the verification process (may require business details and ID verification)
3. Navigate to the Stripe Dashboard
4. Go to Developers > API keys
5. Note your publishable key and secret key (keep the secret key secure!)

### 2. Install Stripe Python Library

1. Connect to your Droplet via SSH
2. Navigate to your Django project and activate the virtual environment:
   ```
   cd ~/django_project
   source venv/bin/activate
   ```
3. Install the Stripe library:
   ```
   pip install stripe
   ```

### 3. Configure Stripe in Django Settings

1. Open your Django settings file:
   ```
   nano my_project/settings.py
   ```
2. Add Stripe configuration at the bottom:
   ```python
   # Stripe Settings
   STRIPE_PUBLISHABLE_KEY = 'your_publishable_key'
   STRIPE_SECRET_KEY = 'your_secret_key'
   STRIPE_PRICE_ID = 'your_price_id'  # You'll create this in the Stripe dashboard
   ```

### 4. Create a Subscription Product in Stripe Dashboard

1. In the Stripe Dashboard, go to Products > Create Product
2. Set up a subscription product:
   - Name: "AI Image Generator Premium"
   - Description: "Advanced image generation features and priority processing"
   - Pricing: Create a recurring price (e.g., $9.99/month)
3. After creating the product, note the Price ID (starts with "price_")
4. Update your Django settings with this Price ID

### 5. Create a Subscription App in Django

1. Create a new Django app for subscriptions:
   ```
   python manage.py startapp subscriptions
   ```
2. Add the app to INSTALLED_APPS in settings.py:
   ```python
   INSTALLED_APPS = [
       # Default apps...
       'image_generator',
       'subscriptions',
   ]
   ```

### 6. Create Subscription Models

1. Edit subscriptions/models.py:
   ```python
   from django.db import models
   from django.contrib.auth.models import User

   class Subscription(models.Model):
       user = models.OneToOneField(User, on_delete=models.CASCADE)
       stripe_customer_id = models.CharField(max_length=100)
       stripe_subscription_id = models.CharField(max_length=100)
       status = models.CharField(max_length=20)
       created_at = models.DateTimeField(auto_now_add=True)
       
       def __str__(self):
           return f"{self.user.username}'s subscription ({self.status})"
   ```

2. Create and apply migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

### 7. Create Subscription Views

1. Edit subscriptions/views.py:
   ```python
   import stripe
   from django.conf import settings
   from django.shortcuts import render, redirect
   from django.contrib.auth.decorators import login_required
   from django.urls import reverse
   from django.http import JsonResponse
   from .models import Subscription

   # Configure Stripe API key
   stripe.api_key = settings.STRIPE_SECRET_KEY

   @login_required
   def subscription_page(request):
       # Check if user already has an active subscription
       try:
           subscription = Subscription.objects.get(user=request.user)
           if subscription.status == 'active':
               return render(request, 'subscriptions/already_subscribed.html')
       except Subscription.DoesNotExist:
           pass
            
       return render(request, 'subscriptions/subscription.html', {
           'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
           'price_id': settings.STRIPE_PRICE_ID,
       })

   @login_required
   def create_checkout_session(request):
       # Create a checkout session for the subscription
       try:
           # Get or create a Stripe customer
           customer = get_or_create_customer(request.user)
           
           checkout_session = stripe.checkout.Session.create(
               customer=customer.id,
               payment_method_types=['card'],
               line_items=[{
                   'price': settings.STRIPE_PRICE_ID,
                   'quantity': 1,
               }],
               mode='subscription',
               success_url=request.build_absolute_uri(reverse('subscription_success')),
               cancel_url=request.build_absolute_uri(reverse('subscription_cancel')),
           )
           
           return JsonResponse({'id': checkout_session.id})
       except Exception as e:
           return JsonResponse({'error': str(e)}, status=400)

   def get_or_create_customer(user):
       # Check if user already has a Stripe customer ID
       try:
           subscription = Subscription.objects.get(user=user)
           return stripe.Customer.retrieve(subscription.stripe_customer_id)
       except Subscription.DoesNotExist:
           # Create a new customer
           customer = stripe.Customer.create(
               email=user.email,
               name=f"{user.first_name} {user.last_name}" if user.first_name else user.username
           )
           return customer

   @login_required
   def subscription_success(request):
       return render(request, 'subscriptions/success.html')

   @login_required
   def subscription_cancel(request):
       return render(request, 'subscriptions/cancel.html')

   @login_required
   def webhook(request):
       # Handle Stripe webhook events
       payload = request.body
       sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
       
       try:
           event = stripe.Webhook.construct_event(
               payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
           )
           
           # Handle the event
           if event['type'] == 'checkout.session.completed':
               session = event['data']['object']
               handle_checkout_session(session)
           elif event['type'] == 'customer.subscription.updated':
               subscription = event['data']['object']
               handle_subscription_updated(subscription)
           elif event['type'] == 'customer.subscription.deleted':
               subscription = event['data']['object']
               handle_subscription_deleted(subscription)
               
           return JsonResponse({'status': 'success'})
       except Exception as e:
           return JsonResponse({'error': str(e)}, status=400)

   def handle_checkout_session(session):
       # Process the completed checkout session
       customer_id = session.get('customer')
       subscription_id = session.get('subscription')
       
       if customer_id and subscription_id:
           # Get the user from the customer ID
           try:
               subscription = Subscription.objects.get(stripe_customer_id=customer_id)
               user = subscription.user
           except Subscription.DoesNotExist:
               # This is a new subscription
               # You would need to map the customer ID to a user
               # This is simplified and would need more logic in a real app
               return
               
           # Update subscription details
           subscription.stripe_subscription_id = subscription_id
           subscription.status = 'active'
           subscription.save()

   def handle_subscription_updated(stripe_subscription):
       # Update subscription status
       try:
           subscription = Subscription.objects.get(
               stripe_subscription_id=stripe_subscription.get('id')
           )
           subscription.status = stripe_subscription.get('status')
           subscription.save()
       except Subscription.DoesNotExist:
           pass

   def handle_subscription_deleted(stripe_subscription):
       # Handle cancelled subscription
       try:
           subscription = Subscription.objects.get(
               stripe_subscription_id=stripe_subscription.get('id')
           )
           subscription.status = 'cancelled'
           subscription.save()
       except Subscription.DoesNotExist:
           pass

   @login_required
   def subscription_management(request):
       try:
           subscription = Subscription.objects.get(user=request.user)
           portal_session = stripe.billing_portal.Session.create(
               customer=subscription.stripe_customer_id,
               return_url=request.build_absolute_uri(reverse('profile')),
           )
           return redirect(portal_session.url)
       except Subscription.DoesNotExist:
           return redirect('subscribe')
   ```

### 8. Create URL Patterns for Subscription

1. Create subscriptions/urls.py:
   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
       path('subscribe/', views.subscription_page, name='subscribe'),
       path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
       path('success/', views.subscription_success, name='subscription_success'),
       path('cancel/', views.subscription_cancel, name='subscription_cancel'),
       path('webhook/', views.webhook, name='stripe_webhook'),
       path('manage/', views.subscription_management, name='manage_subscription'),
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
       path('', include('image_generator.urls')),
       path('subscription/', include('subscriptions.urls')),
   ]

   # Add this to serve media files during development
   if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

### 9. Create Templates for Subscription Pages

1. Create template directories:
   ```
   mkdir -p subscriptions/templates/subscriptions
   ```

2. Create subscriptions/templates/subscriptions/subscription.html:
   ```html
   {% extends 'image_generator/base.html' %}

   {% block content %}
   <h2>Upgrade to Premium</h2>
   <div class="subscription-container">
       <div class="subscription-card">
           <h3>AI Image Generator Premium</h3>
           <p class="price">$9.99/month</p>
           <ul>
               <li>Generate higher resolution images (1024x1024)</li>
               <li>Access to DALL-E 3 for better quality</li>
               <li>Priority processing</li>
               <li>Generate up to 100 images per day</li>
               <li>Save private image history</li>
           </ul>
           <button id="checkout-button">Subscribe Now</button>
       </div>
   </div>

   <script src="https://js.stripe.com/v3/"></script>
   <script>
       const stripe = Stripe('{{ stripe_publishable_key }}');
       const checkoutButton = document.getElementById('checkout-button');
       
       checkoutButton.addEventListener('click', function() {
           // Create a checkout session when the button is clicked
           fetch('/subscription/create-checkout-session/', {
               method: 'POST',
               headers: {
                   'Content-Type': 'application/json',
                   'X-CSRFToken': '{{ csrf_token }}'
               },
           })
           .then(function(response) {
               return response.json();
           })
           .then(function(session) {
               if (session.error) {
                   alert(session.error);
                   return;
               }
               // Redirect to Stripe Checkout
               return stripe.redirectToCheckout({ sessionId: session.id });
           })
           .then(function(result) {
               if (result.error) {
                   alert(result.error.message);
               }
           })
           .catch(function(error) {
               console.error('Error:', error);
           });
       });
   </script>
   {% endblock %}
   ```

3. Create subscriptions/templates/subscriptions/success.html:
   ```html
   {% extends 'image_generator/base.html' %}

   {% block content %}
   <div class="success-container">
       <h2>Subscription Successful!</h2>
       <p>Thank you for subscribing to AI Image Generator Premium!</p>
       <p>You now have access to all premium features:</p>
       <ul>
           <li>Higher resolution images (1024x1024)</li>
           <li>Access to DALL-E 3 for better quality</li>
           <li>Priority processing</li>
           <li>Generate up to 100 images per day</li>
           <li>Save private image history</li>
       </ul>
       <a href="{% url 'home' %}" class="button">Start Generating Images</a>
   </div>
   {% endblock %}
   ```

4. Create subscriptions/templates/subscriptions/cancel.html:
   ```html
   {% extends 'image_generator/base.html' %}

   {% block content %}
   <div class="cancel-container">
       <h2>Subscription Cancelled</h2>
       <p>You have cancelled the subscription process.</p>
       <p>You can subscribe anytime to access premium features.</p>
       <a href="{% url 'home' %}" class="button">Return to Home</a>
   </div>
   {% endblock %}
   ```

5. Create subscriptions/templates/subscriptions/already_subscribed.html:
   ```html
   {% extends 'image_generator/base.html' %}

   {% block content %}
   <div class="success-container">
       <h2>You're Already a Premium Member!</h2>
       <p>You already have an active subscription to AI Image Generator Premium.</p>
       <p>You're enjoying all premium features:</p>
       <ul>
           <li>Higher resolution images (1024x1024)</li>
           <li>Access to DALL-E 3 for better quality</li>
           <li>Priority processing</li>
           <li>Generate up to 100 images per day</li>
           <li>Save private image history</li>
       </ul>
       <a href="{% url 'manage_subscription' %}" class="button">Manage Subscription</a>
       <a href="{% url 'home' %}" class="button secondary">Continue Generating Images</a>
   </div>
   {% endblock %}
   ```

### 10. Add CSS for Subscription Pages

1. Add the following CSS to your base.html or create a separate CSS file:
   ```css
   .subscription-container {
       display: flex;
       justify-content: center;
       margin: 30px 0;
   }
   
   .subscription-card {
       border: 1px solid #ddd;
       border-radius: 8px;
       padding: 20px;
       width: 300px;
       text-align: center;
       box-shadow: 0 4px 8px rgba(0,0,0,0.1);
   }
   
   .subscription-card h3 {
       color: #0066cc;
       margin-bottom: 10px;
   }
   
   .price {
       font-size: 24px;
       font-weight: bold;
       margin: 15px 0;
   }
   
   .subscription-card ul {
       text-align: left;
       margin: 20px 0;
       padding-left: 20px;
   }
   
   .subscription-card li {
       margin-bottom: 8px;
   }
   
   #checkout-button {
       background-color: #0066cc;
       color: white;
       border: none;
       padding: 10px 20px;
       border-radius: 4px;
       cursor: pointer;
       font-size: 16px;
   }
   
   #checkout-button:hover {
       background-color: #0055aa;
   }
   
   .success-container, .cancel-container {
       text-align: center;
       margin: 50px auto;
       max-width: 500px;
   }
   
   .success-container ul {
       text-align: left;
       display: inline-block;
       margin: 20px auto;
   }
   
   .button {
       display: inline-block;
       background-color: #0066cc;
       color: white;
       padding: 10px 20px;
       text-decoration: none;
       border-radius: 4px;
       margin-top: 20px;
   }
   
   .button.secondary {
       background-color: #666;
       margin-left: 10px;
   }
   
   .button:hover {
       background-color: #0055aa;
   }
   ```

### 11. Add Subscription Link to Navigation

1. Update the navigation in image_generator/templates/image_generator/base.html:
   ```html
   <div class="nav">
       <a href="{% url 'home' %}">Generate</a>
       <a href="{% url 'gallery' %}">Gallery</a>
       {% if user.is_authenticated %}
           <a href="{% url 'profile' %}">My Profile</a>
           <a href="{% url 'subscribe' %}">Premium</a>
       {% endif %}
   </div>
   ```

### 12. Update User Profile to Show Subscription Status

1. Modify image_generator/templates/image_generator/profile.html to include subscription status:
   ```html
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
           
           <!-- Add subscription status -->
           {% if subscription and subscription.status == 'active' %}
               <p class="subscription-status premium">
                   <span class="badge">Premium</span> 
                   You are a premium member
                   <a href="{% url 'manage_subscription' %}" class="small-button">Manage</a>
               </p>
           {% else %}
               <p class="subscription-status">
                   <span class="badge basic">Basic</span> 
                   Free account
                   <a href="{% url 'subscribe' %}" class="small-button">Upgrade</a>
               </p>
           {% endif %}
       </div>
   </div>
   ```

2. Add CSS styles for subscription status:
   ```css
   .subscription-status {
       margin-top: 10px;
       padding: 8px 12px;
       background-color: #f8f9fa;
       border-radius: 4px;
   }
   
   .subscription-status.premium {
       background-color: #fff4de;
   }
   
   .badge {
       display: inline-block;
       padding: 3px 8px;
       border-radius: 4px;
       font-size: 0.8em;
       background-color: #6c757d;
       color: white;
       margin-right: 10px;
   }
   
   .badge.premium {
       background-color: #ffc107;
       color: #212529;
   }
   
   .badge.basic {
       background-color: #6c757d;
   }
   
   .small-button {
       font-size: 0.8em;
       padding: 2px 8px;
       background-color: #0066cc;
       color: white;
       text-decoration: none;
       border-radius: 3px;
       margin-left: 10px;
   }
   ```

### 13. Update Profile View to Pass Subscription Status

1. Modify the profile view in image_generator/views.py:
   ```python
   @login_required
   def profile(request):
       # Get or create user profile
       profile, created = UserProfile.objects.get_or_create(user=request.user)
       
       # Get subscription status
       subscription = None
       try:
           from subscriptions.models import Subscription
           subscription = Subscription.objects.get(user=request.user)
       except:
           pass
           
       return render(request, 'image_generator/profile.html', {
           'subscription': subscription
       })
   ```

### 14. Modify Image Generation to Use Premium Features for Subscribers

1. Update the generate_image function in image_generator/views.py:
   ```python
   def generate_image(prompt, user, is_public=True):
       # Check if user has premium subscription
       is_premium = False
       try:
           from subscriptions.models import Subscription
           subscription = Subscription.objects.get(user=user)
           is_premium = subscription.status == 'active'
       except:
           pass
           
       # Call OpenAI API to generate an image
       try:
           # Use better model and higher resolution for premium users
           model = "dall-e-3" if is_premium else "dall-e-2"
           size = "1024x1024" if is_premium else "512x512"
           
           response = client.images.generate(
               model=model,
               prompt=prompt,
               n=1,
               size=size
           )
           
           # Get the image URL from the response format
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
   ```

### 15. Create Utility Function to Check Subscription Status

1. Create a new file subscriptions/utils.py:
   ```python
   from .models import Subscription

   def is_premium_user(user):
       """Check if a user has an active premium subscription"""
       if not user or not user.is_authenticated:
           return False
           
       try:
           subscription = Subscription.objects.get(user=user)
           return subscription.status == 'active'
       except Subscription.DoesNotExist:
           return False
   ```

2. You can then import and use this function across your application:
   ```python
   from subscriptions.utils import is_premium_user
   
   # Example usage
   if is_premium_user(request.user):
       # Enable premium features
   ```

### 16. Set Up Stripe Webhook

1. In the Stripe Dashboard, go to Developers > Webhooks
2. Add an endpoint with your server URL:
   ```
   http://your_droplet_ip/subscription/webhook/
   ```
3. Select events to listen for:
   - checkout.session.completed
   - customer.subscription.updated
   - customer.subscription.deleted
4. After creating the webhook, note the Signing Secret
5. Add the webhook secret to your Django settings:
   ```python
   STRIPE_WEBHOOK_SECRET = 'your_webhook_signing_secret'
   ```

### 17. Restart Gunicorn to Apply Changes

1. Restart the Gunicorn service:
   ```
   sudo systemctl restart gunicorn
   ```

## Expected Outcome
A functional subscription payment system integrated with your AI image generation application, allowing users to pay for premium features such as higher resolution images, better quality models, and increased generation limits.

## Troubleshooting

- **Stripe API Key Issues**: Verify your API keys are correct and properly configured
- **Webhook Errors**: Check that your webhook URL is accessible and the signing secret is correct
- **Payment Processing Failures**: Review Stripe Dashboard logs for detailed error messages
- **CSRF Token Issues**: Ensure your forms include the CSRF token for POST requests
- **Authentication Problems**: Verify that login is working correctly for subscription pages

## Notes

- This implementation uses Stripe Checkout, which is the simplest way to implement payments
- For production use, consider implementing additional security measures
- Stripe provides test card numbers for testing without using real cards (e.g., 4242 4242 4242 4242)
- Remember to switch from test mode to live mode in Stripe when going to production
- Consider implementing email notifications for subscription events
- For a more advanced implementation, you could add different subscription tiers or one-time payments
