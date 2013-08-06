from django.conf.urls import patterns, url
from forum import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^(?P<topic_id>\d+)/$', views.detail, name='detail'),
                       url(r'^(?P<post_id>\d+)/post_reply/$', views.post_reply, name="post_reply"),
                       url(r'^new_post/(?P<topic_id>\d+)/$', views.new_post, name="new_post"),

)
