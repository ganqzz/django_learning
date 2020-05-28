from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Profile


class ExtendedUserCreationForm(UserCreationForm):
    # Userモデルではblank=Trueとなっているので、Form側でrequired=Trueとして必須フィールドにする
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

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


class ExtendedAuthenticationForm(AuthenticationForm):
    pass
