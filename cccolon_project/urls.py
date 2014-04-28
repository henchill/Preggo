from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
from preggo import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'cccolon_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^preggo/', include('preggo.urls')), 
    #url(r'^search/', include('haystack.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns(
		'django.views.static', 
		(r'media/(?P<path>.*)',
			'serve',
			{'document_root': settings.MEDIA_ROOT}),
	)
