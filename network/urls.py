from django.conf.urls import patterns, url
from network import views


urlpatterns = patterns('',
                       url(r'^search_user_thumb_list/$', views.search_user_thumb_list, name="search_user_thumb_list"),
                       url(r'^search_user_thumb_list_exclude/$', views.search_user_thumb_list_exclude, name="search_user_thumb_list_exclude"),
                       url(r'^get_user_thumb_by_id/$', views.get_user_thumb_by_id, name="get_user_thumb_by_id"),
                       url(r'^accept_invitation/(?P<user_id>\d+)/$', views.accept_invitation, name="accept_invitation"),
                       url(r'^remove_friend/$', views.remove_friend, name="remove_friend"),
                       url(r'^send_invitation/$', views.send_invitation, name="send_invitation"),
                       url(r'^add_follow/$', views.add_follow, name="add_follow"),
                       url(r'send_message/$', views.send_message_single, name="send_message"),
)

