from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseBadRequest
from forum.models import *
from forum.forms import *


def index(request):
    reversed_topic_list = Topic.objects.order_by('-date_published')
    topic_list = []
    for x in reversed_topic_list:
        last_post = x.post_set.order_by('-date_published')[0];
        topic_list.append({'id': x.id, 'title': x.title,
                           'post_cnt': x.post_set.count(),
                           'last_editor': last_post.author.get_profile().nickname,
                           'last_edited_time': last_post.date_published,
                           'category': x.category.all()[0].title}
        )

    return render(request, 'forum/index.html', {'topic_list': topic_list})


def detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    return render(request, 'forum/detail.html', {
        'topic': topic, 'first_post': topic.post_set.order_by('date_published')[0],
        'post_form': NewPostForm()
    })


from django.contrib.auth.decorators import login_required
import datetime


@login_required()
def new_topic(request):
    user = request.user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)

        if form.is_valid():
            category = form.cleaned_data['category']
            topic = Topic(title=form.cleaned_data['title'],
                          date_published=datetime.datetime.now()
            )
            topic.save()
            for x in category:
                topic.category.add(x)

            first_post = Post(topic=topic,
                              author=user,
                              date_published=topic.date_published,
                              content=form.cleaned_data['content'])
            first_post.save()
            return HttpResponseRedirect(topic.get_absolute_url())
    else:
        form = NewTopicForm()

    return render(request, 'forum/new_topic.html', {
        'form': form
    })


@login_required
def new_post(request, topic_id):
    user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST)

        if form.is_valid():
            post = Post(topic=Topic.objects.get(id=topic_id),
                        author=user,
                        date_published=datetime.datetime.now(),
                        content=form.cleaned_data['content'])
            post.save()
            return HttpResponseRedirect(post.get_absolute_url())

        topic = get_object_or_404(Topic, id=topic_id)
        return render(request, 'forum/detail.html', {
            'topic': topic, 'first_post': topic.post_set.order_by('date_published')[0],
            'post_form': form
        })

    return Http404()


@login_required
def post_reply(request, post_id):
    user = request.user
    if request.method == 'POST':
        form = NewReplyForm(request.POST)

        if form.is_valid():
            post = Post.objects.get(id=post_id)
            reply = Reply(post=post, author=user,
                          date_published=datetime.datetime.now(),
                          content=form.cleaned_data['content'])
            reply.save()
            return HttpResponse() # already done in JS
        else:
            x = "Unknown error."
            for field, errors in form.errors.items():
                for error in errors:
                    x = error
            return HttpResponseBadRequest(x)
    return Http404()
