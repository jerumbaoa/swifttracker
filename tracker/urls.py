
from django.contrib import admin
from django.conf.urls import patterns, include, url
from swifttracker.views import *
 
urlpatterns = patterns('',
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page_view),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^register/$', register_view),
    url(r'^register/success/$', register_success_view),
    url(r'^home/$', home_view, name="home"),
    url(r'^edit/profile/$', edit_profile_view, name="edit_profile"),
    url(r'^user/projects/(?P<project_id>\d+)/$', project_view, name="project_detail"),
    url(r'^user/projects/add_report/(?P<project_id>\d+)/$', add_report_view, name="add_report"),
    url(r'^admin/', include(admin.site.urls)),
)
