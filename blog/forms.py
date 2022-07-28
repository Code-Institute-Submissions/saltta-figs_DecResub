from django_summernote.widgets import SummernoteWidget
from django import forms
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from .models import Comment, Recipe



# form for comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('author', 'title', 'featured_image', 'content', 'ingredients', 'steps')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'ingredients':  SummernoteWidget(),
            'steps':  SummernoteWidget(),
            'author': forms.HiddenInput(),
        }