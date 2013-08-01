from django.shortcuts import render
from forum.models import *
from pages.models import *


def dashboard(request):
    user = request.user

    stat = {'topic_cnt' : Topic.objects.filter(author=user).count(),
            'post_cnt' : Post.objects.filter(author=user).count(),
            'reply_cnt': Reply.objects.filter(author=user).count(),
            'article_cnt': Article.objects.filter(author=user).count(),
            'comment_cnt': Comment.objects.filter(author=user).count(),
            'tag_cnt': Tag.objects.filter(author=user).count(),
    }

    return render(request, 'xadmin/dashboard.html',
        {
            'stat': stat,
        })