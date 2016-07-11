from django.contrib import admin
from .models import Profile, Project, WeeklyReport
from .forms import ProfileForm
# Register your models here.

class ProfileUser(admin.ModelAdmin):
    list_display = ['user', 'position', 'birthdate', 'phone', 'address' ]
    form = ProfileForm

admin.site.register(Profile, ProfileUser)

class ProjectUser(admin.ModelAdmin):
    list_display = ['name', 'position', 'weekly_hours']
    filter_horizontal = ['username']
    class Meta:
        model = Project

admin.site.register(Project, ProjectUser)

class WeeklyReportUser(admin.ModelAdmin):
    list_display = ['project_name', 'title', 'date_track', 'question1', 'question2', 'question3', 'time_track']
    class Meta:
        model = WeeklyReport

admin.site.register(WeeklyReport, WeeklyReportUser)