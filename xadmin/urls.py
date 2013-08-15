from django.conf.urls import patterns, url
from xadmin import views


urlpatterns = patterns('',
                       url(r'^dashboard/$', views.dashboard, name='dashboard'),
                       url(r'^inbox/$', views.inbox, name='inbox'),
                       url(r'^show_msg_in_inbox/(?P<msg_id>\d+)$', views.show_msg_in_inbox, name="show_msg_in_inbox"),
                       url(r'^send_msg/$', views.send_msg, name="send_msg"),
                       url(r'^add_connections/$', views.add_connections, name="add_connections"),
                       url(r'^manage_connections/$', views.manage_connections, name="manage_connections"),
                       url(r'^new_topic/$', views.new_topic, name="new_topic"),
                       url(r'^new_article/$', views.new_article, name="new_article"),
                       url(r'^recent_traces/$', views.recent_traces, name="recent_traces"),
                       url(r'^update_profile/$', views.update_profile, name='update_profile'),
                       url(r'^on_checkbox$',views.on_checkbox,name="on_checkbox"),
                       url(r'^ckbox_select_all/(?P<page>\d+)$',views.ckbox_select_all,name="ckbox_select_all"),
                       url(r'^ckbox_unselect_all/(?P<page>\d+)$',views.ckbox_unselect_all,name="ckbox_unselect_all"),
                       url(r'^ckbox_remove$',views.ckbox_remove,name="ckbox_remove"),
                       url(r'^ckbox_mark$',views.ckbox_mark,name="ckbox_mark"),
                       url(r'^ckbox_unmark$',views.ckbox_unmark,name="ckbox_unmark"),
                       url(r'^inbox_search$',views.inbox_search,name="inbox_search"),
                       url(r'^inbox_mark_one$',views.inbox_mark_one,name="inbox_mark_one"),
                       url(r'^inbox_unmark_one$',views.inbox_unmark_one,name="inbox_unmark_one"),
                       url(r'^chpsw_sendmail$',views.chpsw_sendmail,name="chpsw_sendmail"),
                       url(r'^chpsw_ckhash$',views.chpsw_ckhash,name="chpsw_ckhash"),
                       url(r'^chpsw_doupdate$',views.chpsw_doupdate,name="chpsw_doupdate"),
)


