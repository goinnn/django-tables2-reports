import django

from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.conf.urls.static import static
from django.contrib import admin
from test_app.views import TestView

admin.autodiscover()

if django.VERSION < (1,4,0):
    from django.conf.urls.defaults import include, patterns, url
elif django.VERSION >= (1,4,0):
    from django.conf.urls import include, url
    if django.VERSION < (1,9,0):
        from django.conf.urls import patterns

if django.VERSION < (1,9,0):
    urlpatterns = patterns(
        '',
        # Examples
        url(r'^$', TestView.as_view(), name='index'),
        url(r'^index_function_view/$', 'test_app.views.index_function_view', name='index_function_view'),
        url(r'^index_function_view_middleware/$', 'test_app.views.index_function_view_middleware', name='index_function_view_middleware'),
        url(r'^admin/', include(admin.site.urls)),
        ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Django 1.10
    from test_app.views import index_function_view, index_function_view_middleware
    urlpatterns = [
        url(r'^$', TestView.as_view(), name='index'),
        url(r'^index_function_view/$', index_function_view, name='index_function_view'),
        url(r'^index_function_view_middleware/$', index_function_view_middleware, name='index_function_view_middleware'),
        url(r'^admin/', include(admin.site.urls)),
        ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
