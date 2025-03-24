import re
from typing import Union, Any

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from PIL import Image

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
                               validators=[validate_username], required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                             validators=[validate_email], required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                               validators=[validate_password], required=True)
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
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), )
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
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Avatar'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Birth date'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
        }

    def clean_avatar(self) -> Union[str, None]:
        """
        Validate image size
        :return:
        """
        image = self.cleaned_data.get('avatar')
        if image:
            img = Image.open(image)
            max_size = 2 * 1024 * 1024  # 2MB
            if img.width > max_size:
                raise forms.ValidationError(f"Image size must be less than {max_size} MB.")
        return image


class EditUserForm(forms.ModelForm):
    """
    Edit user form
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
                               required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                             required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_username(self):
        """
        Validate username
        :return:
        """
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).count():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_email(self):
        """
        Validate email
        :return:
        """
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).count():
            raise forms.ValidationError('Email already exists')
        return email


class ChangePasswordForm(forms.ModelForm):
    """
    Form for changing user password
    """
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'}), required=True)
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}), required=True)
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        required=True)

    class Meta:
        model = User

        fields = ['password']

    def __init__(self, user: AbstractBaseUser, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_password(self) -> str:
        """
        Checks that the password is correct.
        :return:
        """
        password = self.cleaned_data.get('password')
        user = authenticate(username=self.user.username, password=password)
        if not user:
            raise forms.ValidationError('Incorrect password')
        return password

    def clean_new_password(self) -> str:
        """
        Validate changing password
        :return:
        """
        cleaned_data = super().clean()
        current_password = cleaned_data.get("password")
        new_password = cleaned_data.get("new_password")
        validate_password(new_password)
        if current_password == new_password:
            raise forms.ValidationError("New password must be different.")
        return new_password

    def clean_password_confirm(self) -> str:
        """
        Checks that the password is correct.
        :return:
        """
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        password_confirmed = cleaned_data.get("password_confirm")
        validate_password_confirmation(new_password, password_confirmed)
        return password_confirmed
