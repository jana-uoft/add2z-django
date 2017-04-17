from django.contrib.auth.models import User
from django import forms


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