from forum.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from TeenHope.settings import TOPIC_PER_PAGE

def paginate_topic_list(topic_list, GET_data):
    paginator = Paginator(topic_list, TOPIC_PER_PAGE)

    page = GET_data.get('page')
    try:
        topics = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        topics = paginator.page(1)
    return topics

def paginate_post_list(post_list, GET_data):
    paginator = Paginator(post_list, TOPIC_PER_PAGE)

    page = GET_data.get('page')
    try:
        posts = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        posts = paginator.page(1)
    return posts