from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from pages.models import *
from pages.forms import *
from datetime import date

from utils import paginate_article_list
def index(request):
    reversed_article_list = Article.objects.order_by('-date_published')

    tags = request.GET.get("tags","")
    abstract = request.GET.get("abstract","")
    pub_time_start = request.GET.get("pub_time_start","")
    pub_time_end = request.GET.get("pub_time_end","")
    author = request.GET.get("author","")
    title = request.GET.get("title","")
    
    if tags:
        tag = Tag.objects.filter(title__icontains = tags)
        pass

    if abstract:
        reversed_article_list = reversed_article_list.filter(abstract__icontains = abstract)

    if title:
        reversed_article_list = reversed_article_list.filter(title__icontains = title)

    if author:
        author = User.objects.filter(username = author)
        if author:
            reversed_article_list = reversed_article_list.filter(author = author)
    
    if pub_time_start:
        tmp = [int(x.rstrip()) for x in pub_time_start.split(" ")]
        pub_time_start = date(tmp[0],tmp[1],tmp[2])

    if pub_time_end:
        tmp = [int(x.rstrip()) for x in pub_time_end.split(" ")]
        pub_time_end = date(tmp[0],tmp[1],tmp[2])

    if pub_time_start and pub_time_end:
        reversed_article_list = reversed_article_list.filter(date_published__range = (
            pub_time_start,pub_time_end,
        ))
    else:
        if pub_time_start:
            reversed_article_list = reversed_article_list.fitler(date_published__gt = pub_time_start)
        else if pub_time_end:
            reversed_article_list = reversed_article_list.filter(date_published__lt = pub_time_end)

    
    GET_data = request.GET.copy()
    del GET_data["page"]

    article_list = []
    for x in reversed_article_list:
        article_list.append(x)
    return render(request, 'pages/index.html',
                  {'articles': paginate_article_list(article_list, request.GET),
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
