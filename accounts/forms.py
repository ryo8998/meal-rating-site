from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from django import forms

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username','email')
        widgets={
            'username':forms.TextInput(attrs={'placeholder':'Username','class':'form-control'}),
            'email':forms.TextInput(attrs={'placeholder':'Email','class':'form-control'})
        }
        