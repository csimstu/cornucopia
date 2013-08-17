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

def is_same_day(day1,day2): pass
def is_same_month(day1,day2): pass

def format_month_string(datetime):
    return str(datetime.year) + " " + str(datetime.month)

def format_day_string(datetime):
    return str(datetime.day)
