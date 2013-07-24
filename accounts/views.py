from django.core.urlresolvers import reverse
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
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
            return HttpResponse() # already done in JS
        else:
            x = "Unknown error."
            for field, errors in form.errors.items():
                for error in errors:
                    x = error
            return HttpResponseBadRequest(x)
    return Http404()

from django.contrib.auth.decorators import login_required

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(user=request.user, data=request.POST)
        profile = user.get_profile()

        if form.is_valid():
            if form.cleaned_data['new_password'] is not None\
                and len(form.cleaned_data['new_password']) > 0:
                user.set_password(form.cleaned_data['new_password'])
            user.email = form.cleaned_data['email']
            user.save()

            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.nickname = form.cleaned_data['nickname']
            profile.website = form.cleaned_data['website']
            profile.renren = form.cleaned_data['renren']
            profile.qq = form.cleaned_data['qq']
            profile.phone = form.cleaned_data['phone']
            profile.biography = form.cleaned_data['biography']
            profile.motto = form.cleaned_data['motto']

            profile.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        profile = user.get_profile()
        form = ProfileForm(initial={
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'nickname': profile.nickname,
            'website': profile.website,
            'renren': profile.renren,
            'qq': profile.qq,
            'phone': profile.phone,
            'biography': profile.biography,
            'motto': profile.motto,
            'email': user.email},)

    return render(request, 'accounts/update_profile.html', {
        'form': form,
    })

from forms import RegistrationForm
from django.contrib.auth.models import User
from models import Profile


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
            Profile.objects.create(user=user, name=user.username)
            return HttpResponse() # always done in JS
        else:
            x = "Unknown error."
            for field, errors in form.errors.items():
                for error in errors:
                    x = error
            return HttpResponseBadRequest(x)
    return Http404()