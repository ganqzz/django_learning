from django.forms import ModelForm

from .models import Thread, Reply


class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        fields = ('title', 'description')


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ('message',)
