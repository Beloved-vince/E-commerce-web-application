from django.contrib.auth.models import User
from django import forms
from .models import Subscription, Wishlist, Address
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    """Store form using forms model parent class \
        username: maximum length of 100
        email: email field
        password: Password input
    """
    # password = forms.CharField(widget=forms.PasswordInput, required=True)
    # confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        """
        return first_name last_name email and password and confrim to the template
        """
        model = User
        fields = ('first_name','last_name', 'email',)
        
        # def clean(self):
        #     """
        #         Get user data and perform data cleaning,
        #         also check if password and confirm password are the same
        #     """
        #     cleaned_data = super().clean()
        #     password = cleaned_data.get('passsword')
        #     confirm_password = cleaned_data.get('confirm_password')
        #     if password and confirm_password and password != confirm_password:
        #         raise forms.ValidationError('Passwords do not match')
    
        # def save(self, commit=True):
        #     """
        #     Save hashed password to the database
        #     """
        #     user = super().save(commit=False)
        #     if commit:
        #         user.save(using=self._db)
        #     return user


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']


class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = []  # Add any additional fields that might be include in the form


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street", "city", "state", "country", "postal_code"]

    def clean(self):
        cleaned_data = super().clean()
        # Perform additional validation or security checks here
        return cleaned_data
