import re
from typing import Union, Any

from django import forms
from django.contrib.auth.models import User

from main.models import UserProfile


def validate_password(password: str) -> None:
    """
    Check password format.
    :param password:
    :return:
    """
    if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\d])(?=.*[@#$%&_]).{8,}$', password) is None:
        raise forms.ValidationError('Password must contain symbols: a-z, A-Z, 0-9, @#$%&_')


def validate_password_confirmation(password: str, password_confirmed: str) -> None:
    """
    Check password confirmation.
    :param password:
    :param password_confirmed:
    :return:
    """
    if password and password_confirmed and password != password_confirmed:
        raise forms.ValidationError("Passwords do not match.")


def validate_username(username: str) -> None:
    """
    Check if name is already taken
    :param username:
    :return:
    """
    existed_usernames = User.objects.filter(username=username)
    if existed_usernames.count():
        raise forms.ValidationError('Username already exists')


def validate_email(email: str) -> None:
    """
    Check if email is already taken
    :return:
    """
    existed_emails = User.objects.filter(email=email)
    if existed_emails.count():
        raise forms.ValidationError('Email already exists')


class RegisterForm(forms.ModelForm):
    """
    Form for registering a new user
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
                               validators=[validate_username])
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                             validators=[validate_email])
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                               validators=[validate_password])
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_password2(self) -> Union[dict[str, Any] | None]:
        """
        Checks that the password is correct.
        :return:
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmed = cleaned_data.get("password2")
        validate_password_confirmation(password, password_confirmed)
        return cleaned_data


class LoginForm(forms.Form):
    """
    Form for login a user
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                               validators=[validate_password])


class UserProfileForm(forms.ModelForm):
    """
    Form for user profile
    """
    class Meta:
        model = UserProfile
        fields = ('bio', 'avatar', 'birth_date', 'location')

        widgets = {
            'bio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bio'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Avatar'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Birth date'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
        }


class EditUserForm(forms.ModelForm):
    """
    Edit user form
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
                               validators=[validate_username])
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                             validators=[validate_email])

    class Meta:
        model = User
        fields = ('username', 'email')
