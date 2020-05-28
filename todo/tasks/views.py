from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import TaskForm
from .mixins import SuccessTaskListMixin, TaskOwnedByUserMixin
from .models import Task


class TaskListView(ListView):
    """
    View to view tasks. Views tasks for current logged in user
    """
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)  # limited by login user


class NewTaskView(SuccessTaskListMixin, CreateView):
    """
    View to create a task. Owner is set upon validation. Redirect
    to task list upon completion.
    """
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        task = form.save(commit=False)
        task.owner = self.request.user
        task.save()
        return HttpResponseRedirect(self.get_success_url())


class DeleteTaskView(TaskOwnedByUserMixin, SuccessTaskListMixin, DeleteView):
    """
    View to delete a task. Must be owner to delete a task. Redirect
    to task list upon completion.
    """
    model = Task
    pk_url_kwarg = 'task_id'


class TaskView(TaskOwnedByUserMixin, SuccessTaskListMixin, UpdateView):
    """
    View to view and edit a task. Must be owner to edit a task. Redirect
    to task list upon completion.
    """
    model = Task
    form_class = TaskForm
    pk_url_kwarg = 'task_id'

    def get_queryset(self):
        if hasattr(self.request, 'user') and self.request.user.is_active:
            return Task.objects.filter(owner=self.request.user)
        return Task.objects.none()  # 404 not empty form


def toggle_complete_view(request, task_id):
    """
    Toggles complete state of task. If task with id task_id is
    incomplete, mark as complete. Else, mark as incomplete.
    Only the task owner can modify the task.
    """
    try:
        task = Task.objects.get(pk=task_id, owner=request.user)
    except Task.DoesNotExist:
        return HttpResponseNotFound()

    if task.is_complete:
        task.mark_incomplete()
    else:
        task.mark_complete()

    from django.urls import reverse
    return HttpResponseRedirect(reverse('tasks'))
