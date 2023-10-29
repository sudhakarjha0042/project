from django import forms

class ProductSearchForm(forms.Form):
    product_name = forms.CharField(label='Enter the product name or category', max_length=100)
