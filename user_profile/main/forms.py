import re
from typing import Union, Any

from django import forms
from django.contrib.auth.models import User

from main.models import UserProfile


def validate_password(password: str) -> None:
    if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\d])(?=.*[@#$%&_]).{8,}$', password) is None:
        raise forms.ValidationError('Password must contain symbols: a-z, A-Z, 0-9, @#$%&_')


class RegistrationForm(forms.ModelForm):
    """
    Form for registering a new user
    """
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                               validators=[validate_password])
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

    def clean_name(self) -> str:
        """
        Check if name is already taken
        :return:
        """
        name = self.cleaned_data['name']
        existed_usernames = User.objects.filter(username=name)

        if existed_usernames.count():
            raise forms.ValidationError('Username already exists')
        return name

    def clean_email(self) -> str:
        """
        Check if email is already taken
        :return:
        """
        email = self.cleaned_data['email']
        existed_emails = User.objects.filter(email=email)
        if existed_emails.count():
            raise forms.ValidationError('Email already exists')
        return email

    def clean(self) -> Union[dict[str, Any] | None]:
        """
        Checks that the password is correct.
        :return:
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmed = cleaned_data.get("password2")
        if password and password_confirmed and password != password_confirmed:
            self.add_error("password2", "Passwords do not match.")
        return cleaned_data
