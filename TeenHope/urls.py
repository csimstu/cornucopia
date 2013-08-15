from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from TeenHope import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'TeenHope.views.home', name='home'),
                       # url(r'^TeenHope/', include('TeenHope.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^forum/', include('forum.urls', namespace="forum")),
                       url(r'^accounts/', include('accounts.urls', namespace="accounts")),
                       url(r'^pages/', include('pages.urls', namespace="pages")),
                       url(r'^$', "forum.views.home", name="home"),
                       url(r'^xadmin/', include('xadmin.urls', namespace="xadmin")),
                       url(r'^network/', include('network.urls', namespace="network")),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
