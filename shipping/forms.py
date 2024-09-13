from django import forms
from .models import Address


class CustomerAddressForm(forms.ModelForm):
    address_line1 = forms.CharField(label="", required=True, help_text="Enter your Address Line 1",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Address Line 1"}
        ),
    )
    address_line2 = forms.CharField(label="", required=True, help_text="Enter your Address Line 2",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Address Line 2"}
        ),
    )
    landmark = forms.CharField(label="", required=False, help_text="Enter your Landmark",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Landmark"}
        ),
    )
    city = forms.CharField(label="", required=True, help_text="Enter your City",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}
        ),
    )
    zip_code = forms.CharField(label="", min_length=3, required=True, help_text="Enter your Zip Code",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Zip Code"}
        ),
    )
    state = forms.CharField(label="", min_length=1, required=True, help_text="Enter your State",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "State"}
        ),
    )
    country = forms.CharField(label="", min_length=1, required=True, help_text="Enter your Country",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Country"}
        ),
    )
    
    
    class Meta:
        model = Address
        fields = ['address_line1', 'address_line2', 'landmark', 'city', 'zip_code', 'state', 'country']


class UpdateCustomerAddressForm(forms.ModelForm):
    first_name = forms.CharField(label="", min_length=3, required=True, help_text="Enter your First Name",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(label="", min_length=1, required=True, help_text="Enter your Last Name",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
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
    address_line1 = forms.CharField(label="", required=True, help_text="Enter your Address Line 1",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Address Line 1"}
        ),
    )
    address_line2 = forms.CharField(label="", required=True, help_text="Enter your Address Line 2",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Address Line 2"}
        ),
    )
    landmark = forms.CharField(label="", required=False, help_text="Enter your Landmark",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Landmark"}
        ),
    )
    city = forms.CharField(label="", required=True, help_text="Enter your City",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}
        ),
    )
    zip_code = forms.CharField(label="", min_length=3, required=True, help_text="Enter your Zip Code",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Zip Code"}
        ),
    )
    state = forms.CharField(label="", min_length=1, required=True, help_text="Enter your State",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "State"}
        ),
    )
    country = forms.CharField(label="", min_length=1, required=True, help_text="Enter your Country",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Country"}
        ),
    )
    
    
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'email', 'country_code', 'phone', 'address_line1', 'address_line2', 'landmark', 'city', 'zip_code', 'state', 'country']
