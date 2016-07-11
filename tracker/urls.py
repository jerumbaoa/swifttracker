from django.contrib import admin
from django.conf.urls import patterns, include, url
from swifttracker.views import *
 
urlpatterns = patterns('',
    url(r'^$', 'django.contrib.auth.views.login', name="index"),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^register/success/$', RegisterSuccessView.as_view(), name="register_success"),
    url(r'^home/$', HomeView.as_view(), name="home"),
    url(r'^edit/profile/$', EditProfileView.as_view(), name="edit_profile"),
    url(r'^user/projects/(?P<project_id>\d+)/$', ProjectView.as_view(), name="project_detail"),
    url(r'^user/projects/add_report/(?P<project_id>\d+)/$', AddReportView.as_view(), name="add_report"),
    url(r'^user/projects/edit_report/(?P<project_id>\d+)/(?P<report_id>\d+)/$', EditReportView.as_view(), name="edit_report"),
    url(r'^admin/', include(admin.site.urls)),
)