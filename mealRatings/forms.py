from django.forms import ModelForm, widgets
from .models import Meal, MealRating
from django import forms

class MealForm(ModelForm):
    class Meta:
        # choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'),('Evening', 'Evening')]
        model = Meal
        fields = ["name","description","imageUrl","typicalMealTime","countryOfOrigin"]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Meal name here'}),
            'imageUrl': forms.TextInput(attrs={'placeholder': 'Image URL here'}),
            'countryOfOrigin': forms.TextInput(attrs={'placeholder': 'Country'}),
            'typicalMealTime':forms.Select(attrs={'placeholder': 'Pick up meal time from options'}),
            'description':forms.Textarea(attrs={'rows':7})
        }


class MealRatingForm(forms.Form):
    rating = forms.DecimalField(widget=forms.NumberInput(attrs={'type': 'range',"min": 0,"max": 5,"step":0.1,"id":"rating","class":"w-100 mx-2"}))
    # class Meta:
    #     model = MealRating
    #     fields = ["meal","rating"]
    #     widgets = {
    #         "meal":forms.HiddenInput(),
    #         "rating":forms.TextInput(attrs={'type': 'range',"min": "0","max": "5","step":"0.1","id":"rating","class":"w-100 mx-2"})
    #     }