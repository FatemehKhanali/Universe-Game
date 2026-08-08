# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User, Province, city


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')

        return username.strip() if username else username


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'mobile', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['mobile'].widget.attrs.update({'placeholder': 'Mobile Number'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})


# forms.py

from django import forms
from .models import Profile

# forms.py


class ProfileForm(forms.ModelForm):
    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        required=False,
        label="Province"
    )

    class Meta:
        model = Profile
        fields = ['province', 'city', 'postal_code', 'address']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)


        if self.instance and self.instance.city:
            self.fields['province'].initial = self.instance.city.province


        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['city'].queryset = city.objects.filter(province_id=province_id).order_by('title')
            except (ValueError, TypeError):
                self.fields['city'].queryset = city.objects.none()
        elif self.instance and self.instance.city:
            self.fields['city'].queryset = city.objects.filter(province=self.instance.city.province)
        else:
            self.fields['city'].queryset = city.objects.none()
