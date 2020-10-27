from django import forms
from django.contrib.auth.forms import UserChangeForm
from captcha.fields import CaptchaField, CaptchaTextInput

from django.contrib.auth import (
    authenticate,
    get_user_model
)

User = get_user_model()

class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'captcha.html'


class UserLogin(forms.Form):
    username = forms.CharField(label='Username', label_suffix='')
    password = forms.CharField(label='Password', label_suffix='', widget=forms.PasswordInput)
    captcha = CaptchaField(widget=CustomCaptchaTextInput)
    
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')


        # change this later to not specify the password or email bc security
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Incorrect Username or Password')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Username or Password')
            if not user.is_active:
                raise forms.ValidationError('User not active')
            
        return super(UserLogin, self).clean(*args, **kwargs)
        
class UserSignUp(forms.ModelForm):
    username = forms.CharField(label_suffix='', min_length=3, max_length=15)
    email = forms.EmailField(label='Email', label_suffix='')
    email2 = forms.EmailField(label='Confirm Email', label_suffix='')
    password = forms.CharField(widget=forms.PasswordInput(), min_length=10)
    captcha = CaptchaField(widget=CustomCaptchaTextInput)
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
            'captcha'
        ]
        
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        password = self.cleaned_data.get('password')
        if email != email2:
            raise forms.ValidationError('Emails must match.')
        username_query = User.objects.filter(username=username)
        if username_query.exists():
            raise forms.ValidationError('Username is taken.')
        email_query = User.objects.filter(email=email)
        if email_query.exists():
            raise forms.ValidationError(
                "This Email has already been registered.")
    
        return super(UserSignUp, self).clean(*args, **kwargs)
        
class UserEmailChange(forms.ModelForm):
    email = forms.EmailField(label='New Email', label_suffix='')
    email2 = forms.EmailField(label='Confirm New Email', label_suffix='')
    
    class Meta:
        model = User
        fields = [
            'email',
            'email2',
        ]
    
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError('Emails must match.')
        email_query = User.objects.filter(email=email)
        if email_query.exists():
            raise forms.ValidationError(
                "This Email has already been registered.")
                
        return super(UserEmailChange, self).clean(*args, **kwargs)
        
class EditProfile(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )