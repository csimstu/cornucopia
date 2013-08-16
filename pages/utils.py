from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from TeenHope.settings import ARTICLE_PER_PAGE

def paginate_article_list(article_list, GET_data):
    paginator = Paginator(article_list, ARTICLE_PER_PAGE)

    page = GET_data.get('page')
    try:
        articles = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        articles = paginator.page(1)
    return articles

