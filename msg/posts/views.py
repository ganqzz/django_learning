from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic

from . import forms
from . import models

User = get_user_model()


class AllPosts(generic.ListView):
    model = models.Post

    def get_queryset(self):
        return super().get_queryset().select_related("user", "community")


class UserPosts(generic.ListView):
    model = models.Post
    template_name = "posts/user_timeline.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects \
                .prefetch_related("posts") \
                .get(username__iexact=self.kwargs.get("username"))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class SinglePost(generic.DetailView):
    model = models.Post

    def get_queryset(self):
        return super().get_queryset() \
            .select_related("user", "community") \
            .filter(user__username__iexact=self.kwargs.get("username"))


class CreatePost(LoginRequiredMixin, generic.CreateView):
    form_class = forms.PostForm
    model = models.Post

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, generic.DeleteView):
    model = models.Post
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        return super().get_queryset() \
            .select_related("user", "community") \
            .filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Message successfully deleted")
        return super().delete(*args, **kwargs)
