from django.conf.urls import patterns, url
from django.contrib.auth.views import login
from rooming import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^login/?$','django.contrib.auth.views.login',{'template_name': 'rooming/login.html'}, name='login'),
                       url(r'^entry$', views.entry, name='entry'),
                       url(r'^rawentry$', views.rawentry, name='rawentry'),
                       url(r'^data$', views.data, name='data'),
                       url(r'^update$', views.update, name='update'),
                       url(r'^text$', views.text, name='text'),
                       url(r'^removeresident$', views.removeresident, name='removeresident'),

                       url(r'^csv$', views.csvOutput, name='csv'),
                       
)
