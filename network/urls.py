from django.conf.urls import patterns, url
from network import views


urlpatterns = patterns('',
                       url(r'^get_receiver_list/$', views.get_receiver_list, name="get_receiver_list"),
                       url(r'^get_initial_receiver/$', views.get_initial_receiver, name="get_initial_receiver"),
)

