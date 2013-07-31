from django.conf.urls import patterns, url
from accounts import views

urlpatterns = patterns('',
                       url(r'^login$', views.login, name='login'),
                       url(r'^logout$', views.logout, name='logout'),
                       url(r'^update_profile/$', views.update_profile, name='update_profile'),
                       url(r'^register/$', views.register, name='register'),
)
