from django import forms

from . import models


class QuizForm(forms.ModelForm):
    class Meta:
        model = models.Quiz
        fields = ['title', 'description', 'order', 'total_questions', ]


class QuestionForm(forms.ModelForm):
    # TODO: Sortableが空のformをうまく扱えない
    class Media:
        # css = {'all': ('courses/css/order.css',)}
        js = (
            # 'courses/js/vendor/Sortable.min.js',
            # 'courses/js/vendor/jquery-sortable.js',
            # 'courses/js/order.js',
            'courses/js/vendor/jquery.formset.js',
        )


class TrueFalseQuestionForm(QuestionForm):
    class Meta:
        model = models.TrueFalseQuestion
        fields = ['order', 'prompt', ]


class MultipleChoiceQuestionForm(QuestionForm):
    class Meta:
        model = models.MultipleChoiceQuestion
        fields = ['order', 'prompt', 'shuffle_answers', ]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ['order', 'text', 'correct', ]


AnswerFormSet = forms.modelformset_factory(models.Answer, form=AnswerForm,
                                           can_delete=True, extra=2)

AnswerInlineFormSet = forms.inlineformset_factory(
    models.Question, models.Answer,
    extra=2, fields=('order', 'text', 'correct',),
    formset=AnswerFormSet, min_num=1
)
