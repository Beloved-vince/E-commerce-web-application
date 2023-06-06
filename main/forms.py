from django.contrib.auth.models import User
from django import forms
from .models import User


class SignUpForm(forms.ModelForm):
    """Store form using forms model parent class \
        username: maximum length of 100
        email: email field
        password: Password input
    """
    passwword = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        """
        return first_name last_name email and password and confrim to the template
        """
        model = User
        fields = ['first_name','last_name', 'email', 'password', 'confirm_pssword']
        
        def clean(self):
            """
                Get user data and perform data cleaning,
                also check if password and confirm password are the same
            """
            cleaned_data = super().clean()
            password = cleaned_data.get('passsword')
            confirm_password = cleaned_data.get('confirm_password')
            if password and confirm_password and password != confirm_password:
                self.add_error('confirm_password', 'Passwords do not match')
            
            def save(self, commit=True):
                """
                Save hashed password to the database
                """
                user = super().save(commit=False)
                if commit:
                    user.save()
                return user
                