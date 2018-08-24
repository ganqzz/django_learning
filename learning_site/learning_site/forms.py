from django import forms
from django.core import validators


# 1 argument
def must_be_empty(value):
    if value:
        raise forms.ValidationError("is not empty")


class SuggestionForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    verify_email = forms.EmailField(label="Please verify your email address")
    suggestion = forms.CharField(widget=forms.Textarea)
    honeypot = forms.CharField(required=False,
                               widget=forms.HiddenInput,
                               label="Leave empty",
                               # validators=[validators.MaxLengthValidator(0)]  # built-in
                               validators=[must_be_empty]  # custom
                               )

    # entire form validation
    def clean(self):
        cleaned_data = super().clean()  # dict
        email = cleaned_data.get('email')
        verify_email = cleaned_data.get('verify_email')

        if email != verify_email:
            raise forms.ValidationError("You need to enter the same email in both fields")

    # customs: clean_<field>()
    # def clean_honeypot(self):
    #     honeypot = self.cleaned_data['honeypot']
    #     if len(honeypot):
    #         raise forms.ValidationError("honeypot should be left empty. Bad bot!")
    #     return honeypot
