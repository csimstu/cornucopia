from django.conf.urls import patterns, url
from accounts import views

urlpatterns = patterns('',
                       url(r'^login/$', views.login, name='login'),
                       url(r'^logout/$', views.logout, name='logout'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'view_profile/(?P<user_id>\d+)/$', views.view_profile, name='view_profile'),
)
