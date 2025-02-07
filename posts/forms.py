from django import forms
from .models import Post, Comment
from captcha.fields import CaptchaField

class PostForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Post
        fields = ['text', 'captcha']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'parent']
