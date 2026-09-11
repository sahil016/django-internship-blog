from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        weidgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter title'}),
            'content': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Write your content here...'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }