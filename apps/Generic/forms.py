from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, Field
from django.utils.translation import ugettext_lazy as _
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

from .models import GeneralSettings


# Modification of the access form
class AccessForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)  #v2 captcha
    password = forms.CharField(label=_("Password"), min_length=6,
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Password'}))


# Modification of the user creation form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    default_hours = forms.IntegerField(required=False, help_text='Default working hours.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2','default_hours')


# Report a bug
class BugForm(forms.Form):
    # Constructor
    def __init__(self, *args, **kwargs):
        super(BugForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['disabled'] = True

    user = forms.ModelChoiceField(queryset=User.objects.all())
    description = forms.CharField(max_length=1000, required=True, widget=forms.Textarea(attrs={'rows': 6, 'placeholder': 'Description of the bug'}))


# Password reset email
class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label="Email or Username", max_length=254)


# Password reset
class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label="New password",
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="New password confirmation",
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2

class ChooseTheme(forms.Form):
    theme_value = forms.IntegerField(label="Integer")

    def save_theme(self,user):
        value=self.cleaned_data.get('theme_value')
        if GeneralSettings.objects.filter(user=user,parameter="theme").count()!=0:
            row = GeneralSettings.objects.filter(user=user, parameter="theme").first()
            row.value = value
            row.save()
        else:
            new_row = GeneralSettings(user=user,parameter ="theme",value=value)
            new_row.save()

        return value
