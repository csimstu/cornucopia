from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseBadRequest
from forum.models import *
from forum.forms import *
from utils import paginate_topic_list, paginate_post_list

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



def all_topic_index(request):
    reversed_topic_list = Topic.objects.order_by('-date_published')

    return render(request, 'forum/topic_index.html', {
        'category_title': 'All Topics',
        # 'topic_list': reversed_topic_list,
        'topics': paginate_topic_list(reversed_topic_list, request.GET),
    })


def specific_category_index(request, label):
    category = get_object_or_404(Category, label=label)
    reversed_topic_list = Topic.objects.filter(category=category).order_by('-date_published')

    return render(request, 'forum/topic_index.html', {
        'category_title': category.title,
        # 'topic_list': reversed_topic_list,
        'topics': paginate_topic_list(reversed_topic_list, request.GET),
    })


def topic_detail(request, topic_id):
    user = request.user
    topic = get_object_or_404(Topic, id=topic_id)
    has_subscribe = False
    if user.is_authenticated():
        has_subscribe = user.subscribelist.topics.filter(id=topic.id).count() > 0
    return render(request, 'forum/topic_detail.html', {
        'has_subscribed': has_subscribe,
        'topic': topic, 'first_post': topic.post_set.order_by('date_published')[0],
        'posts': paginate_post_list(topic.post_set.order_by('date_published'), request.GET),
        'post_form': NewPostForm()
    })


from django.contrib.auth.decorators import login_required


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

        return HttpResponseBadRequest(form.errors)

    raise Http404()


@login_required
def post_reply(request, post_id):
    user = request.user
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        reply = Reply(post=post, author=user,
                      content=request.POST.get('content'))
        reply.save()
        return HttpResponseRedirect(reverse('forum:topic_detail', kwargs={'topic_id': post.topic.id}))

    raise Http404()

from pages.models import Article


def home(request):
    reversed_topic_list = Topic.objects.order_by('-date_published')
    topic_list = reversed_topic_list
    article_list = []
    reversed_article_list = Article.objects.order_by('-date_published')
    for x in reversed_article_list:
        article_list.append(x)

    return render(request, 'home.html', {
        'hot_topics': topic_list,
        'hot_articles': article_list,
    })
