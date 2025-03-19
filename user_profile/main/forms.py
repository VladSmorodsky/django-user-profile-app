import re
from typing import Union, Any

from django import forms


def validate_password(value: str) -> None:
    """
    Validate a password format.
    :param value:
    :return:
    """
    if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\d])(?=.*[@#$%&_]).{8,}$', value) is None:
        raise forms.ValidationError('Password must contain symbols: a-z, A-Z, 0-9, @#$%&_')


class RegistrationForm(forms.Form):
    """
    Form for registering a new user
    """
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                               validators=[validate_password])
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}), validators=[validate_password])

    def clean_password(self) -> Union[dict[str, Any] | None]:
        """
        Checks that the password is correct.
        :return:
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data
