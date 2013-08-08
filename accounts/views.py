from django.core.urlresolvers import reverse
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render

from forms import LoginForm


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'login_form': form,
    })


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('home'))


from forms import RegistrationForm
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password']
            )
            user.save()
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            auth.login(request, user)
            return HttpResponseRedirect(reverse("home"))
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {
        'register_form': form,
    })

