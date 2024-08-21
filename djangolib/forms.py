from django import forms
from django.contrib.auth.models import User

from .models import FavouriteBook

class FavouriteBookForm(forms.ModelForm):
    class Meta:
        model = FavouriteBook
        fields = ['book']