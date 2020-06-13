from django import forms
from  django.contrib.auth.models import User
from .models import UserProfile

#userprofile
class UserUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['dob', 'bio','city','image']





