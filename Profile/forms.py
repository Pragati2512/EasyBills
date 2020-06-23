from django.contrib.auth.models import User
from .models import Profile, group, group_Member
from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2" , )

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('number',)

class GroupForm(forms.ModelForm):
    class Meta:
        model = group
        fields = ('name', 'type','adm_settings')

class GroupMemberForm(forms.ModelForm):
    class Meta:
        model = group_Member
        fields = ('group' , 'member')
