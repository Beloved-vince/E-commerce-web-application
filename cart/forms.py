from django import forms

class AddToCartForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1, initial=1)
    