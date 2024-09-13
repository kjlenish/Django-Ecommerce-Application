from typing import Any
from django import forms
from .models import Review


class ProductReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(label="", required=True, help_text="Rate the product",
        choices=Review.rating_choices,
            widget=forms.Select(attrs={'class': 'form-control'})
    ),
    review = forms.CharField(label="", min_length=5, required=True, help_text="Review the product",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Country Code"})
        ), 
    
    class Meta:
        model = Review
        fields = ['rating', 'review']
