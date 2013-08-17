from django.conf.urls import patterns, url
from network import views


urlpatterns = patterns('',
                       url(r'^accept_invitation/(?P<user_id>\d+)/$', views.accept_invitation, name="accept_invitation"),
                       url(r'^remove_friend/$', views.remove_friend, name="remove_friend"),
                       url(r'^send_invitation/$', views.send_invitation, name="send_invitation"),
                       url(r'^add_follow/$', views.add_follow, name="add_follow"),
                       url(r'^send_message/$', views.send_message_single, name="send_message"),
                       url(r'^send_message_selected$',views.send_message_selected,name="send_message_selected"),
                       url(r'^subscribe_topic/$', views.subscribe_topic, name="subscribe_topic"),
                       url(r'^unsubscribe_topic/$', views.unsubscribe_topic, name="unsubscribe_topic"),
                       url(r'^subscribe_article/$', views.subscribe_article, name="subscribe_article"),
                       url(r'^unsubscribe_article/$', views.unsubscribe_article, name="unsubscribe_article"),
)

