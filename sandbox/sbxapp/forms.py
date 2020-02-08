from django import forms

from sbxapp.models import Car


class ExampleForm(forms.Form):
    username = forms.CharField(max_length=30, min_length=4,
                               widget=forms.TextInput(attrs={'class': 'input'}))
    text_area = forms.CharField(max_length=100, required=False, widget=forms.Textarea)
    password = forms.CharField(max_length=10, min_length=6, widget=forms.PasswordInput)
    email = forms.EmailField()
    url = forms.URLField()
    boolean = forms.BooleanField()
    date = forms.DateField()
    image = forms.ImageField()
    choice = forms.ChoiceField(
        choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')])
    m_choice = forms.MultipleChoiceField(label='Multi Choice',
        choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')])
    check_box = forms.MultipleChoiceField(
        choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')],
        widget=forms.CheckboxSelectMultiple)
    radio = forms.ChoiceField(
        choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')],
        widget=forms.RadioSelect)

    def clean(self):
        # custom validation
        return super().clean()


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class HashForm(forms.Form):
    text = forms.CharField(label='Enter text here:', widget=forms.Textarea)


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'make', 'year']

    def clean(self):
        # custom validation
        data = self.cleaned_data
        # ...
        obj = self.instance
        return super().clean()  # maintain model validation
