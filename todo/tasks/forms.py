from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """
    A model form for a Task object.
    """

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
        widgets = {'due_date': forms.DateInput(attrs={'type': 'date'})}
