from django import forms


class CustomUserCreationForm(forms.Form):
    UserName = forms.CharField(label='User Name:', max_length=50)
    password1 = forms.CharField(widget=forms.PasswordInput,label='Password:', max_length=50, min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password:', max_length=50, min_length=8)
    Useremail = forms.CharField(label='Email', max_length=200)

class LoginForm(forms.Form):
    UserName = forms.CharField(label='User Name:', max_length=50)
    password = forms.CharField(widget=forms.PasswordInput,label='Password:', max_length=50, min_length=8)
    