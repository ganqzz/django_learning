from django import forms


class ExampleForm(forms.Form):
    text_area = forms.CharField(max_length=100, widget=forms.Textarea)
    password = forms.CharField(max_length=10, min_length=6, widget=forms.PasswordInput)
    email = forms.EmailField()
    url = forms.URLField()
    choice = forms.ChoiceField(
        choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')])
    m_choice = forms.MultipleChoiceField(
        choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')])
    check_box = forms.MultipleChoiceField(
        choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')],
        widget=forms.CheckboxSelectMultiple)
    radio = forms.ChoiceField(
        choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')],
        widget=forms.RadioSelect)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
