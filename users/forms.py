from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re
from tasks.forms import StyledFormMixing
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for field_name in ['first_name', 'last_name', 'username',
                           'email', 'password1', 'password2']:
            self.fields[field_name].help_text = None


class CustomRegistrationForm(StyledFormMixing, forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise forms.ValidationError("Email already exist!")

        return email

    # field error
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []

        if len(password1) < 8:
            errors.append(
                "Password must be at least 8 character long")

        if not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=])', password1):
            errors.append(
                "Password must include uppercase, lowercase, number and special character")

        if errors:
            raise forms.ValidationError(errors)

        return password1

    # non-field error
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')

        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError("Password do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        
        user.set_password(self.cleaned_data.get('password1'))

        if commit:
            user.save()

        return user


class LoginForm(StyledFormMixing, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)