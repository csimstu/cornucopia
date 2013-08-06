from django.conf.urls import patterns, url
from pages import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name="index"),
                       url(r'^(?P<article_id>\d+)$', views.detail, name="detail"),
                       url(r'^new_comment/(?P<article_id>\d+)/$', views.new_comment, name="new_comment"),
                       )
