from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ExtendedUserCreationForm, ProfileForm


def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = ExtendedUserCreationForm()
        profile_form = ProfileForm()

    context = {'form': form, 'profile_form': profile_form}
    return render(request, 'user_profile/register.html', context)


@login_required
def profile(request):
    return render(request, 'user_profile/profile.html')
