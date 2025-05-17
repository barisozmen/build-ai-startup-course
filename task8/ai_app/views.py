from django.shortcuts import render


from django.http import HttpResponse
    
def index(request):
    return HttpResponse("<h1>Hello from Django!</h1><p>Your AI application is running with Django, and served by nginx on your droplet!</p>")