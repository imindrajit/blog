from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from blogengine.views import public_view, profile, register, user_login, user_logout, personalised_view, about, singlePost, addPost


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^register/$', register, name = 'register'),
	url(r'^login/$', user_login, name = 'login'),
	url(r'^logout/$', user_logout, name = 'logout'),
	url(r'^about/$', about, name = 'about'),
	url(r'^blog/(?P<selected_page>\d+)/?$', personalised_view, name = 'self_posts'),
	url(r'^\d{4}/\d{1,2}/(?P<postUrl>[-a-zA-Z0-9]+)/?$', singlePost, name = 'view_post'),
	url(r'^add_blog_post/$', addPost, name = 'add_blog_post'),
	url(r'^profile/$', profile, name='profile'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^comments/', include('django.contrib.comments.urls')),
	url(r'^blogengine/$',public_view, name = 'first_page'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()