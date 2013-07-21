from django.core.urlresolvers import reverse
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render

from forms import ProfileForm, LoginForm


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return HttpResponseRedirect(reverse('forum.views.index'))
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


from django.contrib.auth.decorators import login_required

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('forum.views.index'));

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(user=request.user, data=request.POST)
        profile = user.get_profile()

        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.email = form.cleaned_data['email']
            user.save()
            profile.name = form.cleaned_data['name']
            profile.save()
            return HttpResponseRedirect(reverse('forum.views.index'))
    else:
        form = ProfileForm(initial={
            'name' : user.get_profile().name, 'email': user.email},)

    return render(request, 'accounts/update_profile.html', {
        'form': form,
    })

from forms import RegistrationForm
from django.contrib.auth.models import User
from models import Profile

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password']
            )
            user.save()
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            auth.login(request, user)
            Profile.objects.create(user=user, name=user.username)
            return HttpResponseRedirect(reverse('accounts.views.update_profile'))
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {
            'form': form,
    })