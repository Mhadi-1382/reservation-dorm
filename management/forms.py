from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class PasswordChangeForm(forms.Form):
    username = forms.CharField(max_length=255)
    new_password = forms.CharField(widget=forms.PasswordInput())
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("کاربری با این نام وجود ندارد.")
        return username
