from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'simrooming.views.home', name='home'),
    # url(r'^simrooming/', include('simrooming.foo.urls')),
    url(r'^', include('rooming.urls', namespace='rooming')),
#                       url(r'^login/?$','django.contrib.auth.views.login', {'template_name': 'rooming/login.html'}, name='login'),
    url(r'^login/', 'mit.scripts_login', {'template_name': 'rooming/login.html'}, name='login'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
