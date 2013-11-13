from django.conf import settings

try:
    from django.conf.urls import include, patterns, url
except ImportError:  # Django < 1.4
    from django.conf.urls.defaults import include, patterns, url

# Uncomment the next two lines to enable the admin:
from django.conf.urls.static import static
from django.contrib import admin
from test_app.views import TestView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TestView.as_view(), name='index'),
    url(r'^index_function_view/$', 'test_app.views.index_function_view', name='index_function_view'),
    url(r'^index_function_view_middleware/$', 'test_app.views.index_function_view_middleware', name='index_function_view_middleware'),
    # url(r'^test_project/', include('test_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
