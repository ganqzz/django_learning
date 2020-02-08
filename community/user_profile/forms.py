from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Profile


class ExtendedUserCreationForm(UserCreationForm):
    # Modelではblank=Trueとなっているので、Formでrequired=Trueとして必須フィールドにする
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

    # templateも含めて、django-(crispy-forms|widget-tweaks)を使うとラク
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter username', 'tabindex': '1'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter email', 'tabindex': '2'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter password', 'tabindex': '3'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirm password', 'tabindex': '4'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter first name (optional)',
             'tabindex': '5'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter last name (optional)', 'tabindex': '6'})

    # required程度の変更だけであれば、overrideする必要はない
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('location', 'age')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter location (optional)', 'tabindex': '7'})
        self.fields['age'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter age (optional)', 'tabindex': '8'})


class ExtendedAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter username', 'tabindex': '1'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter password', 'tabindex': '2'})
