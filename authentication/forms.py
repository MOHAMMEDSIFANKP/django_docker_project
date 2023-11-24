from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from .models import *
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name','last_name','username')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [ 'bio', 'profile_image', 'qrcode']
        