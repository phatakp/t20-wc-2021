from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django import forms
from django.apps import apps
from django.utils.translation import gettext_lazy as _


CustomUser = get_user_model()
Team = apps.get_model('main', 'Team')


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name',
                  'password1', 'password2', 'team')
        labels = {'name': 'Name',
                  'email': 'Email',
                  'password1': 'Password',
                  'password2': 'Confirm Password',
                  'team': "WC Winner Prediction (Rs.500)"
                  }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['team'].required = True
        self.fields['team'].queryset = Team.objects.filter(super12=True).exclude(
            shortname__in=['A1', 'A2', 'B1', 'B2'])


class UserLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email Address'

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def clean(self):
        username = self.cleaned_data.get('username')
        if '@' not in username:
            raise forms.ValidationError(
                {'username': 'Please enter valid Email Address'})

        elif not CustomUser.objects.filter(email=username).exists():
            raise forms.ValidationError(
                {'username': 'Email Address not registered'})
        return super().clean()


class UserPwdChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ('old_password',
                  'new_password1',
                  'new_password2',
                  )


class UserPwdResetForm(forms.Form):
    email = forms.EmailField(label='Email Address',
                             required=True,
                             widget=forms.EmailInput())
    new_password1 = forms.CharField(label="New Password",
                                    required=True,
                                    widget=forms.PasswordInput())
    new_password2 = forms.CharField(label="Confirm Password",
                                    required=True,
                                    widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if not email:
            raise ValidationError('Email is required')
        else:
            try:
                user = CustomUser.objects.get(email=email)
            except:
                raise ValidationError('No user exists with this email')
            else:
                new_password1 = cleaned_data.get('new_password1')
                new_password2 = cleaned_data.get('new_password2')
                if new_password1 and new_password2:
                    if new_password1 != new_password2:
                        raise ValidationError('Both Passwords dont match')
                else:
                    raise ValidationError('Password fields are mandatory')
