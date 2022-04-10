from .models import Comment
from django import forms


# form for comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)