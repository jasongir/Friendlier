from django import forms
from main.models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'picture']
        widgets = {
            'description': forms.Textarea(
                attrs= {
                    'cols': 65,
                    'rows': 4,
                    'placeholder': '(optional)',
                }
            )
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'message', ]
        widgets = {
            'text': forms.Textarea(attrs={
                    'cols': 65,
                    'rows': 3,
                    'placeholder': '(optional)',
                }
            )
        }
        

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

