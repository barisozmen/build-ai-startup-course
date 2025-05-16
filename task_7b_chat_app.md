# Task 7B: Chat Application with OpenAI API

## Objective
Create a chat application that integrates with OpenAI's API to provide intelligent responses to user queries. This feature will complement our existing Ghibli Style Image Conversion app by adding conversational AI capabilities.

## Prerequisites
- Completed Task 5: Django Setup
- Completed Task 6: Ghibli Style Image Conversion App
- SSH access to your DigitalOcean Droplet
- OpenAI API key (sign up at [OpenAI](https://openai.com/api/))
- Basic understanding of Django and APIs

## Steps

### 1. Set Up OpenAI API Access

1. Visit [OpenAI](https://openai.com/api/) and create an account
2. Generate an API key from your dashboard
3. Connect to your Droplet via SSH:
   ```
   ssh root@your_droplet_ip
   ```
4. Navigate to your Django project:
   ```
   cd ~/django_project
   source venv/bin/activate
   ```
5. Install the OpenAI Python library:
   ```
   pip install openai
   ```

### 2. Create a Chat App in Django

1. Create a new Django app for the chat functionality:
   ```
   python manage.py startapp chat
   ```

2. Add the new app to INSTALLED_APPS in settings.py:
   ```python
   INSTALLED_APPS = [
       # Default apps...
       'core',
       'ghibli_converter',
       'users',  # If you completed Task 7
       'chat',
   ]
   ```

3. Configure OpenAI API key in settings.py:
   ```python
   # OpenAI API Settings
   OPENAI_API_KEY = 'your-openai-api-key'
   ```

### 3. Create Models for Chat History

1. Edit chat/models.py:
   ```python
   from django.db import models
   from django.contrib.auth.models import User

   class Conversation(models.Model):
       user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
       title = models.CharField(max_length=255, default="New Conversation")
       created_at = models.DateTimeField(auto_now_add=True)
       
       def __str__(self):
           return f"{self.title} - {self.user.username}"

   class Message(models.Model):
       ROLE_CHOICES = [
           ('user', 'User'),
           ('assistant', 'Assistant'),
       ]
       
       conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
       role = models.CharField(max_length=10, choices=ROLE_CHOICES)
       content = models.TextField()
       timestamp = models.DateTimeField(auto_now_add=True)
       
       def __str__(self):
           return f"{self.role}: {self.content[:30]}..."
       
       class Meta:
           ordering = ['timestamp']
   ```

2. Create and apply migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

### 4. Create Views for Chat Interface

1. Edit chat/views.py:
   ```python
   import json
   import openai
   from django.shortcuts import render, redirect, get_object_or_404
   from django.http import JsonResponse
   from django.contrib.auth.decorators import login_required
   from django.conf import settings
   from .models import Conversation, Message

   # Configure OpenAI API key
   openai.api_key = settings.OPENAI_API_KEY

   @login_required
   def chat_home(request):
       conversations = Conversation.objects.filter(user=request.user).order_by('-created_at')
       return render(request, 'chat/home.html', {'conversations': conversations})

   @login_required
   def new_conversation(request):
       conversation = Conversation.objects.create(user=request.user)
       return redirect('conversation', conversation_id=conversation.id)

   @login_required
   def conversation(request, conversation_id):
       conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
       messages = conversation.messages.all()
       
       return render(request, 'chat/conversation.html', {
           'conversation': conversation,
           'messages': messages,
       })

   @login_required
   def send_message(request, conversation_id):
       if request.method == 'POST':
           conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
           data = json.loads(request.body)
           user_message = data.get('message', '').strip()
           
           if user_message:
               # Save user message
               Message.objects.create(
                   conversation=conversation,
                   role='user',
                   content=user_message
               )
               
               # Get conversation history for context
               messages_history = []
               for msg in conversation.messages.all():
                   messages_history.append({"role": msg.role, "content": msg.content})
               
               # If this is the first message, update the conversation title
               if conversation.messages.count() == 1:
                   try:
                       conversation.title = user_message[:30] + "..." if len(user_message) > 30 else user_message
                       conversation.save()
                   except Exception as e:
                       print(f"Error updating conversation title: {e}")
               
               try:
                   # Call OpenAI API
                   response = openai.ChatCompletion.create(
                       model="gpt-3.5-turbo",
                       messages=messages_history,
                       max_tokens=500,
                       temperature=0.7,
                   )
                   
                   # Extract and save assistant's response
                   assistant_message = response.choices[0].message.content
                   Message.objects.create(
                       conversation=conversation,
                       role='assistant',
                       content=assistant_message
                   )
                   
                   return JsonResponse({
                       'status': 'success',
                       'message': assistant_message
                   })
               except Exception as e:
                   return JsonResponse({
                       'status': 'error',
                       'message': str(e)
                   }, status=500)
           
           return JsonResponse({
               'status': 'error',
               'message': 'Empty message'
           }, status=400)
       
       return JsonResponse({
           'status': 'error',
           'message': 'Invalid request method'
       }, status=405)

   @login_required
   def delete_conversation(request, conversation_id):
       conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
       conversation.delete()
       return redirect('chat_home')
   ```

### 5. Create URL Patterns for Chat App

1. Create chat/urls.py:
   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
       path('', views.chat_home, name='chat_home'),
       path('new/', views.new_conversation, name='new_conversation'),
       path('<int:conversation_id>/', views.conversation, name='conversation'),
       path('<int:conversation_id>/send/', views.send_message, name='send_message'),
       path('<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
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
       path('users/', include('users.urls')),  # If you completed Task 7
       path('chat/', include('chat.urls')),
   ]

   if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

### 6. Create Templates for Chat Interface

1. Create template directories:
   ```
   mkdir -p chat/templates/chat
   ```

2. Create chat/templates/chat/home.html:
   ```html
   {% extends "ghibli_converter/base.html" %}

   {% block content %}
   <div class="chat-container">
       <h2>Your Conversations</h2>
       
       <div class="chat-actions">
           <a href="{% url 'new_conversation' %}" class="button">New Conversation</a>
       </div>
       
       <div class="conversation-list">
           {% if conversations %}
               {% for conversation in conversations %}
                   <div class="conversation-item">
                       <a href="{% url 'conversation' conversation.id %}">{{ conversation.title }}</a>
                       <span class="conversation-date">{{ conversation.created_at|date:"M d, Y" }}</span>
                       <a href="{% url 'delete_conversation' conversation.id %}" class="delete-btn" 
                          onclick="return confirm('Are you sure you want to delete this conversation?')">Delete</a>
                   </div>
               {% endfor %}
           {% else %}
               <p>No conversations yet. Start a new one!</p>
           {% endif %}
       </div>
   </div>
   {% endblock %}
   ```

3. Create chat/templates/chat/conversation.html:
   ```html
   {% extends "ghibli_converter/base.html" %}

   {% block content %}
   <div class="chat-container">
       <div class="chat-header">
           <h2>{{ conversation.title }}</h2>
           <a href="{% url 'chat_home' %}" class="button">Back to Conversations</a>
       </div>
       
       <div class="chat-messages" id="chat-messages">
           {% for message in messages %}
               <div class="message {% if message.role == 'user' %}user-message{% else %}assistant-message{% endif %}">
                   <div class="message-content">{{ message.content|linebreaks }}</div>
                   <div class="message-timestamp">{{ message.timestamp|date:"H:i" }}</div>
               </div>
           {% endfor %}
       </div>
       
       <div class="chat-input">
           <textarea id="user-input" placeholder="Type your message here..."></textarea>
           <button id="send-button">Send</button>
       </div>
   </div>

   <script>
       document.addEventListener('DOMContentLoaded', function() {
           const messagesContainer = document.getElementById('chat-messages');
           const userInput = document.getElementById('user-input');
           const sendButton = document.getElementById('send-button');
           
           // Scroll to bottom of messages
           function scrollToBottom() {
               messagesContainer.scrollTop = messagesContainer.scrollHeight;
           }
           
           // Initial scroll to bottom
           scrollToBottom();
           
           // Send message function
           function sendMessage() {
               const message = userInput.value.trim();
               if (!message) return;
               
               // Disable input while processing
               userInput.disabled = true;
               sendButton.disabled = true;
               
               // Add user message to UI
               const userMessageDiv = document.createElement('div');
               userMessageDiv.className = 'message user-message';
               userMessageDiv.innerHTML = `
                   <div class="message-content">${message.replace(/\n/g, '<br>')}</div>
                   <div class="message-timestamp">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
               `;
               messagesContainer.appendChild(userMessageDiv);
               scrollToBottom();
               
               // Clear input
               userInput.value = '';
               
               // Send to server
               fetch('{% url "send_message" conversation.id %}', {
                   method: 'POST',
                   headers: {
                       'Content-Type': 'application/json',
                       'X-CSRFToken': '{{ csrf_token }}'
                   },
                   body: JSON.stringify({ message: message })
               })
               .then(response => response.json())
               .then(data => {
                   if (data.status === 'success') {
                       // Add assistant response to UI
                       const assistantMessageDiv = document.createElement('div');
                       assistantMessageDiv.className = 'message assistant-message';
                       assistantMessageDiv.innerHTML = `
                           <div class="message-content">${data.message.replace(/\n/g, '<br>')}</div>
                           <div class="message-timestamp">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
                       `;
                       messagesContainer.appendChild(assistantMessageDiv);
                       scrollToBottom();
                   } else {
                       alert('Error: ' + data.message);
                   }
               })
               .catch(error => {
                   console.error('Error:', error);
                   alert('An error occurred while sending your message.');
               })
               .finally(() => {
                   // Re-enable input
                   userInput.disabled = false;
                   sendButton.disabled = false;
                   userInput.focus();
               });
           }
           
           // Event listeners
           sendButton.addEventListener('click', sendMessage);
           
           userInput.addEventListener('keydown', function(e) {
               if (e.key === 'Enter' && !e.shiftKey) {
                   e.preventDefault();
                   sendMessage();
               }
           });
           
           // Focus input on load
           userInput.focus();
       });
   </script>
   {% endblock %}
   ```

### 7. Add CSS for Chat Interface

1. Update the CSS in your base template (ghibli_converter/templates/ghibli_converter/base.html) by adding these styles:
   ```css
   /* Chat Styles */
   .chat-container {
       max-width: 800px;
       margin: 0 auto;
       padding: 20px;
   }
   
   .chat-header {
       display: flex;
       justify-content: space-between;
       align-items: center;
       margin-bottom: 20px;
   }
   
   .chat-actions {
       margin: 20px 0;
   }
   
   .conversation-list {
       margin-top: 20px;
   }
   
   .conversation-item {
       padding: 10px;
       border-bottom: 1px solid #eee;
       display: flex;
       justify-content: space-between;
       align-items: center;
   }
   
   .conversation-item a {
       text-decoration: none;
       color: #0066cc;
       flex-grow: 1;
   }
   
   .conversation-date {
       color: #666;
       font-size: 0.8em;
       margin: 0 10px;
   }
   
   .delete-btn {
       color: #cc0000;
       font-size: 0.8em;
       cursor: pointer;
   }
   
   .chat-messages {
       height: 400px;
       overflow-y: auto;
       border: 1px solid #ddd;
       border-radius: 5px;
       padding: 10px;
       margin-bottom: 20px;
       background-color: #f9f9f9;
   }
   
   .message {
       margin-bottom: 15px;
       padding: 10px;
       border-radius: 10px;
       max-width: 80%;
   }
   
   .user-message {
       background-color: #dcf8c6;
       margin-left: auto;
   }
   
   .assistant-message {
       background-color: #fff;
       border: 1px solid #ddd;
       margin-right: auto;
   }
   
   .message-content {
       margin-bottom: 5px;
   }
   
   .message-timestamp {
       font-size: 0.7em;
       color: #888;
       text-align: right;
   }
   
   .chat-input {
       display: flex;
       margin-top: 10px;
   }
   
   .chat-input textarea {
       flex-grow: 1;
       padding: 10px;
       border: 1px solid #ddd;
       border-radius: 5px;
       resize: none;
       height: 60px;
   }
   
   .chat-input button {
       padding: 10px 20px;
       background-color: #0066cc;
       color: white;
       border: none;
       border-radius: 5px;
       margin-left: 10px;
       cursor: pointer;
   }
   
   .chat-input button:hover {
       background-color: #0055aa;
   }
   ```

### 8. Update Navigation Menu

1. Update the navigation in your base template (ghibli_converter/templates/ghibli_converter/base.html):
   ```html
   <div class="nav">
       <a href="{% url 'home' %}">Home</a>
       <a href="{% url 'gallery' %}">Gallery</a>
       <a href="{% url 'chat_home' %}">Chat</a>
       {% if user.is_authenticated %}
           <a href="{% url 'profile' %}">Profile</a>
           <a href="{% url 'logout' %}">Logout</a>
       {% else %}
           <a href="{% url 'login' %}">Login</a>
           <a href="{% url 'register' %}">Register</a>
       {% endif %}
   </div>
   ```

### 9. Register Models in Admin

1. Edit chat/admin.py:
   ```python
   from django.contrib import admin
   from .models import Conversation, Message

   class MessageInline(admin.TabularInline):
       model = Message
       extra = 0

   class ConversationAdmin(admin.ModelAdmin):
       list_display = ('title', 'user', 'created_at')
       list_filter = ('user', 'created_at')
       search_fields = ('title', 'user__username')
       inlines = [MessageInline]

   admin.site.register(Conversation, ConversationAdmin)
   admin.site.register(Message)
   ```

### 10. Restart Gunicorn to Apply Changes

1. Restart the Gunicorn service:
   ```
   sudo systemctl restart gunicorn
   ```

## Expected Outcome
A functional chat application integrated with OpenAI's API that allows users to have intelligent conversations. The chat system will maintain conversation history and provide contextual responses based on the conversation flow.

## Troubleshooting

- **API Key Issues**: Verify your OpenAI API key is correct and has sufficient credits
- **Rate Limiting**: OpenAI has rate limits; implement error handling for when limits are reached
- **Long Response Times**: OpenAI API can sometimes be slow; consider adding loading indicators
- **Context Length Errors**: OpenAI has token limits; implement logic to truncate very long conversations
- **Server Errors**: Check Gunicorn and Django logs for detailed error messages:
  ```
  sudo journalctl -u gunicorn
  ```

## Notes

- The OpenAI API is a paid service with a free tier for initial testing
- Consider implementing rate limiting to prevent excessive API usage
- For production use, store the API key securely using environment variables
- The chat application can be extended with features like:
  - Different AI models selection
  - Conversation summarization
  - Export conversations to PDF/text
  - Integration with the Ghibli image converter (e.g., "Generate an image based on this description")
- Consider implementing a system prompt to give the AI assistant specific instructions about your application
