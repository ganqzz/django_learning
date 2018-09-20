from django.conf.urls import url

from . import views

app_name = 'courses'  # >= 2.0

# 順番に注意：詳細度が高いものを先に
urlpatterns = [
    url(r'^$', views.course_list, name="list"),
    url(r'search/$', views.search, name="search"),
    url(r'(?P<course_pk>\d+)/create-quiz/$', views.quiz_create, name="create-quiz"),
    url(r'(?P<course_pk>\d+)/t(?P<step_pk>\d+)/$', views.text_detail, name="text"),
    url(r'(?P<course_pk>\d+)/q(?P<step_pk>\d+)/$', views.quiz_detail, name="quiz"),
    url(r'(?P<course_pk>\d+)/edit-quiz/(?P<quiz_pk>\d+)/$', views.quiz_edit, name="edit-quiz"),
    url(r'(?P<quiz_pk>\d+)/create-question/(?P<question_type>mc|tf)/$', views.create_question,
        name="create-question"),
    url(r'(?P<quiz_pk>\d+)/edit-question/(?P<question_pk>\d+)/$', views.edit_question,
        name="edit-question"),
    # url(r'(?P<question_pk>\d+)/create-answer/$', views.create_answer, name="create-answer"),
    # url(r'(?P<question_pk>\d+)/edit-answer/(?P<answer_pk>\d+)/$', views.edit_answer,
    #     name="edit-answer"),
    url(r'(?P<question_pk>\d+)/answers/$', views.answer_form, name="answers"),
    url(r'by/(?P<teacher>[-\w]+)/$', views.courses_by_teacher, name="by-teacher"),
    url(r'(?P<pk>\d+)/$', views.course_detail, name="detail"),
]
