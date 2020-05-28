from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

from . import forms
from . import models


# TODO:全般的にformエラー処理が足りない


def course_list(request):
    courses = models.Course.objects.all()

    # filters
    term = request.GET.get('q')
    if term:
        courses = courses.filter(
            Q(title__icontains=term) | Q(description__icontains=term),
        )
    if request.GET.get('published'):
        courses = courses.filter(published=True)

    # aggregate
    courses = courses.annotate(
        total_steps=Count('text', distinct=True) + Count('quiz', distinct=True)
    )
    total = courses.aggregate(total=Sum('total_steps'))
    return render(request, 'courses/course_list.html', {'courses': courses,
                                                        'total': total})


def course_detail_old(request, pk):
    """N+1 problem"""
    course = get_object_or_404(models.Course, pk=pk)
    steps = sorted(chain(course.text_set.all(), course.quiz_set.all()),
                   key=lambda step: step.order)
    return render(request, 'courses/course_detail.html', {'course': course,
                                                          'steps': steps})


def course_detail(request, pk):
    """Solution for N+1 problem"""
    try:
        course = models.Course.objects.prefetch_related(
            'quiz_set', 'text_set', 'quiz_set__question_set'
        ).get(pk=pk)
    except models.Course.DoesNotExist:
        raise Http404
    else:
        steps = sorted(chain(course.text_set.all(), course.quiz_set.all()),
                       key=lambda step: step.order)
    return render(request, 'courses/course_detail.html', {'course': course,
                                                          'steps': steps})


def text_detail(request, course_pk, step_pk):
    step = get_object_or_404(models.Text, course_id=course_pk, pk=step_pk)
    return render(request, 'courses/text_detail.html', {'step': step})


def quiz_detail(request, course_pk, step_pk):
    try:
        step = models.Quiz.objects.select_related('course') \
            .prefetch_related('question_set', 'question_set__answer_set') \
            .get(course_id=course_pk, pk=step_pk)
    except models.Quiz.DoesNotExist:
        raise Http404
    else:
        return render(request, 'courses/quiz_detail.html', {'step': step})


@login_required()
def quiz_create(request, course_pk):
    course = get_object_or_404(models.Course, pk=course_pk)
    form = None

    if request.method == 'POST':
        form = forms.QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)  # not touch db at this time
            quiz.course = course
            quiz.save()
            messages.add_message(request, messages.SUCCESS, "Quiz added")
            return HttpResponseRedirect(quiz.get_absolute_url())
        else:
            messages.add_message(request, messages.ERROR, 'Something wrong')

    form = form or forms.QuizForm()  # invalid => request.POST as old input
    return render(request, 'courses/quiz_form.html', {'form': form, 'course': course})


@login_required()
def quiz_edit(request, course_pk, quiz_pk):
    quiz = get_object_or_404(models.Quiz, pk=quiz_pk)

    if request.method == 'POST':
        form = forms.QuizForm(instance=quiz, data=request.POST)
        if form.is_valid():
            quiz = form.save()
            messages.success(request, "Updated {}".format(quiz.title))
            return HttpResponseRedirect(quiz.get_absolute_url())
        else:
            messages.error(request, 'Something wrong')

    form = forms.QuizForm(instance=quiz)  # invalid => reset
    return render(request, 'courses/quiz_form.html', {'form': form, 'course': quiz.course})


@login_required()
def create_question(request, quiz_pk, question_type):
    quiz = get_object_or_404(models.Quiz, pk=quiz_pk)

    if question_type == 'tf':
        form_class = forms.TrueFalseQuestionForm
    else:
        form_class = forms.MultipleChoiceQuestionForm

    form = None

    if request.method == 'POST':
        form = form_class(request.POST)
        answer_forms = forms.AnswerInlineFormSet(request.POST,
                                                 queryset=models.Answer.objects.none())  # no answer
        if form.is_valid() and answer_forms.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            answers = answer_forms.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            messages.success(request, "Question added")
            return HttpResponseRedirect(quiz.get_absolute_url())
        else:
            messages.error(request, 'Something wrong')

    form = form or form_class()
    answer_forms = forms.AnswerInlineFormSet(queryset=models.Answer.objects.none())  # no answer
    return render(request, 'courses/question_form.html',
                  {'form': form, 'quiz': quiz, 'formset': answer_forms})


@login_required()
def edit_question(request, quiz_pk, question_pk):
    question = get_object_or_404(models.Question, pk=question_pk)

    if hasattr(question, 'truefalsequestion'):  # get~で取得したオブジェクトには、テーブル名の属性が付加される
        form_class = forms.TrueFalseQuestionForm
        question = question.truefalsequestion
    else:
        form_class = forms.MultipleChoiceQuestionForm
        question = question.multiplechoicequestion  # 派生クラスの属性を記憶する

    if request.method == 'POST':
        form = form_class(request.POST, instance=question)
        answer_forms = forms.AnswerInlineFormSet(request.POST,
                                                 queryset=question.answer_set.all())
        if form.is_valid() and answer_forms.is_valid():
            question = form.save()
            answers = answer_forms.save(commit=False)  # 新規Answerが含まれる可能性があるため
            for answer in answer_forms.deleted_objects:  # delete
                answer.delete()
            for answer in answers:
                answer.question = question
                answer.save()
            messages.success(request, "Question updated")
            return HttpResponseRedirect(question.quiz.get_absolute_url())
        else:
            messages.error(request, 'Something wrong')

    form = form_class(instance=question)
    answer_forms = forms.AnswerInlineFormSet(queryset=question.answer_set.all())
    return render(request, 'courses/question_form.html',
                  {'form': form, 'quiz': question.quiz, 'formset': answer_forms})


@login_required()
def create_answer(request, question_pk):
    question = get_object_or_404(models.Question, pk=question_pk)
    form = None

    if request.method == 'POST':
        form = forms.AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            messages.success(request, "Answer added")
            return HttpResponseRedirect(question.get_absolute_url())
        else:
            messages.error(request, 'Something wrong')

    form = form or forms.AnswerForm()
    return render(request, 'courses/answer_form.html', {'form': form, 'question': question})


@login_required()
def edit_answer(request, question_pk, answer_pk):
    answer = get_object_or_404(models.Answer, pk=answer_pk)
    form = None

    if request.method == 'POST':
        form = forms.AnswerForm(instance=answer, data=request.POST)  # instanceの設定を忘れないように
        if form.is_valid():
            answer = form.save()
            messages.success(request, "Answer updated")
            return HttpResponseRedirect(answer.question.get_absolute_url())
        else:
            messages.error(request, 'Something wrong')

    form = form or forms.AnswerForm(instance=answer)
    return render(request, 'courses/answer_form.html', {'form': form, 'question': answer.question})


# Formset
@login_required()
def answers_form(request, question_pk):
    question = get_object_or_404(models.Question, pk=question_pk)
    queryset = question.answer_set.all()
    formset = None

    if request.method == 'POST':
        formset = forms.AnswerFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            answers = formset.save(commit=False)
            for answer in formset.deleted_objects:  # delete
                answer.delete()
            for answer in answers:
                answer.question = question
                answer.save()
            messages.success(request, "Answers updated")
            return HttpResponseRedirect(question.get_absolute_url())
        else:
            messages.error(request, 'Something wrong')

    formset = formset or forms.AnswerFormSet(queryset=queryset)
    return render(request, 'courses/answers_form.html',
                  {'formset': formset, 'question': question})


def courses_by_teacher(request, teacher):
    courses = models.Course.objects.filter(teacher__username=teacher)
    return render(request, 'courses/course_list.html', {'courses': courses})
