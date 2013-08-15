from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from pages.models import *
from pages.forms import *


def index(request):
    reversed_article_list = Article.objects.order_by('-date_published')
    article_list = []
    for x in reversed_article_list:
        article_list.append({
            'id': x.id, 'title': x.title,
            'comment_cnt': x.comment_set.count(),
            'date_published': x.date_published,
            'author': x.author,
            'abstract': x.content,
            'tags': x.tags.all(),
        })
    return render(request, 'pages/index.html',
                  {'article_list': article_list,
                   'main_title': 'Latest Articles'})


def detail(request, article_id):
    user = request.user
    article = get_object_or_404(Article, id=article_id)
    has_subscribed = False
    if user.is_authenticated():
        has_subscribed = user.subscribelist.articles.filter(id=article.id).count() > 0
    return render(request, 'pages/detail.html', {
        'has_subscribed': has_subscribed,
        'article': article, 'comment_form': NewCommentForm()
    })


from django.contrib.auth.decorators import login_required
import datetime



@login_required()
def new_comment(request, article_id):
    user = request.user
    if request.method == 'POST':
        print request.POST
        form = NewCommentForm(request.POST)

        if form.is_valid():
            comment = Comment(author=user,
                              article=Article.objects.get(id=article_id),
                              content=form.cleaned_data['content'])
            comment.save()
            return HttpResponseRedirect(comment.article.get_absolute_url())

        article = get_object_or_404(Article, id=article_id)
        has_subscribed = False
        if user.is_authenticated():
            has_subscribed = user.subscribelist.articles.filter(id=article.id).count() > 0
        return render(request, 'pages/detail.html', {
            'has_subscribed': has_subscribed,
            'article': article, 'comment_form': form
        })
    return Http404()