from django.db import models
   
class GeneratedImage(models.Model):
    prompt = models.TextField()
    image = models.ImageField(upload_to='generated_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image from: {self.prompt[:50]}"