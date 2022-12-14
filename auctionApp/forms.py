from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Layout, Submit
from crispy_forms.bootstrap import FormActions
import datetime


class LoginForm(forms.Form):
    '''Form for user login'''

    username = forms.CharField(
        label='Username',
        max_length=50,
        widget=forms.TextInput(attrs={'autocomplete': 'username'})
    )
    password = forms.CharField(
        label='Password',
        max_length=50,
        widget=forms.PasswordInput(attrs={'autocomplete': 'password'})
    )

    helper = FormHelper()
    helper.form_id = 'login-form'
    helper.layout = Layout(
        Row('username', css_class="mb-2"),
        Row('password', css_class="mb-2"),
        FormActions(
            Submit('login', 'Log in', css_class="mt-2"),
        )
    )


class SignupForm(forms.Form):
    '''Form for user signup'''

    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'username',
            }
        )
    )
    city = forms.CharField(
        label='City',
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'city',
            }
        )
    )
    date_of_birth = forms.DateField (
        label="Date of Birth",
        widget=forms.widgets.SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
    ),
)
    password = forms.CharField(
        label='Password',
        max_length=50,
        widget=forms.PasswordInput(attrs={'autocomplete': 'password'})
    )
    password_confirm = forms.CharField(
        label='Confirm Password',
        max_length=50,
        widget=forms.PasswordInput,
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={'autocomplete': 'email'}
        )
    )

    helper = FormHelper()
    helper.form_id = 'signup-form'
    helper.layout = Layout(
        Row('username', css_class='mb-2'),
        Row('email', css_class='mb-2'),
        Row('city', css_class='mb-2'),
        Row('date_of_birth', css_class='mb-2'),
        Row('password', css_class='mb-2'),
        Row('password_confirm', css_class='mb-2'),
        FormActions(
            Submit('signup', 'Sign up', css_class="btn-primary"),
            css_class='mt-3'
        )
    )

