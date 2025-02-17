from django import forms
from .models import UserAccount


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return password


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
