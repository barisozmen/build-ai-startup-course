from django import forms
   
class ImagePromptForm(forms.Form):
    prompt = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the image you want to generate...'}),
        max_length=1000
    )