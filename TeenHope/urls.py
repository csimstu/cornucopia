from django.conf.urls import patterns, include, url
from TeenHope import settings
from django.conf.urls.static import static
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
    url(r'^lodge/', include('accounts.urls', namespace="accounts")),

    url(r'^$', "forum.views.index", name="home"),

    url(r'^ckeditor/', include('ckeditor.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
