from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate
from .models import *


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control email", 'placeholder': "Username"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-control email", 'placeholder': "Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control email", 'placeholder': "Password", 'autocomplete': "false"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control email", 'placeholder': "Confirm Password", 'autocomplete': "false"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']


    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        if password1 and password1 != password2:
            raise forms.ValidationError("Password & Confirm Password Filed Does Not Match.")

        return self.cleaned_data



class UserLoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control email", 'placeholder': "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control email", 'placeholder': "Password", 'autocomplete': "false"}))


    class Meta:
        model = User
        fields = ['username', 'password']


    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data



class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "First Name"}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Last Name"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-control email", 'placeholder': "Email"}))


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']





class UserProfileForm(forms.ModelForm):
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Contact No."}))
    facebook = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Facebook Profile Link"}))
    twitter = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Twitter Profile Link"}))
    linkedIn = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "LinkedIn Profile Link"}))
    google = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Google Profile Link"}))

    class Meta:
        model = UserProfile
        fields = ['phone', 'facebook', 'twitter', 'linkedIn', 'google']


class AddressForm(forms.ModelForm):
    street_no = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Street No."}))
    street_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Street Name"}))
    unit_no = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class': "form-control email", 'placeholder': "Unit No."}))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "City"}))
    postal_code = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "XXX XXX"}))


    class Meta:
        model = Address
        fields = ['street_no', 'street_name', 'unit_no', 'city', 'postal_code']