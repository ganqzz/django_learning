from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Course, Text, Quiz, User


def create_teacher(name):
    teacher = User.objects.create_user(name)
    return teacher


class CourseModelTests(TestCase):
    def test_course_creation(self):
        course = Course.objects.create(
            title="Python Regular Expressions",
            description="Learn to write regular expressions in Python",
            teacher=create_teacher('teacher1')
        )
        now = timezone.now()
        self.assertLessEqual(course.created_at, now)


class StepModelTestBase(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python Testing",
            description="Learn to write tests in Python",
            teacher=create_teacher('teacher1')
        )


class TextModelTests(StepModelTestBase):
    def test_step_creation(self):
        step = Text.objects.create(
            title="Introduction to Doctests",
            description="Learn to write tests in your docstrings.",
            course=self.course
        )
        self.assertIn(step, self.course.text_set.all())


class QuizModelTests(StepModelTestBase):
    def test_step_creation(self):
        step = Quiz.objects.create(
            title="Review: Doctests",
            description="Learn to write tests in your docstrings.",
            course=self.course,
            total_questions=5
        )
        self.assertIn(step, self.course.quiz_set.all())


class CourseViewTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python Testing",
            description="Learn to write tests in Python",
            teacher=create_teacher('teacher1')
        )
        self.course2 = Course.objects.create(
            title="New Course",
            description="A new Course",
            teacher=create_teacher('teacher2')
        )
        self.text = Text.objects.create(
            title="Introduction to Doctests",
            description="Learn to write tests in your docstrings.",
            course=self.course
        )

    def test_course_list_view(self):
        resp = self.client.get(reverse('courses:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.course, resp.context['courses'])
        self.assertIn(self.course2, resp.context['courses'])
        self.assertTemplateUsed(resp, 'courses/course_list.html')
        self.assertContains(resp, self.course.title)

    def test_course_detail_view(self):
        resp = self.client.get(reverse('courses:detail',
                                       kwargs={'pk': self.course.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.course, resp.context['course'])

    def test_text_detail_view(self):
        resp = self.client.get(reverse('courses:text', kwargs={
            'course_pk': self.course.pk,
            'step_pk': self.text.pk
        }))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.text, resp.context['step'])
