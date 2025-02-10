from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password']

    password = forms.CharField(widget=forms.PasswordInput())

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
