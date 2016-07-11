from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.conf import settings
from django.views.generic import RedirectView, TemplateView
from .models import Profile, Project, WeeklyReport
from swifttracker.forms import *
import datetime


class LoginMixin(TemplateView):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginMixin, self).dispatch(*args, **kwargs)


class RegisterView(TemplateView):
    template_name = 'registration/register.html'
    context = {}

    def get (self, *args, **kwargs):
        self.context['form'] = RegistrationForm()
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        data = self.request.POST
        form = RegistrationForm(data, request=self.request)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/register/success/')

        self.context['form'] = form
        return render(self.request, self.template_name, self.context)

 
class RegisterSuccessView(TemplateView):
    template_name = 'registration/success.html'


class LogoutView(RedirectView):
    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, args, kwargs)


class HomeView(LoginMixin, TemplateView):
    template_name = 'home.html'
    context = {}

    def get(self, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        project = Project.objects.filter(username=self.request.user)
        if profile.birthdate:
            age = int((datetime.date.today() - profile.birthdate).days / 365.25 )
        else:
            self.context['profile'] = Profile.objects.get(user=self.request.user)
            self.context['project'] = Project.objects.filter(username=self.request.user)
            return render(self.request, self.template_name, self.context)
        self.context['profile'] = profile
        self.context['project'] = project
        self.context['age'] = age

        return render(self.request, self.template_name, self.context)
            

class EditProfileView(LoginMixin, TemplateView):
    template_name = 'edit.html'
    context ={}

    def get(self, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)

        form = EditForm(instance=profile, initial={
            'first_name':self.request.user.first_name,
            'last_name':self.request.user.last_name
            })

        self.context['form'] = form
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        form = EditForm(self.request.POST, instance=profile)

        if form.is_valid():
            obj = form.save(commit=False)
            user = User.objects.get(id=self.request.user.id)
            user.last_name = form.cleaned_data['last_name']
            user.first_name = form.cleaned_data['first_name']
            obj.save()
            user.save()

            return HttpResponseRedirect(reverse('home'))

        else:
            self.context['form'] = form
        return render(self.request, self.template_name, self.context)


class ProjectView(LoginMixin, TemplateView):
    template_name = 'projects.html'
    context = {}

    def get(self, *args, **kwargs):
        data = Project.objects.get(id=kwargs['project_id'])
        reports = WeeklyReport.objects.filter(project_name=data, user=self.request.user).order_by('-id')
        self.context['data'] = data
        self.context['reports'] = reports
        return render(self.request, self.template_name, self.context)
        

class AddReportView(LoginMixin, TemplateView):
    template_name = 'add_report.html'
    context = {}

    def get(self, *args, **kwargs):
        self.context['form'] = WeeklyReportForm()
        #self.context['form'] = form
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        project = Project.objects.get(id=kwargs['project_id'], username=self.request.user)
        user = self.request.user

        form = WeeklyReportForm(self.request.POST, user=user, project=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project_detail', kwargs={'project_id':kwargs['project_id']}))
        else:
            self.context['form'] = form
        return render(self.request, self.template_name, self.context)


class EditReportView(LoginMixin, TemplateView):
    template_name = 'edit_report.html'
    context = {}

    def get(self, *args, **kwargs):
        project = WeeklyReport.objects.get(user=self.request.user, id=kwargs['report_id'])
        self.context['form'] = EditWeeklyReportForm(instance=project)
        #self.context['form'] = form
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        project = WeeklyReport.objects.get(id=kwargs['report_id'])
        form = EditWeeklyReportForm(self.request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('project_detail', kwargs={'project_id':kwargs['project_id']}))
        else:
            self.context['form'] = form
        return render(self.request, self.template_name, self.context)
