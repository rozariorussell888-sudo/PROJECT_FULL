from django import forms
from django.core.validators import RegexValidator
from .models import Student

class LoginForm(forms.Form):
    registration_id = forms.CharField(max_length=50, strip=True)
    password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(forms.ModelForm):
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Student
        fields = ['full_name', 'registration_id', 'department', 'email', 'phone']
    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('confirm_password'):
            self.add_error('confirm_password', 'Passwords do not match.')
        return data

class OTPForm(forms.Form):
    otp = forms.CharField(min_length=6, max_length=6, validators=[RegexValidator(r'^\d{6}$','Enter the six-digit OTP.')])

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

class ResetPasswordForm(forms.Form):
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('confirm_password'):
            self.add_error('confirm_password', 'Passwords do not match.')
        return data
