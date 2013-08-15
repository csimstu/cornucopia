from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseBadRequest
from forum.models import *
from forum.forms import *


def all_category_index(request):
    category_list = []
    for category in Category.objects.all():
        category_list.append({
            'title': category.title,
            'label': category.label,
            'intro': category.description,
            'topic_cnt': category.topic_cnt,
            'post_cnt': category.post_cnt,
            'last_editor': User.objects.get(id=category.last_editor_id),
            'last_modified_time': category.last_modified_time,
        })

    return render(request, 'forum/all_category_index.html', {
        'category_list': category_list,
    })


def generate_topic_list(list):
    topic_list = []
    for x in list:
        last_post = x.post_set.order_by('-date_published')[0];
        topic_list.append({'id': x.id, 'title': x.title,
                           'post_cnt': x.post_set.count(),
                           'last_editor': last_post.author.get_profile().nickname,
                           'last_editor_id': last_post.author.id,
                           'last_edited_time': last_post.date_published,
                           'category': x.category.title}
        )
    return topic_list


def all_topic_index(request):
    reversed_topic_list = Topic.objects.order_by('-date_published')

    return render(request, 'forum/topic_index.html', {
        'category_title': 'All Topics',
        'topic_list': generate_topic_list(reversed_topic_list)
    })


def specific_category_index(request, label):
    category = get_object_or_404(Category, label=label)
    reversed_topic_list = Topic.objects.filter(category=category).order_by('-date_published')

    return render(request, 'forum/topic_index.html', {
        'category_title': category.title,
        'topic_list': generate_topic_list(reversed_topic_list),
    })


def topic_detail(request, topic_id):
    user = request.user
    topic = get_object_or_404(Topic, id=topic_id)
    return render(request, 'forum/topic_detail.html', {
        'has_subscribed': user.subscribelist.topics.filter(id=topic.id).count() > 0,
        'topic': topic, 'first_post': topic.post_set.order_by('date_published')[0],
        'post_form': NewPostForm()
    })


from django.contrib.auth.decorators import login_required
import datetime


@login_required
def new_post(request, topic_id):
    user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST)

        if form.is_valid():
            post = Post(topic=Topic.objects.get(id=topic_id),
                        author=user,
                        content=form.cleaned_data['content'])
            post.save()
            return HttpResponseRedirect(post.get_absolute_url())

        topic = get_object_or_404(Topic, id=topic_id)
        return render(request, 'forum/topic_detail.html', {
            'has_subscribed': user.subscribelist.topics.filter(id=topic.id).count() > 0,
            'topic': topic, 'first_post': topic.post_set.order_by('date_published')[0],
            'post_form': form
        })

    return Http404()


@login_required
def post_reply(request, post_id):
    user = request.user
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        reply = Reply(post=post, author=user,
                      content=request.POST.get('content'))
        reply.save()
        return HttpResponseRedirect(reverse('forum:topic_detail', kwargs={'topic_id': post.topic.id}))

    return Http404()

from pages.models import Article


def home(request):
    reversed_topic_list = Topic.objects.order_by('-date_published')
    topic_list = generate_topic_list(reversed_topic_list)
    article_list = []
    reversed_article_list = Article.objects.order_by('-date_published')
    for x in reversed_article_list:
        article_list.append({
            'id': x.id, 'title': x.title,
            'comment_cnt': x.comment_set.count(),
            'date_published': x.date_published,
            'author_name': x.author.get_profile().nickname,
            'abstract': x.content,
            'tags': x.tags.all(),
        })

    return render(request, 'home.html', {
        'hot_topics': topic_list,
        'hot_articles': article_list,
    })
