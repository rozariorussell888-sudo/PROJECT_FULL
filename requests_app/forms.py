from django import forms
from .models import ResourceRequest, ProductRequest

class ResourceRequestForm(forms.ModelForm):
    class Meta:
        model = ResourceRequest
        fields = ['title', 'category', 'course_code', 'description']
        widgets = {'description': forms.Textarea(attrs={'rows': 5})}

class ProductRequestForm(forms.ModelForm):
    class Meta:
        model = ProductRequest
        fields = ['message']
        widgets = {'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add a message (optional)'})}
