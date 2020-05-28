from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tasks.forms import TaskForm
from tasks.models import Task
from . import factories


class TaskListViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('tasks')
        self.user = factories.UserFactory()
        self.tasks = factories.TaskFactory.create_batch(10, owner=self.user)

    def test_task_list_lists_all_tasks(self):
        self.client.force_login(self.user)  # no password

        response = self.client.get(self.url)
        self.assertEqual(len(self.tasks), len(response.context['tasks']))

    def test_task_list_displays_users_tasks_only(self):
        other_user = factories.UserFactory()
        factories.TaskFactory.create(owner=other_user)  # 1 task

        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(len(self.tasks), len(response.context['tasks']))

        self.client.force_login(other_user)
        response = self.client.get(self.url)
        self.assertEqual(1, len(response.context['tasks']))


class NewTaskViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('task-add')
        self.user = factories.UserFactory()

    def test_task_view_shows_create_form(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'tasks/task_form.html')
        self.assertEqual(TaskForm, response.context['form'].__class__)
        self.assertIsNone(response.context.get('task'))

    def test_create_task_always_forces_user(self):
        other_user = factories.UserFactory()

        self.client.force_login(self.user)
        self.client.post(self.url, {
            'owner': other_user.id,
            'title': 'my task'
        }, follow=True)

        self.assertIsNotNone(Task.objects.first())
        self.assertEqual(Task.objects.first().owner, self.user)


class TaskViewTestCase(TestCase):

    def setUp(self):
        self.user = factories.UserFactory()
        self.task = factories.TaskFactory.create(owner=self.user)
        self.url = reverse('task-edit', args=[self.task.id])

    def test_task_view_shows_update_form(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'tasks/task_form.html')
        self.assertEqual(TaskForm, response.context['form'].__class__)
        self.assertIsNotNone(response.context.get('task'))


class ToggleCompleteViewTestCase(TestCase):

    def setUp(self):
        self.user = factories.UserFactory()
        self.client.force_login(self.user)

    def test_toggle_complete_toggles_complete(self):
        task = factories.TaskFactory.create(owner=self.user, complete_time=None)
        url = reverse('task-toggle', args=[task.id])

        self.assertFalse(Task.objects.get(pk=task.id).is_complete)
        self.client.post(url)
        self.assertTrue(Task.objects.get(pk=task.id).is_complete)

    def test_toggle_incomplete_toggles_complete(self):
        task = factories.TaskFactory.create(
            owner=self.user,
            complete_time=timezone.now() - timezone.timedelta(days=1))

        url = reverse('task-toggle', args=[task.id])

        self.assertTrue(Task.objects.get(pk=task.id).is_complete)
        self.client.post(url)
        self.assertFalse(Task.objects.get(pk=task.id).is_complete)

    def test_toggle_complete_returns_404(self):
        url = reverse('task-toggle', args=[12345])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
