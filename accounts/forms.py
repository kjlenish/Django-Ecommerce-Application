from typing import Any
from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import CustomerProfile


class DateInput(forms.DateInput):
    input_type = 'date'


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label="", min_length=3, required=True, help_text="Enter your First Name",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(label="", min_length=1, required=True, help_text="Enter your Last Name",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )
    username = forms.CharField(label="", min_length=3, required=True, help_text="Enter your Username",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}
        ),
    )
    password1 = forms.CharField(label="", min_length=3, required=True, help_text="Enter your Password",
            widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(label="", min_length=3, required=True, help_text="Enter your Password again",
            widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm Password"}
        ),
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="", required=True, help_text="Enter your Username",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}
        ),
    )
    password = forms.CharField(label="", required=True, help_text="Enter your Password",
            widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    
    class Meta:
       fields = ['username', 'password']


class CustomerProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(label="", required=True, help_text="Choose your Gender",
        choices=CustomerProfile.gender_choice,
            widget=forms.Select(attrs={'class': 'form-control'})
    )
    dob = forms.DateField(
        label="",
        required=True,
        help_text="Enter your Date of Birth",
        widget=DateInput(attrs={"class": "form-control", "placeholder": "Date of Birth"})
    )    
    
    class Meta:
        model = CustomerProfile
        fields = ['gender', 'dob']
        widgets = {
            'dob': DateInput()
        }


class CommonContactForm(forms.Form):
    email = forms.EmailField(label="", min_length=5, required=True, help_text="Enter your Email Address",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email Address"}
        ),
    )
    country_code = forms.CharField(label="", max_length=5, required=True, help_text="Enter your Country Code",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Country Code"}
        ),
    )
    phone = forms.IntegerField(label="", required=True, help_text="Enter your Phone Number",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}
        )
    )


class UserUpdateForm(UserChangeForm):
    password = None
    first_name = forms.CharField(label="", min_length=3, required=True, help_text="Enter your First Name",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(label="", min_length=1, required=True, help_text="Enter your Last Name",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UpdateCustomerProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(label="", required=True, help_text="Choose your Gender",
        choices=CustomerProfile.gender_choice,
            widget=forms.Select(attrs={'class': 'form-control'})
    )
    dob = forms.DateField(
        label="",
        required=True,
        help_text="Enter your Date of Birth",
        widget=DateInput(attrs={"class": "form-control", "placeholder": "Date of Birth"})
    )    
    email = forms.EmailField(label="", min_length=5, required=True, help_text="Enter your Email Address",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email Address"}
        ),
    )
    country_code = forms.CharField(label="", max_length=5, required=True, help_text="Enter your Country Code",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Country Code"}
        ),
    )
    phone = forms.IntegerField(label="", required=True, help_text="Enter your Phone Number",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}
        )
    )

    class Meta:
        model = CustomerProfile
        fields = ['gender', 'dob', 'email', 'country_code', 'phone']
        widgets = {
            'dob': DateInput()
        }


class UpdatePasswordForm(SetPasswordForm):    
    
    def __init__(self, user, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(user, *args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = ''
        
        self.fields["new_password1"].widget.attrs["class"] = "form-control"
        self.fields["new_password1"].widget.attrs["placeholder"] = "Enter the new password"

        self.fields["new_password2"].widget.attrs["class"] = "form-control"
        self.fields["new_password2"].widget.attrs["placeholder"] = "Confirm new Password"