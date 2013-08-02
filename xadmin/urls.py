from django.conf.urls import patterns, url
from xadmin import views


urlpatterns = patterns('',
                       url(r'^dashboard/$', views.dashboard, name='dashboard'),
                       url(r'^inbox/$', views.inbox, name='inbox'),
                       url(r'^show_msg_in_inbox/(?P<msg_id>\d+)$', views.show_msg_in_inbox, name="show_msg_in_inbox"),
                       url(r'^send_msg/$', views.send_msg, name="send_msg"),
)

