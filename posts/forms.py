from django import forms
from .models import Post, Comment
from captcha.fields import CaptchaField

class PostForm(forms.ModelForm):
    """Форма для создания поста с капчей."""
    captcha = CaptchaField()

    class Meta:
        model = Post
        fields = ['text', 'captcha']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Введите текст поста...',
                'rows': 5,
                'help_text': 'Текст поста. Поддерживаются теги: b, i, u, a.'
            })
        }

class CommentForm(forms.ModelForm):
    """Форма для добавления комментария."""
    class Meta:
        model = Comment
        fields = ['text', 'parent']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Введите текст комментария...',
                'rows': 3,
                'help_text': 'Текст комментария.'
            })
        }
