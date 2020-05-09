from django import forms

from sbxapp.models import Car

SIZE_CHOICES = [
    ('Small', 'Small'),
    ('Medium', 'Medium'),
    ('Large', 'Large')
]


class ExampleForm(forms.Form):
    username = forms.CharField(max_length=30, min_length=4,
                               widget=forms.TextInput(attrs={'class': 'input'}))
    text_area = forms.CharField(max_length=100, required=False, widget=forms.Textarea)
    password = forms.CharField(max_length=10, min_length=6, widget=forms.PasswordInput)
    email = forms.EmailField()
    url = forms.URLField()
    boolean = forms.BooleanField()
    date = forms.DateField()
    time = forms.TimeField()
    datetime = forms.DateTimeField()
    image = forms.ImageField()
    choice = forms.ChoiceField(choices=SIZE_CHOICES)
    m_choice = forms.MultipleChoiceField(label='Multi Choice',
                                         choices=SIZE_CHOICES)
    check_box = forms.MultipleChoiceField(choices=SIZE_CHOICES,
                                          widget=forms.CheckboxSelectMultiple)
    radio = forms.ChoiceField(choices=SIZE_CHOICES,
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
    year = forms.IntegerField(min_value=1900, max_value=2100)  # override

    class Meta:
        model = Car
        fields = '__all__'
        # widgets = {}  # ここでfield毎のwidgetをカスタマイズできる


    def clean(self):
        # custom validation
        data = self.cleaned_data
        # ...
        obj = self.instance
        return super().clean()  # maintain model validation

    def clean_name(self):
        name = self.cleaned_data['name']
        if name.lower() == 'hoge':
            raise forms.ValidationError('name cannot be "hoge"')
        return name
