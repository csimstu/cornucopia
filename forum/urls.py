from django.conf.urls import patterns, url
from forum import views

urlpatterns = patterns('',
                       url(r'^category$', views.all_category_index, name='all_category_index'),
                       url(r'^category/all$', views.all_topic_index, name='all_topic_index'),
                       url(r'^category/(?P<label>\w+)/$', views.specific_category_index, name='specific_category_index'),
                       url(r'^topic/(?P<topic_id>\d+)/new_post/$', views.new_post, name="new_post"),
                       url(r'^topic/(?P<topic_id>\d+)/$', views.topic_detail, name='topic_detail'),
                       url(r'^post/(?P<post_id>\d+)/post_reply/$', views.post_reply, name="post_reply"),
)
