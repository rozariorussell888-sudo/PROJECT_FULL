from django import forms
from .models import ResourceItem, ResourceReview

class ResourceItemForm(forms.ModelForm):
    class Meta:
        model = ResourceItem
        fields = ['title', 'category', 'description', 'author', 'department', 'course_code', 'share_type', 'price', 'file', 'image']
        widgets = {'description': forms.Textarea(attrs={'rows': 5})}

    def clean(self):
        data = super().clean()
        if data.get('category') != 'equipment' and data.get('share_type') != 'share':
            self.add_error('share_type', 'Only equipment can be rented or sold.')
        if data.get('share_type') in ('rent','sell') and (data.get('price') is None or data['price'] <= 0):
            self.add_error('price', 'A positive price is required for rent or sale.')
        if data.get('share_type') == 'share':
            data['price'] = None
        return data

class ResourceReviewForm(forms.ModelForm):
    class Meta:
        model = ResourceReview
        fields = ['rating', 'comment']
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if not 1 <= rating <= 5:
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return rating
